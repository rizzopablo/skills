---
name: init-project
description: "Inicializa un proyecto/cliente desde cero: crea scaffold, fetcha datos del ERP/Odoo del cliente vía OWRO (instancia configurable, una por cliente), gws (calendar/gmail/drive) y GitLab con ventanas inteligentes (90d reciente / 2 años histórico agregado), genera estado.md con semáforo, métricas y tendencias. Triggers on: '/init-project', '/init', 'inicializar cliente', 'crear proyecto', 'setup client', 'nuevo proyecto'. La carpeta y task_plan.md que crea siguen la mecánica de project-tracker."
---

# Skill: init-project

Inicializa un proyecto/cliente en `$WORKSPACE_ROOT/projects/` con mapa completo de situación.

---

## 🎯 Propósito

Al arrancar un cliente nuevo, generar un **scaffold completo** con:

1. **Scaffold de directorios** (reuniones/, documentos/, tickets/, etc.)
2. **Fetch inteligente por fases** (90d reciente + 2 años histórico agregado)
3. **5 archivos base** que dan el mapa completo del cliente
4. **`estado.md`** con semáforo, alertas, métricas, tendencias y riesgos
5. **Actualización** de `projects/ACTIVE-PROJECTS.md`

---

## ⚡ Cuándo usar

| Situación | Trigger |
|-----------|---------|
| Nuevo cliente | "inicializá el cliente X", "crear proyecto para X" |
| Cliente existente sin proyecto formal | "setup client X", "armar proyecto de X" |
| Refrescar datos de un cliente existente | "refresh proyecto X", "actualizar estado de X" |

---

## 📁 Scaffold generado

> Estructura canonica completa en `WORKSPACE_ROOT/templates/ESTRUCTURA-PROYECTO.md`.
> Resumen (los condicionales se crean solo cuando aplican):

```
projects/CLIENTE/
├── CLAUDE.md          ← Contexto multi-agente (+ AGENTS.md symlink → CLAUDE.md)
├── AGENTS.md          ← symlink a CLAUDE.md (agentes que leen AGENTS.md)
├── git-repos.md       ← 🎯 Manifiesto de repos del proyecto (local, remotes, hooks)
├── .githooks/         ← Hook pre-push del repo local (NO va al repo público)
├── .gitignore         ← secretos + tmp (generado por init_proyecto.py)
├── README.md          ← Dashboard ejecutivo + índice
├── estado.md          ← 🎯 Mapa de situación (semáforo, alertas, métricas, tendencias)
├── contactos.md       ← Contactos del cliente + equipo consultor
├── contratacion.md    ← SOs, montos, productos, periodicidad
├── todo.md            ← Seguimiento de tareas
├── input/             ← material fuente (se enruta y enriquece; raw-data append-only)
│   ├── reuniones/     ← minutas + preparacion/
│   ├── tickets/ / correos/ / documentos/ / raw-data/
├── output/            ← productos elaborados
│   ├── analisis/ / comercial/ / procesos/ / user-stories/
│   ├── entregables/   ← (informes/, handoffs/ si hace falta)
│   └── knwldg/        ← fichas K-XXX
├── src/               ← repo público: producto genérico + docs públicas
│   ├── LICENSE        ← GPL-3.0-or-later (o la licencia elegida)
│   ├── README.md      ← README para usuarios externos
│   ├── cdad/          ← documentación CDAD (epics, specs, projectbrief, adr, .cdad-state)
│   └── docs/          ← documentación de uso y general del producto
└── var/               ← operacion (gitignore tmp/)
    ├── scripts/ / logs/ / tmp/
└── raw-data/          ← (legacy pre-estructura: mover a input/raw-data/)
```

---

## 🗂 Repositorios del proyecto (POLÍTICA OBLIGATORIA)

> Preventivo: esta politica existe para que esa situacion no suceda (push accidental del workspace completo o de datos sensibles).
> Esta sección existe para que eso no vuelva a pasar. Política completa en `AGENTS.md`
> (sección "Política de Repos Anidados").

Todo proyecto creado con este skill obtiene **repo git propio**, separado del repo del
workspace (que no trackea `projects/`).

**Camino preferido:** ejecutar `skills/workspace-ops/scripts/project-gitinit.sh CLIENTE`
(que hace los pasos 1-4 automaticamente: git init, hook pre-push + core.hooksPath,
.gitignore con secretos, .push-allowlist, git-repos.md, symlink AGENTS.md, identidad
git local y commit inicial). Los pasos manuales quedan documentados como referencia
y fallback si el script no está disponible:

