---
name: bugfix
type: template
description: Template para artículos de blog tipo bugfix / problema resuelto
author: lama_su
version: 1.0.0
openclaw:
  compatible_audiences: [funcional, tecnico, ejecutivo]
  sections:
    - problema
    - diagnostico
    - solucion
    - resultado
    - referencias
    - pregunta
  estimated_length:
    short: 1000-1500
    medium: 2000-2500
    long: 3000-3500
---

# [TÍTULO: Bug resuelto en Odoo — descripción corta del problema]

## 🐛 El Problema

[2-3 oraciones describiendo el comportamiento erróneo. Incluir mensaje de error exacto si aplica.]

**Sintomas observados:**
- [Sintoma 1]
- [Sintoma 2]
- [Sintoma 3]

**Impacto:** [Qué dejaba de funcionar, a quién afectaba, frecuencia del problema]

---

## 🔍 Diagnóstico

[Investigación: qué causaba el bug, evidencia encontrada, cómo se aisló el problema.]

**Causa raíz:** [Explicación clara del origen del problema]

[AUDIENCE: tecnico]
```python
# Referencia al archivo y línea donde se origina el bug
# archivo.py, línea X
```
[AUDIENCE_END]

[AUDIENCE: funcional]
**Desde la UI:** [Describir qué se veía en pantalla, qué acción desencadenaba el error]
[AUDIENCE_END]

[AUDIENCE: ejecutivo]
**Impacto en negocio:** [Tiempo perdido, errores en datos, quejas de usuarios, costo estimado]
[AUDIENCE_END]

---

## 🔧 La Solución

[Descripción de la solución aplicada.]

[AUDIENCE: tecnico]
**Cambio aplicado:**
```python
# Antes
[línea problemática]

# Después
[línea corregida]
```
**Explicación técnica:** [Por qué el cambio corrige el bug, qué mecanismo de Odoo se ve afectado]
[AUDIENCE_END]

[AUDIENCE: funcional]
**Cómo verificar que se corrigió:**
1. Ir a [Menú] → [Submenú]
2. Realizar [acción que antes fallaba]
3. Confirmar que [resultado esperado]
[AUDIENCE_END]

[AUDIENCE: ejecutivo]
**Resolución:** [En 2-3 oraciones, qué se hizo y cuánto tiempo tomó]
[AUDIENCE_END]

---

## ✅ Resultado

[Confirmación de que el bug fue resuelto y cómo verificarlo.]

**Verificación:**
- [ ] [Check 1]
- [ ] [Check 2]

**Lección aprendida:** [Insight que puede ayudar a evitar bugs similares]

---

## 📚 Referencias

- [Link a issue de Odoo si existe]
- [Link a PR o commit si aplica]
- [Documentación relevante]

---

## 💬 ¿Te pasó lo mismo?

[Invitación a compartir experiencias similares o soluciones alternativas]

---

**Metadata:**
- Tipo: bugfix
- Audiencia: [funcional|tecnico|ejecutivo]
- Versión Odoo: [v16/v17/v18/v19]
- Topic origen: #[ID]
- Longitud: [short|medium|long]
- Estado: BORRADOR
