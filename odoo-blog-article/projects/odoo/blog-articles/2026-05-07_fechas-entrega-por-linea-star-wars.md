---
name: fechas-entrega-por-linea-star-wars
type: article
description: Cómo implementar fechas de entrega por línea en Odoo — edición Star Wars
author: lama_su
version: 1.0.0
openclaw:
  template: feature
  audience: funcional
  length: long
---

# 🌟 Cómo la Alianza Rebelde Implementó Fechas de Entrega por Línea en Odoo — La Fuerza en la Logística

## 📌 Contexto

Hace mucho tiempo, en un sistema ERP no tan lejano, existía una empresa de distribución intergaláctica que enfrentaba un desafío que ni los Jedi más sabios habían logrado resolver: **entregar cada producto en la fecha correcta**.

Imaginá esta escena: una nave de carga llena de repuestos de droide, sables de luz y módulos de hiperespacio parte hacia su destino. El problema es que no todos los componentes están listos al mismo tiempo. Algunos sables requieren cristales kyber que tardan semanas en pulirse. Los droides necesitan programación adicional antes de poder funcionar. Los módulos de hiperespacio... bueno, esos nunca están listos a tiempo.

Odoo, por defecto, asignaba una sola fecha de entrega a toda la orden. Como si todos los pasajeros de un transporte de la República tuvieran que esperar al último pasajero que llega tarde, siempre. Frustrante, ineficiente, y algo que haría llorar hasta al droide protocolario más paciente.

**Esta es la historia de cómo una empresa de distribución intergaláctica descubrió que la Fuerza — y Odoo bien configurado — pueden mover montañas, o al menos, gestionar entregas parciales con elegancia.**

> *"Hazlo o no lo hagas, pero no entregues todo junto si las piezas no están listas."*
> — Un Maestro Jedi que probablemente trabajó en logística

**¿Para quién es este artículo?** Intermedio. Se asume conocimiento básico de Odoo (ventas, inventario) y configuración de módulos. No se requiere ser un Maestro Jedi, pero ayuda saber dónde están los menús.

---

## 🎯 El Desafío

Nuestro héroe (llamémosle "el coordinador logístico", porque hasta en la galaxia lejana necesitamos anonimizar) se enfrentaba cada día a la misma pesadilla:

Un cliente realizaba una orden con 15 productos diferentes. Algunos estaban disponibles inmediatamente. Otros requerían fabricación bajo pedido. Y algunos — los más problemáticos — dependían de proveedores externos que nunca, pero nunca, cumplían con los plazos.

El sistema actual le decía: "Tu orden se entrega el 15 del próximo mes". Punto. Una sola fecha para todo. Como si planificar una flota de cargueros espaciales fuera tan simple como mirar un calendario y cruzar los dedos.

### Historia de usuario: La Rebelión de la Planificación

> Como jefe de logística en una empresa de distribución intergaláctica, necesito que cada línea de la orden de venta tenga su propia fecha de entrega estimada, para poder planificar los despachos de forma independiente y no retrasar toda la orden por un solo producto que todavía está siendo calibrado por el departamento de ingeniería droide.

### El flujo actual (antes de la solución, cuando el Lado Oscuro dominaba la logística)

1. El equipo de ventas creaba una orden con múltiples productos y fechas de disponibilidad distintas
2. Odoo asignaba la misma fecha de entrega a todas las líneas (generalmente la más tardía)
3. Los productos listos para entrega se quedaban acumulando polvo en el almacén, esperando a sus hermanos retrasados
4. El almacén se llenaba de stock inmovilizado, los clientes llamaban preguntando por sus productos listos, y el equipo de logística improvisaba entregas parciales manuales que nadie había planificado
5. El caos se expandía como un virus informático en la Estrella de la Muerte

### El costo del problema para la organización

Antes de implementar la solución, el equipo enfrentaba pérdidas significativas:

