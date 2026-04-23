#!/usr/bin/env python3
"""
search_server.py - Servidor de búsqueda semántica (mantiene modelo en memoria).

Uso:
    python3 scripts/search_server.py start   # Iniciar servidor
    python3 scripts/search_server.py stop    # Detener servidor
    python3 scripts/search_server.py status  # Ver estado
    python3 scripts/search_server.py restart # Reiniciar servidor

Logs:
    data/server.log      - Log de ejecución y errores
    data/queries.csv     - Historial de consultas (CSV)
"""

import os
import sys
import json
import socket
import signal
import threading
import logging
import csv
from datetime import datetime
from pathlib import Path

# Paths relativos al skill
SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
DATA_DIR = SKILL_DIR / "data"
INDEX_DIR = DATA_DIR / "vector_index"
SOCKET_PATH = DATA_DIR / "search.sock"
PID_FILE = DATA_DIR / "search.pid"
LOG_FILE = DATA_DIR / "server.log"
QUERIES_CSV = DATA_DIR / "queries.csv"

# Configurar logging
def setup_logging():
    """Configura logging a archivo y consola."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    # Logging a archivo
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler(LOG_FILE, encoding='utf-8'),
            logging.StreamHandler(sys.stderr)
        ]
    )
    
    # Inicializar CSV de queries si no existe
    if not QUERIES_CSV.exists():
        with open(QUERIES_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['timestamp', 'query', 'results_count', 'top_score', 'top_file', 'duration_ms'])

logger = setup_logging()
log = logging.getLogger(__name__)

# Global state
model = None
metadata = None
embeddings = None
server_socket = None
running = False
lock = threading.Lock()


def log_query(query, results, duration_ms):
    """Registra consulta en CSV."""
    try:
        with open(QUERIES_CSV, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            timestamp = datetime.now().isoformat()
            results_count = len(results) if results else 0
            top_score = results[0]['score'] if results else 0.0
            top_file = results[0]['file'] if results else ''
            
            writer.writerow([timestamp, query, results_count, f"{top_score:.4f}", top_file, duration_ms])
    except Exception as e:
        log.error(f"Error logging query to CSV: {e}")


def load_index():
    """Carga el índice vectorial en memoria."""
    global model, metadata, embeddings
    
    with lock:
        if model is not None:
            return model, metadata, embeddings
        
        log.info("📚 Cargando índice vectorial...")
        
        # Check index exists
        if not INDEX_DIR.exists():
            log.error("❌ Índice no encontrado. Ejecutá primero: python3 scripts/index_code.py /path/to/code")
            sys.exit(1)
        
        if not (INDEX_DIR / "embeddings.npy").exists():
            log.error("❌ embeddings.npy no encontrado")
            sys.exit(1)
        
        if not (INDEX_DIR / "metadata.json").exists():
            log.error("❌ metadata.json no encontrado")
            sys.exit(1)
        
        import numpy as np
        from sentence_transformers import SentenceTransformer
        
        log.info("📚 Cargando modelo SentenceTransformer...")
        model = SentenceTransformer('all-MiniLM-L6-v2')
        
        log.info("📂 Cargando metadata...")
        with open(INDEX_DIR / "metadata.json", 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        
        log.info("📂 Cargando embeddings a memoria...")
        embeddings = np.load(INDEX_DIR / "embeddings.npy")
        
        log.info(f"✅ Índice listo: {len(metadata)} archivos, {embeddings.nbytes / 1024 / 1024:.1f} MB")
        
        return model, metadata, embeddings


def search(query, top_k=10):
    """Busca query en el índice y retorna top_k resultados."""
    import numpy as np
    import time
    
    start_time = time.time()
    
    model, metadata, embeddings = load_index()
    
    log.info(f"🔍 Buscando: \"{query}\" (top_k={top_k})")
    
    # Encode query
    query_emb = model.encode([query])
    
    # Compute cosine similarity
    similarities = np.dot(embeddings, query_emb.T).flatten()
    
    # Get top indices
    top_indices = np.argsort(similarities)[::-1][:top_k]
    
    # Build results
    results = []
    for idx in top_indices:
        item = metadata[idx]
        results.append({
            'file': item['file'],
            'score': float(similarities[idx]),
            'classes': [c['name'] for c in item.get('classes', [])],
            'functions': [f['name'] for f in item.get('functions', [])],
            'imports': item.get('imports', [])[:10]
        })
    
    duration_ms = (time.time() - start_time) * 1000
    log.info(f"✅ Búsqueda completada: {len(results)} resultados en {duration_ms:.1f}ms")
    
    # Log query to CSV
    log_query(query, results, duration_ms)
    
    return results


def handle_client(conn, addr=None):
    """Maneja conexión de cliente."""
    client_id = threading.current_thread().name
    log.info(f"📡 Conexión recibida ({client_id})")
    
    try:
        # Set timeout para evitar bloqueos infinitos
        conn.settimeout(30.0)
        
        # Receive query
        data = b""
        while True:
            try:
                chunk = conn.recv(8192)
                if not chunk:
                    break
                data += chunk
                
                # Si recibimos datos, intentar parsear
                if data:
                    try:
                        # Verificar si es JSON válido o string simple
                        query = data.decode('utf-8').strip()
                        if query:  # Si hay contenido, procesar
                            break
                    except UnicodeDecodeError:
                        continue  # Esperar más datos
            except socket.timeout:
                log.error(f"❌ Timeout recibiendo datos ({client_id})")
                break
            except Exception as e:
                log.error(f"❌ Error recibiendo datos ({client_id}): {e}", exc_info=True)
                break
        
        if not data:
            log.warning(f"⚠️  Sin datos recibidos ({client_id})")
            return
        
        query = data.decode('utf-8').strip()
        log.info(f"📥 Query recibido ({client_id}): \"{query}\"")
        
        # Search
        results = search(query)
        
        # Send results
        response = json.dumps(results, ensure_ascii=False)
        conn.sendall(response.encode('utf-8'))
        log.info(f"📤 Respuesta enviada ({client_id}): {len(results)} resultados, {len(response)} bytes")
    
    except socket.timeout:
        log.error(f"❌ Timeout de socket ({client_id})")
    except Exception as e:
        log.error(f"❌ Error handling client ({client_id}): {e}", exc_info=True)
    finally:
        try:
            conn.close()
            log.info(f"🔌 Conexión cerrada ({client_id})")
        except:
            pass


def start_server():
    """Inicia el servidor de búsqueda."""
    global server_socket, running
    
    log.info("=" * 60)
    log.info("🚀 Iniciando Code RAG Search Server")
    log.info("=" * 60)
    
    # Check if already running
    if PID_FILE.exists():
        try:
            with open(PID_FILE, 'r') as f:
                pid = int(f.read().strip())
            os.kill(pid, 0)  # Check if process exists
            log.error(f"⚠️  Servidor ya corriendo (PID {pid})")
            print(f"⚠️  Servidor ya corriendo (PID {pid})", file=sys.stderr)
            sys.exit(1)
        except (ProcessLookupError, ValueError):
            # Stale PID file
            log.warning("⚠️  PID file stale, removiendo...")
            PID_FILE.unlink()
    
    # Create data directory
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    # Remove stale socket
    if SOCKET_PATH.exists():
        log.warning(f"⚠️  Socket stale, removiendo: {SOCKET_PATH}")
        SOCKET_PATH.unlink()
    
    # Load index
    load_index()
    
    # Create socket
    log.info(f"🔌 Creando socket Unix: {SOCKET_PATH}")
    server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(str(SOCKET_PATH))
    server_socket.listen(10)
    
    # Setear permisos del socket
    os.chmod(SOCKET_PATH, 0o666)
    
    # Write PID
    with open(PID_FILE, 'w') as f:
        f.write(str(os.getpid()))
    
    log.info(f"✅ Servidor iniciado (PID {os.getpid()})")
    log.info(f"   Socket: {SOCKET_PATH}")
    log.info(f"   Log: {LOG_FILE}")
    log.info(f"   Queries CSV: {QUERIES_CSV}")
    log.info(f"   Listo para búsquedas")
    
    print(f"✅ Servidor iniciado (PID {os.getpid()})", file=sys.stderr)
    print(f"   Socket: {SOCKET_PATH}", file=sys.stderr)
    print(f"   Log: {LOG_FILE}", file=sys.stderr)
    print(f"   Listo para búsquedas", file=sys.stderr)
    
    running = True
    
    # Signal handlers
    def signal_handler(sig, frame):
        log.info(f"🛑 Señal recibida: {sig}")
        stop_server()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Accept connections
    connection_count = 0
    while running:
        try:
            conn, addr = server_socket.accept()
            connection_count += 1
            log.info(f"📡 Aceptando conexión #{connection_count}")
            
            thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            thread.start()
        except Exception as e:
            if running:
                log.error(f"❌ Error accepting connection: {e}", exc_info=True)
    
    stop_server()


def stop_server():
    """Detiene el servidor."""
    global running, server_socket
    
    log.info("🛑 Deteniendo servidor...")
    running = False
    
    if server_socket:
        try:
            server_socket.close()
            log.info("🔌 Socket cerrado")
        except Exception as e:
            log.error(f"Error closing socket: {e}")
    
    if SOCKET_PATH.exists():
        try:
            SOCKET_PATH.unlink()
            log.info(f"🗑️  Socket file removido: {SOCKET_PATH}")
        except Exception as e:
            log.error(f"Error removing socket: {e}")
    
    if PID_FILE.exists():
        try:
            PID_FILE.unlink()
            log.info(f"🗑️  PID file removido: {PID_FILE}")
        except Exception as e:
            log.error(f"Error removing PID file: {e}")
    
    log.info("✅ Servidor detenido")
    print("✅ Servidor detenido", file=sys.stderr)


def check_status():
    """Verifica estado del servidor."""
    if not PID_FILE.exists():
        msg = "❌ Servidor no está corriendo"
        log.info(msg)
        print(msg, file=sys.stderr)
        return False
    
    try:
        with open(PID_FILE, 'r') as f:
            pid = int(f.read().strip())
        os.kill(pid, 0)  # Check if process exists
        
        msg = f"✅ Servidor corriendo (PID {pid})"
        log.info(msg)
        print(f"{msg}", file=sys.stderr)
        print(f"   Socket: {SOCKET_PATH}", file=sys.stderr)
        print(f"   Log: {LOG_FILE}", file=sys.stderr)
        return True
    except ProcessLookupError:
        msg = "⚠️  PID file existe pero el proceso no está corriendo"
        log.warning(msg)
        print(msg, file=sys.stderr)
        PID_FILE.unlink()
        return False
    except Exception as e:
        msg = f"❌ Error verificando estado: {e}"
        log.error(msg)
        print(msg, file=sys.stderr)
        return False


def show_logs(tail=50):
    """Muestra las últimas líneas del log."""
    if not LOG_FILE.exists():
        print("❌ Log file no encontrado", file=sys.stderr)
        return
    
    print(f"📋 Últimas {tail} líneas de {LOG_FILE}:")
    print("=" * 60)
    
    with open(LOG_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines[-tail:]:
            print(line, end='')
    
    print("=" * 60)


def show_queries(tail=20):
    """Muestra las últimas consultas del CSV."""
    if not QUERIES_CSV.exists():
        print("❌ Queries CSV no encontrado", file=sys.stderr)
        return
    
    print(f"📊 Últimas {tail} consultas de {QUERIES_CSV}:")
    print("=" * 60)
    
    with open(QUERIES_CSV, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)
        
        if len(rows) <= 1:
            print("Sin consultas registradas")
            return
        
        # Print header
        header = rows[0]
        print(" | ".join(header))
        print("-" * 60)
        
        # Print last N rows
        for row in rows[-tail:]:
            # Truncate query if too long
            query = row[1][:50] + "..." if len(row[1]) > 50 else row[1]
            print(f"{row[0][:19]} | {query} | {row[2]} results | {row[3]} | {row[5]}ms")
    
    print("=" * 60)


def main():
    if len(sys.argv) < 2:
        print("Uso: python3 search_server.py [start|stop|status|restart|logs|queries]", file=sys.stderr)
        print()
        print("Comandos:")
        print("  start    - Iniciar servidor")
        print("  stop     - Detener servidor")
        print("  status   - Ver estado")
        print("  restart  - Reiniciar servidor")
        print("  logs     - Ver log de ejecución")
        print("  queries  - Ver historial de consultas")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == 'start':
        start_server()
    elif command == 'stop':
        stop_server()
    elif command == 'status':
        check_status()
    elif command == 'restart':
        stop_server()
        start_server()
    elif command == 'logs':
        tail = int(sys.argv[2]) if len(sys.argv) > 2 else 50
        show_logs(tail)
    elif command == 'queries':
        tail = int(sys.argv[2]) if len(sys.argv) > 2 else 20
        show_queries(tail)
    else:
        print(f"❌ Comando desconocido: {command}", file=sys.stderr)
        print("Uso: python3 search_server.py [start|stop|status|restart|logs|queries]", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
