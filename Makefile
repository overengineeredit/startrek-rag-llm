.PHONY: setup run clean process-content process-html process-urls process-all help test-quick test-ci test-format test-lint test-security test-docker test-unit versions update-versions

VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

# Default paths - can be overridden with environment variables
CONTENT_FOLDER ?= $(PWD)/test_content
URLS_FILE ?= $(CONTENT_FOLDER)/star_trek_urls.txt

# Version management
versions:
	@echo "Current versions:"
	@echo "  ChromaDB: 0.4.24"
	@echo "  Python: 3.11"
	@echo "  Docker BuildKit: 1"
	@echo ""
	@echo "To update versions, edit the following files:"
	@echo "  - .github/workflows/build-and-test.yml (env.CHROMA_VERSION)"
	@echo "  - .github/workflows/test-only.yml (env.CHROMA_VERSION)"
	@echo "  - .github/workflows/release.yml (env.CHROMA_VERSION)"
	@echo "  - docker-compose.yml (CHROMA_VERSION environment variable)"
	@echo "  - config/versions.env (reference file)"

update-versions:
	@echo "Version update helper:"
	@echo "1. Update CHROMA_VERSION in all workflow files"
	@echo "2. Update docker-compose.yml if needed"
	@echo "3. Update config/versions.env as reference"
	@echo "4. Test with: make test-docker"
	@echo ""
	@echo "Current ChromaDB version locations:"
	@grep -r "CHROMA_VERSION" .github/workflows/ || true
	@grep -r "chromadb/chroma" docker-compose.yml || true

setup:
	@echo "Setting up virtual environment..."
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r startrek-rag/requirements.txt

run:
	@echo "Starting the application..."
	$(PYTHON) startrek-rag/app.py