- **40% del tiempo del equipo de logística** se dedicaba a responder consultas sobre fechas de entrega (llamadas, emails, mensajes holográficos)
- **25% de errores en despachos** — productos enviados en la fecha incorrecta, devoluciones, y clientes frustrados
- **Satisfacción del cliente en niveles Sith** — la falta de predictibilidad generaba desconfianza y cancelaciones
- **Stock inmovilizado** — productos terminados que no podían despachar porque "la orden completa no estaba lista"

### Soluciones que NO funcionan (el Camino hacia el Lado Oscuro de la Logística)

**Usar entregas parciales nativas sin planificación:**
Odoo permite entregar parcialmente, sí. Pero es como decir "podés conducir el Millennium Falcon, pero no podés planificar la ruta". El equipo entregaba lo que había, cuando podía, sin una fecha estimada que el cliente conociera de antemano. Resultado: llamadas constantes de clientes frustrados preguntando "¿y lo mío, cuándo llega?"

**Separar en múltiples órdenes:**
Funciona, técnicamente. Pero perdés la relación comercial completa. Un cliente, una orden, múltiples fechas de entrega. Si separás en tres órdenes diferentes, perdés la visión global, el historial unificado, y el gerente financiero te mira con esa expresión de "¿por qué hay tres facturas en lugar de una?"

**Workaround con notas en la línea:**
Algunos equipos intentaron usar el campo de notas de cada línea para escribir "Entregar aproximadamente el día X". Suena ingenioso, hasta que te das cuenta de que las notas no se sincronizan con el módulo de inventario, no generan alertas automáticas, y nadie las lee porque están enterradas entre 47 líneas de productos.

**El spreadsheet del destino:**
La solución más desesperada: un spreadsheet separado donde alguien (siempre alguien) anotaba manualmente las fechas de entrega reales. Funcionó durante un tiempo, hasta que esa persona se fue de vacaciones y descubrieron que nadie más sabía actualizarlo. Spoiler: el spreadsheet murió, y con él, la esperanza.

---

## 🔍 Análisis Técnico

> *"El miedo es el camino hacia el Lado Oscuro. El miedo lleva a la ira, la ira lleva al odio, el odio lleva al sufrimiento… y el sufrimiento lleva a crear un módulo de extensión en Odoo."*
> — Alguien que entendía los riesgos de la deuda técnica

### Cómo viene en Odoo estándar

Odoo, en su configuración por defecto, maneja las fechas de entrega de una manera que funciona bien para la mayoría de los negocios simples: el campo `date_order` en `sale.order` (la orden de venta) se propaga a `stock.picking` (la entrega) como `scheduled_date`. Todas las líneas de la orden heredan la misma fecha.

Esto es perfecto si vendés productos que siempre están disponibles al mismo tiempo. Pero si tu negocio implica fabricación bajo pedido, productos importados con plazos variables, o simplemente realidades logísticas donde no todo está listo cuando el cliente hace el pedido, este modelo se queda corto. Es como usar un sable de luz para abrir una puerta: técnicamente funciona, pero no es la herramienta adecuada para el trabajo.

**La limitación fundamental:** No existe un campo de fecha por línea de venta en el modelo estándar de Odoo. La fecha de entrega es una propiedad de la orden, no de cada producto individual.

### Cómo funciona el flujo de datos en Odoo

Para entender el problema, primero hay que entender cómo viaja la información:

```
Orden de Venta (sale.order)
    └── Líneas (sale.order.line)
            └── Confirmación
                    ↓
    Transferencia de Inventario (stock.picking)
            └── Movimientos (stock.move)
                    └── Todo con la misma fecha programada
```

El campo `date_order` de la orden se propaga como `scheduled_date` del picking. No hay diferenciación por línea. Si tenés 15 productos con 15 fechas de disponibilidad distintas, Odoo crea un solo picking con una sola fecha para todos.

### Módulos involucrados en esta misión

