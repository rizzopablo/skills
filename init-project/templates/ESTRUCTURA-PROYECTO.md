# ESTRUCTURA-PROYECTO.md — Estructura canonica de proyectos

> Documento canonico. Todo proyecto en `projects/CLIENTE/` sigue esta estructura. El skill `init-project`
> la genera automaticamente. Referencia desde: AGENTS.md (Politica de Repos Anidados)
> y template CLAUDE.md de cada proyecto.

## Mapa canonico

```
projects/CLIENTE/
├── ── Raiz: fichas de gestion ──
├── CLAUDE.md              contexto multi-agente
├── AGENTS.md              (symlink -> CLAUDE.md, para agentes que leen AGENTS.md)
├── README.md              dashboard ejecutivo
├── estado.md              mapa de situacion (semaforo, alertas, metricas)
├── contactos.md           contactos del cliente + equipo consultor
├── contratacion.md        historico comercial (SOs, montos, patron de compra)
├── todo.md                seguimiento de tareas
├── git-repos.md           manifiesto de repos (politica de repos post-incidente)
├── .cron-last-check.md    (condicional: si el proyecto tiene cron de revision)
├── k_CCC                  (condicional: clientes con codigo knwldg)
│
├── input/                 ← lo que LLEGA de afuera. Se enruta y se enriquece.
│   ├── reuniones/         minutas + preparacion/  (YYYY-MM-DD-tema.md)
│   ├── tickets/           casos de soporte (transcripcion + resumen de estado)
│   ├── correos/           correos relevantes
│   ├── documentos/        documentacion compartida por el cliente
│   └── raw-data/          exports automaticos de APIs (OWRO/gws)
│
├── output/                ← productos elaborados (nacen del trabajo del proyecto)
│   ├── analisis/          analisis, matrices, planillas de trabajo
│   ├── comercial/         propuestas, onepagers, pricing
│   ├── procesos/          levantamiento funcional, BPMN
│   ├── user-stories/      HUs especificas
│   ├── entregables/       TODO lo que sale al cliente o devteam
│   │   └── informes/, handoffs/    (subdirs si hace falta)
│   ├── knwldg/            fichas destiladas K-XXX
│   └── <doc-cdad>/docs/   (ciclos CDAD de documentacion: ver seccion CDAD)
│
├── src/                   ← FRONTERA DE PUBLICACION (codigo + su doc)
│   ├── <codigo>/          modulos odoo, paquetes_poc, etc.
│   ├── cdad/              documentacion CDAD (sale con el codigo al publicar):
│   │   ├── projectbrief/  (CDAD)
│   │   ├── adr/           (CDAD)
│   │   ├── epics/         (CDAD)
│   │   ├── specs/         (CDAD)
│   │   ├── .cdad-state.json
│   │   └── hitos/         gestion de hitos cuando aplique
│   └── docs/              documentacion de uso y general del producto
│   └── (working-state CDAD se excluye de publicacion por defecto, ver abajo)
│
└── var/                   ← operacion, privado
    ├── scripts/           automatizacion del proyecto
    ├── logs/              ejecucion y crons
    └── tmp/               temporal (GITIGNORED)
```

## Reglas de flujo (la semantica importa mas que la ubicacion)

- **`input/` = lo que llega de afuera.** Se enruta y se enriquece (transcripciones,
  resumenes de estado de tickets, anotaciones, notas de reunion). Se EDITA: el
  enriquecimiento es parte de los datos. No se genera contenido nuevo aqui:
  lo elaborado va a output/.
  - **`input/raw-data/` es la unica zona inmutable (append-only):** exports
    automaticos de OWRO/gws. No se edita ni se borra; solo se agrega. Si el raw y
    el enriquecimiento conviven (ej. ticket), mantener capas separadas:
    `2026-09-10-tkt-103391.md` (raw/referencia) y `2026-09-10-tkt-103391-notas.md`
    (anotado), para que el enriquecimiento sea siempre re-verificable contra el raw.
- **`output/` = producto elaborado.** Analisis, propuestas, HUs, fichas knwldg,
  entregables al cliente. Aqui nace nuestro trabajo.
- **`src/` = frontera de publicacion.** Todo el resto del proyecto es privado y
  nunca sale del repo local. `src/` (codigo + docs/) es lo unico publicable a
  remotos (odoo.sh, GitLab), siempre via repo separado y autorizacion explicita.
- **`var/` = operacion.** Scripts de proyecto, logs, temporales. Privado.
  Los scripts de var/scripts/ suelen contener paths privados o datos de cliente:
  no son publicables. Si un script se generaliza, se promueve a `src/` o a un
  skill — deteccion de nivel meta (meta-analisis del workspace), NO tarea del
  agente del proyecto.
- **`tmp/` siempre gitignored.**

## CDAD (Contract-Driven AI Development) — doble ubicacion

CDAD se usa para generar codigo y para generar documentacion. El layout CDAD
(`projectbrief/`, `adr/`, `epics/`, `specs/`, `.cdad-state.json`, memory bank)
es del artefacto que se esta produciendo y viaja con el:

- **Ciclo que genera codigo** → layout en `src/cdad/`. Sale con el modulo al publicar.
- **Ciclo que genera documentacion** (agente documentador) → entregable en
  `output/` con su propio layout CDAD (ej. `output/<documento>/docs/...`).
- Un proyecto puede tener ambos ciclos activos, con estado CDAD independiente.

### ⚠️ Excepcion de migracion: CDAD activo

El skill `cdad-cycle` busca `docs/.cdad-state.json` EN LA RAIZ del proyecto, y
los specs/verificadores de un ciclo activo congelan rutas relativas exactas
(allowlists, hashes, paths de AC). Por eso:

- **Mientras un ciclo CDAD este activo**: `docs/` y los directorios que participan
  del sistema de contratos (modelado, verificadores, artefactos citados por
  specs con path relativo) se mantienen en su ubicacion actual — NO se migran.
- **Al cierre del ciclo/epic**: migrar al layout canonico (`src/cdad/` para
  ciclo de codigo; `output/<doc>/docs/` para ciclo de documentacion) actualizando
  en la misma operacion specs y verificadores que referencian las rutas viejas.

## Working-state CDAD y publicacion

`.cdad-state.json`, `activeContext.md`, `progress.md` y el memory bank son
working-state interno. Al publicar `src/`:

- **Default (template):** se excluyen de la publicacion.
- **Opcion por proyecto:** en `git-repos.md` el proyecto declara
  `cdad-state: privado` (default) o `compartido-en-publicacion` (permite
  retomar el ciclo en otro entorno antes de cerrar el epic).
- Si se elige compartido, auditar que el estado no arrastre datos de cliente
  (activeContext suele citarlos) — checklist previa al push en `git-repos.md`.

## Repos git del proyecto

Ver `git-repos.md` del proyecto (creado por `init-project` / `project-gitinit.sh`):
repo local propio, remotes (ninguno por defecto), hook pre-push doblegate
(`.push-allowlist` + `WORKSPACE_PUSH_CONFIRM=1`), `core.hooksPath .githooks`
(config local NO versionada: re-ejecutar tras clonar).

## Archivar proyectos

Proyecto terminado o de prueba → mover carpeta completa a `archive/` y marcar
en `projects/INDEX.md`.
