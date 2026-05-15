---
name: odoo-blog-article
emoji: 📝
description: Transforma casos resueltos de Odoo en artículos de blog publicables, anonimizados y estructurados
author: lama_su
version: 1.0.0
openclaw:
  type: skill
  requires: {}
  provides:
    output: markdown
    attachments: true
  parameters:
    - name: CONTEXT
      type: conversation
      description: Topic/conversación donde se ejecuta el skill
      default: auto-detected
    - name: TYPE
      type: choice
      options: [bugfix, feature, integration]
      description: Tipo de caso / estructura del artículo
      default: auto-detected
    - name: AUDIENCE
      type: choice
      options: [funcional, tecnico, ejecutivo]
      description: Audiencia objetivo del artículo
      default: funcional
    - name: LENGTH
      type: choice
      options: [short, medium, long]
      description: Longitud objetivo del artículo
      default: medium
    - name: OUTPUT_DIR
      type: path
      description: Directorio de salida para el archivo generado
      default: projects/odoo/blog-articles/
    - name: ATTACH
      type: boolean
      description: Adjuntar archivo en la sesión
      default: true
  validation:
    - anonymization_complete
    - structure_follows_template
    - length_within_range
    - audience_content_appropriate
---

# 📝 Odoo Blog Article Generator

Transforma casos resueltos en topics de soporte de Odoo en artículos de blog profesionales, anonimizados y listos para publicar.

## Propósito

Este skill convierte el conocimiento tácito generado en conversaciones de soporte en contenido de marketing educativo estructurado. Cada caso resuelto se transforma en un artículo de blog que puede ayudar a toda la comunidad Odoo.

## Casos de Uso

- **Consultor resuelve caso complejo** → Genera artículo en 5-10 minutos (vs 4-8 horas manualmente)
- **Equipo de marketing necesita contenido** → Accede a base de casos resueltos automatizada
- **Nuevo consultor necesita aprender** → Lee artículos de casos previos para onboarding acelerado

## Instalación

Este skill está diseñado para funcionar con cualquier LLM desde cualquier entorno (CLI, IDE, web, Telegram, etc.). No requiere instalación adicional.

## Uso

### Invocación Básica

```
/odoo-blog-article --type feature --audience funcional --length medium
```

### Parámetros

| Parámetro | Opciones | Default | Descripción |
|-----------|----------|---------|-------------|
| `--type` | `bugfix`, `feature`, `integration` | Auto-detectado | Tipo de caso |
| `--audience` | `funcional`, `tecnico`, `ejecutivo` | `funcional` | Audiencia objetivo |
| `--length` | `short`, `medium`, `long` | `medium` | Longitud del artículo |
| `--output-dir` | path | `projects/odoo/blog-articles/` | Directorio de salida |
| `--attach` | `true`, `false` | `true` | Adjuntar en sesión |

### Longitudes

- **`short`** (1000-1500 palabras): Caso simple, solución directa
- **`medium`** (2000-3500 palabras): Caso completo con contexto y ejemplos
- **`long`** (4000-6000 palabras): Caso complejo con troubleshooting extendido

## Proceso

El skill opera en **4 fases automatizadas**:

### Fase 1: Lectura del Contexto
- Lee historial del topic (50-100 mensajes)
- Identifica problema central, solución implementada, módulos involucrados
- Clasifica tipo de caso (bugfix/feature/integration)

### Fase 2: Anonimización
Transforma datos sensibles en genéricos:
- Nombres de clientes → "una empresa de [sector]"
- Nombres de personas → "el equipo", "el administrador", "[rol]"
- Fechas específicas → "durante la implementación"
- Montos monetarios → "redujo costos operativos"
- URLs/IDs internos → eliminados o genericizados

### Fase 3: Generación del Artículo
Selecciona template según tipo y audiencia:

| Tipo | Estructura |
|------|------------|
| `bugfix` | 🐛 Problema → 🔍 Diagnóstico → 🔧 Solución → ✅ Resultado → 📚 Referencias |
| `feature` | 📌 Contexto → 🎯 Desafío → 🔍 Análisis → 💡 Solución → ✅ Resultados → 📚 Profundizar |
| `integration` | 📌 Escenario → 🔍 Arquitectura → 💡 Implementación → ⚠️ Consideraciones → ✅ Resultado |

### Fase 4: Validación y Entrega
- Aplica checklist de seguridad, calidad y transferibilidad
- Genera archivo `YYYY-MM-DD_titulo-slug.md`
- Adjunta en conversación si `ATTACH=true`

## Ejemplos

### Feature Funcional

**Entrada:** Topic de fechas de entrega por línea en órdenes de venta
**Invocación:**
```
/odoo-blog-article --type feature --audience funcional --length medium
```
**Salida:** Artículo de ~2500 palabras con:
- Historia de usuario del jefe de logística
- Análisis técnico de cómo Odoo maneja fechas por defecto
- Paso a paso desde la UI
- Beneficios por rol (Ventas, Logística, Administración)

### Bugfix Técnico

**Entrada:** Topic de error en conciliación bancaria
**Invocación:**
```
/odoo-blog-article --type bugfix --audience tecnico --length short
```
**Salida:** Artículo de ~1200 palabras con:
- Código de diagnóstico
- Referencias a archivos de Odoo core
- Solución con snippets de código

## Templates

- `templates/bugfix.md` - Para casos de error resuelto
- `templates/feature.md` - Para implementaciones nuevas
- `templates/integration.md` - Para conectores entre sistemas

Cada template incluye marcadores `[AUDIENCE: tipo]` para contenido condicional según la audiencia seleccionada.

## Referencias

- **Documentación completa:** Ver `SKILL.md`
- **Ejemplos generados:** Ver `examples/`
- **Prompts separados:** Ver `prompts/`
- **Tests de comportamiento:** Ver `tests/test_behavior.md`

## Limitaciones Éticas

**Nunca publicar:**
- Información que identifique un cliente específico
- Vulnerabilidades de seguridad sin reporte previo a Odoo S.A.
- Código propietario de terceros sin licencia abierta
- Workarounds que violen términos de servicio Odoo Enterprise

## Mejora Continua

Después de cada ejecución, clasificar resultado:
- ❌ **Malo:** Error obvio, dato sensible expuesto
- ⚠️ **OK:** Funciona pero podría ser mejor
- ✅ **Excelente:** Listo para publicar con mínimos ajustes

Las respuestas "OK" son donde vive la mejora real del sistema.

## Licencia

Este skill sigue los principios de OpenClaw para interoperabilidad entre LLMs y entornos.