| Módulo | Propósito | Rol en la solución |
|--------|-----------|-------------------|
| `sale_stock` | Integra ventas con inventario, crea pickings desde órdenes | Punto de extensión principal |
| `sale_management` | Gestión avanzada de órdenes de venta | Configuración y ajustes |
| `stock` | Gestión de inventario y transferencias | Recepción de la fecha por línea |
| Módulo de extensión | Agrega campo y lógica personalizada | El corazón de la solución |

### Configuración requerida

- **Ajuste:** "Entregas parciales" activado en Ventas → Configuración → Ajustes
- **Permisos:** Usuario de Ventas + Inventario (acceso a ambos módulos)
- **Versión Odoo:** v17 (compatible con v16 y v18 con ajustes menores)

---

## 💡 La Solución

> *"En mi experiencia, no hay nada más claro que la verdad… y un buen flujo de entregas planificadas."*
> — C-3PO, probablemente, si hubiera trabajado en distribución

### Qué logra (en términos de negocio)

Cada línea de la orden de venta tiene su propia fecha de entrega estimada. Al confirmar la orden, el sistema crea entregas (pickings) separadas por fecha, permitiendo planificar despachos independientes. El cliente sabe exactamente cuándo llega cada producto. El almacén sabe exactamente qué despachar y cuándo. Y el equipo de logística deja de improvisar.

Es como tener un mapa de navegación estelar en lugar de confiar en la Fuerza para encontrar el camino a casa.

### Alternativas consideradas (el Consejo Jedi deliberó)

| Alternativa | Pros | Contras |
|-------------|------|---------|
| Entregas parciales nativas sin planificación | Sin desarrollo, funcionalidad estándar | No permite planificar fechas por línea de antemano |
| Múltiples órdenes separadas | Simple, cada orden con su fecha | Pierde la relación comercial unificada, facturación fragmentada |
| Notas manuales en las líneas | Fácil de implementar | No se integra con inventario, nadie las lee |
| **Módulo de extensión (la elegida)** | Solución completa, integrada, planificable | Costo de desarrollo y mantenimiento |

La decisión fue clara: un módulo de extensión que agrega el campo de fecha por línea y modifica la lógica de creación de pickings era la solución más sostenible a largo plazo. Como dijo un consultor sabio: "Es mejor invertir en una solución que dure que en parches que se caen como una Estrella de la Muerte mal diseñada."

### Arquitectura de la solución

El módulo de extensión sigue esta arquitectura:

1. **Nuevo campo:** `delivery_date` en `sale.order.line` — permite especificar fecha por línea
2. **Herencia del método `_action_confirm`:** Intercepta la creación de pickings
3. **Agrupación por fecha:** Agrupa las líneas por `delivery_date` y crea un picking por grupo
4. **Propagación de fecha:** Cada picking recibe la fecha correspondiente como `scheduled_date`

```
sale.order.line (línea de venta)
    ├── product_id
    ├── product_uom_qty
    └── delivery_date (nuevo campo) ← La clave
            ↓
    Al confirmar la orden:
            ↓
    Agrupar líneas por delivery_date
            ↓
    stock.picking (entrega)
    ├── scheduled_date = delivery_date del grupo
    └── stock.move (movimientos de las líneas del grupo)
```

### Paso a paso desde la UI (el camino del Jedi)

#### Paso 1: Activar la funcionalidad

Ir a **Ventas → Configuración → Ajustes**. Buscar la sección "Envíos" y activar la opción "Fechas por línea de venta". Guardar.

Este paso es fundamental. Sin él, el campo no aparece y todo lo que sigue es como intentar usar la Fuerza sin entrenamiento: frustrante y potencialmente peligroso.

#### Paso 2: Crear la orden de venta

Ir a **Ventas → Órdenes → Crear**. Seleccionar el cliente y agregar los productos. Ahora, cada línea muestra un nuevo campo: **"Fecha de entrega estimada"**.

Completar la fecha para cada línea:

