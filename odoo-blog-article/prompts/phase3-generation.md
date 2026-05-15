---
name: phase3-generation
type: phase
description: Fase 3 - Generación del artículo usando templates
phase: 3
---

# Phase 3: Generación del Artículo

## Objetivo
Producir un artículo estructurado usando el template correspondiente al tipo de caso y audiencia seleccionada.

## Entrada
- `anonymized_case` de Phase 2
- `TYPE`: bugfix | feature | integration
- `AUDIENCE`: funcional | tecnico | ejecutivo
- `LENGTH`: short | medium | long

## Selección de Template

### Según Tipo de Caso (`TYPE`)

| Tipo | Archivo Template | Estructura Principal |
|------|------------------|---------------------|
| `bugfix` | `templates/bugfix.md` | 🐛 Problema → 🔍 Diagnóstico → 🔧 Solución → ✅ Resultado → 📚 Referencias |
| `feature` | `templates/feature.md` | 📌 Contexto → 🎯 Desafío → 🔍 Análisis → 💡 Solución → ✅ Resultados → 📚 Profundizar |
| `integration` | `templates/integration.md` | 📌 Escenario → 🔍 Arquitectura → 💡 Implementación → ⚠️ Consideraciones → ✅ Resultado |

### Referencia Rápida de Secciones por Template

**bugfix:**
1. 🐛 El Problema (2-3 oraciones + síntomas + impacto)
2. 🔍 Diagnóstico (causa raíz + evidencia)
3. 🔧 La Solución (código o configuración + verificación)
4. ✅ Resultado (checklist de verificación + lección aprendida)
5. 📚 Referencias (issues, commits, docs)
6. 💬 ¿Te pasó lo mismo?

**feature:**
1. 📌 Contexto (gancho + sector + promesa de valor)
2. 🎯 El Desafío (historia de usuario + flujo actual vs deseado + soluciones que NO funcionan)
3. 🔍 Análisis Técnico (estado default + módulos + arquitectura)
4. 💡 La Solución (alternativas + implementación + configuración y pruebas)
5. ✅ Resultados y Beneficios (por rol + impacto medible + lecciones)
6. 📚 Para Profundizar (docs, OCA, forum)
7. 💬 ¿Tu experiencia es diferente?

**integration:**
1. 📌 Escenario (sistemas involucrados + por qué integrar)
2. 🔍 Arquitectura (protocolo + autenticación + flujo de datos + modelo)
3. 💡 Implementación (configuración ambos lados + código esencial + pruebas)
4. ⚠️ Consideraciones y Limitaciones (rate limits + errores comunes + edge cases)
5. ✅ Resultado (qué se logra + beneficios + verificación)
6. 📚 Referencias (docs de ambos sistemas)
7. 💬 ¿Integraste de otra forma?

## Adaptación por Audiencia

Los templates contienen marcadores `[AUDIENCE: tipo]` para contenido condicional.

### Marcadores de Audiencia

```markdown
[AUDIENCE: funcional]
Contenido solo para audiencia funcional
[AUDIENCE_END]

[AUDIENCE: tecnico]
Contenido solo para audiencia técnica
[AUDIENCE_END]

[AUDIENCE: ejecutivo]
Contenido solo para audiencia ejecutiva
[AUDIENCE_END]
```

### Regla de Procesamiento

**Si `AUDIENCE = funcional`:**
- Incluir TODO el contenido
- Remover SOLO los bloques `[AUDIENCE: tecnico]` y `[AUDIENCE: ejecutivo]`

**Si `AUDIENCE = tecnico`:**
- Incluir contenido base + bloques `[AUDIENCE: tecnico]`
- Remover bloques `[AUDIENCE: ejecutivo]` que no apliquen

**Si `AUDIENCE = ejecutivo`:**
- Incluir contenido base + bloques `[AUDIENCE: ejecutivo]`
- Remover detalles técnicos excesivos (código, archivos específicos)

### Jerarquía de Contenido por Audiencia

| Audiencia | Prioridad de Contenido | Ejemplos |
|-----------|------------------------|----------|
| **funcional** | Casos de negocio, historias de usuario, flujo UI | "Ir a Ventas → Órdenes → Crear" |
| **tecnico** | Código con contexto funcional, arquitectura | "Ver `sale_order.py`, herencia de `sale.order`" |
| **ejecutivo** | ROI, métricas, timeline, riesgos | "Inversión de X, ROI en Y meses" |

## Longitudes Objetivo por Tipo

