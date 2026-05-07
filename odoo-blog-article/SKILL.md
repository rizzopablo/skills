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

3. **Clasificar tipo de solución** (juicio)
   - **Funcional:** Configuración, flujo de trabajo, proceso de negocio
   - **Técnico:** Desarrollo de código, API, integración
   - **Híbrido:** Ambos aspectos presentes

**Criterio de clasificación:**
- Si la solución se puede implementar desde la UI sin código → Funcional
- Si requiere crear/modified archivos `.py`, `.xml`, `.js` → Técnico
- Si hay ambos aspectos → Híbrido (priorizar enfoque funcional en el artículo)

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

**Objetivo:** Producir artículo estructurado con enfoque funcional prioritario.

#### Principio de Contenido: Funcional sobre Técnico

**Jerarquía:**

1. **Primero (prioridad):** Explicación funcional
   - Casos de negocio concretos
   - Historias de usuario: "Como [rol], necesito [objetivo] para [beneficio]"
   - Flujos de trabajo desde la UI (Menú → Submenú → Acción)
   - Impacto operacional (tiempo, errores, retrabajos)

2. **Segundo (mínimo):** Referencias técnicas
   - Nombre del archivo (ej: `sale_order.py`)
   - 1-2 líneas de código si es esencial
   - Referencia a documentación oficial

3. **Excepción:** Si el tema es específicamente técnico
   - Mantener contexto funcional (por qué alguien necesitaría esto)
   - Incluir código completo con explicación de negocio

#### Estructura del Artículo

**Longitudes objetivo:**
- `short`: 1200-1800 palabras
- `medium`: 2000-3000 palabras
- `long`: 3500+ palabras

---

**📌 Introducción (300-400 palabras)**

**Propósito:** Contextualizar para que cualquier lector entienda por qué esto es relevante.

**Debe incluir:**
- **Gancho:** Pregunta o escenario que genere identificación ("¿Alguna vez te encontraste con que...?")
- **Contexto del sector:** Dónde es común este problema (distribución, manufactura, retail...)
- **Por qué existe:** Razones de diseño o técnicas que hacen que esta situación sea frecuente
- **Impacto general:** Cómo afecta el día a día (no solo técnicamente, sino operacionalmente)
- **Promesa de valor:** Qué podrá hacer el lector después de leer el artículo
- **Nivel y prerrequisitos:** Intermedio/avanzado, qué conocimientos se asumen

**Juicio requerido:** Seleccionar el gancho que mejor se alinee con el problema específico del caso.

---

**🎯 El Desafío (400-600 palabras)**

**Propósito:** Que el lector comprenda la naturaleza del problema y por qué las soluciones obvias fallan.

**Debe incluir:**
- **Historia de usuario:** Personaje (rol genérico) enfrentando el problema en situación real
- **Flujo actual vs. deseado:** Paso a paso desde la UI (cómo se hace hoy vs. cómo debería hacerse)
- **Impacto cuantificable:** Tiempo perdido, errores comunes, retrabajos, consultas de clientes
- **Soluciones que NO funcionan:** 2-3 enfoques que la gente intenta primero + por qué cada uno falla
- **Complejidad oculta:** Limitaciones técnicas o de diseño que hacen que una solución simple no sea posible
- **Quiénes enfrentan esto:** Sectores, roles, tamaños de empresa donde es más frecuente

**Juicio requerido:** Evaluar qué soluciones alternativas son más relevantes mencionar según el caso.

---

**🔍 Análisis Técnico (500-700 palabras)**

**Propósito:** Proporcionar comprensión profunda de la arquitectura relevante al problema.

**Debe incluir:**
- **Estado Default de Odoo:** Cómo viene "de fábrica", qué supuestos de diseño tomó Odoo y por qué
- **Módulos involucrados:** Listar módulos relevantes con propósito de cada uno y cómo se relacionan
- **Arquitectura de datos:** Modelos principales, campos relevantes, relaciones (one2many, many2one)
- **Flujo de datos:** Cómo viaja la información cuando ocurre la acción relevante
- **Comportamiento default vs. necesario:** Contrastar qué hace Odoo hoy vs. qué necesitamos
- **Limitaciones encontradas:** Barreras técnicas específicas (campos inexistentes, vistas no heredables)
- **Archivos de referencia:** Rutas completas a archivos de Odoo relevantes
- **Versiones afectadas:** Aplica a todas las versiones o solo algunas, diferencias Community/Enterprise

**Juicio requerido:** Determinar qué nivel de detalle técnico es necesario según la clasificación (funcional/técnico/híbrido).

---

**💡 La Solución (800-1200 palabras)**

**Propósito:** Guiar al lector paso a paso, priorizando explicación funcional.

**Enfoque general (200-300 palabras):**
- **Qué logra (en términos de negocio):** Explicar resultado funcional, no implementación técnica
- **Por qué este enfoque:** Razones funcionales y prácticas (no solo técnicas)
- **Alternativas consideradas:** 2-3 enfoques alternativos con pros/contras desde perspectiva de usuario
- **Prerrequisitos funcionales:** Módulos instalados, permisos necesarios, configuración previa

**Implementación Funcional (para soluciones funcionales, 500-700 palabras):**

