# Cómo implementar fechas de entrega por línea en Odoo — desarrollo custom

## 📌 Contexto

Odoo asigna una sola fecha de entrega a toda la orden de venta. En escenarios de producción por lotes o distribución multi-almacén, cada línea puede necesitar una fecha distinta. Este artículo muestra cómo extender `sale.order` para soportar fechas por línea y cómo integrar con `stock.picking`.

**¿Para quién es este artículo?** Avanzado. Se asume conocimiento de desarrollo en Odoo (modelos, vistas, herencia) y del ciclo de ventas→inventario.

---

## 🎯 El Desafío

**Historia de usuario:**
> Como desarrollador, necesito extender `sale.order.line` para incluir una fecha de entrega estimada, y hacer que `sale_stock` respete esa fecha al crear los pickings.

**El problema técnico:** `sale_stock` toma `order.date_order` y lo usa como `scheduled_date` en todas las líneas del picking. No hay mecanismo nativo para fechas diferenciadas por línea.

**Soluciones que NO funcionan:**
- **Override de `_prepare_procurement_values`:** Solo afecta la planificación MRP, no la fecha del picking.
- **Modificar `stock.move` directamente:** Se sobrescribe en cada recomputo de la orden.
- **Usar `delivery_date` de `sale.order`:** Es a nivel de orden, no de línea.

---

## 🔍 Análisis Técnico

**Estado default de Odoo:**
`sale.order.line` no tiene campo de fecha propia. `sale_stock._prepare_order_line_moves()` usa `order.date_order` como `date` para todos los `stock.move`.

**Módulos involucrados:**
| Módulo | Propósito |
|--------|-----------|
| `sale` | Modelo base `sale.order` y `sale.order.line` |
| `sale_stock` | Integra ventas con inventario, crea `stock.picking` y `stock.move` |
| `stock` | Gestión de inventario, pickings, movimientos |

**Arquitectura de datos:**
- Modelos principales: `sale.order.line`, `stock.move`, `stock.picking`
- Relaciones: `sale.order.line → stock.move` (vía procurement), `stock.move → stock.picking`
- Flujo de datos: `sale.order` → `_prepare_order_line_moves()` → `stock.move.create()` → `stock.picking`

**Archivos de referencia:**
- `addons/sale_stock/models/sale_order.py` — `_prepare_order_line_moves()` (línea ~400)
- `addons/sale/models/sale_order.py` — Modelo base `sale.order.line`
- `addons/stock/models/stock_move.py` — Modelo `stock.move`, campo `date`

---

## 💡 La Solución

**Enfoque:** Extender `sale.order.line` con campo `delivery_date`, override de `_prepare_order_line_moves()` para usar esa fecha en `stock.move`.

**Alternativas consideradas:**
| Alternativa | Pros | Contras |
|-------------|------|---------|
| Módulo OCA `sale_order_line_delivery_date` | Ya existe | No integra con picking correctamente en v17 |
| Desarrollo custom | Control total | Mantenimiento en cada upgrade |

**Código esencial:**

```python
# custom_sale_delivery_date/models/sale_order.py
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    delivery_date = fields.Date(
        string='Fecha de entrega estimada',
        help='Fecha en que este producto estará disponible para entrega'
    )
```

```python
# custom_sale_delivery_date/models/sale_order.py
class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    def _prepare_order_line_moves(self, group_id):
        """Override para usar delivery_date por línea en stock.move"""
        moves_data = super()._prepare_order_line_moves(group_id)
        
        for move_vals in moves_data:
            # move_vals['sale_line_id'] apunta al order line
            line = self.env['sale.order.line'].browse(move_vals['sale_line_id'])
            if line.delivery_date:
                move_vals['date'] = line.delivery_date
        
        return moves_data
```

**Explicación técnica:** `_prepare_order_line_moves()` retorna una lista de dicts con los valores para crear `stock.move`. Overrideamos para inyectar `delivery_date` en `date` cuando está definida en la línea de venta.

**Vista (XML):**
```xml
<!-- custom_sale_delivery_date/views/sale_order_view.xml -->
<record id="view_order_form_delivery_date" model="ir.ui.view">
    <field name="name">sale.order.form.delivery.date</field>
    <field name="model">sale.order</field>
    <field name="inherit_id" ref="sale.view_order_form"/>
    <field name="arch">
        <xpath expr="//field[@name='order_line']/tree/field[@name='date_planned']" position="after">
            <field name="delivery_date" optional="show"/>
        </xpath>
    </field>
</record>
```

**Verificación funcional:**
- [ ] Crear orden con 3 líneas, fechas diferentes → 3 pickings con `scheduled_date` distintos
- [ ] Confirmar orden sin `delivery_date` → comportamiento default (sin cambios)
- [ ] Cambiar `delivery_date` en línea existente → `stock.move.date` se actualiza

---

## ✅ Resultados y Beneficios

**Mejoras funcionales:**
- Cada línea de venta planifica su entrega independientemente
- Pickings se crean con fecha correcta desde el inicio
- Sin necesidad de ajustar manualmente después de confirmar

**Impacto medible:**
- Desarrollo: ~4 horas (modelo + vista + tests)
- Mantenimiento: bajo (override mínimo, solo 1 método)

**Beneficios por rol:**
| Rol | Qué gana |
|-----|----------|
| Desarrollador | Código limpio, override mínimo, fácil de mantener |
| Consultor | Configuración simple, sin ajustes manuales post-confirmación |
| Usuario final | Planificación de entregas precisa sin cambiar su flujo de trabajo |

**Lecciones aprendidas:**
- `_prepare_order_line_moves()` es el punto de extensión correcto (no `action_confirm`)
- Verificar que el override no afecte órdenes sin `delivery_date` definido

---

## 📚 Para Profundizar

- [Código fuente: sale_stock/models/sale_order.py](https://github.com/odoo/odoo/blob/17.0/addons/sale_stock/models/sale_order.py) — Método `_prepare_order_line_moves()`
- [Módulo OCA: sale_order_line_delivery_date](https://github.com/OCA/sale-work) — Alternativa comunitaria
- [Extending Odoo — Herencia de modelos](https://www.odoo.com/documentation/17.0/developer/reference/addons/odoo.html) — Guía oficial de herencia

---

## 💬 ¿Implementaste esto de otra forma?

¿Usaste otro método de extensión? ¿Encontraste edge cases que este enfoque no cubre? Compartí tu solución en los comentarios.

---

**Metadata:**
- Tipo: feature
- Audiencia: tecnico
- Versión Odoo: v17
- Topic origen: #567
- Estado: BORRADOR