1. **Crear repo:** `git init` en `projects/CLIENTE/` + commit inicial del scaffold.
   - Si ya existe un repo en el directorio (ej. clone de un GitLab interno del equipo), NO re-envolver:
     es un repo legítimo con remote propio. Documentarlo en `git-repos.md` tal cual.
2. **Instalar hook pre-push:** copiar `skills/workspace-ops/git-hooks/pre-push` a
   `projects/CLIENTE/.githooks/pre-push` (chmod +x) y ejecutar SIEMPRE
   `git config core.hooksPath .githooks` en el repo del proyecto.
   ⚠️ `core.hooksPath` es config local NO versionada: no sobrevive a clones ni
   reinicializaciones. Re-ejecutarlo siempre y declararlo en `git-repos.md`.
3. **Generar `git-repos.md`** (manifiesto de repos, ver sección abajo).
4. **Reglas de remotes:**
   - Nunca crear remotes sin autorización explícita del usuario (destino exacto + visibilidad
     + contenido curado sin secretos ni datos de clientes).
   - Por defecto el repo del proyecto no tiene remotes: todo queda commit local.
   - Si el proyecto necesita publicar código (odoo.sh, GitLab), preguntar qué subdirectorio es
     publicable y montar un **repo separado solo para ese subdirectorio** con su propio remote.
     NUNCA pushear el proyecto entero. Cada remote debe quedar declarado en `git-repos.md`.

### Plantilla `git-repos.md`

```markdown
# Repositorios: CLIENTE

## Repo local del proyecto
- Path: projects/CLIENTE/
- Origen: creado por init-project (YYYY-MM-DD) / clone de <URL>
- Remotes: NINGUNO (politica: commit local; push requiere autorizacion explicita)
- Hook pre-push: instalado (doblegate: .push-allowlist + WORKSPACE_PUSH_CONFIRM=1)
- core.hooksPath: .githooks (config local - re-ejecutar si se clona/reinicializa:
  `git config core.hooksPath .githooks`)

## Contenido publicable (si aplica)
- Subdirectorio: <path relativo> | Destino autorizado: <remote URL, visibilidad>
- Estado: NO DEFINIDO (default: nada es publicable sin decision explicita)
- Contenido: producto genérico, README de usuario, LICENSE, docs públicas y `.env.example`
  con placeholders. Sin datos locales, documentos internos ni políticas de publicación.
- core.hooksPath del repo público: <ruta al hook del repo local> (config local, no
  versionada; el hook no se versiona en el público)

## Repos anidados (clones existentes, si aplica)
- <path>: <remote URL> (repo legitimo de <fuente>, no re-envolver)

## Historial de autorizaciones de push
- (fecha | remote | qué se pusheó | autorizado por)
```

### Plantilla `.push-allowlist`

Archivo vacío (crearlo, sin contenido). El hook pre-push deniega todo push salvo que el
remote figure aquí Y se pase `WORKSPACE_PUSH_CONFIRM=1`. Toda excepción queda auditada
en el log de pushes definido por el hook.

---

## 🌍 Repos públicos vs repos locales (criterio general)

Todo proyecto puede tener dos repositorios con propósitos distintos. **No son espejos:** el
público se escribe para un desconocido que quiera usar el producto; el local conserva el
trabajo, las decisiones y la configuración del entorno.

| Repo | Contenido | No contiene |
|---|---|---|
| Local (privado) | estado, plan, diseño, decisiones, spikes, brief, `input/`, `output/`, configuración local, políticas, hooks, logs | — |
| Público (aunque sea privado hoy) | producto genérico, README de usuario, `LICENSE`, docs de arquitectura/configuración/seguridad/desarrollo/despliegue, `.env.example` con placeholders, código y pruebas | datos locales, documentos de trabajo, políticas internas, dependencias instaladas, artefactos de build |

### Reglas del repo público

1. **Genérico:** sirve a cualquiera que quiera usar el producto. Nada que solo tenga sentido
   para el proyecto, el cliente o el entorno.
2. **Sin datos locales:** no dominios, IPs, hostnames, rutas del host, nombres de usuarios,
   clientes o instancias, ni credenciales. Usar placeholders (`gateway.example.com`,
   `sso.example.com`).
3. **Sin políticas internas:** nada de reglas de push, squash, working-state CDAD, autoridad,
   hooks, allowlist, logs de publicación ni documentos de gestión.
4. **Sin dependencias ni artefactos:** `node_modules/`, `dist/`, `build/`, `coverage/`, logs y
   temporales. Todo eso va en `.gitignore`; se instala o se genera, no se versiona.
