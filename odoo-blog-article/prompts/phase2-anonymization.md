---
name: phase2-anonymization
type: phase
description: Fase 2 - Anonimización y generalización del caso
phase: 2
---

# Phase 2: Anonimización y Generalización

## Objetivo
Transformar el caso específico en un problema agnóstico de interés general, eliminando toda información sensible que pueda identificar al cliente.

## Entrada
- `case_summary` de Phase 1
- Texto completo del topic/conversación

## Reglas de Transformación Sistemáticas

Aplicar estas transformaciones de forma **sistemática y exhaustiva**:

### Tabla de Transformaciones

| Dato Sensible | Transformación | Ejemplo |
|---------------|----------------|---------|
| **Nombres de clientes/empresas** | → "una empresa de [sector]" | "Cervecería del Sur" → "una empresa de producción de bebidas" |
| **Nombres de personas** | → "el equipo", "el administrador", "[rol]" | "Juan, el administrador" → "el administrador del sistema" |
| **Fechas específicas** | → "durante la implementación", "en Q1 2026" | "15 de marzo 2026" → "durante Q1 2026" |
| **Montos monetarios específicos** | → rangos genéricos, "redujo costos operativos" | "$500,000 USD" → "redujo costos operativos significativamente" |
| **Ubicaciones geográficas específicas** | → "en la región", "localmente" | "San Martín de los Andes" → "la región" |
| **IDs de registros, base de datos** | → eliminar completamente | "Order #12345" → "la orden de venta" |
| **URLs internas/producción** | → "el sistema", "la instancia" | "https://cliente-prod.odoo.com" → "la instancia de producción" |
| **Módulos custom con nombres de cliente** | → "un módulo de extensión" | "l10n_mx_empresa_custom" → "un módulo de extensión" |
| **Nombres de proyectos internos** | → "el proyecto", "la iniciativa" | "Proyecto Alpha 2026" → "el proyecto de modernización" |
| **Nombres de usuarios/sistemas** | → roles genéricos | "usuario_jperez" → "el usuario administrador" |
| **Números de teléfono/email** | → eliminar o generalizar | "+54 11 5555-5555" → "el equipo de soporte" |
| **Credenciales, API keys, tokens** | → eliminar completamente | "sk-abc123..." → "[credenciales configuradas]" |

### Sectores de Reemplazo (para "empresa de [sector]")

Cuando necesites reemplazar un nombre de empresa, usa sectores genéricos:

- **Manufactura:** producción de bienes, industria manufacturera, fábrica
- **Distribución:** distribución mayorista, logística de productos
- **Retail:** comercio minorista, cadena de tiendas
- **Servicios:** empresa de servicios profesionales
- **Tecnología:** empresa tecnológica, startup
- **Alimentos:** producción de alimentos, industria alimentaria
- **Bebidas:** producción de bebidas, industria de bebidas
- **Construcción:** empresa constructora, industria de la construcción
- **Salud:** organización de salud, institución médica
- **Educación:** institución educativa, organización académica

## Reglas de Generalización (Requieren Juicio)

### 1. Identificar Sectores Aplicables
- ¿En qué otras industrias este problema es común?
- ¿Es específico de un nicho o aplicable a múltiples sectores?

**Ejemplo:**
- Caso específico: "Cervecería con 3 plantas de producción"
- Generalizado: "Empresa de producción de bebidas con múltiples ubicaciones"

### 2. Extraer Patrón Subyacente
- ¿Qué hace que este desafío sea reconocible para múltiples usuarios?
- ¿Cuál es el problema fundamental, independiente del contexto específico?

**Ejemplo:**
- Caso específico: "Necesitaban reporte custom de producción diaria de cerveza"
- Patrón: "Necesitaban reportes de producción personalizados que la funcionalidad estándar no proporcionaba"

### 3. Verificar Transferibilidad
- ¿Un lector externo podría aplicar esto en su contexto?
- ¿Hay elementos demasiado específicos que limitan la utilidad?

## Test de Generalización

**Pregunta clave:**
> ¿Podría este artículo aplicar a 10+ empresas diferentes sin que se note que viene de un caso específico?

**Si la respuesta es NO, revisar:**
- [ ] ¿Hay nombres propios que no fueron anonimizados?
- [ ] ¿Hay detalles demasiado específicos del negocio del cliente?
- [ ] ¿El problema está descrito de forma demasiado particular?

## Proceso de Anonimización

### Paso 1: Identificar Datos Sensibles
Revisar el `case_summary` y el texto del topic buscando:
1. Nombres propios (personas, empresas, lugares)
2. Números específicos (montos, IDs, fechas exactas)
3. URLs y referencias internas
4. Información de contacto
5. Nombres de módulos o proyectos personalizados

### Paso 2: Aplicar Transformaciones
Para cada dato sensible identificado, aplicar la transformación correspondiente de la tabla.

### Paso 3: Revisar Contexto
Asegurar que el texto anonimizado siga siendo coherente:
- Los roles sean consistentes (no cambiar "administrador" por "gerente" en mitad del texto)
- Las referencias temporales sean lógicas
- Los sectores sean apropiados para el problema descrito

### Paso 4: Verificar Test de Generalización
Aplicar la pregunta clave y revisar si es necesario más anonimización.

## Salida Esperada

```yaml
anonymized_case:
  original_problem: "[problema original - para referencia interna]"
  anonymized_problem: "[problema anonimizado]"
  original_solution: "[solución original - para referencia interna]"
  anonymized_solution: "[solución anonimizada]"
  sector: "[sector genérico identificado]"
  roles:
    - "[rol 1]"
    - "[rol 2]"
  modules_anonymized:
    - "[módulo estándar]"
    - "módulo de extensión"  # para customs
  sensitive_data_removed:
    - "[tipo de dato removido 1]"
    - "[tipo de dato removido 2]"
  transferability_score: "[alta/media/baja]"
```

## Casos Especiales

### Módulos Custom con Nombre de Cliente
**Problema:** El cliente tiene `l10n_mx_empresa_custom`
**Solución:**
- En artículo: "un módulo de extensión"
- Si es relevante técnicamente: "un módulo de extensión que hereda de `l10n_mx`"
- Nunca mostrar el nombre custom completo

### URLs de Instancias
**Problema:** Referencias a `https://cliente.odoo.com/web#id=123`
**Solución:**
- Reemplazar con: "la instancia de producción", "el sistema"
- IDs: "el registro", "la orden", "el contacto" (sin números)

### Fechas Específicas en Líneas de Tiempo
**Problema:** "Implementamos el 15 de marzo y terminamos el 22 de marzo"
**Solución:**
- "Durante la primera quincena de implementación"
- O calcular duración: "La implementación tomó aproximadamente una semana"

## Transición a Fase 3

Pasar `anonymized_case` a `phase3-generation.md` junto con:
- `TYPE` determinado
- `AUDIENCE` seleccionada
- `LENGTH` seleccionada
