---
name: test-behavior
description: Tests de comportamiento esperado del skill odoo-blog-article
type: test-suite
---

# Tests de Comportamiento: odoo-blog-article

## Suite: Generación de Artículos

### Test 1: Feature Funcional Medium

**ID:** TC-001  
**Descripción:** Generación de artículo tipo feature para audiencia funcional con longitud medium  
**Prioridad:** Alta

#### Entrada

**Contexto:** Topic de soporte Odoo con caso resuelto sobre fechas de entrega por línea

**Parámetros:**
```yaml
TYPE: feature
AUDIENCE: funcional
LENGTH: medium
OUTPUT_DIR: projects/odoo/blog-articles/
ATTACH: true
```

#### Comportamiento Esperado

1. **Lectura del Contexto (Phase 1)**
   - [ ] El skill debe leer el historial completo del topic (50+ mensajes)
   - [ ] Debe identificar el problema: "Necesitan fechas de entrega diferentes por línea de venta"
   - [ ] Debe identificar la solución: "Campo custom en sale.order.line + lógica de agrupación de pickings"
   - [ ] Debe clasificar tipo como `feature` (no bugfix ni integration)
   - [ ] Debe detectar audiencia como `funcional` (más consultores que desarrolladores en el topic)

2. **Anonimización (Phase 2)**
   - [ ] Nombre de cliente "Cervecería del Sur" → "una empresa de producción de bebidas"
   - [ ] Nombre "Juan (administrador)" → "el administrador del sistema"
   - [ ] Fecha "15 de marzo" → "durante la implementación"
   - [ ] IDs de órdenes → "la orden de venta", "los registros"
   - [ ] Test de generalización: ¿Aplica a 10+ empresas? → SÍ

3. **Generación (Phase 3)**
   - [ ] Debe usar template `templates/feature.md`
   - [ ] Debe incluir secciones: Contexto, Desafío, Análisis, Solución, Resultados, Profundizar, Pregunta final
   - [ ] Debe incluir historia de usuario con rol "jefe de logística"
   - [ ] Debe describir flujo UI: "Ventas → Órdenes → ..."
   - [ ] NO debe incluir bloques `[AUDIENCE: tecnico]` ni `[AUDIENCE: ejecutivo]`
   - [ ] Debe incluir tabla de beneficios por rol

4. **Validación y Entrega (Phase 4)**
   - [ ] Debe pasar checklist de seguridad (sin nombres reales, sin URLs)
   - [ ] Debe pasar checklist de calidad (historia de usuario, flujo UI)
   - [ ] Longitud debe estar entre 2000-3500 palabras
   - [ ] Debe generar archivo con nombre formato `YYYY-MM-DD_titulo-slug.md`
   - [ ] Debe adjuntar archivo en la conversación
   - [ ] Metadata al final debe incluir: tipo, audiencia, versión Odoo, topic origen, estado BORRADOR

#### Criterios de Éxito
- Artículo generado y adjuntado
- Longitud dentro de rango medium
- Sin datos sensibles
- Estructura completa según template feature

---

### Test 2: Bugfix Técnico Short

**ID:** TC-002  
**Descripción:** Generación de artículo tipo bugfix para audiencia técnica con longitud short  
**Prioridad:** Alta

#### Entrada

**Contexto:** Topic sobre error de conciliación bancaria en Odoo v17

**Parámetros:**
```yaml
TYPE: bugfix
AUDIENCE: tecnico
LENGTH: short
OUTPUT_DIR: projects/odoo/blog-articles/
ATTACH: true
```

#### Comportamiento Esperado

1. **Lectura del Contexto (Phase 1)**
   - [ ] Debe identificar error específico en módulo `account`
   - [ ] Debe identificar causa raíz: problema en reconciliación con pagos parciales
   - [ ] Debe clasificar tipo como `bugfix` (corrección de error)
   - [ ] Debe detectar audiencia como `tecnico` (hay código y referencias a archivos `.py`)

2. **Anonimización (Phase 2)**
   - [ ] Datos de prueba del cliente → datos de ejemplo genéricos
   - [ ] URLs de instancia de prueba → "la instancia de prueba"

