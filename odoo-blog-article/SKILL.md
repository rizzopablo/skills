---
name: odoo-blog-article
description: Transform resolved Odoo support cases into publishable blog articles with functional focus, anonymization, and expansive content.
metadata:
  { "openclaw": { "emoji": "📝", "requires": {} } }
---

# Skill: Odoo Blog Article Generator

**Propósito:** Transformar casos resueltos en topics de Odoo en artículos de blog publicables, anonimizados y de interés general para la comunidad.

**Principio:** Una sola habilidad, múltiples contextos. El proceso es constante; los parámetros suministran el mundo específico.

---

## Parámetros de Entrada

| Parámetro | Tipo | Descripción | Default |
|-----------|------|-------------|---------|
| `CONTEXT` | Conversación actual | Topic/conversación donde se ejecuta el skill | Detectado automáticamente |
| `TYPE` | bugfix\|feature\|integration | Tipo de caso / estructura del artículo | Auto-detectado |
| `AUDIENCE` | funcional\|tecnico\|ejecutivo | Audiencia objetivo del artículo | `funcional` |
| `LENGTH` | short\|medium\|long | Longitud objetivo del artículo | `medium` |
| `OUTPUT_DIR` | Path | Directorio de salida | `projects/odoo/blog-articles/` |
| `ATTACH` | boolean | Adjuntar archivo en la sesión | `true` |

---

## Proceso (Receta)

### Fase 1 — Lectura y Síntesis del Contexto

**Objetivo:** Comprender el caso completo leyendo toda la conversación.

**Pasos:**

1. **Detectar contexto actual**
   - `chat_id`: ID del grupo/topic donde se ejecuta
   - `topic_id`: ID del topic (si es forum)
   - Leer historial completo de la conversación (últimos 50-100 mensajes)

2. **Identificar elementos clave** (juicio, no conclusión predeterminada)
   - ¿Cuál es el problema central descrito en los primeros mensajes?
   - ¿Qué solución se implementó (mensajes finales con código o confirmación)?
   - ¿Qué archivos, módulos o configuraciones están involucrados?
   - ¿Hay referencias a documentación, módulos OCA, o forum oficial?
   - ¿Qué decisiones técnicas o funcionales se tomaron y por qué?

3. **Clasificar tipo de caso** (para seleccionar template)
   - **bugfix:** Error resuelto, comportamiento incorrecto corregido
   - **feature:** Implementación nueva, funcionalidad agregada
   - **integration:** Conector entre Odoo y sistema externo

**Criterio de clasificación:**
- Si el caso es "algo estaba roto → lo arreglamos" → bugfix
- Si el caso es "necesitábamos esto → lo implementamos" → feature
- Si el caso es "conectar Odoo con X sistema" → integration
- Si no está claro → feature (default)

4. **Clasificar audiencia objetivo** (para adaptar contenido dentro del template)
   - **funcional:** Para consultores y usuarios avanzados. Sin código, flujo UI completo.
   - **tecnico:** Para desarrolladores. Código con explicación, arquitectura interna.
   - **ejecutivo:** Para directores y tomadores de decisiones. ROI, métricas, timeline.

**Criterio de clasificación:**
- Default → funcional (la mayoría de lectores son consultores)
- Si el topic tiene código, archivos, desarrollo → tecnico
- Si el topic es sobre costos, ROI, decisiones de negocio → ejecutivo

---

### Fase 2 — Anonimización y Generalización

**Objetivo:** Transformar caso específico en problema agnóstico de interés general.

**Reglas de transformación (computación, aplicar sistemáticamente):**

| Dato Sensible | Transformación |
|---------------|----------------|
| Nombres de clientes/empresas | → "una empresa de [sector]" |
| Nombres de personas | → "el equipo", "el administrador", "[rol]" |
| Fechas específicas | → "durante la implementación", "en Q1 2026" |
| Montos monetarios | → rangos genéricos, "redujo costos operativos" |
| Ubicaciones geográficas | → "en la región", "localmente" |
| IDs de registros, base de datos | → eliminar completamente |
| URLs internas/producción | → "el sistema", "la instancia" |
| Módulos custom con nombres de cliente | → "un módulo de extensión" |

**Reglas de generalización (juicio):**

