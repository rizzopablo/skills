# Integrar Odoo con Shopify — guía completa para configurar sincronización de productos y ventas

## 📌 Escenario

Tenés una tienda online en Shopify y gestionás tu contabilidad e inventario en Odoo. Cada vez que entra una venta en Shopify, tenés que registrarla manualmente en Odoo: crear cliente, crear orden, registrar envío, actualizar inventario. Son 15-20 minutos por pedido.

Con 50 pedidos por día, son 10-15 horas semanales de trabajo manual. Error-prone, repetitivo, y un desperdicio de tiempo que podrías usar para hacer crecer el negocio.

Este artículo muestra cómo configurar la integración entre Odoo y Shopify para automatizar:
- Sincronización de productos (precio, stock, descripción)
- Importación de pedidos de Shopify a Odoo
- Actualización de estado de envío desde Odoo a Shopify

**Sistemas involucrados:**
| Sistema | Rol | Versión |
|---------|-----|---------|
| Odoo | ERP: contabilidad, inventario, ventas | v17 |
| Shopify | Tienda online | Latest |

---

## 🔍 Arquitectura de la Integración

**Protocolo de comunicación:** REST API (Shopify) + JSON-RPC (Odoo)

**Configuración en Odoo:**
1. Ir a Apps → Buscar "Shopify" → Instalar módulo oficial `shopifyerpconnect`
2. Ir a Ventas → Configuración → Ajustes → Sección Shopify
3. Ingresar:
   - **Tienda:** `mitienda.myshopify.com`
   - **API Key:** Generada en Shopify Admin → Apps → Develop apps
   - **API Secret:** Generada junto con la API Key
4. Guardar

**Configuración en Shopify:**
1. Ir a Shopify Admin → Settings → Apps and sales channels
2. Click en "Develop apps" → "Create an app"
3. Configurar permissions:
   - `read_products`, `write_products`
   - `read_orders`, `write_orders`
   - `read_inventory`, `write_inventory`
4. Instalar app y copiar API Key + Secret

**Verificación de conexión:**
- En Odoo, ir a Ventales → Shopify → "Test Connection"
- Debe mostrar "Conexión exitosa" con versión de API de Shopify

---

## 💡 Implementación

**Enfoque general:** Usar el módulo comunitario `shopifyerpconnect` (OCA) que conecta ambos sistemas vía API. Alternativas consideradas: desarrollo custom (más flexible pero más costoso) o Zapier/Make (más fácil pero menos control).

**Configuración paso a paso:**

**Paso 1: Configurar Shopify**
1. Crear app en Shopify con permisos de lectura/escritura
2. Copiar API Key y API Secret

**Paso 2: Configurar Odoo**
1. Instalar módulo `shopifyerpconnect`
2. Ingresar credenciales en Ajustes → Shopify
3. Testear conexión

**Paso 3: Sincronizar productos**
1. Ir a Ventas → Shopify → Productos
2. Click en "Importar desde Shopify"
3. Seleccionar productos a sincronizar
4. Mapear categorías de Shopify con categorías de Odoo

**Paso 4: Configurar importación de pedidos**
1. Ir a Ventas → Shopify → Configuración
2. Activar "Importar pedidos automáticamente"
3. Configurar frecuencia (cada 15 min recomendado)
4. Seleccionar canal de ventas en Odoo

**Paso 5: Configurar actualización de envío**
1. En Odoo, al confirmar el picking, el estado se envía a Shopify
2. Shopify notifica al cliente automáticamente

---

## ⚠️ Consideraciones y Limitaciones

**Rate limits:**
- Shopify: 2 calls/segundo por app (40 calls/segundo con bucket)
- Odoo: sin límite nativo, pero dependerá del servidor

**Errores comunes:**
| Error | Causa | Solución |
|-------|-------|----------|
| "Connection failed" | API Key incorrecta | Regenerar en Shopify Admin |
| "Product not found" | SKU no mapeado | Verificar mapeo de productos |
| "Order import failed" | Cliente sin email | Configurar cliente genérico en Odoo |

**Edge cases:**
- **Descuentos:** Los descuentos de Shopify se importan como líneas separadas en Odoo
- **Envío:** El costo de envío aparece como línea de producto en Odoo
- **Devoluciones:** No se sincronizan automáticamente (requiere configuración adicional)

**Monitoreo:**
- Ir a Ventales → Shopify → Logs para ver errores de sincronización
- Configurar notificación por email en caso de error de importación

---

## ✅ Resultado

**Qué se logra:**
- Pedidos de Shopify se importan automáticamente a Odoo cada 15 minutos
- Inventario se sincroniza bidireccionalmente (venta en Shopify → baja en Odoo)
- Estado de envío se actualiza en Shopify cuando se confirma el picking en Odoo

**Beneficios:**
| Antes | Después |
|-------|---------|
| 15-20 min por pedido manual | 0 minutos — todo automático |
| Errores de tipeo frecuentes | Sin errores humanos |
| Inventario desactualizado | Stock sincronizado en tiempo real |

**Verificación:**
- [ ] Crear pedido de prueba en Shopify → aparece en Odoo en ≤15 min
- [ ] Confirmar picking en Odoo → estado actualizado en Shopify
- [ ] Verificar que el stock se decrementó en ambos sistemas

---

## 📚 Referencias

- [Documentación de Shopify API](https://shopify.dev/docs/api/admin-rest) — REST API para productos, órdenes e inventario
- [Módulo OCA: shopifyerpconnect](https://github.com/OCA/connector-shopify) — Conector comunitario para Odoo
- [Configuración de Shopify en Odoo](https://www.odoo.com/documentation/17.0/esp_ecommerce.html) — Docs oficiales de e-commerce

---

## 💬 ¿Integraste de otra forma?

¿Usaste Zapier, Make, o desarrollo custom en vez del conector OCA? ¿Encontraste limitaciones que este enfoque no cubre? Compartí tu experiencia en los comentarios.

---

**Metadata:**
- Tipo: integration
- Audiencia: funcional
- Versión Odoo: v17
- Sistemas: Odoo v17 + Shopify Latest
- Topic origen: #890
- Estado: BORRADOR
