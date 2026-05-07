---
type: integration
audience: funcional|tecnico|ejecutivo
description: Template para artículos de integración / conector entre sistemas
---

# [TÍTULO: Integrar Odoo con [Sistema Externo] — guía completa]

## 📌 Escenario

[300-400 palabras. Contexto + qué sistemas intervienen + por qué necesitan comunicarse + promesa de valor.]

**Sistemas involucrados:**
| Sistema | Rol | Versión |
|---------|-----|---------|
| Odoo | [qué hace en la integración] | [v16/v17/v18/v19] |
| [Sistema externo] | [qué hace] | [versión] |

---

## 🔍 Arquitectura de la Integración

[500-700 palabras. Protocolos + autenticación + flujo de datos + modelo de datos compartido.]

**Protocolo de comunicación:**
- [REST API / XML-RPC / JSON-RPC / Webhooks / CSV / otro]
- [Formato de datos: JSON / XML / otro]

[AUDIENCE: tecnico]
**Autenticación:**
- [Tipo: API Key / OAuth 2.0 / Basic Auth / otro]
- [Cómo se gestiona el token/credencial]
- [Rotación y seguridad]

**Flujo de datos:**
```
[Diagrama ASCII del flujo]
Odoo → [endpoint] → Sistema externo
Sistema externo → [webhook/callback] → Odoo
```

**Modelo de datos:**
| Odoo campo | Sistema externo campo | Tipo | Notas |
|------------|----------------------|------|-------|
| [campo] | [campo] | [tipo] | [transformación si aplica] |

**Archivos de referencia:**
- `custom_addons/[nombre]/[archivo].py` — [qué hace]
- `custom_addons/[nombre]/[archivo].xml` — [qué hace]
[AUDIENCE_END]

[AUDIENCE: funcional]
**Configuración en Odoo:**
- [Settings necesarios — dónde y qué valor]
- [Permisos requeridos — qué roles]

**Configuración en [Sistema externo]:**
- [Qué configurar del lado del sistema externo]
[AUDIENCE_END]

[AUDIENCE: ejecutivo]
**Por qué integrar:**
- [Beneficio de negocio de la integración]
- [Alternativa sin integración — costo manual]
[AUDIENCE_END]

---

## 💡 Implementación

[800-1200 palabras. Configuración en ambos lados + código/esencial + pruebas.]

**Enfoque general:**
[Qué se logra, por qué este enfoque, alternativas consideradas]

**Alternativas consideradas:**
| Alternativa | Pros | Contras |
|-------------|------|---------|
| [Opción A] | [pros] | [contras] |
| [Opción B] | [pros] | [contras] |

[AUDIENCE: tecnico]
**Código esencial:**
```python
# Conexión y autenticación
# archivo.py, línea X
[código clave — 2-3 líneas con explicación]

# Envío/Recepción de datos
# archivo.py, línea Y
[código clave — 2-3 líneas con explicación]
```

**Manejo de errores:**
```python
# Retry logic / error handling
[código clave — 1-2 líneas]
```
[AUDIENCE_END]

[AUDIENCE: funcional]
**Configuración paso a paso:**
1. Ir a [Menú] → [Submenú] → [Acción]
2. Ingresar [credenciales/endpoint]
3. Seleccionar [qué datos sincronizar]
4. Guardar y probar

**Verificación de conexión:**
- [Cómo confirmar que los sistemas se comunican]
[AUDIENCE_END]

[AUDIENCE: ejecutivo]
**Timeline de implementación:**
- Análisis y diseño: [X] días
- Desarrollo: [X] días
- Testing y validación: [X] días
- Total: [X] días

**ROI estimado:**
- [Tiempo ahorrado / errores eliminados / valor]
[AUDIENCE_END]

---

## ⚠️ Consideraciones y Limitaciones

[200-300 palabras. Rate limits + errores comunes + edge cases + monitoreo.]

**Rate limits y performance:**
- [Límites del sistema externo]
- [Cómo manejar grandes volúmenes]

**Errores comunes:**
| Error | Causa | Solución |
|-------|-------|----------|
| [error 1] | [causa] | [solución] |
| [error 2] | [causa] | [solución] |

**Edge cases:**
- [Situación especial 1 + cómo se maneja]
- [Situación especial 2 + cómo se maneja]

**Monitoreo:**
- [Cómo verificar que la integración sigue funcionando]
- [Logs donde buscar errores]

---

## ✅ Resultado

[200-300 palabras. Qué se logra al final + beneficios + verificación.]

**Qué se logra:**
- [Descripción del flujo automatizado]

**Beneficios:**
| Antes | Después |
|-------|---------|
| [Proceso manual] | [Automatizado] |
| [Error frecuente] | [Eliminado] |

**Verificación:**
- [ ] [Check 1]
- [ ] [Check 2]

---

## 📚 Referencias

- [Docs del sistema externo — 1-2 oraciones]
- [Docs de Odoo relevantes]
- [Librerías o herramientas usadas]

---

## 💬 ¿Integraste de otra forma?

[100-150 palabras. Invitación a compartir experiencias alternativas]

---

**Metadata:**
- Tipo: integration
- Audiencia: [funcional|tecnico|ejecutivo]
- Versión Odoo: [v16/v17/v18/v19]
- Sistemas: [Odoo vX + Sistema externo vY]
- Topic origen: #[ID]
- Estado: BORRADOR
