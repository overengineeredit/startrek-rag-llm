#!/bin/bash

# CI Local Test Script - Simulates GitHub Actions environment
# Run this to test your changes before pushing to GitHub

set -e  # Exit on any error

echo "🚀 Starting CI Local Test Simulation"
echo "====================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "docker-compose.yml" ]; then
    print_error "Please run this script from the project root directory"
    exit 1
fi

# Step 1: Lint and Format Check
print_status "Step 1: Running Lint and Format Check"
echo "----------------------------------------"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    print_warning "Virtual environment not found. Creating one..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
print_status "Installing dependencies..."
pip install --upgrade pip
pip install flake8 black isort mypy
pip install -r startrek-rag/requirements.txt
pip install -r content_loader/requirements.txt

# Run flake8
print_status "Running flake8..."
flake8 startrek-rag/ content_loader/ --count --select=E9,F63,F7,F82 --show-source --statistics
flake8 startrek-rag/ content_loader/ --count --exit-zero --statistics
print_success "flake8 passed"

# Run black check
print_status "Running black check..."
black --check startrek-rag/ content_loader/
print_success "black check passed"

# Run isort check
print_status "Running isort check..."
isort --check-only startrek-rag/ content_loader/
print_success "isort check passed"

# Run mypy
print_status "Running mypy..."
mypy startrek-rag/ content_loader/ --ignore-missing-imports || true
print_success "mypy completed"

# Step 2: Security Scan
print_status "Step 2: Running Security Scan"
echo "--------------------------------"

# Install security tools
pip install bandit safety

# Run Bandit
print_status "Running Bandit security scan..."
bandit -r startrek-rag/ content_loader/ -f json -o bandit-report.json || true
cat bandit-report.json
print_success "Bandit scan completed"

# Run Safety
print_status "Running Safety check..."
safety check --output json > safety-report.json || true
cat safety-report.json
print_success "Safety check completed"

# Step 3: Build Docker Images
print_status "Step 3: Building Docker Images"
echo "-----------------------------------"

# Check Docker
if ! command -v docker &> /dev/null; then
    print_warning "Docker not found, skipping Docker build step"
else
    print_status "Building RAG application image..."
    docker build -t startrek-rag:test startrek-rag/
    print_success "RAG application image built"
    
    print_status "Building content loader image..."
    docker build -t content-loader:test content_loader/
    print_success "Content loader image built"
    
    print_status "Testing Docker Compose build..."
    docker compose build
    print_success "Docker Compose build completed"
fi

# Step 4: Precompile Python Code
print_status "Step 4: Precompiling Python Code"
echo "-------------------------------------"

print_status "Precompiling RAG application..."
cd startrek-rag
python -m py_compile app.py
python -m py_compile config.py
python -m py_compile embed.py
python -m py_compile db_config.py
python -m py_compile routes/__init__.py
python -m py_compile routes/api.py
python -m py_compile services/__init__.py
python -m py_compile services/rag_service.py
print_success "RAG application precompiled"

cd ../content_loader
python -m py_compile process_content.py
python -m py_compile enhanced_processor.py
python -m py_compile html_processor.py
print_success "Content loader precompiled"

cd ..
print_status "Generating bytecode files..."
find . -name "*.py" -exec python -m py_compile {} \;
print_success "All Python files compiled"

# Step 5: Unit Tests
print_status "Step 5: Running Unit Tests"
echo "-------------------------------"

# Install test dependencies
pip install pytest pytest-cov pytest-mock

# Check if tests directory exists
print_status "Checking test files..."
if [ ! -d "tests" ]; then
    print_error "Tests directory not found. Please ensure tests/ directory exists with test files."
    exit 1
fi

if [ ! -f "tests/test_imports.py" ]; then
    print_error "tests/test_imports.py not found. Please ensure test files exist."
    exit 1
fi

print_success "Test files found and ready to use"

# Run unit tests
print_status "Running unit tests..."
pytest tests/ -v --cov=startrek-rag --cov=content_loader --cov-report=term-missing --cov-report=html --cov-report=xml
print_success "Unit tests completed"

# Step 6: Integration Tests
print_status "Step 6: Running Integration Tests"
echo "--------------------------------------"

print_status "Testing basic functionality without external services..."

# Test RAG functionality
cd startrek-rag
python -c "
import sys
sys.path.insert(0, '.')

# Mock ChromaDB dependencies
from unittest.mock import patch, MagicMock

with patch('chromadb.Client'), patch('chromadb.PersistentClient'):
    from config import Config
    from app import create_app
    print('✅ Config and app imports work')
    
    config = Config()
    print(f'✅ Config created: chroma_url={config.chroma_url}')
    
    # Test app creation with mocked RAG service
    with patch('services.rag_service.RAGService'):
        app = create_app()
        print(f'✅ App created: {app.name}')
"

# Test content loader functionality
cd ../content_loader
python -c "
import sys
sys.path.insert(0, '.')

from enhanced_processor import EnhancedContentProcessor
from html_processor import HTMLProcessor
print('✅ Content loader imports work')

processor = EnhancedContentProcessor()
print(f'✅ Enhanced processor created: chunk_size={processor.chunk_size}')

html_processor = HTMLProcessor()
print(f'✅ HTML processor created: chunk_size={html_processor.chunk_size}')
"

cd ..
print_success "Integration tests completed"

# Step 7: Coverage Report
print_status "Step 7: Coverage Report"
echo "----------------------------"

# Show coverage summary if available
if command -v coverage &> /dev/null; then
    print_status "Coverage summary:"
    coverage report || true
fi

if [ -f "coverage.xml" ]; then
    print_success "Coverage XML report generated"
else
    print_warning "No coverage XML report found"
fi

if [ -d "htmlcov" ]; then
    print_success "Coverage HTML report generated in htmlcov/"
    print_status "Open htmlcov/index.html in your browser to view detailed coverage"
else
    print_warning "No coverage HTML report found"
fi

# Final Summary
echo ""
echo "🎉 CI Local Test Simulation Complete!"
echo "====================================="
print_success "All tests passed locally"
print_status "You can now push to GitHub with confidence"
echo ""
print_status "Next steps:"
echo "  1. Review any warnings above"
echo "  2. Commit your changes"
echo "  3. Push to GitHub"
echo "  4. Check GitHub Actions for final verification" 