**No incluir código.** Describir:
1. **Flujo de trabajo desde la UI:**
   - Paso 1: Ir a [Menú] → [Submenú] → [Acción]
   - Paso 2: Click en [Botón]
   - Paso 3: Completar [Campo]
   - Paso 4: Guardar/Confirmar
2. **Pantallas involucradas:** Qué se ve en cada pantalla
3. **Campos nuevos/modificados:** Nombre, tipo, propósito funcional
4. **Comportamiento esperado:** Qué pasa después de cada acción
5. **Puntos de atención:** Errores comunes, trampas de configuración
6. **Verificación funcional:** Checkpoints desde la UI ("Deberías ver una nueva columna en...")

**Implementación Técnica (para soluciones técnicas, 500-700 palabras):**

Para cada paso:
- **Objetivo funcional:** Qué se logra en términos de negocio
- **Contexto:** Por qué es necesario este desarrollo
- **Referencia técnica:** "Ver `archivo.py`, línea X" (1-2 líneas de código si es esencial)
- **Explicación funcional:** Qué hace el código en términos de negocio
- **Verificación funcional:** Cómo confirmar desde la UI que funciona

**Configuración y Pruebas (150-250 palabras):**
- **Settings necesarios:** Dónde en la UI, qué valor debe tener
- **Permisos:** Qué roles necesitan acceso y por qué
- **Scenario de prueba:** Datos de ejemplo para probar (ej: "Crear orden con 3 líneas, fechas diferentes")
- **Pasos de verificación:** Instrucciones completas desde la UI

**Juicio requerido:** Decidir cuántos pasos son necesarios para que sea replicable sin ambigüedades.

---

**✅ Resultados y Beneficios (300-400 palabras)**

**Propósito:** Que el lector entienda el valor concreto y pueda evaluar si vale la pena en su contexto.

**Debe incluir:**
- **Mejoras funcionales detalladas:** Qué cambia en el día a día, con ejemplos concretos de uso
- **Impacto medible:** Tiempo ahorrado, errores reducidos, consultas eliminadas (rangos o porcentajes genéricos)
- **Beneficios por rol:** Qué gana cada tipo de usuario (Ventas, Logística, Administración, Clientes)
- **Mejoras en reporting:** Cómo mejora la visibilidad y toma de decisiones
- **Lecciones aprendidas:** Insights obtenidos que pueden ayudar a otros
- **Qué monitorear:** Indicadores o señales a observar después de implementar
- **Posibles extensiones:** Ideas para mejorar o expandir la solución en el futuro

**Juicio requerido:** Priorizar los beneficios más relevantes según el sector/rol del caso original.

---

**📚 Para Profundizar (200-300 palabras)**

**Propósito:** Proporcionar recursos de calidad para expandir comprensión más allá del artículo.

**Debe incluir:**
- **Documentación oficial Odoo:** Links específicos con 1-2 oraciones explicando qué contiene cada uno
- **Módulos OCA relacionados:** Repositorios que abordan temas similares, descripción de qué hace cada uno
- **Forum y comunidad:** Threads relevantes, grupos de discusión, canales de Slack/Discord
- **Artículos complementarios:** Blogs o tutoriales que profundicen en aspectos relacionados
- **Videos o conferencias (opcional):** Charlas de Odoo Experience o tutoriales en video

**Juicio requerido:** Seleccionar recursos que realmente aporten valor, no solo listar links.

---

**💬 ¿Tu experiencia es diferente? (100-150 palabras)**

**Propósito:** Fomentar participación de la comunidad y reconocer enfoques alternativos.

**Debe incluir:**
- **Invitación abierta:** Preguntar si otros implementaron esto de forma diferente
- **Reconocimiento de alternativas:** Validar que pueden existir múltiples soluciones válidas
- **Llamado a compartir:** Animar a compartir experiencias, mejoras, problemas encontrados
- **Dónde continuar:** Links a forum, issues de GitHub, o canales de discusión

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
- [ ] ¿Un consultor funcional puede entenderlo sin saber programación?
- [ ] ¿Hay al menos 1 historia de usuario concreta (con personaje y situación)?
- [ ] ¿El flujo está descrito desde la UI (Menú → Acción)?
- [ ] ¿El código es mínimo (solo referencias, 1-2 líneas)?
- [ ] ¿Los beneficios están por rol (Ventas, Logística, etc.)?
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
   - Metadata al final: Topic origen, fecha, longitud, estado (BORRADOR)

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
/odoo-blog-article --length medium
```

**Output:**
- Archivo: `projects/odoo/blog-articles/2026-04-14_fechas-entrega-por-linea.md`
- Adjunto en sesión para descarga inmediata
- Artículo: ~2500 palabras, enfoque funcional, anonimizado

---

## Referencias

- Plantilla completa: `templates/article-template.md`
- Anonimización: `prompts/anonymization.md`
- Ejemplo: `examples/sample-article.md`

Si no encuentras el template y el ejemplo, debes guiar al usuario para que te describa qué tipo de artículo le gusta, crear con el usuario un template y un ejemplo, almacenarlo en el lugar de referencia para que puedas usarlo. Si el template y el ejemplo ya existen, usas los existentes sin crear uno nuevo.


