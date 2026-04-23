#!/usr/bin/env python3
"""
auto_search.py - Cliente de búsqueda con auto-inicio del servidor.

Uso:
    python3 scripts/auto_search.py "tu búsqueda"
    
Este script:
1. Verifica si el servidor está corriendo
2. Si no, lo inicia automáticamente
3. Espera a que el servidor esté listo
4. Ejecuta la búsqueda
5. Deja el servidor corriendo para búsquedas futuras

Logs:
    data/server.log   - Log del servidor
    data/client.log   - Log del cliente
    data/queries.csv  - Historial de consultas
"""

import os
import sys
import subprocess
import time
import logging
from pathlib import Path

# Paths relativos al skill
SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
DATA_DIR = SKILL_DIR / "data"
SOCKET_PATH = DATA_DIR / "search.sock"
PID_FILE = DATA_DIR / "search.pid"
LOG_FILE = DATA_DIR / "auto_search.log"

SEARCH_SERVER = SCRIPT_DIR / "search_server.py"
SEARCH_CLIENT = SCRIPT_DIR / "search_client.py"

# Configurar logging
def setup_logging():
    """Configura logging a archivo."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler(LOG_FILE, encoding='utf-8'),
            logging.StreamHandler(sys.stderr)
        ]
    )

log = logging.getLogger(__name__)


def is_server_running():
    """Verifica si el servidor está corriendo."""
    if not PID_FILE.exists():
        log.debug("PID file no existe")
        return False
    
    try:
        with open(PID_FILE, 'r') as f:
            pid = int(f.read().strip())
        os.kill(pid, 0)  # Check if process exists
        log.debug(f"Servidor corriendo (PID {pid})")
        return True
    except (ProcessLookupError, ValueError, FileNotFoundError) as e:
        log.debug(f"Servidor no corre: {e}")
        return False


def wait_for_socket(timeout=30):
    """Espera a que el socket esté disponible."""
    log.info(f"Esperando socket... (timeout: {timeout}s)")
    
    start = time.time()
    while time.time() - start < timeout:
        if SOCKET_PATH.exists():
            # Verificar que se pueda conectar
            try:
                import socket
                client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                client.settimeout(1.0)
                client.connect(str(SOCKET_PATH))
                client.close()
                log.info("✅ Socket disponible y conectable")
                return True
            except Exception as e:
                log.debug(f"Socket existe pero no conectable: {e}")
        
        time.sleep(0.5)
    
    log.error(f"❌ Timeout esperando socket ({timeout}s)")
    return False


def start_server():
    """Inicia el servidor en background."""
    log.info("🚀 Iniciando servidor de búsqueda...")
    print("🔄 Iniciando servidor de búsqueda...", file=sys.stderr)
    
    # Start server in background
    proc = subprocess.Popen(
        [sys.executable, str(SEARCH_SERVER), 'start'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        start_new_session=True
    )
    
    # Wait for server to start
    if wait_for_socket(timeout=30):
        print("✅ Servidor iniciado", file=sys.stderr)
        log.info("✅ Servidor iniciado exitosamente")
        return True
    
    print("⚠️  Timeout esperando servidor", file=sys.stderr)
    log.error("⚠️  Timeout esperando servidor")
    
    # Check if process died
    if proc.poll() is not None:
        stderr_output = proc.stderr.read().decode('utf-8') if proc.stderr else ""
        log.error(f"Servidor murió al iniciar: {stderr_output}")
        print(f"❌ Error al iniciar servidor:", file=sys.stderr)
        print(stderr_output, file=sys.stderr)
    
    return False


def main():
    setup_logging()
    
    if len(sys.argv) < 2:
        print("Uso: python3 auto_search.py \"<query>\" [top_k] [timeout]", file=sys.stderr)
        print()
        print("Ejemplos:")
        print("  python3 auto_search.py \"rounding decimal POS\"")
        print("  python3 auto_search.py \"currency conversion\" 20")
        print()
        print("Este script inicia el servidor automáticamente si no está corriendo.")
        print()
        print("Logs:")
        print(f"  {LOG_FILE}")
        print(f"  {DATA_DIR / 'server.log'}")
        print(f"  {DATA_DIR / 'queries.csv'}")
        sys.exit(1)
    
    # Parse arguments
    query = sys.argv[1]
    top_k = sys.argv[2] if len(sys.argv) > 2 else "10"
    timeout = sys.argv[3] if len(sys.argv) > 3 else "30"
    
    log.info("=" * 60)
    log.info("🚀 Code RAG Auto Search")
    log.info(f"   Query: \"{query}\"")
    log.info(f"   Top-K: {top_k}")
    log.info(f"   Timeout: {timeout}s")
    log.info("=" * 60)
    
    # Check/start server
    if is_server_running():
        log.info("✅ Servidor ya está corriendo")
        print("✅ Servidor ya está corriendo", file=sys.stderr)
    else:
        log.info("⚠️  Servidor no está corriendo, iniciando...")
        print("🔄 Servidor no está corriendo, iniciando...", file=sys.stderr)
        
        if not start_server():
            log.error("❌ No se pudo iniciar el servidor")
            print("❌ No se pudo iniciar el servidor", file=sys.stderr)
            print()
            print("Ver logs:", file=sys.stderr)
            print(f"  {LOG_FILE}", file=sys.stderr)
            print(f"  {DATA_DIR / 'server.log'}", file=sys.stderr)
            sys.exit(1)
    
    # Execute search
    log.info("🔍 Ejecutando búsqueda...")
    
    cmd = [sys.executable, str(SEARCH_CLIENT), query, top_k, timeout]
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        log.info("✅ Búsqueda completada exitosamente")
    else:
        log.error(f"❌ Búsqueda fallida (código {result.returncode})")
        print()
        print("❌ Búsqueda fallida", file=sys.stderr)
        print()
        print("Ver logs para más detalles:", file=sys.stderr)
        print(f"  python3 {SEARCH_SERVER} logs", file=sys.stderr)
        print(f"  python3 {SEARCH_SERVER} queries", file=sys.stderr)
    
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
