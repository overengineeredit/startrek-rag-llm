#!/bin/bash

# Quick Test Script - Fast feedback during development
# Run this for quick checks before the full CI simulation

set -e

echo "⚡ Quick Test - Fast Feedback Loop"
echo "=================================="

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "docker-compose.yml" ]; then
    print_error "Please run this script from the project root directory"
    exit 1
fi

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
    print_status "Using existing virtual environment"
else
    print_error "Virtual environment not found. Run test-ci-local.sh first to set up the environment."
    exit 1
fi

# Quick format check
print_status "Quick format check..."
black --check startrek-rag/ content_loader/ || {
    print_error "Black formatting issues found. Run: black startrek-rag/ content_loader/"
    exit 1
}

isort --check-only startrek-rag/ content_loader/ || {
    print_error "Import sorting issues found. Run: isort startrek-rag/ content_loader/"
    exit 1
}

print_success "Format check passed"

# Quick syntax check
print_status "Quick syntax check..."
python -m py_compile startrek-rag/app.py
python -m py_compile startrek-rag/config.py
python -m py_compile content_loader/enhanced_processor.py
python -m py_compile content_loader/html_processor.py
print_success "Syntax check passed"

# Quick import test
print_status "Quick import test..."
python -c "
import sys
sys.path.insert(0, 'startrek-rag')
sys.path.insert(0, 'content_loader')

try:
    from config import Config
    from app import create_app
    from enhanced_processor import EnhancedContentProcessor
    from html_processor import HTMLProcessor
    print('✅ All imports successful')
except ImportError as e:
    print(f'❌ Import error: {e}')
    exit(1)
"
print_success "Import test passed"

# Quick Docker build test (if Docker is available)
if command -v docker &> /dev/null; then
    print_status "Quick Docker build test..."
    docker build -t startrek-rag:quick-test startrek-rag/ > /dev/null 2>&1 || {
        print_error "Docker build failed for RAG application"
        exit 1
    }
    docker build -t content-loader:quick-test content_loader/ > /dev/null 2>&1 || {
        print_error "Docker build failed for content loader"
        exit 1
    }
    print_success "Docker builds passed"
else
    print_status "Docker not available, skipping build test"
fi

echo ""
print_success "🎉 Quick test completed successfully!"
print_status "Your code is ready for the full CI test or commit" 