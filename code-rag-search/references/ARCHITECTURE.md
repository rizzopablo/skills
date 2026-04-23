# Arquitectura Interna - Code RAG Search

## Visión General

```
┌─────────────────────────────────────────────────────────────┐
│                    CODE RAG SEARCH                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │   index_    │    │   search_   │    │   search_   │     │
│  │   code.py   │    │  server.py  │    │  client.py  │     │
│  │             │    │             │    │             │     │
│  │  • Escanea  │    │  • Socket   │    │  • Conecta  │     │
│  │  • Parsea   │    │  • Modelo   │    │  • Query    │     │
│  │  • Embeds   │    │  • Similar. │    │  • Result.  │     │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘     │
│         │                  │                  │             │
│         ▼                  ▼                  ▼             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              data/vector_index/                      │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────┐  │   │
│  │  │ embeddings   │  │  metadata    │  │  index   │  │   │
│  │  │   .npy       │  │   .json      │  │  _info   │  │   │
│  │  │  (numpy)     │  │  (archivos)  │  │  .json   │  │   │
│  │  └──────────────┘  └──────────────┘  └──────────┘  │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Componentes

### 1. index_code.py (Indexador)

**Responsabilidad:** Crear índice vectorial desde código fuente.

**Flujo:**
```
1. Escanear directorio → lista de archivos
2. Para cada archivo:
   a. Parsear (AST para Python, regex para otros)
   b. Extraer: clases, funciones, imports
   c. Generar texto representativo
3. Generar embeddings (Sentence Transformers)
4. Guardar: embeddings.npy + metadata.json
```

**Tecnologías:**
- `ast` (Python AST parser)
- `sentence-transformers` (all-MiniLM-L6-v2)
- `numpy` (almacenamiento de embeddings)

**Output:**
- `embeddings.npy`: Matriz [n_archivos × 384]
- `metadata.json`: Lista de metadata por archivo
- `index_info.json`: Información del índice

### 2. search_server.py (Servidor)

**Responsabilidad:** Mantener modelo en memoria para búsquedas rápidas.

**Arquitectura:**
```
┌─────────────────────────────────────────────┐
│              search_server.py               │
├─────────────────────────────────────────────┤
│                                             │
│  ┌───────────────────────────────────────┐ │
│  │  Memoria (cargado al inicio)          │ │
│  │  • model: SentenceTransformer         │ │
│  │  • embeddings: numpy array [n×384]    │ │
│  │  • metadata: list[dict]               │ │
│  └───────────────────────────────────────┘ │
│                                             │
│  ┌───────────────────────────────────────┐ │
│  │  Socket Server (Unix socket)          │ │
│  │  • data/search.sock                   │ │
│  │  • Thread per client                  │ │
│  │  • JSON protocol                      │ │
│  └───────────────────────────────────────┘ │
│                                             │
└─────────────────────────────────────────────┘
```

**Protocolo:**
```
Cliente → Servidor: "query string"
Servidor → Cliente: JSON[results]
```

**Similaridad Coseno:**
```python
query_emb = model.encode([query])  # [1 × 384]
similarities = np.dot(embeddings, query_emb.T).flatten()  # [n]
top_indices = np.argsort(similarities)[::-1][:top_k]
```

### 3. search_client.py (Cliente)

**Responsabilidad:** Enviar queries y mostrar resultados.

**Flujo:**
```
1. Conectar a socket
2. Enviar query (UTF-8)
3. Recibir JSON
4. Formatear y mostrar
```

### 4. auto_search.py (Auto Cliente)

**Responsabilidad:** Abstraer gestión del servidor.

**Flujo:**
```
1. Verificar si servidor corre (PID file)
2. Si no, iniciar en background
3. Esperar socket disponible
4. Ejecutar search_client.py
```

## Estructura de Datos

### embeddings.npy

```
Shape: [n_archivos × 384]
Tipo: float32
Tamaño: n × 384 × 4 bytes

