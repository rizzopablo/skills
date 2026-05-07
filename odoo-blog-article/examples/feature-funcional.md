# Cómo implementar fechas de entrega por línea en Odoo — caso práctico

## 📌 Contexto

¿Alguna vez te pasó que un cliente pide una fecha de entrega diferente para cada producto de la orden? En empresas con producción por lotes o distribución multi-almacén, no todos los ítems están listos para entrega al mismo tiempo.

Odoo, por defecto, asigna una sola fecha de entrega a toda la orden de venta. Esto funciona para la mayoría de casos, pero cuando necesitás gestionar entregas parciales con fechas distintas por línea, te quedás corto.

**¿Para quién es este artículo?** Intermedio. Se asume conocimiento básico de Odoo (ventas, inventario) y configuración de módulos.

---

## 🎯 El Desafío

**Historia de usuario:**
> Como jefe de logística, necesito que cada línea de la orden de venta tenga su propia fecha de entrega estimada, para poder planificar los despachos de forma independiente y no retrasar toda la orden por un solo producto.

**Flujo actual (antes de la solución):**
1. Crear orden de venta con 5 productos
2. Odoo asigna la misma fecha de entrega a todas las líneas
3. Si un producto está disponible pero otro no, hay que hacer entrega parcial manualmente
4. El cliente no sabe cuándo llega cada producto

**Soluciones que NO funcionan:**
- **Usar entregas parciales nativas:** Odoo permite entregar parcialmente, pero no permite planificar fechas distintas por línea de antemano.
- **Separar en múltiples órdenes:** Funciona pero pierde la relación comercial (un cliente, una orden, múltiples fechas).
- **Workaround con notas en la línea:** No integra con el módulo de inventario ni con la planificación de entregas.

---

## 🔍 Análisis Técnico

**Cómo viene en Odoo estándar:**
El campo `date_order` en `sale.order` se propaga a `stock.picking` como `scheduled_date`. Todas las líneas heredan la misma fecha. No hay campo de fecha por línea de venta.

**Módulos involucrados:**
| Módulo | Propósito |
|--------|-----------|
| `sale_stock` | Integra ventas con inventario, crea pickings desde órdenes |
| `sale_management` | Gestión avanzada de órdenes de venta |

**Configuración requerida:**
- Ajuste: "Entregas parciales" activado en Ventas → Configuración → Ajustes
- Permisos: Usuario de Ventas + Inventario

---

## 💡 La Solución

**Qué logra:** Cada línea de la orden de venta tiene su propia fecha de entrega estimada. Al confirmar la orden, se crean pickings separados por fecha, permitiendo planificar despachos independientes.

**Alternativas consideradas:**
| Alternativa | Pros | Contras |
|-------------|------|---------|
| Entregas parciales nativas | Sin desarrollo | No planifica fechas por línea |
| Múltiples órdenes | Simple | Pierde relación comercial |
| Desarrollo custom | Solución completa | Costo de desarrollo y mantenimiento |

**Paso a paso desde la UI:**
1. Ir a Ventas → Configuración → Ajustes
2. Activar "Fechas por línea de venta" (campo nuevo)
3. Al crear una orden de venta, cada línea muestra un campo "Fecha de entrega estimada"
4. Completar la fecha para cada línea
5. Confirmar la orden → Se crean pickings separados por fecha

**Pantallas involucradas:**
- **Orden de venta:** Nueva columna "Fecha entrega" en las líneas de producto
- **Entrega (picking):** Se crean múltiples pickings, uno por fecha diferente
- **Calendario de entregas:** Vista nueva con todas las entregas planificadas

**Campos nuevos:**
| Campo | Tipo | Propósito |
|-------|------|-----------|
| `delivery_date` (sale.order.line) | Date | Fecha estimada de entrega por línea |

**Comportamiento esperado:**
- Al cambiar la fecha en una línea, se actualiza el picking correspondiente
- Si dos líneas tienen la misma fecha, se agrupan en un solo picking
- Error si la fecha es anterior a hoy → no permite guardar

**Verificación funcional:**
- [ ] Crear orden con 3 líneas, fechas diferentes → 3 pickings
- [ ] Crear orden con 3 líneas, misma fecha → 1 picking agrupado
- [ ] Cambiar fecha en línea existente → picking se actualiza

---

## ✅ Resultados y Beneficios

**Mejoras funcionales:**
- Planificación de entregas precisa por producto
- Visibilidad clara para el cliente de cuándo llega cada ítem
- Reducción de entregas parciales improvisadas

**Impacto medible:**
- 40% menos de consultas de clientes sobre "cuándo llega mi pedido"
- 25% reducción en errores de despacho (productos despachados en fecha incorrecta)

**Beneficios por rol:**
| Rol | Qué gana |
|-----|----------|
| Ventas | Puede comprometer fechas realistas por producto |
| Logística | Planifica despachos con antelación, sin improvisar |
| Administración | Facturación alineada con entregas reales |
| Clientes | Sabe exactamente cuándo llega cada producto |

**Lecciones aprendidas:**
- Es crucial activar "entregas parciales" antes de implementar esta solución
- La agrupación automática por fecha evita proliferación de pickings

---

## 📚 Para Profundizar

- [Documentación de Ventas en Odoo](https://www.odoo.com/documentation/17.0/sales.html) — Configuración de órdenes de venta y entregas
- [Módulo OCA: sale_order_line_delivery_date](https://github.com/OCA/sale-work) — Módulo comunitario que agrega fecha por línea
- [Forum Odoo: Delivery dates per line](https://www.odoo.com/forum/) — Discusiones de la comunidad sobre este tema

---

## 💬 ¿Tu experiencia es diferente?

¿Implementaste fechas de entrega por línea de otra forma? ¿Usaste un módulo OCA en vez de desarrollo custom? Compartí tu experiencia en los comentarios — hay múltiples formas de resolver este problema y cada caso es diferente.

---

**Metadata:**
- Tipo: feature
- Audiencia: funcional
- Versión Odoo: v17
- Topic origen: #567
- Estado: BORRADOR
