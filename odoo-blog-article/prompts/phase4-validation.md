---
name: phase4-validation
type: phase
description: Fase 4 - Validación y entrega del artículo
phase: 4
---

# Phase 4: Validación y Entrega

## Objetivo
Asegurar la calidad del artículo generado antes de entregarlo al usuario, aplicando un checklist completo de validación.

## Entrada
- `generated_article` de Phase 3
- Parámetros originales: `TYPE`, `AUDIENCE`, `LENGTH`, `OUTPUT_DIR`, `ATTACH`

## Checklist de Validación

### 1. Seguridad y Anonimización

Verificar que NO haya datos sensibles expuestos:

- [ ] **¿Ningún nombre de cliente real aparece?**
  - Buscar: nombres de empresas conocidas, nombres propios
  - Verificar: que todos estén transformados a genéricos

- [ ] **¿Ningún dato financiero específico está expuesto?**
  - Buscar: montos específicos, "$XXX,XXX", "XXX USD"
  - Verificar: que estén transformados a rangos o descripciones genéricas

- [ ] **¿No hay URLs de producción o internas?**
  - Buscar: "https://", "http://", dominios específicos
  - Verificar: que estén reemplazadas por "el sistema", "la instancia"

- [ ] **¿No hay IDs de registros reales?**
  - Buscar: "#12345", "ID:", "Order #", números de ticket
  - Verificar: que estén reemplazados por "el registro", "la orden"

- [ ] **¿No hay credenciales o API keys en código?**
  - Buscar: "sk-", "api_key", "token", "password"
  - Verificar: que estén reemplazadas por placeholders o eliminadas

- [ ] **¿No hay nombres de personas?**
  - Buscar: nombres propios que no sean roles genéricos
  - Verificar: que estén reemplazados por "el equipo", "el administrador", "[rol]"

- [ ] **¿No hay ubicaciones geográficas específicas?**
  - Buscar: nombres de ciudades, países específicos
  - Verificar: que estén reemplazadas por "en la región", "localmente"

**Si falla algún ítem:**
- Regresar a Phase 2 (Anonimización)
- Reprocesar el contenido
- Volver a validar

### 2. Calidad Funcional

Verificar que el contenido cumpla con estándares de calidad:

**Para `AUDIENCE = funcional`:**
- [ ] **¿Un consultor funcional puede entenderlo sin saber programación?**
  - Verificar: no hay código sin explicación
  - Verificar: los conceptos técnicos están explicados

- [ ] **¿Hay al menos 1 historia de usuario concreta?**
  - Verificar: hay bloque de quote con "Como [rol], necesito..."
  - Verificar: el personaje y situación son claros

- [ ] **¿El flujo está descrito desde la UI (Menú → Acción)?**
  - Verificar: hay pasos como "Ir a Ventas → Órdenes → Crear"
  - Verificar: los menús y botones son identificables

- [ ] **¿El código es mínimo (solo referencias, 1-2 líneas)?**
  - Verificar: no hay bloques de código extensos
  - Verificar: si hay código, es solo para ilustrar (no para copiar)

- [ ] **¿Los beneficios están por rol (Ventas, Logística, etc.)?**
  - Verificar: tabla de beneficios con columnas "Rol" y "Qué gana"
  - Verificar: múltiples roles están cubiertos

**Para `AUDIENCE = tecnico`:**
- [ ] **¿El código tiene explicación funcional?**
  - Verificar: cada bloque de código tiene comentario explicando QUÉ hace en términos de negocio
  - Verificar: no solo CÓMO lo hace

- [ ] **¿Las referencias técnicas son precisas?**
  - Verificar: archivos y modelos de Odoo están correctamente referenciados
  - Verificar: versiones de módulos son correctas

- [ ] **¿La arquitectura está explicada?**
  - Verificar: hay diagrama o descripción de flujo de datos
  - Verificar: las relaciones entre modelos están claras

**Para `AUDIENCE = ejecutivo`:**
- [ ] **¿El costo del problema está cuantificado?**
  - Verificar: hay estimación de tiempo perdido, errores, retrabajos

- [ ] **¿El ROI está estimado?**
  - Verificar: hay proyección de retorno de inversión
  - Verificar: hay métricas de éxito

- [ ] **¿Hay timeline de implementación?**
  - Verificar: duración estimada por fase (análisis, desarrollo, testing)

### 3. Transferibilidad

Verificar que el artículo sea útil para la comunidad en general:

- [ ] **¿Podría este artículo aplicar a 10+ empresas diferentes?**
  - Pregunta: ¿Es demasiado específico de un sector o situación particular?

- [ ] **¿Un lector externo podría identificar el cliente original?**
  - Debe ser NO
  - Verificar: que no haya detalles únicos que identifiquen al cliente

- [ ] **¿El problema descrito es reconocible para usuarios de Odoo?**
  - Verificar: que el problema sea común en implementaciones Odoo
  - Verificar: que la solución sea aplicable en contextos similares

- [ ] **¿La solución es aplicable en contextos similares?**
  - Verificar: que no dependa de configuraciones ultra-específicas
  - Verificar: que sea replicable con esfuerzo razonable