Ejemplo: 10,000 archivos → 15.4 MB
```

### metadata.json

```json
[
  {
    "file": "odoo/addons/account/models/account_move.py",
    "hash": "sha256:abc123...",
    "classes": [
      {"name": "AccountMove", "methods": ["action_post"], "line": 10}
    ],
    "functions": [
      {"name": "_compute_amount", "line": 50, "args": []}
    ],
    "imports": ["odoo", "odoo.fields"],
    "size": 12345,
    "indexed_at": "2026-04-22T22:00:00"
  }
]
```

### Texto para Embedding (Python)

```
File: odoo/addons/account/models/account_move.py
Imports: odoo, odoo.fields, odoo.models, odoo.tools
Class: AccountMove
  Methods: action_post, _compute_amount, button_draft
Class: AccountMoveLine
  Methods: _compute_tax_ids
Function: _compute_tax_fields()
Function: _recompute_tax_lines(partner, currency)
```

## Performance

### Tiempos Típicos

| Operación | Tiempo | Nota |
|-----------|--------|------|
| Carga de índice | 2-5s | Depende del tamaño |
| Embedding query | ~20ms | Single query |
| Similaridad | ~5ms | Dot product numpy |
| Búsqueda total | ~40ms | Con servidor en memoria |

### Memoria

| Componente | Tamaño |
|------------|--------|
| Modelo (all-MiniLM-L6-v2) | ~80 MB |
| Embeddings (10k archivos) | ~15 MB |
| Metadata (10k archivos) | ~25 MB |
| **Total** | **~120 MB** |

### Optimizaciones

1. **Batch encoding:** Procesa queries en batches de 32
2. **Memory-mapped arrays:** numpy.load con mmap_mode (futuro)
3. **Quantization:** Embeddings en float16 (futuro)

## Seguridad

### Socket Unix

- Solo accesible desde mismo usuario
- Permisos: `srwxr-xr-x` (644)
- Ubicación: `data/search.sock` (dentro del skill)

### Validación de Input

- Queries limitadas a 1KB
- Timeout de conexión: 30s
- Max top_k: 100

## Extensiones Futuras

### Posibles Mejoras

1. **Búsqueda híbrida:** Embeddings + BM25 (full-text)
2. **Chunking:** Embeddings por función/clase (no archivo completo)
3. **Cache de queries:** LRU cache para queries frecuentes
4. **Multi-index:** Soportar múltiples codebases indexados
5. **API REST:** Opcional HTTP además de socket
6. **Windows support:** Named pipes en vez de Unix socket

### Modelos Alternativos

- `all-mpnet-base-v2`: Mejor calidad, más lento
- `codebert-base`: Especializado en código
- `multilingual-e5`: Soporte multi-idioma

---

## Decisiones de Diseño

### ¿Por qué socket Unix?

- **Más rápido** que HTTP (no hay overhead TCP)
- **Más simple** que gRPC/protobuf
- **Seguro** (solo usuario local)
- **Portátil** (Linux/macOS)

### ¿Por qué all-MiniLM-L6-v2?

- **Rápido:** 384 dimensiones (vs 768 de BERT base)
- **Calidad:** Suficiente para código
- **Tamaño:** ~80MB (fácil de distribuir)
- **CPU-friendly:** No requiere GPU

### ¿Por qué no base de datos vectorial?

- **Simplicidad:** numpy es suficiente para <100k archivos
- **Zero dependencies:** Sin PostgreSQL, Redis, etc.
- **Portabilidad:** Un solo archivo .npy
- **Performance:** Dot product numpy es muy rápido

---

## Troubleshooting Interno

### Debug Mode

```bash
# Ver logs del servidor
python3 scripts/search_server.py start 2>&1 | tee /tmp/search.log

# Inspeccionar índice
python3 -c "
import numpy as np
import json
from pathlib import Path

emb = np.load('data/vector_index/embeddings.npy')
with open('data/vector_index/metadata.json') as f:
    meta = json.load(f)

print(f'Embeddings: {emb.shape}')
print(f'Archivos: {len(meta)}')
print(f'Primer archivo: {meta[0][\"file\"]}')
"
```

### Profiling

```bash
# Tiempo de búsqueda
time python3 scripts/search_client.py "query"

# Memoria del servidor
ps -o pid,rss,command -p $(cat data/search.pid)
```
