---
name: phase1-context-analysis
type: phase
description: Fase 1 - Lectura y síntesis del contexto del caso
phase: 1
---

# Phase 1: Lectura y Síntesis del Contexto

## Objetivo
Comprender el caso completo leyendo toda la conversación del topic de soporte.

## Entrada
- `CONTEXT`: Conversación/topic completo de soporte Odoo (50-100 mensajes típicamente)
- Parámetros opcionales: `TYPE`, `AUDIENCE`, `LENGTH`

## Pasos a Ejecutar

### 1. Detectar Contexto Actual
- Identificar `chat_id` o `topic_id` del contexto
- Leer historial completo de la conversación
- Identificar el rango relevante (primeros mensajes describen problema, últimos describen solución)

### 2. Extraer Elementos Clave
Analizar la conversación y extraer:

**Problema Central:**
- ¿Cuál es el problema descrito en los primeros mensajes?
- ¿Qué intentaba hacer el usuario cuando encontró el problema?
- ¿Cuál es el impacto en el negocio?

**Solución Implementada:**
- ¿Qué solución se implementó? (código compartido, configuración, confirmación)
- ¿Quién proporcionó la solución? (consultor, comunidad, documentación)
- ¿Fue validada por el cliente?

**Módulos y Componentes Involucrados:**
- Listar todos los módulos de Odoo mencionados (ej: `sale_stock`, `account`, `l10n_ar`)
- Identificar módulos de terceros o custom si los hay
- Notar dependencias entre módulos

**Decisiones Técnicas:**
- ¿Qué alternativas se consideraron?
- ¿Por qué se eligió esta solución específica?
- ¿Hay trade-offs documentados?

**Referencias Externas:**
- Links a documentación oficial de Odoo
- Módulos OCA mencionados
- Posts del forum oficial
- Issues o commits de referencia

### 3. Clasificar Tipo de Caso

**Criterios de Clasificación:**

| Indicadores | Tipo | Descripción |
|-------------|------|-------------|
| "Algo estaba roto → lo arreglamos" | `bugfix` | Error resuelto, comportamiento incorrecto corregido |
| "Necesitábamos esto → lo implementamos" | `feature` | Implementación nueva, funcionalidad agregada |
| "Conectar Odoo con X sistema" | `integration` | Conector entre Odoo y sistema externo |

**Reglas:**
- Si hay código de FIX o corrección de error → `bugfix`
- Si hay desarrollo de nueva funcionalidad → `feature`
- Si involucra APIs, webhooks, sincronización con externos → `integration`
- Si no está claro → `feature` (default)

### 4. Clasificar Audiencia Objetivo (si no especificada)

**Criterios de Clasificación:**

| Indicadores en el Topic | Audiencia |
|-------------------------|-----------|
| Mayoría son consultores/usuarios avanzados | `funcional` (default) |
| Hay código, archivos `.py`, `.xml`, desarrollo | `tecnico` |
| Se discute ROI, costos, decisiones de negocio | `ejecutivo` |

**Reglas:**
- Default → `funcional`
- Solo cambiar a `tecnico` si hay desarrollo explícito
- Solo cambiar a `ejecutivo` si hay discusión de costos/decisiones de negocio

### 5. Determinar Longitud Recomendada (si no especificada)

**Criterios:**
- Caso simple, una sola acción → `short`
- Caso completo con configuración, varios pasos → `medium`
- Caso complejo con múltiples escenarios, troubleshooting → `long`

## Salida Esperada

### Resumen Estructurado del Caso

```yaml
case_summary:
  problem: "[Descripción clara del problema]"
  solution: "[Descripción de la solución implementada]"
  modules:
    - "[módulo1]"
    - "[módulo2]"
  type: "[bugfix|feature|integration]"
  audience: "[funcional|tecnico|ejecutivo]"
  length_recommended: "[short|medium|long]"
  key_decisions:
    - "[Decisión 1 y por qué]"
    - "[Decisión 2 y por qué]"
  external_refs:
    - "[Link a doc]"
    - "[Módulo OCA]"
```

### Verificación de Entrada

Antes de pasar a Fase 2, verificar:
- [ ] Se identificó claramente el problema
- [ ] Se identificó la solución implementada
- [ ] Se clasificó el tipo de caso
- [ ] Se determinó la audiencia apropiada

**Si falta información crítica:**
- Solicitar al usuario que aclare el tipo de caso
- O usar default (`feature`, `funcional`) y documentar la incertidumbre

## Transición a Fase 2

Pasar el `case_summary` estructurado a `phase2-anonymization.md` para procesamiento.
