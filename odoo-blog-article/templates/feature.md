---
type: feature
audience: funcional|tecnico|ejecutivo
description: Template para artículos de feature / implementación nueva
---

# [TÍTULO: Cómo implementar [feature] en Odoo — caso práctico]

## 📌 Contexto

[300-400 palabras. Gancho + contexto del sector + por qué este problema es común + promesa de valor.]

**¿Para quién es este artículo?** [Nivel: intermedio/avanzado, prerrequisitos]

---

## 🎯 El Desafío

[400-600 palabras. Historia de usuario + flujo actual vs deseado + impacto + soluciones que NO funcionan.]

**Historia de usuario:**
> Como [rol], necesito [objetivo] para [beneficio].

**Flujo actual (antes de la solución):**
1. [Paso 1 — qué hacían antes]
2. [Paso 2 — problema que encontraban]
3. [Paso 3 — consecuencia]

**Soluciones que NO funcionan:**
- [Alternativa 1 + por qué falla]
- [Alternativa 2 + por qué falla]

[AUDIENCE: ejecutivo]
**Costo del problema:** [Tiempo perdido semanal, errores, retrabajos, impacto en satisfacción]
[AUDIENCE_END]

---

## 🔍 Análisis Técnico

[500-700 palabras. Estado default de Odoo + módulos involucrados + arquitectura de datos + flujo de datos.]

**Cómo viene en Odoo estándar:**
[Descripción del comportamiento default y sus limitaciones para este caso]

**Módulos involucrados:**
| Módulo | Propósito |
|--------|-----------|
| [nombre] | [qué hace] |
| [nombre] | [qué hace] |

[AUDIENCE: tecnico]
**Arquitectura de datos:**
- Modelos principales: `[modelo]` (campos relevantes: [lista])
- Relaciones: [one2many, many2one, many2many]
- Flujo de datos: [cómo viaja la información]

**Archivos de referencia:**
- `addons/[ruta]/[archivo].py` — [qué contiene]
- `addons/[ruta]/[archivo].xml` — [qué contiene]
[AUDIENCE_END]

[AUDIENCE: funcional]
**Configuración requerida:**
- [Ajuste de settings necesario]
- [Permisos requeridos]
[AUDIENCE_END]

---

## 💡 La Solución

[800-1200 palabras. Enfoque general + implementación + configuración y pruebas.]

**Qué logra (en términos de negocio):**
[Explicación funcional del resultado, no la implementación técnica]

**Alternativas consideradas:**
| Alternativa | Pros | Contras |
|-------------|------|---------|
| [Opción A] | [pros] | [contras] |
| [Opción B] | [pros] | [contras] |

**Implementación:**

[AUDIENCE: funcional]
**Paso a paso desde la UI:**
1. Ir a [Menú] → [Submenú] → [Acción]
2. Click en [Botón]
3. Completar [Campo] con [valor]
4. Guardar / Confirmar

**Pantallas involucradas:**
- [Descripción de cada pantalla y qué se ve]

**Campos nuevos/modificados:**
| Campo | Tipo | Propósito |
|-------|------|-----------|
| [nombre] | [tipo] | [qué hace] |

**Comportamiento esperado:**
- [Qué pasa después de cada acción]
- [Puntos de atención / errores comunes]

**Verificación funcional:**
- [ ] [Checkpoint 1 desde la UI]
- [ ] [Checkpoint 2 desde la UI]
[AUDIENCE_END]

[AUDIENCE: tecnico]
**Código esencial:**
```python
# archivo.py, línea X
# Explicación funcional de qué hace este código
[código clave — 1-2 líneas]
```

**Referencias técnicas:**
- Ver `addons/[ruta]/[archivo].py` — [qué hace]
- Herencia de `[modelo]` — [por qué es necesario]

**Verificación funcional:**
- [ ] [Cómo confirmar desde la UI que funciona]
[AUDIENCE_END]

[AUDIENCE: ejecutivo]
**Timeline de implementación:**
- Análisis: [X] días
- Desarrollo: [X] días
- Testing: [X] días
- Total: [X] días

**ROI estimado:**
- [Beneficio cuantificable]
[AUDIENCE_END]

**Configuración y Pruebas:**
- **Settings:** [Dónde en la UI, qué valor]
- **Permisos:** [Roles que necesitan acceso]
- **Scenario de prueba:** [Datos de ejemplo]
- **Pasos de verificación:** [Instrucciones completas]

---

## ✅ Resultados y Beneficios

[300-400 palabras. Mejoras funcionales + impacto medible + beneficios por rol + lecciones aprendidas.]

**Mejoras funcionales:**
- [Qué cambia en el día a día]

**Impacto medible:**
- [Tiempo ahorrado / errores reducidos / etc.]

**Beneficios por rol:**
| Rol | Qué gana |
|-----|----------|
| [Ventas] | [beneficio] |
| [Logística] | [beneficio] |
| [Administración] | [beneficio] |

**Lecciones aprendidas:**
- [Insight que puede ayudar a otros]

**Extensiones futuras:**
- [Ideas para mejorar o expandir]

---

## 📚 Para Profundizar

- [Documentación oficial Odoo — 1-2 oraciones]
- [Módulos OCA relacionados — descripción]
- [Forum y comunidad — links relevantes]

---

## 💬 ¿Tu experiencia es diferente?

[100-150 palabras. Invitación abierta + reconocimiento de alternativas + llamado a compartir]

---

**Metadata:**
- Tipo: feature
- Audiencia: [funcional|tecnico|ejecutivo]
- Versión Odoo: [v16/v17/v18/v19]
- Topic origen: #[ID]
- Estado: BORRADOR