### 4. Formato y Estructura

Verificar aspectos técnicos del documento:

- [ ] **¿Título claro y descriptivo (60-80 caracteres)?**
  - Verificar: incluye acción + contexto de Odoo
  - Ejemplo válido: "Cómo implementar fechas de entrega por línea en Odoo"

- [ ] **¿Longitud dentro del target seleccionado?**
  - `short`: 1000-1500 palabras
  - `medium`: 2000-3500 palabras
  - `long`: 4000-6000 palabras
  - Verificar: hacer conteo aproximado

- [ ] **¿Todas las secciones del template están presentes?**
  - Verificar: según `TYPE`, comparar contra estructura esperada
  - bugfix: 6 secciones
  - feature: 7 secciones
  - integration: 7 secciones

- [ ] **¿Links verificados y activos?**
  - Verificar: documentación oficial de Odoo
  - Verificar: módulos OCA mencionados
  - Nota: si no se pueden verificar en tiempo real, marcar para revisión manual

- [ ] **¿Tags relevantes asignados?**
  - Verificar: módulos de Odoo mencionados
  - Verificar: versión de Odoo

- [ ] **¿Metadata completa al final?**
  - Verificar bloque:
    ```markdown
    **Metadata:**
    - Tipo: [bugfix|feature|integration]
    - Audiencia: [funcional|tecnico|ejecutivo]
    - Versión Odoo: [v16/v17/v18/v19]
    - Topic origen: #[ID]
    - Estado: BORRADOR
    ```

### 5. Consistencia

Verificar coherencia interna del artículo:

- [ ] **¿La solución responde al problema planteado?**
  - Verificar: que no haya desconexión entre secciones

- [ ] **¿Los módulos mencionados son consistentes?**
  - Verificar: que no haya módulos en análisis que no aparezcan en solución

- [ ] **¿La audiencia es consistente?**
  - Verificar: que no haya código extenso si audience=funcional
  - Verificar: que no haya detalles de UI excesivos si audience=tecnico

- [ ] **¿El tono es consistente?**
  - Verificar: professional pero accesible
  - Verificar: sin cambios bruscos de voz

## Proceso de Validación

### Paso 1: Revisión Automática
Aplicar todas las verificaciones de seguridad y formato que sean automatizables.

### Paso 2: Revisión Manual (si aplica)
Para verificaciones que requieren juicio (calidad funcional, transferibilidad).

### Paso 3: Clasificación del Resultado

Clasificar el artículo según calidad:

| Clasificación | Criterios | Acción |
|---------------|-----------|--------|
| ❌ **Malo** | Error obvio, dato sensible expuesto, estructura incompleta | Rechazar, volver a Fase 2 o 3 |
| ⚠️ **OK** | Funciona pero podría ser mejor (falta contexto, beneficios poco claros) | Entregar con nota de mejora |
| ✅ **Excelente** | Listo para publicar con mínimos ajustes | Entregar normalmente |

**Importante:** Las respuestas "OK" son donde vive la mejora real del sistema. Documentar brechas.

### Paso 4: Generación del Archivo

Si pasa validación:

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
   - Metadata: Al final del archivo

4. **Adjuntar en sesión (si ATTACH = true):**
   - Enviar archivo como adjunto
   - Caption informativo:
     ```
     📄 Artículo generado: [Título]
     📁 Ubicación: [ruta completa]
     📊 Longitud: [X] palabras
     ✅ Estado: BORRADOR (revisar antes de publicar)
     
     🔍 Recordatorio: Verificar checklist de seguridad antes de publicar
     ```

## Manejo de Errores

### Si falla validación de seguridad:
```
ERROR: Datos sensibles detectados en el artículo
- Sección: [sección]
- Problema: [descripción]
- Acción: Reprocesando anonimización...
```
Regresar a Phase 2.

### Si falla validación de estructura:
```
ERROR: Estructura incompleta
- Template: [type]
- Faltan secciones: [lista]
- Acción: Completando secciones faltantes...
```
Regresar a Phase 3.

### Si longitud fuera de rango:
```
WARNING: Longitud fuera de target
- Target: [length] ([min]-[max] palabras)
- Actual: [count] palabras
- Acción: [Expandiendo|Condensando] contenido...
```
Ajustar en Phase 3.

## Salida Final

```yaml
delivered_article:
  filename: "YYYY-MM-DD_<titulo-slug>.md"
  path: "[OUTPUT_DIR]/[filename]"
  word_count: "[número]"
  validation_status:
    security: "[pass|fail]"
    quality: "[pass|fail]"
    transferability: "[pass|fail]"
    format: "[pass|fail]"
  classification: "[malo|ok|excelente]"
  attached: "[true|false]"
  notes: "[notas de mejora si aplica]"
```

## Mejora Continua

Después de entregar, registrar:

1. **Clasificación del resultado** (malo/ok/excelente)
2. **Brechas identificadas** (si classification = ok)
3. **Sugerencias de mejora** para el skill

**Principio:** Las respuestas "OK" son donde vive la mejora real del sistema.