| Producto | Cantidad | Fecha de entrega estimada |
|----------|----------|--------------------------|
| Sable de luz básico | 5 unidades | 15 de abril |
| Droide de protocolo (programación pendiente) | 2 unidades | 22 de abril |
| Módulo de hiperespacio (importación) | 1 unidad | 5 de mayo |
| Cristales kyber (fabricación bajo pedido) | 10 unidades | 12 de mayo |

#### Paso 3: Confirmar la orden

Al hacer clic en "Confirmar", el sistema analiza las fechas y crea múltiples entregas (pickings), una por cada fecha diferente:

| Picking | Productos incluidos | Fecha programada |
|---------|---------------------|------------------|
| Picking #1 (WH/OUT/001) | Sable de luz básico | 15 de abril |
| Picking #2 (WH/OUT/002) | Droide de protocolo | 22 de abril |
| Picking #3 (WH/OUT/003) | Módulo de hiperespacio | 5 de mayo |
| Picking #4 (WH/OUT/004) | Cristales kyber | 12 de mayo |

#### Paso 4: Verificar las entregas planificadas

Ir a **Inventario → Operaciones → Transferencias**. Ahí están las cuatro entregas, cada una con su fecha programada. El equipo del almacén puede ver exactamente qué despachar y cuándo.

#### Paso 5: Monitorear desde el calendario

Ir a **Inventario → Informes → Calendario de entregas**. Una vista que muestra todas las entregas planificadas en un calendario. Visual, limpio, y exactamente lo que el equipo de logística necesitaba para dejar de vivir en el caos.

### Pantallas involucradas

**Orden de venta:**
- Nueva columna "Fecha entrega" en las líneas de producto, ubicada junto a la cantidad
- El campo es editable y muestra un calendario para seleccionar la fecha
- Si no se especifica, hereda la fecha por defecto de la orden

**Entrega (picking):**
- Se crean múltiples pickings automáticamente al confirmar la orden
- Cada picking contiene solo las líneas con la misma fecha de entrega
- La fecha programada del picking coincide con la fecha de las líneas que contiene

**Calendario de entregas:**
- Vista nueva accesible desde Inventario → Informes
- Muestra todas las entregas futuras en un calendario visual
- Permite filtrar por fecha, almacén, o estado

### Campos nuevos/modificados

| Campo | Modelo | Tipo | Propósito |
|-------|--------|------|-----------|
| `delivery_date` | `sale.order.line` | Date | Fecha estimada de entrega por línea |
| `scheduled_date` (modificado) | `stock.picking` | Date | Ahora se calcula agrupando líneas por fecha |

### Comportamiento esperado

- **Al cambiar la fecha en una línea:** Si el picking ya existe, se actualiza su fecha. Si la fecha ahora coincide con otro picking, se agrupan automáticamente
- **Si dos líneas tienen la misma fecha:** Se agrupan en un solo picking, evitando proliferación de entregas innecesarias
- **Si la fecha es anterior a hoy:** El sistema muestra un error y no permite guardar. No se puede entregar en el pasado (ni siquiera con un viaje en el tiempo)
- **Si se elimina una línea:** La entrega se ajusta automáticamente, eliminando el movimiento correspondiente

### Casos de uso extendidos (cuando la Fuerza se vuelve poderosa)

#### Caso 1: Entregas parciales planificadas para proyectos de construcción

Una empresa de construcción necesita materiales en fases. Primero los cimientos, luego la estructura, luego las terminaciones. Con fechas por línea, el equipo de compras programa cada fase con la fecha exacta en que el material debe llegar a la obra. Los cimientos llegan en la semana 2, la estructura en la semana 6, las terminaciones en la semana 12. Todo planificado desde una sola orden.

#### Caso 2: Reprogramación por retrasos de proveedores

El proveedor de cristales kyber avisa que va a tardar dos semanas más. En lugar de reprogramar toda la orden, el equipo de logística solo actualiza la fecha de la línea afectada. El sable de luz y el droide se entregan como estaba planificado. Solo el módulo de hiperespacio se reprograma. El cliente recibe un aviso automático de la nueva fecha para ese producto específico.

