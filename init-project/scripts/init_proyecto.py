#!/usr/bin/env python3
"""
init_proyecto.py — Crea el scaffold canonico de un proyecto nuevo.

Estructura canonica: templates/ESTRUCTURA-PROYECTO.md del workspace.
(raiz de fichas + input/ + output/ + src/ + var/, repositorio git local
 con hook pre-push, git-repos.md y symlink AGENTS.md)

Uso:
  python3 init_proyecto.py "Nombre del Cliente" [--dir nombre_directorio]
                                          [--instancia <instancia-odoo>]
                                          [--sin-owro]

La instancia Odoo es POR CLIENTE y no se hardcodea: se resuelve en este orden
  1. flag --instancia
  2. variable OWRO_INSTANCE (entorno o .env)
y si no hay ninguna, el script degrada a scaffold sin datos en vez de adivinar.

Variables de entorno (opcionales, o definidas en .env junto a este script):
  WORKSPACE_ROOT   raiz del workspace (default: auto-deteccion desde este archivo)
  OWRO_INSTANCE    instancia de datos (una por cliente) para consultas OWRO.
                   Sin valor: se genera el scaffold sin datos.
  NO_GIT=1         no inicializar el repo git del proyecto

El archivo .env es LOCAL y NUNCA se versiona (gitignored). Su plantilla es
.env.example. Cualquier dato privado del entorno (nombres de instancia, URLs
internas, credenciales) vive ahi, no en el codigo.
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import date
from pathlib import Path


# ─── Carga de .env (sin dependencia externa; env var gana sobre .env) ────

def load_env(path: Path) -> dict:
    data = {}
    if not path.is_file():
        return data
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        data[key.strip()] = value.strip().strip("'\"")
    return data


def resolve_workspace() -> Path:
    """Detecta el workspace: env var, o caminando hacia arriba hasta encontrar
    un directorio con projects/ y skills/ (templates/ es opcional)."""
    env = os.environ.get("WORKSPACE_ROOT")
    if env:
        p = Path(env).expanduser().resolve()
        if (p / "projects").is_dir():
            return p
    for parent in Path(__file__).resolve().parents:
        if (parent / "projects").is_dir() and (parent / "skills").is_dir():
            return parent
    print("ERROR: no se pudo detectar WORKSPACE_ROOT (usar variable de entorno).",
          file=sys.stderr)
    sys.exit(1)


WORKSPACE = resolve_workspace()
PROJECTS_DIR = WORKSPACE / "projects"
TEMPLATES_DIR = WORKSPACE / "templates"
SKILL_DIR = Path(__file__).resolve().parent.parent

# .env del skill: pares KEY=VALUE. Las variables ya presentes en el entorno
# tienen prioridad sobre el .env.
_ENV = load_env(SKILL_DIR / ".env")
_ENV.update(os.environ)
ENV = _ENV
# Instancia Odoo del cliente. Sin default embebido a proposito: cada cliente
# tiene la suya (self-hosted, cloud u odoo.sh) y el nombre no se puede adivinar.
OWRO_INSTANCE = ENV.get("OWRO_INSTANCE", "").strip()
W = "$WORKSPACE_ROOT"


def instancia_label(instancia: str) -> str:
    return instancia or "sin configurar (scaffold sin datos)"


def set_instancia(nombre: str) -> str:
    """Override de la instancia (flag --instancia). Vacio = usar .env/entorno."""
    global OWRO_INSTANCE
    if nombre:
        OWRO_INSTANCE = nombre.strip()
    return OWRO_INSTANCE


# ─── OWRO helper (opcional: degrade elegante sin instancia) ─────────────

def owro_query(model, method, args, fields=None, limit=100):
    """Consulta OWRO en la instancia configurada.

    Devuelve [] (y avisa) si no hay instancia configurada o si OWRO no esta
    disponible: el scaffold se genera igual, sin datos.
    """
    if not OWRO_INSTANCE:
        print("  (OWRO_INSTANCE no definido: pasar --instancia <nombre> o definirla"
              " en .env — scaffold sin datos)")
        return []
    try:
        sys.path.insert(0, str(WORKSPACE))
        from skills.owro.owro_config import get_owro_client, get_base_url
    except Exception:
        print("  (OWRO no disponible: scaffold sin datos)")
        return []
    payload = {"model": model, "method": method, "args": args, "kwargs": {}}
    if fields:
        payload["kwargs"]["fields"] = fields
    if limit and method in ("buscar", "buscar_leer"):
        payload["kwargs"]["limit"] = limit
    try:
        client = get_owro_client()
        url = f"{get_base_url()}/api/v1/odoo/{OWRO_INSTANCE}/query"
        response = client.post(url, json=payload, timeout=30)
        response.raise_for_status()
        return response.json().get("data", [])
    except Exception as exc:
        print(f"  (OWRO fallo: {exc} — scaffold sin datos)")
        return []


def buscar_cliente(nombre):
    ids = owro_query("res.partner", "buscar",
                     [[["name", "ilike", f"%{nombre}%"]]], limit=20)
    if not ids:
        print(f"  No se encontraron clientes en OWRO (instancia: "
              f"{instancia_label(OWRO_INSTANCE)}).")
        return None
    companies = owro_query("res.partner", "leer", [ids],
                           fields=["id", "name", "email", "phone", "street",
                                   "street2", "city", "state_id", "country_id",
                                   "zip", "website", "vat", "is_company"],
                           limit=20)
    for c in companies:
        if c.get("is_company"):
            return c
    return companies[0] if companies else None


def buscar_contactos(partner_id):
    ids = owro_query("res.partner", "buscar",
                     [[["parent_id", "=", partner_id]]], limit=20)
    if not ids:
        return []
    return owro_query("res.partner", "leer", [ids],
                      fields=["id", "name", "email", "phone", "function", "mobile"],
                      limit=20)


# ─── Formateadores ──────────────────────────────────────────────────────

def safe_str(v):
    return (v or "").strip() if isinstance(v, str) else (v if v else "")


def formatear_contactos(contactos):
    if not contactos:
        return "_(pendiente de relevar)_"
    lines = []
    for c in contactos:
        parts = [c.get("name", "?")]
        if c.get("email"):
            parts.append(c["email"])
        if c.get("phone"):
            parts.append(c["phone"])
        if c.get("function"):
            parts.append(f"({c['function']})")
        lines.append("- " + " | ".join(parts))
    return "\n".join(lines)


def formatear_direccion(cliente):
    if not cliente:
        return "_(pendiente)_"
    parts = []
    for k in ("street", "street2", "city", "zip"):
        if cliente.get(k):
            parts.append(cliente[k])
    for k in ("state_id", "country_id"):
        v = cliente.get(k)
        if isinstance(v, list) and len(v) > 1:
            parts.append(v[1])
    return ", ".join(parts) if parts else "_(pendiente)_"


def carve(name: str) -> str:
    """Nombre de cliente -> slug de directorio."""
    slug = name.lower().strip()
    slug = "".join(ch if ch.isalnum() or ch in "-_" else "-" for ch in slug)
    return "-".join(part for part in slug.split("-") if part) or "cliente"


# ─── Scaffold canonico ──────────────────────────────────────────────────

DIRS = {
    "input/reuniones/preparacion": "minutas + preparaciones (YYYY-MM-DD-tema.md)",
    "input/tickets": "casos de soporte",
    "input/correos": "correos relevantes",
    "input/documentos": "documentacion compartida por el cliente",
    "input/raw-data": "exports automaticos (append-only, no editar)",
    "output/analisis": "analisis, matrices, planillas de trabajo",
    "output/comercial": "propuestas, onepagers, pricing",
    "output/procesos": "levantamiento funcional, BPMN",
    "output/user-stories": "historias de usuario",
    "output/entregables": "todo lo que sale al cliente o devteam",
    "output/knwldg": "fichas destiladas K-XXX",
    "src": "codigo + docs (frontera de publicacion)",
    "src/cdad": "documentacion CDAD (projectbrief/ adr/ epics/ specs/ .cdad-state.json)",
    "src/docs": "documentacion de uso y general del producto",
    "var/scripts": "automatizacion del proyecto",
    "var/logs": "logs de ejecucion y crons",
    "var/tmp": "temporal (gitignored)",
}


def write_template_gitignore(project_dir: Path):
    (project_dir / ".gitignore").write_text("""# Secretos y credenciales (NUNCA versionar)
