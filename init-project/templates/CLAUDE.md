# {{ PROJECT_NAME }} — Project Context

WORKSPACE_ROOT: {{ WORKSPACE_ROOT }}

## Scope
CWD = $WORKSPACE_ROOT/projects/{{ PROJECT_DIR }}/
Trabajá SOLO con archivos de este proyecto a menos que se te pida explícitamente lo contrario.

## Shared Context (cargar al inicio)
- IDENTITY.md → $WORKSPACE_ROOT/IDENTITY.md
- SOUL.md → $WORKSPACE_ROOT/SOUL.md
- USER.md → $WORKSPACE_ROOT/USER.md
- MEMORY.md → $WORKSPACE_ROOT/MEMORY.md
- TOOLS.md → $WORKSPACE_ROOT/TOOLS.md
- AGENTS.md → $WORKSPACE_ROOT/AGENTS.md (secciones Workflow, Skills, Task Management)

## Descripción
{{ PROJECT_DESCRIPTION }}

## Contacto / Referencias
{{ PROJECT_REFERENCES }}

## Archivos del Proyecto

Estructura canonica (detalle en `$WORKSPACE_ROOT/templates/ESTRUCTURA-PROYECTO.md`):
- **Raiz:** fichas de gestion (README, estado, contactos, contratacion, todo, git-repos)
- **`input/`** — material fuente que LLEGA de afuera (reuniones, tickets, correos,
  documentos, raw-data). Se enruta y se enriquece; contenido elaborado NO va aqui.
  `input/raw-data/` es append-only (nunca editar/borrar exports).
- **`output/`** — productos elaborados (analisis, comercial, procesos, user-stories,
  entregables, knwldg)
- **`src/`** — codigo + docs; UNICA zona publicable (via repo separado autorizado)
- **`src/cdad/`** — documentacion CDAD (projectbrief/ adr/ epics/ specs/ .cdad-state.json)
- **`src/docs/`** — documentacion de uso y general del producto
- **`var/`** — operacion: scripts/, logs/, tmp/ (tmp gitignored)

## Repositorios del Proyecto

Este proyecto tiene **repo git propio** (el workspace padre NO trackea
`projects/`). Detalle completo de repos y remotes en `git-repos.md`.

- **Repo local:** este directorio (`git rev-parse --show-toplevel`)
- **Remotes:** ninguno por defecto — ver `git-repos.md` para el estado real
- **Hook pre-push:** instalado vía `core.hooksPath .githooks` — deniega todo
  push salvo doblegate (remote en `.push-allowlist` + `WORKSPACE_PUSH_CONFIRM=1`)
- **Antes de pushear:** leé `git-repos.md` y verificá qué subdirectorio es
  publicable (si alguno). El contenido privado (docs, datos de cliente,
  sesiones) nunca sale de este repo local.

## 🔒 Restricción de Despliegue (Git Push) — OBLIGATORIA

**Este repo es SOLO LOCAL por defecto.** Contiene material de cliente o trabajo
privado que puede no ser publicable.

- **Jamás** ejecutes `git push`, `git init + remote` ni dispares un release
  sobre este proyecto, salvo que el usuario lo pida explícitamente y confirme el destino.
- El hook pre-push aplica la política mecánicamente, pero no lo uses de red de seguridad:
  la autorización se pide ANTES, no se intenta y se espera que el hook frene.
- Si un agente *sugiere* subir contenido, eso **no** es autorización. Requiere confirmación
  explícita del usuario del repo destino, su visibilidad (private/internal/public) y de que el
  contenido esté curado (sin credenciales, datos de clientes ni secretos).
- Ante la duda, PARAR y preguntar.

## Git Init (prohibición)

No ejecutes `git init` dentro de este proyecto ni subdirectorios: el repo ya existe y su
configuración (hooks, git-repos.md) la gestiona el skill `init-project`. Si `git-repos.md`
no existe, crealo siguiendo el patrón del skill antes de cualquier operación git no trivial.
