# Guía de Uso Detallada - Code RAG Search

## Índice

1. [Instalación](#instalación)
2. [Indexación](#indexación)
3. [Búsqueda](#búsqueda)
4. [Casos de Uso](#casos-de-uso)
5. [Troubleshooting](#troubleshooting)
6. [API Interna](#api-interna)

---

## Instalación

### Requisitos

- Python 3.8+
- pip3
- 1GB+ de espacio libre (para dependencias + índice)
- 512MB+ RAM (más para codebases grandes)

### Pasos

```bash
# 1. Navegar al directorio del skill
cd code-rag-search/

# 2. Ejecutar setup
./scripts/setup.sh

# 3. Verificar instalación
source venv/bin/activate
python3 -c "import sentence_transformers; print('OK')"
```

### Instalación Manual (alternativa)

```bash
# Crear venv
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install sentence-transformers numpy scikit-learn tqdm

# Verificar
python3 -c "from sentence_transformers import SentenceTransformer; print('OK')"
```

---

## Indexación

### Indexación Básica

```bash
python3 scripts/index_code.py /path/to/codebase
```

### Opciones

```bash
# Extensiones específicas
python3 scripts/index_code.py ~/src/project --extensions .py,.js,.ts

# Output personalizado
python3 scripts/index_code.py ~/src/odoo --output /tmp/mi_indice

# Ver ayuda completa
python3 scripts/index_code.py --help
```

### Extensiones Soportadas

Por defecto:
- `.py` (Python)
- `.js`, `.ts`, `.jsx`, `.tsx` (JavaScript/TypeScript)
- `.rb` (Ruby)
- `.java` (Java)
- `.go` (Go)
- `.rs` (Rust)
- `.cpp`, `.c`, `.h` (C/C++)

### Análisis por Lenguaje

**Python (.py):**
- Extrae clases con métodos
- Extrae funciones con argumentos
- Extrae imports
- Genera embeddings del contenido estructurado

**Otros lenguajes:**
- Análisis básico por patrones regex
- Embeddings del contenido raw (primeros 2KB)

### Tiempos de Indexación

| Codebase | Archivos | Tiempo | Tamaño Índice |
|----------|----------|--------|---------------|
| Pequeño | 100 | ~10s | 5 MB |
| Mediano | 1,000 | ~1 min | 50 MB |
| Grande | 10,000 | ~5 min | 500 MB |
| Muy grande | 50,000 | ~20 min | 2.5 GB |

### Re-indexación

El índice se debe regenerar cuando:
- Se agregan archivos nuevos
- Se modifican significativamente archivos existentes
- Se cambia de rama (git)

```bash
# Re-indexar completo
python3 scripts/index_code.py /path/to/codebase

# El nuevo índice reemplaza al anterior automáticamente
```

---

## Búsqueda

### Modos de Búsqueda

#### A. Auto Search (Recomendado)

```bash
python3 scripts/auto_search.py "query"
```

**Ventajas:**
- Inicia servidor automáticamente si es necesario
- Ideal para búsquedas esporádicas
- No requiere gestión manual

#### B. Cliente + Servidor Manual

```bash
# Iniciar servidor (persiste en memoria)
python3 scripts/search_server.py start

# Múltiples búsquedas rápidas (~40ms c/u)
python3 scripts/search_client.py "primera query"
python3 scripts/search_client.py "segunda query"
python3 scripts/search_client.py "tercera query"

# Parar cuando termines
python3 scripts/search_server.py stop
```

**Ventajas:**
- Máxima velocidad para múltiples búsquedas
- Control total sobre el ciclo de vida
- Ideal para sesiones de investigación intensiva

#### C. Servidor en Background

```bash
# Iniciar en background
python3 scripts/search_server.py start &

# Usar desde múltiples terminales/sesiones
python3 scripts/search_client.py "query1"
python3 scripts/search_client.py "query2"

# Matar cuando termines
kill $(cat data/search.pid)
```

### Ejemplos de Queries

**Búsqueda por funcionalidad:**
```bash
python3 scripts/auto_search.py "currency rounding precision"
python3 scripts/auto_search.py "tax calculation invoice"
python3 scripts/auto_search.py "user authentication login"
```

**Búsqueda por patrón de código:**
```bash
python3 scripts/auto_search.py "decorator retry database connection"
python3 scripts/auto_search.py "context manager file handling"
python3 scripts/auto_search.py "async http request timeout"
```

**Búsqueda por nombre (parcial):**
```bash
python3 scripts/auto_search.py "compute amount total"
python3 scripts/auto_search.py "onchange partner address"
python3 scripts/auto_search.py "constraint unique name"
```

### Interpretación de Resultados

**Score (0-1):**
- `> 0.8`: Muy relevante (alta confianza)
- `0.6-0.8`: Relevante (buena coincidencia)
- `0.4-0.6`: Moderadamente relevante
- `< 0.4`: Baja relevancia (posible ruido)

**Estructura de resultado:**
```json
{
  "file": "odoo/addons/account/models/account_move.py",
  "score": 0.847,
  "classes": ["AccountMove", "AccountMoveLine"],
  "functions": ["_compute_amount", "_recompute_tax_lines"],
  "imports": ["odoo", "odoo.fields", "odoo.models"]
}
```

---

## Casos de Uso

### 1. Exploración de Codebase Nuevo

```bash
# Indexar
python3 scripts/index_code.py ~/src/new-project

# Explorar estructura
python3 scripts/auto_search.py "main entry point"
python3 scripts/auto_search.py "configuration settings"
python3 scripts/auto_search.py "database models"
```

### 2. Búsqueda de Bug

```bash
# Buscar código relacionado al problema
python3 scripts/auto_search.py "currency rounding loss"
python3 scripts/auto_search.py "precision decimal fields"

# Una vez identificado el archivo, leer directamente
cat ~/src/odoo/odoo/fields.py | grep -A 10 "class Monetary"
```

### 3. Implementar Feature Similar

```bash
# Buscar implementaciones existentes
python3 scripts/auto_search.py "export csv report"
python3 scripts/auto_search.py "pdf invoice generation"

# Copiar patrón y adaptar
```

### 4. Code Review

```bash
# Antes de revisar un PR, entender el contexto
python3 scripts/auto_search.py "payment workflow state machine"
python3 scripts/auto_search.py "inventory valuation methods"
```

---

## Troubleshooting

### "Index not found"

```bash
# Verificar directorio de índice
ls -la data/vector_index/

# Si está vacío, re-indexar
python3 scripts/index_code.py /path/to/code
```

### "Server not running"

```bash
# Verificar estado
python3 scripts/search_server.py status

# Iniciar manualmente
python3 scripts/search_server.py start

# Si falla, ver logs
tail -f /tmp/search_server.log
```

### "Socket error"

```bash
# Socket stale (servidor murió pero socket persiste)
rm data/search.sock
rm data/search.pid

# Re-iniciar
python3 scripts/search_server.py restart
```

### "Out of memory"

```bash
# Para codebases muy grandes, indexar por subdirectorios
python3 scripts/index_code.py ~/src/odoo/addons
python3 scripts/index_code.py ~/src/odoo/odoo

# O aumentar swap
sudo swapon --show
```

### "Slow search"

```bash
# Verificar servidor esté corriendo (no auto_search)
python3 scripts/search_server.py status

# Si no, iniciar manualmente
python3 scripts/search_server.py start

# Búsquedas deberían ser ~40ms con servidor en memoria
```

### Dependencias fallidas

```bash
# Re-instalar forzado
./scripts/setup.sh --force

# O manual
source venv/bin/activate
pip install --force-reinstall sentence-transformers numpy
```

---

## API Interna

### Usar desde Python

```python
import sys
from pathlib import Path

# Agregar scripts al path
SCRIPT_DIR = Path("/path/to/code-rag-search/scripts")
sys.path.insert(0, str(SCRIPT_DIR))

from search_client import search

# Buscar
results = search("currency rounding", top_k=10)

for r in results:
    print(f"{r['file']}: {r['score']:.3f}")
```

### Usar desde Bash (pipe)

```bash
# Buscar y filtrar por score
python3 scripts/search_client.py "query" 20 | \
    grep -E "^[0-9]+\." | \
    head -5
```

### Integración con Otros Scripts

```python
#!/usr/bin/env python3
"""Ejemplo: Búsqueda automática + apertura de archivos"""

import subprocess
import json

def search_and_open(query, max_results=3):
    # Buscar
    result = subprocess.run(
        ['python3', 'scripts/search_client.py', query, str(max_results)],
        capture_output=True,
        text=True
    )
    
    # Parsear output (simplificado)
    # En producción, usar API directa en vez de parsear stdout
    
    print(f"Búsqueda: {query}")
    print(result.stdout)

# Uso
search_and_open("decimal precision rounding")
```

---

## Performance Tips

1. **Mantener servidor corriendo** durante sesiones de investigación
2. **Indexar solo extensiones relevantes** (no todo el repo si solo buscás Python)
3. **Excluir directorios grandes** (node_modules, vendor, build)
4. **Usar queries específicas** ("currency rounding" vs "currency")
5. **Batch de búsquedas** con servidor persistente vs auto_search individual

---

## Limitaciones Conocidas

- **No soporta Windows nativo** (socket Unix)
- **No búsqueda full-text** (solo embeddings semánticos)
- **No soporta queries multi-lenguaje natural** (mejor en inglés/código)
- **Índice estático** (no actualiza en tiempo real, requiere re-indexar)