client_secrets.json
*.key
*.pem
*.p12
*.pfx
.env
*.env
*token*
credentials*
secrets*

# Temporales
var/tmp/
__pycache__/
*.pyc
.DS_Store
*~
*.swp
*.bak
""")


def write_git_repos(project_dir: Path, dir_name: str, hoy: str, hook_instalado: bool):
    hook_line = (
        "- Hook pre-push: instalado (doblegate: .push-allowlist + WORKSPACE_PUSH_CONFIRM=1)"
        if hook_instalado else
        "- Hook pre-push: NO INSTALADO (no se encontro el hook del workspace: copiar\n"
        "  manualmente antes de cualquier push — ver AGENTS.md del workspace)"
    )
    (project_dir / "git-repos.md").write_text(f"""# Repositorios: {dir_name}

## Repo local del proyecto
- Path: projects/{dir_name}/
- Origen: creado por init-project ({hoy})
- Remotes: NINGUNO (politica: commit local; push requiere autorizacion explicita
  del usuario: destino exacto + visibilidad + contenido curado sin secretos ni
  datos de clientes)
{hook_line}
- core.hooksPath: .githooks (config local - RE-EJECUTAR si se clona/reinicializa:
  `git config core.hooksPath .githooks`)

## Politica CDAD / working-state
- cdad-state: privado (default - no se publica el working-state CDAD)

