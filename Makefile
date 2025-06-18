.PHONY: setup run clean

# Python virtual environment
VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

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

help:
	@echo "Available commands:"
	@echo "  make setup    - Create virtual environment and install dependencies"
	@echo "  make run      - Start the application"
	@echo "  make clean    - Remove virtual environment and temporary files" 