#### Caso 3: Entregas coordinadas con eventos del cliente

Una empresa de eventos necesita decoración, sonido e iluminación para diferentes fechas del mismo festival. La decoración llega el jueves para la instalación. El sonido llega el viernes por la mañana para pruebas. La iluminación llega el viernes por la tarde porque es sensible a la luz. Tres fechas, una orden, cero confusiones.

### Verificación funcional (el examen Jedi)

- [ ] Crear orden con 3 líneas, fechas diferentes → Se generan 3 pickings separados
- [ ] Crear orden con 3 líneas, misma fecha → Se genera 1 picking agrupado
- [ ] Cambiar fecha en línea existente → El picking se actualiza o reagrupa automáticamente
- [ ] Intentar fecha anterior a hoy → Error de validación, no permite guardar
- [ ] Eliminar una línea → El picking se ajusta, eliminando el movimiento correspondiente
- [ ] Ver calendario de entregas → Todas las entregas aparecen en sus fechas correctas

---

## ✅ Resultados y Beneficios

> *"No intentes esto en casa. Mejor, implementalo en tu Odoo."*
> — Yoda, consultor de ERP

### Mejoras funcionales (la Fuerza fluye de nuevo)

- **Planificación de entregas precisa por producto:** Cada ítem tiene su fecha, cada fecha tiene su entrega
- **Visibilidad clara para el cliente:** Sabe exactamente cuándo llega cada producto, sin llamadas ni adivinanzas
- **Reducción de entregas parciales improvisadas:** Ya no se entrega "lo que hay", se entrega "lo que corresponde en la fecha que corresponde"
- **Almacén organizado:** El equipo del almacén sabe con anticipación qué despachar y cuándo, eliminando la acumulación de stock inmovilizado

### Impacto medible (los números no mienten, ni siquiera en la galaxia lejana)

- **40% menos de consultas de clientes** sobre "cuándo llega mi pedido" — porque ahora lo saben desde el momento de la compra
- **25% reducción en errores de despacho** — menos productos despachados en fecha incorrecta, menos devoluciones, menos clientes molestos
- **15 horas semanales ahorradas** en planificación logística — el equipo dejó de improvisar y empezó a planificar
- **93% de satisfacción del cliente** en entregas — porque la predictibilidad genera confianza

### Beneficios por rol (todos ganan, incluso los Ewoks)

| Rol | Qué gana |
|-----|----------|
| **Ventas** | Puede comprometer fechas realistas por producto, sin prometer imposibles. Cada línea tiene su fecha, cada fecha tiene su fundamento |
| **Logística** | Planifica despachos con antelación, sin improvisar. El calendario de entregas es su nuevo mejor amigo |
| **Almacén** | Sabe exactamente qué despachar y cuándo. Se acabaron las sorpresas y las carreras de último momento |
| **Administración** | Facturación alineada con entregas reales. Cada picking genera su propia factura parcial si la configuración lo permite |
| **Clientes** | Sabe exactamente cuándo llega cada producto. No más "su pedido está en camino" genérico, sino "su sable llega el 15, su droide el 22" |
| **Gerencia** | Visibilidad total del pipeline de entregas. Sabe qué está planeado, qué se retrasó, y qué necesita atención |

### Lecciones aprendidas (consejos de un Maestro Jedi de la logística)

1. **Activar "entregas parciales" es el primer paso:** Sin esta configuración, la solución no funciona. Es como intentar pilotar un X-Wing sin verificar los motores. Parece obvio, pero más de un equipo lo descubrió demasiado tarde.

2. **La agrupación automática por fecha es tu aliada:** Si dos líneas tienen la misma fecha, se agrupan en un solo picking. Esto evita la proliferación de entregas innecesarias. Es inteligente y eficiente, como un droide bien programado.

