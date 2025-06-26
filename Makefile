.PHONY: setup run clean process-content process-html process-urls process-all help

VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

# Default paths - can be overridden with environment variables
CONTENT_FOLDER ?= $(PWD)/test_content
URLS_FILE ?= $(CONTENT_FOLDER)/star_trek_urls.txt

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