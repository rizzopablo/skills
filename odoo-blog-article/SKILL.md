---
name: odoo-blog-article
description: Transform resolved Odoo support cases into publishable blog articles with functional focus, anonymization, and expansive content.
metadata:
  { "openclaw": { "emoji": "📝", "requires": {} } }
---

# Skill: Odoo Blog Article Generator

**Propósito:** Transformar casos resueltos en topics de Odoo en artículos de blog publicables, anonimizados y de interés general para la comunidad.

**Principio:** Una sola habilidad, múltiples contextos. El proceso es constante; los parámetros suministran el mundo específico.

**Versión:** 1.0.0 (Estandarizado Lama Su)

---

## Estructura del Skill (Arquitectura Lama Su)

```
odoo-blog-article/
├── README.md                    # Documentación principal estandarizada
├── SKILL.md                     # Esta referencia técnica
├── build.yaml                   # Configuración de build
├── templates/                   # Templates por tipo de caso
│   ├── bugfix.md               # 🐛 Bugfix resuelto
│   ├── feature.md              # 💡 Feature implementada
│   └── integration.md          # 🔌 Integración entre sistemas
├── examples/                    # Ejemplos de artículos generados
│   ├── bugfix-funcional.md
│   ├── bugfix-tecnico.md
│   ├── feature-funcional.md
│   ├── feature-tecnico.md
│   ├── integration-funcional.md
│   └── integration-tecnico.md
├── prompts/                     # Prompts separados por fase
│   ├── system-prompt.md        # Prompt principal del sistema
│   ├── phase1-context-analysis.md
│   ├── phase2-anonymization.md
│   ├── phase3-generation.md
│   └── phase4-validation.md
└── tests/
    └── test_behavior.md        # Tests de comportamiento esperado
```

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

## Proceso de 4 Fases

### Fase 1 — Lectura y Síntesis del Contexto

**Objetivo:** Comprender el caso completo leyendo toda la conversación.

**Ver prompt:** `prompts/phase1-context-analysis.md`

**Pasos:**
1. Detectar contexto actual (chat_id, topic_id)
2. Identificar elementos clave (problema, solución, módulos, decisiones)
3. Clasificar tipo de caso (bugfix/feature/integration)
4. Clasificar audiencia objetivo

**Criterio de clasificación del tipo:**
- Si el caso es "algo estaba roto → lo arreglamos" → **bugfix**
- Si el caso es "necesitábamos esto → lo implementamos" → **feature**
- Si el caso es "conectar Odoo con X sistema" → **integration**
- Si no está claro → **feature** (default)

---

### Fase 2 — Anonimización y Generalización

**Objetivo:** Transformar caso específico en problema agnóstico de interés general.

**Ver prompt:** `prompts/phase2-anonymization.md`

**Reglas de transformación sistemáticas:**

| Dato Sensible | Transformación |
|---------------|----------------|
| Nombres de clientes/empresas | → "una empresa de [sector]" |
| Nombres de personas | → "el equipo", "el administrador", "[rol]" |
| Fechas específicas | → "durante la implementación", "en Q1 2026" |
| Montos monetarios | → "redujo costos operativos", "inversión significativa" |
| Ubicaciones geográficas | → "en la región", "localmente" |
| IDs de registros, base de datos | → eliminar completamente |
| URLs internas/producción | → "el sistema", "la instancia" |
| Módulos custom con nombres de cliente | → "un módulo de extensión" |

**Test de generalización:** ¿Podría este artículo aplicar a 10+ empresas diferentes sin que se note que viene de un caso específico?

---

### Fase 3 — Generación del Artículo

**Objetivo:** Producir artículo estructurado usando el template correspondiente.

**Ver prompt:** `prompts/phase3-generation.md`

**Selección de Template:**