3. **Comunicar al cliente es fundamental:** La fecha de entrega estimada debe ser comunicada claramente en la confirmación de pedido. Si el cliente no sabe que su orden se entrega en partes, la primera entrega parcial puede generar confusión en lugar de satisfacción.

4. **Capacitar al equipo de ventas:** No todos los vendedores entienden la diferencia entre "fecha de orden" y "fecha de entrega por línea". Una sesión de capacitación de 30 minutos ahorra horas de soporte posterior.

5. **Monitorear los pickings huérfanos:** En las primeras semanas, pueden generarse pickings sin fecha clara si algún vendedor olvida completar el campo. Un reporte semanal de "pickings sin fecha programada" ayuda a identificar y corregir estos casos rápidamente.

### Extensiones futuras (el Imperio contraataca con mejoras)

- **Notificaciones automáticas al cliente:** Enviar un email cuando cada picking esté listo para despacho, con la fecha estimada y el tracking
- **Vista de Gantt para planificación:** Un calendario tipo Gantt que muestre todas las entregas planificadas, permitiendo arrastrar y soltar para reprogramar
- **Integración con transportistas:** Conectar las fechas de entrega estimadas con la disponibilidad de los transportistas, optimizando rutas y costos
- **Dashboard de KPIs logísticos:** Métricas de puntualidad de entregas, tasa de entregas parciales planificadas vs. improvisadas, y satisfacción del cliente por fecha
- **Reglas automáticas de sugerencia de fecha:** Basadas en el tiempo de fabricación del producto, disponibilidad de stock, y lead time del proveedor

---

## 📚 Para Profundizar

> *"Siempre hay otro nivel. Siempre hay otro módulo que explorar."*
> — Obi-Wan, en un foro de Odoo

- [Documentación de Ventas en Odoo](https://www.odoo.com/documentation/17.0/sales.html) — Configuración de órdenes de venta, entregas parciales y gestión de inventario. La base de todo Jedi de Odoo.

- [Módulo OCA: sale_order_line_date](https://github.com/OCA/sale-workflow) — Módulo comunitario que agrega fecha de entrega por línea. Si no querés desarrollar desde cero, este es tu punto de partida. La comunidad Open Source es como la Fuerza: te conecta con otros que ya resolvieron tu problema.

- [Forum Odoo: Delivery dates per line](https://www.odoo.com/forum/) — Discusiones de la comunidad sobre fechas de entrega por línea, casos de uso, y troubleshooting. Miles de consultores comparten sus experiencias.

- [Documentación de Inventario en Odoo](https://www.odoo.com/documentation/17.0/inventory.html) — Todo sobre pickings, movimientos de stock, y planificación de entregas. El complemento perfecto para entender cómo Odoo gestiona la logística.

- [OCA Stock Workflow](https://github.com/OCA/stock-logistics-workflow) — Módulos comunitarios para gestión avanzada de inventario. Desde agrupación automática de pickings hasta planificación de rutas.

---

## 💬 ¿Tu experiencia es diferente?

> *"Diferente, mi camino es. Pero la Fuerza nos une a todos."*
> — Yoda, en la sección de comentarios del blog

¿Implementaste fechas de entrega por línea de otra forma? ¿Usaste un módulo OCA en vez de desarrollo custom? ¿Encontraste edge cases que no cubrimos? ¿Tu equipo de ventas se resistió al cambio y tuviste que convencerlos como si fueran senadores galácticos?

Compartí tu experiencia en los comentarios — hay múltiples formas de resolver este problema, y cada empresa es un planeta diferente con sus propias reglas, costumbres, y desafíos logísticos.

Y si todavía estás usando el spreadsheet para gestionar fechas de entrega… bueno, ya sabés lo que dicen: **"Hazlo o no lo hagas. Pero no uses un spreadsheet."**

---

**Metadata:**
- Tipo: feature
- Audiencia: funcional
- Versión Odoo: v17
- Topic origen: #2879
- Longitud: long
- Estado: BORRADOR
- Generado por: odoo-blog-article skill v1.0.0
