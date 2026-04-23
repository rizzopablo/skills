#!/usr/bin/env python3
"""
search_client.py - Cliente rápido de búsqueda (requiere servidor corriendo).

Uso:
    python3 scripts/search_client.py "tu búsqueda"
    
Ver estado del servidor:
    python3 scripts/search_server.py status
    
Ver logs:
    python3 scripts/search_server.py logs
    python3 scripts/search_server.py queries
"""

import socket
import json
import sys
import logging
from datetime import datetime
from pathlib import Path

# Paths relativos al skill
SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
DATA_DIR = SKILL_DIR / "data"
SOCKET_PATH = DATA_DIR / "search.sock"
LOG_FILE = DATA_DIR / "client.log"

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


def search(query, top_k=10, timeout=30):
    """Envía query al servidor y retorna resultados."""
    log.info(f"🔍 Buscando: \"{query}\" (top_k={top_k})")
    
    try:
        # Verificar socket existe
        if not SOCKET_PATH.exists():
            error_msg = f"❌ Socket no encontrado: {SOCKET_PATH}"
            log.error(error_msg)
            print(error_msg, file=sys.stderr)
            print("   Iniciá el servidor con: python3 scripts/search_server.py start", file=sys.stderr)
            return None
        
        log.info(f"🔌 Conectando a {SOCKET_PATH}...")
        
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client.settimeout(timeout)  # Timeout para evitar bloqueos infinitos
        
        client.connect(str(SOCKET_PATH))
        log.info("✅ Conectado al servidor")
        
        # Send query
        client.sendall(query.encode('utf-8'))
        log.info(f"📤 Query enviado: {len(query)} bytes")
        
        # Receive response
        data = b""
        client.settimeout(timeout)  # Timeout para recepción
        
        log.info("📥 Esperando respuesta...")
        while True:
            try:
                chunk = client.recv(8192)
                if not chunk:
                    break
                data += chunk
                log.debug(f"Recibido chunk: {len(chunk)} bytes (total: {len(data)})")
            except socket.timeout:
                log.error("❌ Timeout esperando respuesta del servidor")
                print("❌ Timeout: El servidor no respondió en {timeout}s", file=sys.stderr)
                break
        
        client.close()
        
        if not data:
            error_msg = "❌ No se recibió respuesta del servidor"
            log.error(error_msg)
            print(error_msg, file=sys.stderr)
            return None
        
        log.info(f"✅ Respuesta recibida: {len(data)} bytes")
        
        results = json.loads(data.decode('utf-8'))
        log.info(f"✅ Parseados {len(results)} resultados")
        
        return results
    
    except FileNotFoundError:
        error_msg = f"❌ Socket no encontrado: {SOCKET_PATH}"
        log.error(error_msg)
        print(error_msg, file=sys.stderr)
        print("   Iniciá el servidor con: python3 scripts/search_server.py start", file=sys.stderr)
        return None
    except ConnectionRefusedError:
        error_msg = "❌ Conexión rechazada"
        log.error(error_msg)
        print(error_msg, file=sys.stderr)
        print("   Verificá que el servidor esté corriendo: python3 scripts/search_server.py status", file=sys.stderr)
        return None
    except socket.timeout:
        error_msg = f"❌ Timeout de conexión ({timeout}s)"
        log.error(error_msg)
        print(error_msg, file=sys.stderr)
        print("   El servidor puede estar ocupado o bloqueado", file=sys.stderr)
        print("   Ver logs: python3 scripts/search_server.py logs", file=sys.stderr)
        return None
    except json.JSONDecodeError as e:
        error_msg = f"❌ Error parseando respuesta JSON: {e}"
        log.error(error_msg)
        print(error_msg, file=sys.stderr)
        print(f"   Datos recibidos: {data[:200]}...", file=sys.stderr)
        return None
    except Exception as e:
        error_msg = f"❌ Error: {e}"
        log.error(error_msg, exc_info=True)
        print(error_msg, file=sys.stderr)
        return None


def format_results(results, query):
    """Formatea resultados para mostrar."""
    if not results:
        print("❌ No se encontraron resultados")
        return
    
    print()
    print(f"🔍 Resultados para: \"{query}\"")
    print("=" * 70)
    print()
    
    for i, r in enumerate(results, 1):
        print(f"{i}. {r['file']}")
        print(f"   Score: {r['score']:.4f}")
        
        if r.get('classes'):
            classes_str = ', '.join(r['classes'][:5])
            if len(r['classes']) > 5:
                classes_str += f" (+{len(r['classes']) - 5} más)"
            print(f"   Clases: {classes_str}")
        
        if r.get('functions'):
            funcs_str = ', '.join(r['functions'][:7])
            if len(r['functions']) > 7:
                funcs_str += f" (+{len(r['functions']) - 7} más)"
            print(f"   Funciones: {funcs_str}")
        
        if r.get('imports'):
            imports_str = ', '.join(r['imports'][:5])
            if len(r['imports']) > 5:
                imports_str += f" (+{len(r['imports']) - 5} más)"
            print(f"   Imports: {imports_str}")
        
        print()
    
    print("=" * 70)
    print(f"✅ {len(results)} resultados encontrados")


def main():
    setup_logging()
    
    if len(sys.argv) < 2:
        print("Uso: python3 search_client.py \"<query>\" [top_k] [timeout]", file=sys.stderr)
        print()
        print("Ejemplos:")
        print("  python3 search_client.py \"rounding decimal POS\"")
        print("  python3 search_client.py \"currency conversion\" 20")
        print("  python3 search_client.py \"query\" 10 60  # timeout 60s")
        print()
        print("Ver logs:")
        print("  python3 search_server.py logs")
        print("  python3 search_server.py queries")
        sys.exit(1)
    
    # Parse arguments
    query = sys.argv[1]
    top_k = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    timeout = int(sys.argv[3]) if len(sys.argv) > 3 else 30
    
    log.info("=" * 60)
    log.info(f"🚀 Code RAG Search Client")
    log.info(f"   Query: \"{query}\"")
    log.info(f"   Top-K: {top_k}")
    log.info(f"   Timeout: {timeout}s")
    log.info("=" * 60)
    
    # Search
    results = search(query, top_k, timeout)
    
    if results is not None:
        format_results(results, query)
    else:
        log.error("❌ Búsqueda fallida")
        sys.exit(1)


if __name__ == "__main__":
    main()