## Contenido publicable (si aplica)
- Subdirectorio: NO DEFINIDO (default: nada es publicable sin decision explicita)

## Historial de autorizaciones de push
- (fecha | remote | que se pusheo | autorizado por)
""")


def write_estado(project_dir: Path, nombre, cliente, hoy):
    estado = f"""# Estado: {nombre} — 🟢/🟡/🔴

## 🔴 Alertas (requieren accion inmediata)
- (completar tras el primer relevamiento)

## 🟡 Atencion (requieren seguimiento)
- (completar)

## 🟢 Estable
- (completar)

## 📈 Metricas 90 dias
| Metrica | Valor | vs periodo anterior |
|---------|-------|-------------------|
| Tickets abiertos | - | - |
| Tickets cerrados/mes | - | - |

## ⚠️ Riesgos
| Riesgo | Prob | Impacto | Mitigacion |
|--------|------|---------|------------|

## 💰 Comercial
- Producto/Servicio: (completar)
- Horas contratadas vs registradas: -

## 📅 Proximos 30 dias
- (completar)

---
_Datos iniciales{' obtenidos' if cliente else ' pendientes'}{f' via OWRO (instancia {OWRO_INSTANCE})' if cliente else ''} el {hoy}._
"""
    (project_dir / "estado.md").write_text(estado)


def write_claude(project_dir: Path, dir_name, nombre, cliente, contactos, hoy,
                 hook_ok: bool = False):
    shared = [f for f in ("IDENTITY.md", "SOUL.md", "USER.md", "MEMORY.md",
                           "TOOLS.md") if (WORKSPACE / f).is_file()]
    shared_txt = (f"- {', '.join(shared)} de {W}/" if shared
                  else f"- _(sin archivos de contexto en la raiz de {W}/)_")
    hook_txt = ("- Hook pre-push (doblegate) activo via `core.hooksPath .githooks`."
                if hook_ok else
                "- Hook pre-push: NO INSTALADO (falta el hook del workspace). "
                "Instalarlo antes de cualquier push.")
    claude = f"""# {nombre} — Project Context