5. **Licencia desde el día uno:** `LICENSE` con el texto completo de la GPL y la declaración
   `GPL-3.0-or-later` (o la licencia que el humano elija), `license` en `package.json` y
   cabeceras SPDX en los archivos fuente.
6. **Configuración por entorno:** valores requeridos sin defaults locales; `.env.example` con
   placeholders; el repo no arranca con datos de nadie.
7. **README para externos:** qué es, requisitos, instalación, configuración, uso, docs y
   licencia. No mencionar el repo privado, el cliente ni la política de publicación.

### Dónde va cada cosa

- Diseño, decisiones, spikes, brief, estado, plan, `input/` y `output/` → repo local.
- Configuración local (dominios, hosts, IPs, rutas, credenciales) → repo local
  (`output/operacion/` o `var/`).
- Políticas de publicación, hooks, allowlist y logs → repo local (`var/`).
- Código, README público, `LICENSE`, docs genéricas y `.env.example` → repo público (`src/`).

### Verificación antes de publicar

```bash
# 1. ¿Qué se publicaría?
git -C src ls-files

# 2. ¿Quedan datos locales? (adaptar los patrones al proyecto)
git -C src grep -nE 'dominio-propio|/home/|@|cliente|usuario-local' || true

# 3. ¿Quedan dependencias o artefactos?
git -C src ls-files | grep -E 'node_modules|dist/|build/|coverage/' || true

# 4. ¿Hay licencia?
test -f src/LICENSE

# 5. ¿El README habla del repo privado o de políticas internas?
grep -niE 'privado|squash|working-state|publicación' src/README.md || true
```

Si algo falla, se mueve al repo local antes de publicar. El push sigue la política del
proyecto (squash si corresponde) y solo lo autoriza el humano.

### Cuándo se aplica

Desde el primer commit del repo público, **aunque todavía sea privado**. La visibilidad puede
cambiar; el contenido debe estar listo para ser público en cualquier momento. El hook
pre-push y la política de publicación viven en el repo local; el repo público no los lleva.

## 🔄 Flujo de fetch por fases

> ⚠️ **La instancia Odoo es POR CLIENTE — nunca hardcodear un nombre.**
> Cada cliente vive en su propia instancia (self-hosted, cloud u odoo.sh) y el identificador
> cambia en cada uno. La instancia se resuelve, en este orden:
>
> 1. `OWRO_INSTANCE` en el `.env` del skill (config local del entorno, nunca versionada).
> 2. Flag `--instancia <nombre>` de `scripts/init_proyecto.py` (prioridad sobre `.env`).
> 3. `list_instances()` (skill `owro`) para ver las disponibles.
> 4. Ante la duda, **preguntar al usuario**. No asumir ni inventar un nombre.
>
> En todas las llamadas pasar la instancia explícita: `owro_query(instance=<instancia>, ...)`.
> Si el cliente todavía no tiene instancia accesible, el scaffold se puede generar igual
> (`--sin-owro`) y los datos se completan a mano después.
> Verificar de paso que la instancia es la del cliente correcto: un `res.partner` homónimo
> en otra instancia es un cliente distinto.

### FASE 1 — BLOQUEANTE (paralelo, 2-4 llamadas OWRO)

Datos críticos que definen quién es el cliente y qué está pasando ahora. Sin estos no se puede armar `estado.md`.

| Dato | Fuente | Detalle |
|------|--------|---------|
| Partner + datos fiscales | OWRO `<instancia>` `res.partner` | Identificación fiscal (VAT/RUC/RFC), industria, país, dirección. Buscar por nombre, `buscar_leer` con fields |
| SOs activas | OWRO `<instancia>` `sale.order` | Contratos vigentes: número, fecha, monto, producto, estado, próximo vencimiento |
| Contactos clave | OWRO `<instancia>` `res.partner` (hijos) | Nombre, cargo, email, teléfono, partner ID |
| Tickets ABIERTOS | OWRO `<instancia>` `helpdesk.ticket` | Detalle completo: stage != done. Estos van a alertas |
| Tareas ABIERTAS | OWRO `<instancia>` `project.task` | Detalle completo: stage != done. Trabajo en curso |

### FASE 2 — PARALELO ALTO VALOR (paralelo, no bloquea FASE 1)

Datos que construyen métricas y tendencias. **Agregados, no detalle individual.**