| Length | Palabras | Cuándo Usar |
|--------|----------|-------------|
| `short` | 1000-1500 | Caso simple, solución directa, sin ejemplos extensos |
| `medium` | 2000-3500 | Caso completo con contexto, explicación paso a paso, 1-2 ejemplos |
| `long` | 4000-6000 | Caso complejo con contexto profundo, múltiples ejemplos, troubleshooting, lecciones extendidas |

### Distribución de Palabras por Sección (feature, medium)

| Sección | Palabras | % del Total |
|---------|----------|-------------|
| Contexto | 300-400 | ~12% |
| El Desafío | 400-600 | ~18% |
| Análisis Técnico | 500-700 | ~22% |
| La Solución | 800-1200 | ~38% |
| Resultados | 300-400 | ~12% |
| Profundizar | ~100 | ~4% |
| Pregunta final | ~100 | ~4% |

## Proceso de Generación

### Paso 1: Cargar Template
1. Localizar archivo en `templates/{TYPE}.md`
2. Si no existe, usar template por defecto más cercano o informar al usuario
3. Cargar ejemplos de referencia en `examples/{TYPE}-{AUDIENCE}.md` si existen

### Paso 2: Analizar Estructura del Template
1. Identificar todas las secciones marcadas con `##`
2. Identificar marcadores `[AUDIENCE: tipo]`
3. Identificar placeholders `[CAMPO]` que necesitan relleno

### Paso 3: Filtrar por Audiencia
1. Si `AUDIENCE != funcional`, remover secciones no aplicables
2. Procesar marcadores `[AUDIENCE: tipo]` según reglas
3. Asegurar coherencia del flujo narrativo

### Paso 4: Rellenar Contenido
Para cada sección del template:

**Usar información de `anonymized_case`:**
- Reemplazar placeholders con datos reales del caso
- Adaptar tono y nivel de detalle según `AUDIENCE`
- Expandir o condensar según `LENGTH`

**Prioridades de contenido:**
1. Información del `anonymized_case` (problema, solución, módulos)
2. Decisiones técnicas documentadas
3. Referencias externas encontradas
4. Conocimiento general sobre Odoo (complementar si falta)

### Paso 5: Generar Título
Formato sugerido:
- Incluir acción principal + contexto de Odoo
- Longitud: 60-80 caracteres
- Ejemplo: "Cómo implementar fechas de entrega por línea en Odoo — caso práctico"

### Paso 6: Generar Slug para Archivo
```
YYYY-MM-DD_<titulo-en-kebab-case>.md
```

Ejemplo: `2026-04-14_fechas-entrega-por-linea.md`

## Ejemplos de Referencia

Usar ejemplos existentes como guía de:
- Tono y estilo de escritura
- Nivel de detalle apropiado
- Formato de tablas y código
- Longitud de secciones

**Ejemplos disponibles:**
- `examples/bugfix-funcional.md`
- `examples/bugfix-tecnico.md`
- `examples/feature-funcional.md`
- `examples/feature-tecnico.md`
- `examples/integration-funcional.md`
- `examples/integration-tecnico.md`

## Calidad del Contenido Generado

### Verificar antes de entregar:

**Estructura:**
- [ ] Todas las secciones del template están presentes
- [ ] Marcadores de audiencia procesados correctamente
- [ ] Longitud dentro del rango objetivo

**Contenido:**
- [ ] Problema descrito claramente
- [ ] Solución explicada paso a paso
- [ ] Módulos y componentes identificados
- [ ] Beneficios cuantificados cuando sea posible

**Estilo:**
- [ ] Tono profesional pero accesible
- [ ] Uso consistente de emojis en encabezados
- [ ] Tablas formateadas correctamente
- [ ] Listas de verificación funcionales

## Salida Esperada

```yaml
generated_article:
  title: "[Título del artículo]"
  slug: "[titulo-en-kebab-case]"
  filename: "YYYY-MM-DD_[slug].md"
  content: "[Texto completo en Markdown]"
  word_count: "[número]"
  sections:
    - "[sección 1]"
    - "[sección 2]"
    - "..."
  metadata:
    type: "[bugfix|feature|integration]"
    audience: "[funcional|tecnico|ejecutivo]"
    length: "[short|medium|long]"
    odoo_version: "[v16/v17/v18/v19]"
    topic_origin: "#[ID]"
    status: "BORRADOR"
```

## Transición a Fase 4

Pasar `generated_article` a `phase4-validation.md` para verificación final.