3. **Generación (Phase 3)**
   - [ ] Debe usar template `templates/bugfix.md`
   - [ ] Debe incluir: Problema, Diagnóstico, Solución, Resultado, Referencias
   - [ ] Debe incluir código con explicación funcional
   - [ ] Debe referenciar archivos específicos de Odoo core
   - [ ] NO debe incluir explicaciones extensas de UI (audiencia técnica)

4. **Validación y Entrega (Phase 4)**
   - [ ] Longitud entre 1000-1500 palabras (short)
   - [ ] Código debe tener explicación de QUÉ hace, no solo CÓMO
   - [ ] Debe incluir referencias a archivos y líneas de Odoo

#### Criterios de Éxito
- Artículo tipo bugfix generado
- Longitud dentro de rango short
- Código técnico presente con explicación funcional
- Referencias precisas a archivos Odoo

---

### Test 3: Integration Ejecutivo Long

**ID:** TC-003  
**Descripción:** Generación de artículo tipo integration para audiencia ejecutiva con longitud long  
**Prioridad:** Media

#### Entrada

**Contexto:** Topic sobre integración Odoo + Shopify para e-commerce

**Parámetros:**
```yaml
TYPE: integration
AUDIENCE: ejecutivo
LENGTH: long
OUTPUT_DIR: projects/odoo/blog-articles/
ATTACH: true
```

#### Comportamiento Esperado

1. **Lectura del Contexto (Phase 1)**
   - [ ] Debe identificar dos sistemas: Odoo y Shopify
   - [ ] Debe identificar objetivo de integración: sincronización de órdenes e inventario
   - [ ] Debe clasificar tipo como `integration` (conexión entre sistemas)
   - [ ] Debe detectar audiencia como `ejecutivo` (discusión de costos y ROI en el topic)

2. **Anonimización (Phase 2)**
   - [ ] Nombre de empresa del caso → sector genérico de e-commerce
   - [ ] Volúmenes específicos de ventas → "volumen significativo de transacciones"

3. **Generación (Phase 3)**
   - [ ] Debe usar template `templates/integration.md`
   - [ ] Debe incluir: Escenario, Arquitectura, Implementación, Consideraciones, Resultado
   - [ ] Debe incluir secciones de ROI, timeline, métricas de éxito
   - [ ] Debe incluir costo del problema cuantificado
   - [ ] NO debe incluir código extenso ni detalles técnicos de implementación
   - [ ] Debe incluir riesgos y mitigaciones

4. **Validación y Entrega (Phase 4)**
   - [ ] Longitud entre 4000-6000 palabras (long)
   - [ ] Debe incluir ROI estimado
   - [ ] Debe incluir timeline de implementación por fases
   - [ ] Beneficios deben estar cuantificados en términos de negocio

#### Criterios de Éxito
- Artículo tipo integration generado
- Longitud dentro de rango long
- Enfoque ejecutivo con métricas y ROI
- Sin detalles técnicos excesivos

---

### Test 4: Auto-detección de Tipo y Audiencia

**ID:** TC-004  
**Descripción:** Verificar que el skill detecte automáticamente TYPE y AUDIENCE cuando no se especifican  
**Prioridad:** Alta

#### Entrada

**Contexto:** Topic sobre desarrollo de módulo custom para flujo de aprobación de facturas

**Parámetros:**
```yaml
TYPE: auto-detected  # No especificado
AUDIENCE: auto-detected  # No especificado
LENGTH: medium
```

#### Comportamiento Esperado

- [ ] Debe analizar el topic y detectar que hay código Python y XML
- [ ] Debe clasificar TYPE como `feature` (implementación nueva)
- [ ] Debe clasificar AUDIENCE como `tecnico` (hay desarrollo explícito)
- [ ] Debe informar al usuario las detecciones realizadas
- [ ] Debe proceder con la generación usando los valores detectados

#### Criterios de Éxito
- Detección correcta de TYPE como feature
- Detección correcta de AUDIENCE como tecnico
- Comunicación clara al usuario de las decisiones tomadas

---

### Test 5: Validación de Seguridad - Detección de Datos Sensibles

**ID:** TC-005  
**Descripción:** Verificar que el skill detecte y rechace contenido con datos sensibles no anonimizados  
**Prioridad:** Crítica