WORKSPACE_ROOT: {W}/

## Scope
CWD = {W}/projects/{dir_name}/
Trabajá SOLO con archivos de este proyecto a menos que se te pida explícitamente lo contrario.

## Shared Context (cargar al inicio)
{shared_txt}
- AGENTS.md de {W}/ (o el symlink local AGENTS.md de este proyecto)

## Descripción
Proyecto de consultoría para {nombre}.

## Contacto / Referencias
- **Cliente:** {nombre}{f" (ID Odoo: {cliente['id']})" if cliente else ""}
- **Dirección:** {formatear_direccion(cliente)}
- **Identificación fiscal (VAT/RUC/RFC):** {safe_str(cliente.get('vat')) if cliente else '_(pendiente)_'}
- **Fuente de datos:** OWRO — instancia {instancia_label(OWRO_INSTANCE)}
- **Contactos:**
{formatear_contactos(contactos)}

## Archivos del Proyecto

Estructura canonica (detalle en {W}/templates/ESTRUCTURA-PROYECTO.md):
- **Raiz:** fichas de gestion (README, estado.md, contactos.md, todo.md, git-repos.md)
- **input/** — material fuente que LLEGA de afuera (se enruta y enriquece).
  input/raw-data/ es append-only.
- **output/** — productos elaborados (analisis, comercial, procesos, entregables, knwldg)
- **src/** — codigo + docs; UNICA zona publicable (via repo separado autorizado)
- **src/cdad/** — documentacion CDAD (projectbrief/ adr/ epics/ specs/ .cdad-state.json)
- **src/docs/** — documentacion de uso y general del producto
- **var/** — operacion: scripts/, logs/, tmp/ (tmp gitignored)

## Repositorios del Proyecto
- Repo local propio. Remotes: ninguno por defecto. Ver `git-repos.md`.
{hook_txt}
- Jamas ejecutar `git push` sin autorizacion explicita del usuario (destino
  exacto, visibilidad, contenido curated sin secretos).

_Creado por init-project el {hoy}._
"""
    (project_dir / "CLAUDE.md").write_text(claude)


def write_readme(project_dir: Path, nombre, dir_name, hoy):
    readme = f"""# {nombre}

- **Origen:** init-project ({hoy})
- Estructura canonica: ver `CLAUDE.md` y `$WORKSPACE_ROOT/templates/ESTRUCTURA-PROYECTO.md`
- Estado de situacion: `estado.md`
- Repos: `git-repos.md`
"""
    (project_dir / "README.md").write_text(readme)


# ─── Init git del proyecto (camino: project-gitinit.sh, fallback inline) ─

def hook_disponible(script_gitinit: Path) -> bool:
    """El workspace puede dejar el proyecto con hook pre-push instalado?"""
    if script_gitinit.is_file():
        return True
    return (script_gitinit.parent.parent / "git-hooks" / "pre-push").is_file()


def init_git(project_dir: Path, script_gitinit: Path) -> bool:
    """Inicializa el repo git del proyecto. Devuelve si el hook pre-push quedo
    instalado (para no mentir en git-repos.md si el workspace no lo provee)."""
    if os.environ.get("NO_GIT"):
        print("  NO_GIT=1: sin repo git")
        return False
    if script_gitinit.is_file():
        # project-gitinit.sh: arg1=cliente, arg3=nota de origen
        r = subprocess.run(["bash", str(script_gitinit), project_dir.name,
                            "--", "creado por init-project"],
                           capture_output=True, text=True)
        if r.returncode == 0:
            print("  repo git inicializado (project-gitinit.sh)")
            return True
        print(f"  project-gitinit.sh fallo ({r.stderr.strip()}): fallback inline")
    # fallback inline (misma politica)
    subprocess.run(["git", "-C", str(project_dir), "init", "-q", "-b", "master"],
                   check=False)
    hook_src = script_gitinit.parent.parent / "git-hooks" / "pre-push"
    hook_ok = hook_src.is_file()
    if hook_ok:
        hooks = project_dir / ".githooks"
        hooks.mkdir(exist_ok=True)
        (hooks / "pre-push").write_bytes(hook_src.read_bytes())
        (hooks / "pre-push").chmod(0o755)
    subprocess.run(["git", "-C", str(project_dir), "config", "core.hooksPath",
                    ".githooks"], check=False)
    (project_dir / ".push-allowlist").touch()
    if not hook_ok:
        print("  (hook pre-push del workspace no encontrado: repo SIN proteccion"
              " anti-push — instalarlo manualmente antes de pushear)")
    print("  repo git inicializado (inline)")
    return hook_ok


# ─── Main ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Scaffold canonico de proyecto")
    parser.add_argument("cliente", help='Nombre del cliente (ej: "Acme SA")')
    parser.add_argument("--dir", dest="dir_name", help="Nombre de directorio (default: slug del nombre)")
    parser.add_argument("--instancia", help="Instancia Odoo del cliente (prioridad sobre .env)")
    parser.add_argument("--sin-owro", action="store_true", help="No consultar OWRO")
    args = parser.parse_args()

    nombre = args.cliente.strip()
    dir_name = args.dir_name or carve(nombre)
    hoy = date.today().isoformat()
    project_dir = PROJECTS_DIR / dir_name

    if project_dir.exists():
        print(f"ERROR: ya existe {project_dir} — para refrescar datos usar el flujo"
              " de refresh, no re-init.", file=sys.stderr)
        sys.exit(1)

    instancia = set_instancia(args.instancia)
    print(f"Inicializando proyecto: {nombre} -> projects/{dir_name}/")

    cliente = contactos = None
    if not args.sin_owro:
        if instancia:
            print(f"  Buscando '{nombre}' en OWRO (instancia: {instancia})...")
        cliente = buscar_cliente(nombre)
        if cliente:
            print(f"  Cliente encontrado: {cliente['name']} (id {cliente['id']})")
            contactos = buscar_contactos(cliente["id"])

    print("  Creando estructura canonica...")
    project_dir.mkdir(parents=True)
    for rel, _desc in DIRS.items():
        (project_dir / rel).mkdir(parents=True, exist_ok=True)

    gitinit = WORKSPACE / "skills/workspace-ops/scripts/project-gitinit.sh"
    hook_ok = hook_disponible(gitinit)
    write_template_gitignore(project_dir)
    write_git_repos(project_dir, dir_name, hoy, hook_ok)
    write_estado(project_dir, nombre, cliente, hoy)
    write_claude(project_dir, dir_name, nombre, cliente, contactos, hoy, hook_ok)
    write_readme(project_dir, nombre, dir_name, hoy)
    (project_dir / "todo.md").write_text(
        f"# {nombre} - Todo\n\n## Pendiente\n- [ ] Primer relevamiento (ver init-project SKILL: FASE 1)\n")

    # contacto.md con lo capturado
    (project_dir / "contactos.md").write_text(
        f"# Contactos: {nombre}\n\n{formatear_contactos(contactos)}\n")

    # symlink AGENTS.md -> CLAUDE.md (agentes que leen AGENTS.md)
    if not (project_dir / "AGENTS.md").exists():
        (project_dir / "AGENTS.md").symlink_to("CLAUDE.md")

    init_git(project_dir, gitinit)

    print(f"""
Listo: projects/{dir_name}/
Estructura canonica + repo local con politica de repos (git-repos.md).
Siguiente paso: fetch por fases (FASE 1/2 del SKILL) y completar estado.md.
Actualiza $WORKSPACE_ROOT/projects/INDEX.md con la entrada nueva.""")


if __name__ == "__main__":
    main()