| Dato | Fuente | Qué traer |
|------|--------|-----------|
| Tickets cerrados últimos 2 años | OWRO `<instancia>` `helpdesk.ticket` | 🙅 NO detalle individual → 📊 **Conteo por mes, categoría, prioridad, asignado** |
| Tareas completadas últimos 2 años | OWRO `<instancia>` `project.task` | 🙅 NO detalle individual → 📊 **Conteo por mes, tipo, proyecto asignado** |
| Timesheets últimos 90 días | OWRO `<instancia>` `account.analytic.line` | 🙅 NO cada línea → 📊 **Total horas, promedio semanal, horas por proyecto** |
| Último chatter | OWRO `<instancia>` `mail.message` | Últimos 20 mensajes (sin adjuntos). Contexto inmediato |
| Reuniones últimos 90d | gws calendar | Fechas + títulos + participantes. NO minutas completas |
| Correos últimos 90d | gws gmail | **SOLO FROM/TO contactos del cliente** (filtrar newslists, notifs automáticas, facturas electrónicas). Conteo total + top-5 remitentes + asuntos |

**Filtro de correos**: si el cliente tiene 5 contactos, buscar `from:(mail1 OR mail2 OR mail3)` + `to:(mail1 OR mail2 OR mail3)` desde hace 90 días. Resultado típico: 10-30 correos reales.

### FASE 3 — GENERAR `estado.md`

Con los datos de FASE 1 + FASE 2, generar el archivo `estado.md` (ver plantilla abajo).

### FASE 3.5 — BACKGROUND RÁPIDO (después de generar estado.md)

Se lanzan en segundo plano mientras el usuario ya está viendo el dashboard.

| Dato | Fuente | Qué traer |
|------|--------|-----------|
| 📝 Minutas últimas 5 reuniones | gws calendar + drive | De las 5 reuniones más recientes, bajar minutas y extraer **action_items**. Cruzar action_items vs tickets abiertos → indicador de cumplimiento |
| Documentos Drive recientes | gws drive | Solo metadatos: nombre, fecha, tipo. NO descargar |
| Issues GitLab abiertos | GitLab | Título + estado + asignado. Sin closed |
| Adjuntos OWRO | OWRO `<instancia>` `ir.attachment` | Solo conteo + tamaño total. Alerta si > 50MB |

### FASE 4 — ON-DEMAND (no se tocan en init)

Solo se fetchan cuando el usuario pregunta específicamente.

| Dato | Cuándo |
|------|--------|
| Detalle de ticket cerrado específico | Si investigando un patrón |
| Cuerpo de correo específico | Si parece relevante en un asunto |
| Documento Drive > 5MB | Si el usuario lo pide expresamente |
| Issues GitLab cerrados | Bajo demanda |
| Historial completo de chatter | Solo si se investiga una crisis |
| Detalle individual de timesheets | Si hay anomalía en horas |

---

## 📄 Archivos que se generan

### `CLAUDE.md`
Contexto completo del proyecto con:
- Descripción del cliente y su negocio
- Contactos principales (copiados de `contactos.md`)
- Skills relevantes referenciados
- Referencias a los archivos del proyecto

### `README.md`
Dashboard ejecutivo con:
- Ficha rápida: razón social, partner ID, identificación fiscal, industria
- Contactos clave
- Índice de todos los archivos del proyecto
- Estado resumido (enlace a `estado.md`)

### `estado.md` — Mapa de situación
```markdown
# Estado: CLIENTE — 🟢/🟡/🔴

## 🔴 Alertas (requieren acción inmediata)
— Tickets abiertos críticos
— Tareas bloqueadas
— SLA breached
— Silencio del cliente (sin correos/reuniones en X días)

## 🟡 Atención (requieren seguimiento)
— Tickets abiertos en stage intermedio
— Tareas sin avance reciente
— Action items pendientes de últimas reuniones
— Horas gastadas vs contratadas (desviación)

## 🟢 Estable
— ...

## 📈 Métricas 90 días
| Métrica | Valor | vs período anterior |
|---------|-------|-------------------|
| Tickets abiertos | X | +/- Y |
| Tickets cerrados/mes | X | tendencia |
| Horas registradas | X | vs horas contratadas |
| Tiempo medio resolución | X días | |
| SLA compliance | X% | |
| Correos cliente | X | frecuencia |
| Reuniones | X | frecuencia |

## 📊 Tendencias 2 años (agregado)
| Mes | Tickets cerrados | Por categoría top | Tareas completadas |
|-----|-----------------|-------------------|-------------------|
| ... | ... | ... | ... |

Detectar: estacionalidad, picos, categorías dominantes.

## 📝 Action items últimas 5 reuniones
| Reunión | Fecha | Action item | Estado |
|---------|-------|-------------|--------|
| ... | ... | ... | ✅ cumplido / ⏳ pendiente / ❌ vencido |

Cruzar contra tickets abiertos para detectar pendientes resueltos vs colgados.

## ⚠️ Riesgos
| Riesgo | Prob | Impacto | Mitigación |
|--------|------|---------|------------|

## 💰 Comercial
- Última SO: ...
- Gasto mensual promedio: ...
- Producto/Servicio: ...
- Próximo vencimiento: ...
- Horas contratadas vs registradas: ...
- Patrón de compra: ...

## 📅 Próximos 30 días
— ...
```

