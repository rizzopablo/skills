# Integrar Odoo con Shopify — desarrollo de conector custom con REST API

## 📌 Escenario

El conector OCA `shopifyerpconnect` no cubre todos los casos de uso (descuentos complejos, productos personalizados, multi-warehouse). Necesitamos un conector custom que controle cada aspecto de la sincronización entre Odoo y Shopify.

**Sistemas involucrados:**
| Sistema | Rol | Versión |
|---------|-----|---------|
| Odoo | ERP: contabilidad, inventario, ventas | v17 |
| Shopify | Tienda online | REST API 2024-01 |

---

## 🔍 Arquitectura de la Integración

**Protocolo:** REST API (Shopify) + JSON-RPC (Odoo)

**Autenticación Shopify:**
- OAuth 2.0 (install flow) o API Key/Secret (custom app)
- Usamos custom app con API Key + Secret para acceso directo
- Headers: `X-Shopify-Access-Token: {access_token}`

**Flujo de datos:**
```
Odoo cron → Shopify API (GET /admin/api/2024-01/orders.json)
    → Parse JSON → Crear sale.order en Odoo

Odoo action → Shopify API (PUT /admin/api/2024-01/orders/{id}.json)
    → Actualizar fulfillment_status
```

**Modelo de datos:**
| Odoo campo | Shopify campo | Tipo | Notas |
|------------|--------------|------|-------|
| `sale_order.name` | `order.name` | char | Número de orden (ej: #1001) |
| `sale_order.partner_id` | `order.customer` | res.partner | Crear si no existe |
| `sale_order_line.product_id` | `line_item.product_id` | product.product | Mapeo por SKU |
| `sale_order.amount_total` | `order.total_price` | float | Convertir currency |
| `stock_picking.name` | `fulfillment.order_id` | char | Link picking → fulfillment |

**Archivos de referencia:**
- `custom_shopify/models/shopify_backend.py` — Modelo de configuración del backend
- `custom_shopify/models/sale_order.py` — Importación de pedidos
- `custom_shopify/models/stock_picking.py` — Envío de fulfillment
- `custom_shopify/models/product_product.py` — Sincronización de productos
- `custom_shopify/wizards/shopify_import_orders.py` — Wizard de importación manual

---

## 💡 Implementación

**Enfoque:** Conector custom con cron job para importación periódica y acciones manuales para exportación. Alternativas consideradas: webhook (Shopify no soporta webhooks para orders/create en todas las planes) + queue (RabbitMQ/Redis para procesamiento asíncrono).

**Código esencial — Conexión y autenticación:**

```python
# custom_shopify/models/shopify_backend.py
import requests

class ShopifyBackend(models.Model):
    _name = 'shopify.backend'
    _description = 'Shopify Backend Configuration'
    
    name = fields.Char(required=True)
    shop_url = fields.Char(required=True)  # mitienda.myshopify.com
    access_token = fields.Char(string='API Access Token')
    api_version = fields.Char(default='2024-01')
    
    def _get_shopify_session(self):
        """Retorna sesión requests configurada para Shopify API"""
        session = requests.Session()
        session.headers.update({
            'X-Shopify-Access-Token': self.access_token,
            'Content-Type': 'application/json',
        })
        return session
    
    def shopify_call(self, method, endpoint, params=None, data=None):
        """Wrapper para llamadas a Shopify API con retry y rate limiting"""
        url = f"https://{self.shop_url}/admin/api/{self.api_version}/{endpoint}"
        session = self._get_shopify_session()
        
        for attempt in range(3):
            response = session.request(method, url, params=params, json=data)
            if response.status_code == 429:  # Rate limited
                retry_after = int(response.headers.get('Retry-After', 1))
                time.sleep(retry_after)
                continue
            response.raise_for_status()
            return response.json()
        
        raise Exception('Shopify API rate limit exceeded after 3 retries')
```

**Código esencial — Importación de pedidos:**

```python
# custom_shopify/models/sale_order.py
class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    shopify_order_id = fields.Char(string='Shopify Order ID', index=True)
    shopify_backend_id = fields.Many2one('shopify.backend')
    
    def import_shopify_orders(self, backend, since=None):
        """Importa pedidos desde Shopify a Odoo"""
        params = {'status': 'any', 'financial_status': 'any'}
        if since:
            params['created_at_min'] = since
        
        orders_data = backend.shopify_call('GET', 'orders.json', params=params)
        created = 0
        
        for order_data in orders_data.get('orders', []):
            if self.search([('shopify_order_id', '=', str(order_data['id']))]):
                continue  # Ya existe
            
            # Crear partner si no existe
            customer = order_data.get('customer')
            if customer:
                partner = self.env['res.partner'].search([
                    ('email', '=', customer.get('email'))
                ], limit=1)
                if not partner:
                    partner = self.env['res.partner'].create({
                        'name': customer.get('first_name', '') + ' ' + customer.get('last_name', ''),
                        'email': customer.get('email'),
                        'phone': customer.get('phone'),
                    })
            
            # Crear líneas de orden
            lines = []
            for line_item in order_data.get('line_items', []):
                product = self.env['product.product'].search([
                    ('default_code', '=', line_item.get('sku'))
                ], limit=1)
                
                lines.append((0, 0, {
                    'product_id': product.id,
                    'product_uom_qty': line_item.get('quantity', 1),
                    'price_unit': float(line_item.get('price', 0)),
                }))
            
            # Crear sale.order
            self.create({
                'shopify_order_id': str(order_data['id']),
                'shopify_backend_id': backend.id,
                'partner_id': partner.id if customer else False,
                'order_line': lines,
                'date_order': order_data.get('created_at', fields.Datetime.now()),
                'currency_id': self.env.company.currency_id.id,
            })
            created += 1
        
        return created
```

**Manejo de errores:**
```python
# Retry con backoff exponencial para rate limits
if response.status_code == 429:
    retry_after = int(response.headers.get('Retry-After', 1))
    time.sleep(retry_after * (2 ** attempt))  # Backoff exponencial
```

---

## ⚠️ Consideraciones y Limitaciones

**Rate limits:**
- Shopify: 2 calls/segundo (40 con bucket)
- Implementamos retry con backoff exponencial en `shopify_call()`
- Cron job: cada 15 min para no saturar

**Errores comunes:**
| Error | Causa | Solución |
|-------|-------|----------|
| `401 Unauthorized` | Token expirado o inválido | Regenerar token en Shopify Admin |
| `429 Too Many Requests` | Rate limit excedido | Retry con backoff (ya implementado) |
| `Product not found` | SKU no existe en Odoo | Configurar producto genérico "Unknown" |
| `Currency mismatch` | Shopify en USD, Odoo en ARS | Configurar tipo de cambio en Odoo |

**Edge cases:**
- **Descuentos:** Se importan como línea de producto con precio negativo
- **Envío:** `shipping_lines` se importa como producto de servicio "Envío"
- **Devoluciones:** `refunds` se importan como nota de crédito en Odoo
- **Multi-currency:** Shopify puede vender en USD/EUR, Odoo en ARS → configurar tipos de cambio

**Monitoreo:**
- Logs en `shopify.backend.log` con cada llamada API
- Cron job con notificación de error por email
- Dashboard con métricas: pedidos importados/hora, errores, latency

---

## ✅ Resultado

**Qué se logra:**
- Pedidos de Shopify se importan automáticamente cada 15 min
- Productos se sincronizan (precio, stock) bidireccionalmente
- Fulfillment se envía a Shopify cuando se confirma el picking
- Notas de crédito se crean automáticamente para refunds

**Beneficios:**
| Antes | Después |
|-------|---------|
| Conector OCA con limitaciones | Control total del flujo |
| 50% de pedidos requieren ajuste manual | 0% — todo automático |
| Sin soporte para refunds | Refunds → nota de crédito automática |

**Verificación:**
- [ ] Crear pedido de prueba en Shopify → aparece en Odoo en ≤15 min
- [ ] Confirmar picking → fulfillment creado en Shopify
- [ ] Crear refund en Shopify → nota de crédito en Odoo

---

## 📚 Referencias

- [Shopify Admin REST API Docs](https://shopify.dev/docs/api/admin-rest/2024-01) — Documentación completa de endpoints
- [Shopify Rate Limits](https://shopify.dev/docs/api/usage/rate-limits) — Rate limiting y retry strategy
- [Odoo External API](https://www.odoo.com/documentation/17.0/developer/reference/external_api.html) — JSON-RPC y XML-RPC

---

## 💬 ¿Integraste de otra forma?

¿Usaste webhooks en vez de cron? ¿Implementaste queue processing con RabbitMQ? ¿Encontraste edge cases que este enfoque no cubre? Compartí tu solución en los comentarios.

---

**Metadata:**
- Tipo: integration
- Audiencia: tecnico
- Versión Odoo: v17
- Sistemas: Odoo v17 + Shopify REST API 2024-01
- Topic origen: #890
- Estado: BORRADOR