1. **Identificar sectores aplicables:** ¿En qué otras industrias este problema es común?
2. **Extraer patrón subyacente:** ¿Qué hace que este desafío sea reconocible para múltiples usuarios?
3. **Verificar transferibilidad:** ¿Un lector externo podría aplicar esto en su contexto?

**Test de generalización:** ¿Podría este artículo aplicar a 10+ empresas diferentes sin que se note que viene de un caso específico?

---

### Fase 3 — Generación del Artículo

**Objetivo:** Producir artículo estructurado usando el template correspondiente al tipo de caso y audiencia.

#### Selección de Template

**Según tipo de caso (`TYPE`):**

| Tipo | Template | Estructura |
|------|----------|------------|
| `bugfix` | `templates/bugfix.md` | 🐛 Problema → 🔍 Diagnóstico → 🔧 Solución → ✅ Resultado → 📚 Referencias |
| `feature` | `templates/feature.md` | 📌 Contexto → 🎯 Desafío → 🔍 Análisis → 💡 Solución → ✅ Resultados → 📚 Profundizar |
| `integration` | `templates/integration.md` | 📌 Escenario → 🔍 Arquitectura → 💡 Implementación → ⚠️ Consideraciones → ✅ Resultado |

**Según audiencia (`AUDIENCE`):**

Los templates usan marcadores `[AUDIENCE: tipo]` para adaptar contenido:
- `[AUDIENCE: funcional]` → Solo para audiencia funcional (flujo UI, sin código)
- `[AUDIENCE: tecnico]` → Solo para audiencia técnica (código, arquitectura)
- `[AUDIENCE: ejecutivo]` → Solo para audiencia ejecutiva (ROI, timeline, métricas)

Al generar el artículo, **incluir solo las secciones de la audiencia seleccionada** y remover los marcadores.

#### Principio de Contenido

**Jerarquía según audiencia:**

- **funcional:** Explicación funcional primero (casos de negocio, historias de usuario, flujo UI). Código mínimo o ninguno.
- **tecnico:** Código con explicación funcional (qué hace en términos de negocio). Arquitectura interna, archivos de referencia.
- **ejecutivo:** Problema de negocio, ROI, métricas, timeline de implementación, riesgos y mitigación.

**Principio de Genericidad:**

El skill `odoo-blog-article` es portable: funciona con cualquier LLM, desde cualquier entorno (CLI, IDE, web, Telegram, etc.). Los artículos generados **NO deben referenciar**:
- El entorno específico donde se ejecuta el skill (Telegram, Discord, CLI, etc.)
- La tecnología de IA utilizada (Qwen, Claude, GPT, etc.)
- Herramientas específicas de OpenClaw o del sistema que lo ejecuta

Los artículos deben ser **agnósticos del entorno de generación**. Si el caso involucra una integración con IA, describirla como "un sistema de IA" sin especificar el proveedor. El foco es siempre el caso de Odoo, no la herramienta que genera el artículo.

#### Longitudes objetivo:
- `short`: 1000-1500 palabras (caso simple, solución directa, sin ejemplos extensos)
- `medium`: 2000-3500 palabras (caso completo con contexto, explicación paso a paso, 1-2 ejemplos)
- `long`: 4000-6000 palabras (caso completo con contexto profundo, explicación detallada, múltiples ejemplos, casos de uso adicionales, troubleshooting, lecciones extendidas)

---

**Referencia rápida de secciones por template:**

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

---

### Fase 4 — Validación y Entrega

**Objetivo:** Asegurar calidad antes de entregar.

#### Checklist de Validación (aplicar sistemáticamente)

**Seguridad y Anonimización:**
- [ ] ¿Ningún nombre de cliente real aparece?
- [ ] ¿Ningún dato financiero específico está expuesto?
- [ ] ¿No hay URLs de producción o internas?
- [ ] ¿No hay IDs de registros reales?
- [ ] ¿No hay credenciales o API keys en código?

**Calidad Funcional:**
- [ ] ¿Un consultor funcional puede entenderlo sin saber programación? (solo si audience=funcional)
- [ ] ¿Hay al menos 1 historia de usuario concreta (con personaje y situación)? (feature/integration)
- [ ] ¿El flujo está descrito desde la UI (Menú → Acción)? (audience=funcional)
- [ ] ¿El código es mínimo (solo referencias, 1-2 líneas)? (audience=funcional)
- [ ] ¿El código tiene explicación funcional? (audience=tecnico)
- [ ] ¿Los beneficios están por rol (Ventas, Logística, etc.)? (feature)
- [ ] ¿Las verificaciones son funcionales (desde la UI)?