| Tipo | Template | Estructura |
|------|----------|------------|
| `bugfix` | `templates/bugfix.md` | 🐛 Problema → 🔍 Diagnóstico → 🔧 Solución → ✅ Resultado → 📚 Referencias |
| `feature` | `templates/feature.md` | 📌 Contexto → 🎯 Desafío → 🔍 Análisis → 💡 Solución → ✅ Resultados → 📚 Profundizar |
| `integration` | `templates/integration.md` | 📌 Escenario → 🔍 Arquitectura → 💡 Implementación → ⚠️ Consideraciones → ✅ Resultado |

**Marcadores de Audiencia:**
Los templates usan `[AUDIENCE: tipo]` para contenido condicional. Al generar, incluir solo secciones de la audiencia seleccionada.

**Longitudes objetivo:**
- `short`: 1000-1500 palabras
- `medium`: 2000-3500 palabras
- `long`: 4000-6000 palabras

---

### Fase 4 — Validación y Entrega

**Objetivo:** Asegurar calidad antes de entregar.

**Ver prompt:** `prompts/phase4-validation.md`

**Checklist de Validación:**

**Seguridad y Anonimización:**
- [ ] ¿Ningún nombre de cliente real aparece?
- [ ] ¿Ningún dato financiero específico está expuesto?
- [ ] ¿No hay URLs de producción o internas?
- [ ] ¿No hay IDs de registros reales?
- [ ] ¿No hay credenciales o API keys en código?

**Calidad Funcional:**
- [ ] ¿Un consultor funcional puede entenderlo sin saber programación? (solo si audience=funcional)
- [ ] ¿Hay al menos 1 historia de usuario concreta?
- [ ] ¿El flujo está descrito desde la UI? (audience=funcional)
- [ ] ¿Los beneficios están por rol? (feature)

**Transferibilidad:**
- [ ] ¿Podría este artículo aplicar a 10+ empresas diferentes?
- [ ] ¿Un lector externo podría identificar el cliente original? (debe ser NO)

**Formato:**
- [ ] ¿Título claro y descriptivo (60-80 caracteres)?
- [ ] ¿Longitud dentro del target seleccionado?
- [ ] ¿Metadata completa al final?

---

## Principios de Diseño

### 1. Portabilidad del Contenido
Los artículos generados NO deben referenciar:
- El entorno específico donde se ejecuta el skill (Telegram, Discord, CLI, etc.)
- La tecnología de IA utilizada (GPT, Claude, Qwen, etc.)
- Herramientas específicas de OpenClaw o el sistema

Los artículos deben ser **agnósticos del entorno de generación**.

### 2. Templates Condicionales por Audiencia
Cada template usa marcadores `[AUDIENCE: tipo]` para adaptar contenido:
- `[AUDIENCE: funcional]` → Solo para audiencia funcional
- `[AUDIENCE: tecnico]` → Solo para audiencia técnica
- `[AUDIENCE: ejecutivo]` → Solo para audiencia ejecutiva

### 3. Anonimización Sistemática
Las reglas de transformación son predefinidas y se aplican consistentemente, no dependen del juicio humano en cada caso.

### 4. Principio "Bastante Bien"
Después de cada ejecución, clasificar resultado:
- ❌ **Malo:** Error obvio, dato sensible expuesto
- ⚠️ **OK:** Funciona pero podría ser mejor
- ✅ **Excelente:** Listo para publicar

Las respuestas "OK" son donde vive la mejora real del sistema.

---

## Generación de Archivo

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
   - Enviar archivo como adjunto
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

- **Documentación principal:** `README.md`
- **Configuración de build:** `build.yaml`
- **Prompts:** `prompts/`
- **Templates:** `templates/`
- **Ejemplos:** `examples/`
- **Tests:** `tests/test_behavior.md`

---

## Notas de Estandarización Lama Su

Este skill ha sido estandarizado siguiendo la arquitectura Lama Su:

1. ✅ Metadatos YAML completos en `README.md`
2. ✅ `build.yaml` con configuración de build
3. ✅ Prompts separados por fase en `prompts/`
4. ✅ Tests de comportamiento en `tests/`
5. ✅ Templates con frontmatter estandarizado
6. ✅ Ejemplos de referencia para cada combinación

Ver `README.md` para documentación de uso completa.