#### Entrada

**Contexto:** Topic que contiene:
- Nombre de empresa real: "Inversiones García S.A."
- URL de producción: "https://garcia-prod.odoo.com"
- ID de orden: "Order #12345"
- API Key: "sk-abc123xyz789"

**Parámetros:**
```yaml
TYPE: feature
AUDIENCE: funcional
LENGTH: medium
```

#### Comportamiento Esperado

1. **Fase 2 - Anonimización**
   - [ ] Debe detectar todos los datos sensibles
   - [ ] Debe aplicar transformaciones:
     - "Inversiones García S.A." → "una empresa del sector [detectado]"
     - "https://garcia-prod.odoo.com" → "la instancia de producción"
     - "Order #12345" → "la orden de venta"
     - "sk-abc123xyz789" → "[credenciales configuradas]" (o eliminar)

2. **Fase 4 - Validación**
   - [ ] Debe pasar todas las verificaciones de seguridad
   - [ ] Si detecta datos sensibles no procesados, debe:
     - Informar del problema específico
     - Volver a Fase 2 para reprocesar
     - No entregar artículo con datos sensibles expuestos

#### Criterios de Éxito
- Datos sensibles completamente anonimizados
- Artículo no contiene información que identifique al cliente
- Test de generalización pasa (aplica a 10+ empresas)

---

### Test 6: Longitud Short vs Medium vs Long

**ID:** TC-006  
**Descripción:** Verificar que diferentes longitudes produzcan artículos de tamaños apropiados  
**Prioridad:** Media

#### Entradas y Comportamientos

**Caso Short:**
- Parámetros: LENGTH=short
- Contexto: Caso simple de configuración de settings
- Esperado: 1000-1500 palabras, estructura concisa, sin ejemplos extensos

**Caso Medium:**
- Parámetros: LENGTH=medium
- Contexto: Caso completo con configuración y flujo de trabajo
- Esperado: 2000-3500 palabras, contexto completo, 1-2 ejemplos

**Caso Long:**
- Parámetros: LENGTH=long
- Contexto: Caso complejo con múltiples escenarios y troubleshooting
- Esperado: 4000-6000 palabras, contexto profundo, múltiples ejemplos, edge cases

#### Criterios de Éxito
- Cada longitud produce artículo dentro de su rango objetivo
- Short es suficiente para casos simples
- Long incluye troubleshooting y lecciones extendidas

---

### Test 7: Manejo de Templates Ausentes

**ID:** TC-007  
**Descripción:** Verificar comportamiento cuando no se encuentran templates o ejemplos  
**Prioridad:** Baja

#### Entrada

**Contexto:** Topic válido
**Templates:** Simular ausencia de archivos en `templates/`

#### Comportamiento Esperado

- [ ] Debe detectar que no existen templates
- [ ] Debe informar al usuario de la situación
- [ ] Debe guiar al usuario para describir qué tipo de artículo necesita
- [ ] Debe crear template básico junto con el usuario
- [ ] Debe almacenar template creado para uso futuro

#### Criterios de Éxito
- Comunicación clara de la situación
- Guía efectiva al usuario
- Creación de template funcional

---

## Suite: Validación y Calidad

### Test 8: Checklist Completo de Validación

**ID:** TC-008  
**Descripción:** Verificar que se apliquen todos los items del checklist de validación  
**Prioridad:** Alta

#### Checklist a Verificar

**Seguridad y Anonimización:**
- [ ] Ningún nombre de cliente real
- [ ] Ningún dato financiero específico
- [ ] No hay URLs de producción
- [ ] No hay IDs de registros
- [ ] No hay credenciales o API keys
- [ ] No hay nombres de personas
- [ ] No hay ubicaciones geográficas específicas

**Calidad Funcional (para funcional):**
- [ ] Consultor funcional puede entenderlo
- [ ] Al menos 1 historia de usuario concreta
- [ ] Flujo descrito desde UI
- [ ] Código mínimo o ninguno
- [ ] Beneficios por rol

**Transferibilidad:**
- [ ] Aplicable a 10+ empresas
- [ ] No identificable el cliente original
- [ ] Problema reconocible para usuarios Odoo
- [ ] Solución aplicable en contextos similares

