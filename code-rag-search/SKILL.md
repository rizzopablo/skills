---
name: code-rag-search
description: Búsqueda semántica de código fuente con embeddings vectoriales. Use when searching codebases by meaning, finding functions/classes, or exploring unfamiliar code. Requires initial indexing.
---

# Code RAG Search

Búsqueda semántica de código fuente usando embeddings vectoriales (Sentence Transformers).

## Quick Start

```bash
# 1. Instalación (primera vez)
cd code-rag-search/
./scripts/setup.sh

# 2. Indexar un directorio de código fuente
python3 scripts/index_code.py /path/to/source/code

# 3. Buscar
python3 scripts/auto_search.py "rounding decimal POS"
```

## Estructura del Skill

```
code-rag-search/
├── SKILL.md                 # Este archivo
├── scripts/
│   ├── setup.sh            # Instalación (venv + dependencias)
│   ├── index_code.py       # Crear índice vectorial
│   ├── search_server.py    # Servidor de búsqueda (socket local)
│   ├── search_client.py    # Cliente rápido (requiere servidor)
│   └── auto_search.py      # Cliente con auto-inicio
└── data/                    # Generado automáticamente
    ├── vector_index/       # Embeddings + metadata
    ├── search.sock         # Socket (cuando servidor activo)
    ├── server.log          # Log de ejecución del servidor
    ├── client.log          # Log de ejecución del cliente
    ├── queries.csv         # Historial de consultas (CSV)
    └── auto_search.log     # Log de auto_search
```

## Comandos

### Instalación

```bash
./scripts/setup.sh
```

Crea:
- `venv/` con Python virtual environment
- Instala: `sentence-transformers`, `numpy`, `scikit-learn`

### Indexar Código

```bash
python3 scripts/index_code.py /path/to/codebase [extensions]
```

**Ejemplos:**
```bash
# Indexar todo Python
python3 scripts/index_code.py ~/src/odoo

# Solo Python y JS
python3 scripts/index_code.py ~/src/myproject .py,.js

# Ver ayuda
python3 scripts/index_code.py --help
```

**Proceso:**
1. Escanea directorio recursivamente
2. Extrae clases, funciones, imports de cada archivo
3. Genera embeddings con `all-MiniLM-L6-v2`
4. Guarda en `data/vector_index/`

**Tiempo:** ~1-2 minutos para 10k archivos

### Buscar

**Opción A: Auto (recomendado)**
```bash
python3 scripts/auto_search.py "query de búsqueda"
```
Inicia el servidor si no está corriendo.

**Opción B: Cliente rápido**
```bash
# Primero iniciar servidor
python3 scripts/search_server.py start

# Luego buscar (múltiples queries, ~40ms c/u)
python3 scripts/search_client.py "primera búsqueda"
python3 scripts/search_client.py "otra búsqueda"

# Ver logs y consultas
python3 scripts/search_server.py logs
python3 scripts/search_server.py queries
```

**Opción C: Servidor en background**
```bash
# Iniciar en background
python3 scripts/search_server.py start &

# Usar desde múltiples sesiones/terminales
python3 scripts/search_client.py "query"
```

## Flujo de Trabajo Típico

```bash
# 1. Setup inicial (solo primera vez)
cd code-rag-search/
./scripts/setup.sh

# 2. Indexar código fuente (cada vez que cambie el código)
python3 scripts/index_code.py ~/src/odoo

# 3. Múltiples búsquedas (servidor persiste en memoria)
python3 scripts/auto_search.py "rounding precision"
python3 scripts/auto_search.py "currency conversion"
python3 scripts/auto_search.py "tax calculation"

# 4. Cuando termines, parar servidor (opcional)
python3 scripts/search_server.py stop
```

## Output Format

Cada resultado incluye:
- **file**: Ruta relativa del archivo
- **score**: Similaridad coseno (0-1, más alto = más relevante)
- **classes**: Clases definidas en el archivo
- **functions**: Funciones/métodos definidos

**Ejemplo:**
```
1. odoo/addons/account/models/account_move.py
   Score: 0.847
   Clases: AccountMove, AccountMoveLine
   Funciones: _compute_amount, _recompute_tax_lines

2. odoo/odoo/fields.py
   Score: 0.723
   Clases: Field, Monetary, Float
   Funciones: convert_to_cache, convert_to_record
```

## Configuración y Paths

**Paths relativos al directorio del skill:**
- `data/vector_index/` - Índice vectorial (embeddings + metadata)
- `data/search.sock` - Socket Unix para comunicación cliente/servidor
- `data/search.pid` - PID del servidor
- `data/server.log` - Log de ejecución del servidor
- `data/queries.csv` - Historial de consultas (CSV)

**Modelo de embeddings:** `sentence-transformers/all-MiniLM-L6-v2`
- 384 dimensiones
- ~80MB
- Rápido, buena calidad para código

## Logging y Auditoría

El servidor genera automáticamente:

**1. Log de ejecución** (`data/server.log`):
```bash
# Ver últimas 50 líneas
python3 scripts/search_server.py logs

# Ver en tiempo real
tail -f data/server.log
```

**2. Historial de consultas** (`data/queries.csv`):
```bash
# Ver últimas 20 consultas
python3 scripts/search_server.py queries

# Exportar/analizar
cat data/queries.csv
```

**Columnas del CSV:**
- `timestamp`: Fecha y hora ISO-8601
- `query`: Texto de la consulta
- `results_count`: Cantidad de resultados
- `top_score`: Score del primer resultado
- `top_file`: Archivo del primer resultado
- `duration_ms`: Tiempo de procesamiento en milisegundos

## Limitaciones

- **No distribuye el índice**: Cada usuario debe indexar su propio código
- **Socket Unix**: Solo funciona en Linux/macOS (no Windows nativo)
- **Memoria**: ~500MB RAM para índice de 10k archivos
- **Idioma**: Mejor para inglés/código; embeddings menos precisos para español

## Troubleshooting

**"Server not running":**
```bash
python3 scripts/search_server.py start
```

**"Socket not found":**
```bash
# Verificar servidor
python3 scripts/search_server.py status

# Ver logs
python3 scripts/search_server.py logs

# Re-iniciar
python3 scripts/search_server.py restart
```

**"Búsqueda se cuelga / no responde":**
```bash
# 1. Ver logs del servidor
python3 scripts/search_server.py logs

# 2. Ver queries registradas
python3 scripts/search_server.py queries

# 3. Parar y re-iniciar servidor
python3 scripts/search_server.py stop
python3 scripts/search_server.py start

# 4. Probar con timeout mayor
python3 scripts/search_client.py "query" 10 60
```

**"Index not found":**
```bash
# Re-indexar
python3 scripts/index_code.py /path/to/code
```

**Errores de dependencias:**
```bash
# Re-instalar
./scripts/setup.sh --force
```

## Ver También

- `references/USAGE.md` - Guía detallada de uso
- `references/ARCHITECTURE.md` - Arquitectura y diseño interno