clean:
	@echo "Cleaning up..."
	rm -rf $(VENV)
	rm -rf startrek-rag/_temp/*
	rm -rf startrek-rag/__pycache__
	rm -rf startrek-rag/*.pyc
	rm -rf content_loader/__pycache__
	rm -rf content_loader/*.pyc
	rm -rf tests/__pycache__
	rm -rf tests/*.pyc
	rm -f bandit-report.json safety-report.json coverage.xml
	rm -rf htmlcov/

# Test targets
test-quick:
	@echo "Running quick tests for fast feedback..."
	./test-quick.sh

test-ci:
	@echo "Running full CI simulation locally..."
	./test-ci-local.sh

test-format:
	@echo "Running format checks..."
	@if [ ! -d "$(VENV)" ]; then echo "Virtual environment not found. Run 'make setup' first."; exit 1; fi
	. $(VENV)/bin/activate && black --check startrek-rag/ content_loader/
	. $(VENV)/bin/activate && isort --check-only startrek-rag/ content_loader/
	@echo "✅ Format checks passed"

test-lint:
	@echo "Running linting checks..."
	@if [ ! -d "$(VENV)" ]; then echo "Virtual environment not found. Run 'make setup' first."; exit 1; fi
	. $(VENV)/bin/activate && pip install flake8
	. $(VENV)/bin/activate && flake8 startrek-rag/ content_loader/ --count --select=E9,F63,F7,F82 --show-source --statistics
	. $(VENV)/bin/activate && flake8 startrek-rag/ content_loader/ --count --exit-zero --statistics
	@echo "✅ Linting checks passed"

test-security:
	@echo "Running security scans..."
	@if [ ! -d "$(VENV)" ]; then echo "Virtual environment not found. Run 'make setup' first."; exit 1; fi
	. $(VENV)/bin/activate && pip install bandit safety
	. $(VENV)/bin/activate && bandit -r startrek-rag/ content_loader/ -f json -o bandit-report.json || true
	. $(VENV)/bin/activate && safety check --output json > safety-report.json || true
	@echo "✅ Security scans completed"

test-docker:
	@echo "Testing Docker builds..."
	@if ! command -v docker &> /dev/null; then echo "Docker not found, skipping Docker tests"; exit 0; fi
	docker build -t startrek-rag:test startrek-rag/
	docker build -t content-loader:test content_loader/
	docker compose build
	@echo "✅ Docker builds passed"

test-unit:
	@echo "Running unit tests..."
	@if [ ! -d "$(VENV)" ]; then echo "Virtual environment not found. Run 'make setup' first."; exit 1; fi
	. $(VENV)/bin/activate && pip install pytest pytest-cov pytest-mock
	. $(VENV)/bin/activate && pytest tests/ -v --cov=startrek-rag --cov=content_loader --cov-report=term-missing --cov-report=html --cov-report=xml
	@echo "✅ Unit tests completed"

# Content processing targets
process-content:
	@echo "Processing content files with detailed output..."
	@echo "Content folder: $(CONTENT_FOLDER)"
	docker compose run --rm -v $(PWD)/content_loader:/app -v $(CONTENT_FOLDER):/app/content app python /app/process_content.py /app/content

process-content-verbose:
	@echo "Processing content files with verbose logging..."
	@echo "Content folder: $(CONTENT_FOLDER)"
	docker compose run --rm -v $(PWD)/content_loader:/app -v $(CONTENT_FOLDER):/app/content app python /app/process_content.py /app/content --verbose

process-html:
	@echo "Processing HTML files with detailed output..."
	@echo "Content folder: $(CONTENT_FOLDER)"
	docker compose run --rm -v $(PWD)/content_loader:/app -v $(CONTENT_FOLDER):/app/content app python /app/enhanced_processor.py --folder /app/content

process-html-verbose:
	@echo "Processing HTML files with verbose logging..."
	@echo "Content folder: $(CONTENT_FOLDER)"
	docker compose run --rm -v $(PWD)/content_loader:/app -v $(CONTENT_FOLDER):/app/content app python /app/enhanced_processor.py --folder /app/content --verbose

process-urls:
	@echo "Processing URLs from file with detailed output..."
	@echo "URLs file: $(URLS_FILE)"
	docker compose run --rm -v $(PWD)/content_loader:/app -v $(dir $(URLS_FILE)):/app/urls_dir app python /app/enhanced_processor.py --urls-file /app/urls_dir/$(notdir $(URLS_FILE))

process-urls-verbose:
	@echo "Processing URLs from file with verbose logging..."
	@echo "URLs file: $(URLS_FILE)"
	docker compose run --rm -v $(PWD)/content_loader:/app -v $(dir $(URLS_FILE)):/app/urls_dir app python /app/enhanced_processor.py --urls-file /app/urls_dir/$(notdir $(URLS_FILE)) --verbose

process-all:
	@echo "Processing all content types with detailed output..."
	$(MAKE) process-content
	$(MAKE) process-html
	$(MAKE) process-urls

process-all-verbose:
	@echo "Processing all content types with verbose logging..."
	$(MAKE) process-content-verbose
	$(MAKE) process-html-verbose
	$(MAKE) process-urls-verbose

help:
	@echo "Available commands:"
	@echo "  make setup         - Create virtual environment and install dependencies"
	@echo "  make run           - Start the application"
	@echo "  make clean         - Remove virtual environment and temporary files"
	@echo ""
	@echo "Version Management:"
	@echo "  make versions      - Show current versions and where they're defined"
	@echo "  make update-versions - Show instructions for updating versions"
	@echo ""
	@echo "Testing (Local CI Simulation):"
	@echo "  make test-quick    - Quick tests for fast feedback during development"
	@echo "  make test-ci       - Full CI simulation (lint, security, Docker, tests)"
	@echo "  make test-format   - Run format checks (black, isort)"
	@echo "  make test-lint     - Run linting checks (flake8)"
	@echo "  make test-security - Run security scans (bandit, safety)"
	@echo "  make test-docker   - Test Docker builds"
	@echo "  make test-unit     - Run unit tests with coverage"
	@echo ""
	@echo "Content Processing (with detailed output):"
	@echo "  make process-content - Process text content files and add to ChromaDB"
	@echo "  make process-html  - Process HTML files and add to ChromaDB"
	@echo "  make process-urls  - Process URLs from file and add to ChromaDB"
	@echo "  make process-all   - Process all content types (text, HTML, URLs)"
	@echo ""
	@echo "Content Processing (with verbose logging):"
	@echo "  make process-content-verbose - Process text files with verbose logging"
	@echo "  make process-html-verbose  - Process HTML files with verbose logging"
	@echo "  make process-urls-verbose  - Process URLs with verbose logging"
	@echo "  make process-all-verbose   - Process all content with verbose logging"
	@echo ""
	@echo "Custom Paths:"
	@echo "  You can override default paths using environment variables:"
	@echo "  CONTENT_FOLDER=/path/to/your/content make process-content"
	@echo "  URLS_FILE=/path/to/your/urls.txt make process-urls"
	@echo "  CONTENT_FOLDER=/path/to/content URLS_FILE=/path/to/urls.txt make process-all"
	@echo ""
	@echo "Current defaults:"
	@echo "  Content folder: $(CONTENT_FOLDER)"
	@echo "  URLs file: $(URLS_FILE)" 