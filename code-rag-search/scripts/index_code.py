#!/usr/bin/env python3
"""
index_code.py - Crea índice vectorial desde un directorio de código fuente.

Uso:
    python3 scripts/index_code.py /path/to/codebase [extensions]
    
Ejemplos:
    python3 scripts/index_code.py ~/src/odoo
    python3 scripts/index_code.py ~/src/myproject .py,.js
    python3 scripts/index_code.py --help
"""

import os
import sys
import json
import hashlib
import ast
import re
from pathlib import Path
from datetime import datetime

# Agregar path relativo al skill
SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
DATA_DIR = SKILL_DIR / "data"
INDEX_DIR = DATA_DIR / "vector_index"

# Default extensions
DEFAULT_EXTENSIONS = ['.py', '.js', '.ts', '.jsx', '.tsx', '.rb', '.java', '.go', '.rs', '.cpp', '.c', '.h']


def parse_python_file(filepath):
    """Extrae clases, funciones e imports de un archivo Python."""
    result = {
        'classes': [],
        'functions': [],
        'imports': []
    }
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            source = f.read()
        
        tree = ast.parse(source)
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                result['classes'].append({
                    'name': node.name,
                    'methods': methods,
                    'line': node.lineno
                })
            elif isinstance(node, ast.FunctionDef):
                result['functions'].append({
                    'name': node.name,
                    'line': node.lineno,
                    'args': [arg.arg for arg in node.args.args if arg.arg != 'self']
                })
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        result['imports'].append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ''
                    for alias in node.names:
                        result['imports'].append(f"{module}.{alias.name}")
    
    except SyntaxError:
        pass  # Skip files with syntax errors
    except Exception as e:
        print(f"  ⚠️  Error parsing {filepath}: {e}", file=sys.stderr)
    
    return result


def extract_text_content(filepath, parsed_info):
    """Genera texto representativo del archivo para embedding."""
    lines = []
    
    # Nombre del archivo
    lines.append(f"File: {filepath}")
    
    # Imports
    if parsed_info['imports']:
        lines.append("Imports: " + ", ".join(sorted(set(parsed_info['imports']))[:20]))
    
    # Clases
    for cls in parsed_info['classes']:
        lines.append(f"Class: {cls['name']}")
        if cls['methods']:
            lines.append(f"  Methods: {', '.join(cls['methods'][:10])}")
    
    # Funciones
    for func in parsed_info['functions']:
        args_str = ", ".join(func['args'][:5])
        lines.append(f"Function: {func['name']}({args_str})")
    
    return "\n".join(lines)


def scan_directory(root_path, extensions):
    """Escanea directorio y retorna lista de archivos."""
    files = []
    root = Path(root_path).resolve()
    
    print(f"📂 Escaneando: {root}")
    
    for ext in extensions:
        pattern = f"*{ext}"
        matches = list(root.rglob(pattern))
        # Excluir directorios comunes
        matches = [
            m for m in matches 
            if not any(part.startswith('.') or part in ['node_modules', 'venv', '__pycache__', 'build', 'dist', '.git'] 
                      for part in m.relative_to(root).parts)
        ]
        files.extend(matches)
        print(f"  {ext}: {len(matches)} archivos")
    
    return sorted(set(files))


def compute_file_hash(filepath):
    """Computa hash SHA256 de un archivo."""
    hash_md5 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Crear índice vectorial de código fuente')
    parser.add_argument('codebase_path', help='Directorio de código fuente a indexar')
    parser.add_argument('--extensions', '-e', 
                       help='Extensiones a incluir (comma-separated, ej: .py,.js)',
                       default=None)
    parser.add_argument('--output', '-o',
                       help='Directorio de salida (default: data/vector_index/)',
                       default=None)
    
    args = parser.parse_args()
    
    # Parse extensions
    if args.extensions:
        extensions = [ext.strip() if ext.strip().startswith('.') else f'.{ext.strip()}' 
                     for ext in args.extensions.split(',')]
    else:
        extensions = DEFAULT_EXTENSIONS
    
    # Output directory
    output_dir = Path(args.output) if args.output else INDEX_DIR
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"🔧 Code RAG Search - Indexer")
    print(f"============================")
    print(f"Extensiones: {', '.join(extensions)}")
    print(f"Output: {output_dir}")
    print()
    
    # Scan files
    files = scan_directory(args.codebase_path, extensions)
    total_files = len(files)
    
    if total_files == 0:
        print("❌ No se encontraron archivos")
        sys.exit(1)
    
    print(f"\n📊 Total: {total_files} archivos")
    print()
    
    # Import ML libraries
    print("📚 Cargando modelo de embeddings...")
    from sentence_transformers import SentenceTransformer
    import numpy as np
    from tqdm import tqdm
    
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Process files
    print("🔄 Procesando archivos...")
    metadata = []
    texts = []
    
    for filepath in tqdm(files, desc="Extrayendo contenido"):
        try:
            rel_path = str(filepath.relative_to(Path(args.codebase_path).resolve()))
            parsed = parse_python_file(filepath) if filepath.suffix == '.py' else {
                'classes': [], 'functions': [], 'imports': []
            }
            
            # Para archivos no-Python, extraer texto simple
            if filepath.suffix != '.py':
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    # Extraer patrones simples
                    text_content = f"File: {rel_path}\n{content[:2000]}"
                except:
                    text_content = f"File: {rel_path}"
            else:
                text_content = extract_text_content(rel_path, parsed)
            
            texts.append(text_content)
            metadata.append({
                'file': rel_path,
                'hash': compute_file_hash(filepath),
                'classes': parsed['classes'],
                'functions': parsed['functions'],
                'imports': parsed['imports'][:20],  # Limitar imports
                'size': filepath.stat().st_size,
                'indexed_at': datetime.now().isoformat()
            })
        
        except Exception as e:
            print(f"  ⚠️  Error con {filepath}: {e}", file=sys.stderr)
            continue
    
    print(f"\n✅ Procesados: {len(texts)} archivos")
    
    # Generate embeddings
    print("🧮 Generando embeddings...")
    embeddings = model.encode(texts, show_progress_bar=True, batch_size=32)
    
    # Save
    print(f"💾 Guardando en {output_dir}...")
    
    np.save(output_dir / "embeddings.npy", embeddings)
    
    with open(output_dir / "metadata.json", 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    # Save index info
    index_info = {
        'created_at': datetime.now().isoformat(),
        'source_path': str(Path(args.codebase_path).resolve()),
        'total_files': len(metadata),
        'extensions': extensions,
        'model': 'all-MiniLM-L6-v2',
        'embedding_dim': embeddings.shape[1] if len(embeddings.shape) > 1 else 384
    }
    
    with open(output_dir / "index_info.json", 'w', encoding='utf-8') as f:
        json.dump(index_info, f, indent=2)
    
    print()
    print("✅ Índice creado exitosamente!")
    print()
    print(f"  Archivos indexados: {len(metadata)}")
    print(f"  Dimensión embeddings: {embeddings.shape[1] if len(embeddings.shape) > 1 else 384}")
    print(f"  Tamaño embeddings: {embeddings.nbytes / 1024 / 1024:.1f} MB")
    print(f"  Ubicación: {output_dir}")
    print()
    print("Ahora podés buscar con:")
    print(f"  python3 {SCRIPT_DIR / 'auto_search.py'} \"tu búsqueda\"")
    print()


if __name__ == "__main__":
    main()