### `contactos.md`
Tabla con: nombre, cargo, email, teléfono, partner ID (de OWRO) + equipo consultor asignado.

### `contratacion.md`
Historial de SOs: número, fecha, monto, producto, estado. Patrón de compra identificado.

---

## 🧠 Árbol de decisión

```
¿El proyecto/cliente ya existe en projects/?
├── NO → Crear todo desde cero (scaffold + fetch por fases + generar archivos)
├── SÍ → ¿Refrescar datos?
│   ├── SÍ → Refetch (FASE 1 + FASE 2 + FASE 3.5), regenerar estado.md (preguntar antes)
│   └── NO → Salir
```

---

## ⚠️ Reglas

1. **Siempre preguntar** antes de sobreescribir un proyecto existente.
2. **No descargar archivos grandes** (>50MB) de Drive sin confirmar.
3. **🔴 Instancia Odoo por cliente, nunca hardcodeada.** Resolver en cada init (`.env` → `--instancia` → `list_instances()` → preguntar). Pasar `instance=<instancia>` explícito en cada llamada `owro_query()`. Nunca asumir que dos clientes comparten instancia, ni que el nombre de la instancia coincide con el del cliente.
4. **Limitar resultados** en todas las consultas OWRO (default 80).
5. **No incluir claves ni tokens** en los archivos generados.
6. **Ventanas inteligentes:**
   - **90 días** para actividad reciente (tickets abiertos, tareas, timesheets, reuniones, correos)
   - **2 años** para histórico agregado (conteo de tickets/tareas por mes, tendencia de horas, estacionalidad)
   - **Últimas 5 reuniones** para minutas y action_items
7. **Correos filtrados**: solo FROM/TO contactos del cliente. NO newslists, NO notifs automáticas, NO facturas electrónicas.
8. **Tickets cerrados**: solo agregado por mes/categoría/prioridad. NO detalle individual en init.
9. **Tareas completadas**: solo agregado por mes/tipo/proyecto. NO detalle individual en init.
10. **Actualizar `projects/ACTIVE-PROJECTS.md`** al crear un proyecto nuevo.
11. **Repos:** ejecutar los 4 pasos de la sección "Repositorios del proyecto" (git init,
    hook pre-push + core.hooksPath, git-repos.md, reglas de remotes). Prohibido `git init`
    fuera de este flujo. Nunca crear remotes sin autorización explícita del usuario.
12. **Skills que necesita este skill:**
    - Acceso al ERP/Odoo del cliente: puede ser `owro`, `vulpo`, `mcp-odoo` o el medio habilitado en el entorno del agente (resolver la instancia primero)
    - `gws` → calendar, gmail, drive
    - `gitlab-api` → repos del cliente
    - Módulo Python para scripting: el correspondiente al medio habilitado (ej. `owro_query(instance=<instancia>, ...)` si se usa OWRO)

---

## 🔄 Post-inicialización

Después de crear el proyecto, el agente debería:
1. Confirmar al usuario que el proyecto está listo
2. Mostrar resumen ejecutivo de `estado.md` (semáforo + alertas + métricas clave)
3. Preguntar si quiere revisar `estado.md` completo
4. Preguntar si quiere profundizar en algún aspecto específico (tickets, tareas, reuniones, etc.)

---

## 📁 Ubicación

- **Base:** `$WORKSPACE_ROOT/skills/init-project/`
- **SKILL.md:** Este archivo

## 📁 Scripts

- **`scripts/init_proyecto.py`** — Generador del scaffold canonico (input/output/var, git-repos.md, hook pre-push, symlink AGENTS.md).
  Config local via `.env` (gitignored, plantilla: `.env.example`; clave `OWRO_INSTANCE`) o flag
  `--instancia <nombre>` (prioridad sobre `.env`). Sin instancia configurado genera el scaffold
  sin datos (`--sin-owro` para forzar ese modo). Invocar desde `/skills/init-project/scripts/`.

  ```bash
  python3 scripts/init_proyecto.py "Nombre del Cliente" --dir nombre-dir --instancia <instancia-odoo>
  ```
