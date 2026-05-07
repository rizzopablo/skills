# Prompt: Anonimización y Generalización

**Objetivo:** Transformar un caso específico de cliente en un problema genérico de interés general.

## Input

```
[Descripción original del caso con datos sensibles]
```

## Instrucciones

### Paso 1: Identificar datos sensibles

Buscar y marcar:
- [ ] Nombres propios (personas, empresas, marcas)
- [ ] Ubicaciones geográficas específicas
- [ ] Fechas exactas (excepto año)
- [ ] Montos monetarios específicos
- [ ] IDs de registros (base de datos, tickets, órdenes)
- [ ] URLs internas o de producción
- [ ] Nombres de módulos personalizados con nombres de cliente

### Paso 2: Aplicar transformaciones

**Tabla de reemplazo:**

| Tipo | Original | Transformado |
|------|----------|--------------|
| Empresa | "Cervecería del Sur S.A." | "una empresa de producción de bebidas" |
| Persona | "Juan, el administrador" | "el administrador del sistema" |
| Lugar | "San Martín de los Andes" | "la región" |
| Fecha | "15 de marzo 2026" | "durante Q1 2026" |
| Monto | "$500,000 USD" | "redujo costos operativos significativamente" |
| ID | "Order #12345" | "la orden de venta" |
| Módulo | "l10n_mx_allende_custom" | "un módulo de extensión" |

### Paso 3: Generalizar el problema

**Preguntas guía:**
1. ¿Qué otros sectores enfrentan este mismo problema?
2. ¿Qué hace que este desafío sea común (no único)?
3. ¿Cómo se describiría este problema en un forum público de Odoo?

**Ejemplo de transformación:**

```
ANTES (específico):
"El cliente de cervezas artesanales necesita que en las órdenes 
de venta aparezca la fecha de entrega solicitada por línea porque 
tienen entregas escalonadas según maduración de lotes."

DESPUÉS (agnóstico):
"Empresas con producción por lotes necesitan gestionar fechas de 
entrega diferenciadas por producto, ya que no todos los ítems 
están listos para entrega al mismo tiempo."
```

### Paso 4: Validar

**Checklist:**
- [ ] ¿Podría este artículo aplicar a 10+ empresas diferentes?
- [ ] ¿Un lector externo podría identificar el cliente original?
- [ ] ¿El problema descrito es reconocible para usuarios de Odoo?
- [ ] ¿La solución es aplicable en contextos similares?

## Output

```
[Descripción anonimizada y generalizada lista para artículo]
```

---

## Ejemplos Completos

### Ejemplo 1: Localización Fiscal

**Input:**
```
Cliente argentino con CUIT 30-12345678-9 necesita que las facturas 
muestren IVA 21% discriminado por línea, pero además el impuesto 
Internos del 8% para productos de lujo. Usamos l10n_ar_ux como base.
```

**Output:**
```
Empresas en jurisdicciones con impuestos múltiples necesitan 
discriminar diferentes tasas impositivas por producto, no solo 
a nivel de factura. Esto es común en países con impuestos federales 
y provinciales, o con tasas diferenciadas por categoría de producto.
```

### Ejemplo 2: Manufactura

**Input:**
```
Industrias Exabytes Ltda. tiene 3 plantas de producción
y necesita que MRP calcule el abastecimiento considerando lead times 
diferentes según la planta de origen.
```

**Output:**
```
Empresas con múltiples plantas de producción necesitan que la 
planificación de materiales considere lead times diferenciados 
según la ubicación de origen, ya que los tiempos de traslado 
impactan directamente en la disponibilidad real.
```

### Ejemplo 3: Retail

**Input:**
```
Matruck (flota de 50 camiones) necesita mantener timesheets por 
chofer vinculados a órdenes de trabajo específicas para calcular 
costos por viaje.
```

**Output:**
```
Empresas con flotas de vehículos necesitan vincular horas de 
trabajo de operadores a órdenes de servicio específicas para 
calcular costos precisos por proyecto o viaje.
```

---

## Notas

- **Priorizar claridad sobre precisión:** Mejor perder un detalle técnico que exponer datos sensibles
- **Mantener la esencia funcional:** El problema central debe seguir siendo reconocible
- **Usar sector en vez de empresa:** "una empresa de logística" > "una transportista"
- **Referenciar módulos oficiales:** Si el caso usó módulos custom, buscar equivalentes en OCA o Enterprise