**Formato:**
- [ ] Título claro (60-80 caracteres)
- [ ] Longitud dentro de target
- [ ] Metadata completa al final

---

### Test 9: Clasificación de Resultado

**ID:** TC-009  
**Descripción:** Verificar que el skill clasifique el resultado según calidad  
**Prioridad:** Media

#### Escenarios

**Escenario 1: Excelente**
- Artículo completo, bien estructurado, sin errores
- Esperado: Clasificación ✅ Excelente
- Acción: Entregar normalmente

**Escenario 2: OK (necesita mejora)**
- Artículo funciona pero falta contexto en sección de análisis
- Esperado: Clasificación ⚠️ OK
- Acción: Entregar con nota de mejora, documentar brecha

**Escenario 3: Malo**
- Artículo con datos sensibles no anonimizados
- Esperado: Clasificación ❌ Malo
- Acción: No entregar, volver a procesar

---

## Suite: Salida y Entrega

### Test 10: Formato de Archivo y Metadata

**ID:** TC-010  
**Descripción:** Verificar formato correcto del archivo generado  
**Prioridad:** Alta

#### Verificaciones

**Nombre de archivo:**
- Formato: `YYYY-MM-DD_<titulo-slug>.md`
- Ejemplo válido: `2026-04-14_fechas-entrega-por-linea.md`

**Metadata al final:**
```markdown
**Metadata:**
- Tipo: feature
- Audiencia: funcional
- Versión Odoo: v17
- Topic origen: #567
- Longitud: medium
- Estado: BORRADOR
```

**Adjunto:**
- [ ] Archivo adjunto en conversación
- [ ] Caption informativo con título, ruta, longitud
- [ ] Recordatorio de checklist de seguridad

---

## Suite: Casos de Borde

### Test 11: Topic con Pocos Mensajes

**ID:** TC-011  
**Descripción:** Comportamiento con topic de menos de 50 mensajes  
**Prioridad:** Baja

#### Entrada
Topic con solo 20 mensajes, caso resuelto

#### Comportamiento Esperado
- [ ] Debe leer todos los mensajes disponibles
- [ ] Debe informar que el contexto es limitado
- [ ] Debe generar artículo más corto o solicitar confirmación
- [ ] Debe ajustar expectativas de calidad

---

### Test 12: Caso No Clasificable

**ID:** TC-012  
**Descripción:** Topic que no encaja claramente en bugfix/feature/integration  
**Prioridad:** Baja

#### Entrada
Topic ambiguo, mezcla de consulta y configuración

#### Comportamiento Esperado
- [ ] Debe aplicar default: TYPE=feature
- [ ] Debe informar al usuario de la clasificación por defecto
- [ ] Debe solicitar confirmación o ajuste del usuario

---

## Resumen de Tests

| ID | Descripción | Prioridad | Estado |
|----|-------------|-----------|--------|
| TC-001 | Feature funcional medium | Alta | Pendiente |
| TC-002 | Bugfix técnico short | Alta | Pendiente |
| TC-003 | Integration ejecutivo long | Media | Pendiente |
| TC-004 | Auto-detección de parámetros | Alta | Pendiente |
| TC-005 | Validación de seguridad | Crítica | Pendiente |
| TC-006 | Diferentes longitudes | Media | Pendiente |
| TC-007 | Templates ausentes | Baja | Pendiente |
| TC-008 | Checklist de validación | Alta | Pendiente |
| TC-009 | Clasificación de resultado | Media | Pendiente |
| TC-010 | Formato de archivo | Alta | Pendiente |
| TC-011 | Topic con pocos mensajes | Baja | Pendiente |
| TC-012 | Caso no clasificable | Baja | Pendiente |

## Notas de Implementación de Tests

Para ejecutar estos tests:

1. Preparar contextos de prueba (topics simulados o reales anonimizados)
2. Invocar skill con parámetros específicos
3. Verificar salida contra comportamiento esperado
4. Documentar resultados y brechas

**Tests automatizables:** TC-005 (validación de seguridad), TC-010 (formato de archivo)

**Tests que requieren juicio:** TC-001 (calidad de contenido), TC-009 (clasificación de resultado)