**Transferibilidad:**
- [ ] ¿Podría este artículo aplicar a 10+ empresas diferentes?
- [ ] ¿Un lector externo podría identificar el cliente original? (debe ser NO)
- [ ] ¿El problema descrito es reconocible para usuarios de Odoo?
- [ ] ¿La solución es aplicable en contextos similares?

**Formato:**
- [ ] ¿Título claro y descriptivo (60-80 caracteres)?
- [ ] ¿Longitud dentro del target seleccionado?
- [ ] ¿Links verificados y activos?
- [ ] ¿Tags relevantes asignados?

#### Generación de Archivo

1. **Crear directorio si no existe:**
   ```
   OUTPUT_DIR = "projects/odoo/blog-articles/"
   ```

2. **Generar nombre de archivo:**
   ```
   Formato: YYYY-MM-DD_<titulo-slug>.md
   Ejemplo: 2026-04-14_fechas-entrega-por-linea.md
   ```

3. **Escribir archivo:**
   - Contenido: Artículo completo en Markdown
   - Metadata al final: Tipo, audiencia, topic origen, fecha, longitud, estado (BORRADOR)

4. **Adjuntar en sesión (si ATTACH = true):**
   - Enviar archivo como adjunto en la misma conversación
   - Caption: Título, ruta completa, recordatorio de checklist

---

## Límites Éticos

**Nunca publicar:**
- Información que identifique un cliente específico
- Vulnerabilidades de seguridad sin reporte previo a Odoo S.A.
- Código propietario de terceros sin licencia abierta
- Workarounds que violen términos de servicio Odoo Enterprise

**Siempre verificar:**
- Que la solución funciona en la versión mencionada
- Que los links a documentación oficial están activos
- Que el código de ejemplo es autocontenido y testeable

---

## Mejora Continua (Principio: "Bastante Bien")

**Después de cada ejecución:**

1. **Clasificar resultado:**
   - ❌ Malo: Error obvio, dato sensible expuesto, artículo incomprensible
   - ⚠️ OK: Funciona pero podría ser mejor (falta contexto, beneficios poco claros)
   - ✅ Excelente: Listo para publicar con mínimos ajustes

2. **Si es "OK":** Analizar brecha
   - ¿Qué sección quedó débil?
   - ¿Qué juicio faltó aplicar?
   - ¿Qué contexto no se incluyó?

3. **Actualizar skill:** Codificar aprendizaje en la receta para próxima ejecución

**Principio:** Las respuestas "OK" son donde vive la mejora real del sistema.

---

## Ejemplo de Invocación

**Contexto:** Topic #28 de ODOO_OFAP donde se resolvió caso de fechas de entrega por línea.

**Invocación:**
```
/odoo-blog-article --type feature --audience funcional --length medium
```

**Output:**
- Archivo: `projects/odoo/blog-articles/2026-04-14_fechas-entrega-por-linea.md`
- Adjunto en sesión para descarga inmediata
- Artículo: ~2500 palabras, enfoque funcional, anonimizado

---

## Referencias

- **Templates:**
  - `templates/bugfix.md` — Bugfix / problema resuelto
  - `templates/feature.md` — Feature / implementación nueva
  - `templates/integration.md` — Integración / conector entre sistemas
- **Ejemplos:**
  - `examples/bugfix-funcional.md` — Bugfix con audiencia funcional
  - `examples/bugfix-tecnico.md` — Bugfix con audiencia técnica
  - `examples/feature-funcional.md` — Feature con audiencia funcional
  - `examples/feature-tecnico.md` — Feature con audiencia técnica
  - `examples/integration-funcional.md` — Integración con audiencia funcional
  - `examples/integration-tecnico.md` — Integración con audiencia técnica
- **Anonimización:** `prompts/anonymization.md`

Si no encuentras los templates y ejemplos, debes guiar al usuario para que te describa qué tipo de artículo le gusta, crear con el usuario un template y un ejemplo, almacenarlo en el lugar de referencia para que puedas usarlo. Si los templates y ejemplos ya existen, usas los existentes sin crear uno nuevo.
