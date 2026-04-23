#!/bin/bash
#
# setup.sh - Instalación del entorno virtual y dependencias
# Uso: ./scripts/setup.sh [--force]
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
VENV_DIR="$SKILL_DIR/venv"
DATA_DIR="$SKILL_DIR/data"

echo "🔧 Code RAG Search - Setup"
echo "=========================="
echo ""

# Check for --force flag
FORCE=false
if [[ "$1" == "--force" ]]; then
    FORCE=true
    echo "⚠️  Force mode: removing existing venv"
    rm -rf "$VENV_DIR"
fi

# Create virtual environment
if [[ -d "$VENV_DIR" ]]; then
    echo "✅ Virtual environment already exists at: $VENV_DIR"
else
    echo "📦 Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip --quiet

# Install dependencies
echo "📥 Installing dependencies..."
pip install --quiet \
    sentence-transformers \
    numpy \
    scikit-learn \
    tqdm

# Create data directory
echo "📁 Creating data directory..."
mkdir -p "$DATA_DIR/vector_index"

# Verify installation
echo ""
echo "🔍 Verifying installation..."
python3 -c "
import sentence_transformers
import numpy
print(f'  sentence-transformers: {sentence_transformers.__version__}')
print(f'  numpy: {numpy.__version__}')
"

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Index your codebase:"
echo "     python3 scripts/index_code.py /path/to/your/code"
echo ""
echo "  2. Start searching:"
echo "     python3 scripts/auto_search.py \"your query\""
echo ""
