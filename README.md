# Star Trek RAG LLM System

[![codecov](https://codecov.io/gh/overengineeredit/startrek-rag-llm/branch/main/graph/badge.svg)](https://codecov.io/gh/overengineeredit/startrek-rag-llm)

A complete Retrieval-Augmented Generation (RAG) system built with ChromaDB, LangChain, and Ollama, designed to answer questions about Star Trek content using vector embeddings and large language models.

## 🚀 Features

- **Vector Database**: ChromaDB for efficient similarity search
- **Content Processing**: Automated text chunking and embedding generation
- **HTML Processing**: Extract text from HTML files and web pages
- **URL Processing**: Fetch and process content from web URLs
- **Custom Folder Support**: Process content from any folder or URLs from any file
- **RAG Pipeline**: Complete retrieval-augmented generation workflow
- **Docker Support**: Containerized deployment for easy setup
- **LLM Integration**: Ollama integration for local LLM inference
- **REST API**: Flask-based API with clean architecture
- **Service Layer**: Modular, maintainable code structure
- **Request Validation**: Input validation with Marshmallow schemas

## 🏗️ Architecture

The system follows a clean, modular architecture with clear separation of concerns:

### **Core Components**

#### 1. **RAG Application** (`startrek-rag/`)
- **Application Factory**: Clean Flask app initialization
- **API Blueprints**: Organized REST endpoints under `/api/` prefix
- **Service Layer**: Business logic encapsulated in `services/rag_service.py`
- **Configuration Management**: Centralized config with dataclasses
- **Error Handling**: Comprehensive exception handling throughout

#### 2. **Content Loader** (`content_loader/`)
- Content processing and chunking
- Embedding generation via API calls
- Vector database population

#### 3. **Vector Database** (`chroma/`)
- ChromaDB instance for storing embeddings
- Persistent storage for vector data

### **Architecture Benefits**
- ✅ **Modular Design**: Easy to extend and maintain
- ✅ **Testability**: Clear separation enables unit testing
- ✅ **Scalability**: Service layer supports horizontal scaling
- ✅ **Maintainability**: Clean code structure with proper abstractions
- ✅ **Error Handling**: Comprehensive error management
- ✅ **Validation**: Input validation with Marshmallow schemas

## 📋 Prerequisites

- **Docker & Docker Compose**
- **Python 3.10+** (for local development)
- **Ollama** (for LLM functionality)
- **Git**

## 🛠️ Installation & Setup

### Option 1: Docker Setup (Recommended)

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd startrek-rag-llm
   ```

2. **Start the services:**
   ```bash
   docker compose up -d
   ```

3. **Process content:**
   ```bash
   make process-content
   ```

4. **Start Ollama (for LLM functionality):**
   ```bash
   # Start Ollama service
   sudo systemctl start ollama
   
   # Or run manually with host binding
   OLLAMA_HOST=0.0.0.0:11434 ollama serve
   ```

5. **Pull the required model:**
   ```bash
   ollama pull llama3.2
   ```

## 🚀 Quick Start Commands

### Prerequisites: Build Environment (First Time Setup)

**Before running the local startup commands, ensure your environment is built:**

```bash
# 1. Clone the repository (if not already done)
git clone <your-repo-url>
cd startrek-rag-llm

# 2. Install Ollama (if not already installed)
# Follow: https://ollama.com/download

# 3. Pull the required model
ollama pull llama3.2

# 4. Build Docker images (first time or after code changes)
docker compose build

# 5. Verify Docker and Docker Compose are installed
docker --version
docker compose --version
```

### Local Startup (Recommended for Development)

**Step 1: Start Ollama with Docker compatibility**
```bash
# Stop any existing Ollama service
sudo systemctl stop ollama

# Start Ollama with host binding for Docker containers
nohup bash -c 'OLLAMA_HOST=0.0.0.0:11434 ollama serve' > ollama.log 2>&1 &

# Verify Ollama is accessible
curl -s http://localhost:11434/api/tags
```

**Step 2: Start Docker services**
```bash
# Start the application and ChromaDB
docker compose up -d

# Verify services are running
docker compose ps

# Check system health
curl -s http://localhost:8080/api/health
```

**Step 3: Process Star Trek content (optional)**
```bash
# Add Star Trek content to the vector database
make process-content

# Check database stats
curl -s http://localhost:8080/api/stats
```

**Step 4: Test the system**
```bash
# Ask a Star Trek question
curl -X POST http://localhost:8080/api/query \\
  -H "Content-Type: application/json" \\
  -d '{"query": "Who is Captain Kirk?", "num_results": 5}'
```

### Local Shutdown

**Stop all services:**
```bash
# Stop Docker containers
docker compose down

# Stop Ollama processes
pkill ollama

# Verify everything is stopped
docker compose ps
ps aux | grep ollama
```

### Option 2: Local Development Setup

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd startrek-rag-llm
   ```

2. **Create virtual environment:**
   ```bash
   make setup
   ```

3. **Start ChromaDB:**
   ```bash
   docker compose up -d chroma
   ```

4. **Install content loader dependencies:**
   ```bash
   cd content_loader
   pip install -r requirements.txt
   cd ..
   ```

5. **Start the RAG application:**
   ```bash
   make run
   ```

## 🚀 Usage

### API Endpoints

All endpoints are organized under the `/api/` prefix for consistency:

#### **Root Endpoint**
```bash
curl http://localhost:8080/
```
Returns API information and available endpoints.

#### **1. Query the RAG System**
```bash
curl -X POST http://localhost:8080/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Who is Captain Kirk?", "num_results": 5}'
```

#### **2. Add Documents to Vector Database**
```bash
curl -X POST http://localhost:8080/api/add \
  -H "Content-Type: application/json" \
  -d '{
    "document": "Your document text",
    "metadata": {"source": "filename", "chunk_id": 1},
    "id": "unique_id"
  }'
```

#### **3. Generate Embeddings**
```bash
curl -X POST http://localhost:8080/api/embed \
  -H "Content-Type: application/json" \
  -d '{"text": "Your text here"}'
```

#### **4. Get Collection Statistics**
```bash
curl http://localhost:8080/api/stats
```

#### **5. Health Check**
```bash
curl http://localhost:8080/api/health
```

### Content Processing

#### **Custom Folder Support** 🆕

The system now supports processing content from custom folders and URLs from custom files:

```bash
# Process content from a custom folder
CONTENT_FOLDER=/path/to/your/content make process-content

# Process URLs from a custom file
URLS_FILE=/path/to/your/urls.txt make process-urls

# Process both with custom paths
CONTENT_FOLDER=/path/to/content URLS_FILE=/path/to/urls.txt make process-all

# With verbose logging
CONTENT_FOLDER=/path/to/content make process-content-verbose
```

**Examples:**
```bash
# Process content from your documents folder
CONTENT_FOLDER=/home/user/star_trek_docs make process-content

# Process URLs from a different file
URLS_FILE=/home/user/my_urls.txt make process-urls

# Process everything with custom paths
CONTENT_FOLDER=/home/user/docs URLS_FILE=/home/user/urls.txt make process-all
```

**Default Paths:**
- **Content Folder**: `$(PWD)/test_content` (your current test_content folder)
- **URLs File**: `$(PWD)/test_content/star_trek_urls.txt`

#### Process New Content

```bash
# Add your content files to test_content/
make process-content

# Or use a custom folder
CONTENT_FOLDER=/path/to/your/content make process-content
```

#### Process HTML Files
```bash
# Process HTML files in test_content/
make process-html

# Or use a custom folder
CONTENT_FOLDER=/path/to/your/html make process-html
```

#### Process URLs from File
```bash
# Process URLs listed in test_content/star_trek_urls.txt
make process-urls

# Or use a custom URLs file
URLS_FILE=/path/to/your/urls.txt make process-urls
```

#### Process All Content Types
```bash
# Process text, HTML, and URLs in one command
make process-all

# Or use custom paths for all
CONTENT_FOLDER=/path/to/content URLS_FILE=/path/to/urls.txt make process-all
```

#### Enhanced Output and Logging

The content processors now provide detailed output and comprehensive statistics during processing:

**Standard Output (Default)**
- Real-time progress tracking for each file/URL
- File size and content length information
- Chunk processing progress with timing
- Success/failure indicators for each operation
- Summary statistics at completion

**Verbose Logging (Optional)**
```bash
# Enable verbose logging for detailed debugging
make process-content-verbose
make process-html-verbose
make process-urls-verbose
make process-all-verbose
```

**Statistics Output**
The processors provide comprehensive statistics including:
- Total files/URLs processed
- Total chunks extracted and processed
- Total embeddings generated
- Total documents added to ChromaDB
- Processing time and performance metrics
- Error counts and success rates
- File type breakdowns
- Average chunk sizes and processing times

**Example Output**
```
🚀 Starting Enhanced Content Processor at 2024-01-15 10:30:00
   App URL: http://app:8080
   Chunk Size: 1000
   Overlap: 200

📁 Processing folder: /app/content
📁 Found 5 files to process:
   Text files: 3
   HTML files: 2

📄 Processing text file 1/3: startrek_original_series.txt
   File size: 15,432 bytes
   Content length: 15,432 characters
   Split into 45 potential chunks
   Found 42 non-empty chunks
   Processing chunk 1/42 (length: 1,234 chars)
   ✅ Chunk 1 processed successfully in 0.045s
   ...
📄 Completed processing startrek_original_series.txt: 42/42 chunks in 2.34s

============================================================
PROCESSING STATISTICS
============================================================
Total Files Processed: 5
Total URLs Processed: 0
Total Chunks Processed: 156
Total Embeddings Generated: 156
Total Documents Added to ChromaDB: 156
Errors Encountered: 0
Total Processing Time: 8.45 seconds
Average Time per Chunk: 0.054 seconds

File Type Breakdown:
  Text Files: 3
  HTML Files: 2
  URLs: 0

✅ SUCCESS: All content processed without errors
============================================================
```

#### Manual Content Processing
```bash
# Process text files
docker compose run --rm \
  -v $(PWD)/content_loader:/app \
  -v $(PWD)/test_content:/app/content \
  app python /app/process_content.py /app/content

# Process HTML files
docker compose run --rm \
  -v $(PWD)/content_loader:/app \
  -v $(PWD)/test_content:/app/content \
  app python /app/enhanced_processor.py --folder /app/content

# Process URLs from file
docker compose run --rm \
  -v $(PWD)/content_loader:/app \
  -v $(PWD)/test_content:/app/content \
  app python /app/enhanced_processor.py --urls-file /app/content/star_trek_urls.txt
```

### HTML and URL Processing

The system now supports processing HTML documents and web URLs:

> **Note:**
> Advanced HTML chunking with the `unstructured` library fails due to a bug where it requests non-existent NLTK resources (like `averaged_perceptron_tagger_eng`). This is a known upstream issue that affects multiple versions. The system automatically falls back to BeautifulSoup-based extraction, which provides reliable HTML ingestion and good content extraction. A bug report has been submitted to the [unstructured GitHub](https://github.com/Unstructured-IO/unstructured) project. The fallback solution ensures your HTML and URL processing works reliably in production.

#### **Supported File Types**
- **Text Files**: `.txt`, `.md`, `.rst`
- **HTML Files**: `.html`, `.htm`, `.xhtml`

#### **HTML Processing Features**
- **Structured Extraction**: Uses `unstructured` library for intelligent content parsing (if available)
- **BeautifulSoup Integration**: Fallback parsing for complex HTML structures or NLTK issues
- **Content Cleaning**: Removes scripts, styles, and normalizes text
- **Metadata Extraction**: Captures titles, headings, and content structure
- **Smart Chunking**: Creates overlapping chunks with sentence boundary awareness

#### **URL Processing Features**
- **Web Scraping**: Fetches content from web pages
- **User-Agent Headers**: Proper browser identification for compatibility
- **Error Handling**: Graceful handling of network issues and invalid URLs
- **Content Validation**: Ensures meaningful content extraction

#### **Processing Options**
```bash
# Custom chunk size and overlap
docker compose run --rm \
  -v $(PWD)/content_loader:/app \
  -v $(PWD)/test_content:/app/content \
  app python /app/enhanced_processor.py \
    --folder /app/content \
    --chunk-size 1500 \
    --overlap 300

# Process specific URLs
docker compose run --rm \
  -v $(PWD)/content_loader:/app \
  -v $(PWD)/test_content:/app/content \
  app python /app/enhanced_processor.py \
    --urls-file /app/content/star_trek_urls.txt \
    --app-url http://app:8080
```

### Makefile Commands

The system provides convenient Makefile commands for common operations:

#### **Available Commands**
```bash
# View all available commands
make help
```

**Output:**
```
Available commands:
  make setup         - Create virtual environment and install dependencies
  make run           - Start the application
  make clean         - Remove virtual environment and temporary files

Content Processing (with detailed output):
  make process-content - Process text content files and add to ChromaDB
  make process-html  - Process HTML files and add to ChromaDB
  make process-urls  - Process URLs from file and add to ChromaDB
  make process-all   - Process all content types (text, HTML, URLs)

Content Processing (with verbose logging):
  make process-content-verbose - Process text files with verbose logging
  make process-html-verbose  - Process HTML files with verbose logging
  make process-urls-verbose  - Process URLs with verbose logging
  make process-all-verbose   - Process all content with verbose logging

Custom Paths:
  You can override default paths using environment variables:
  CONTENT_FOLDER=/path/to/your/content make process-content
  URLS_FILE=/path/to/your/urls.txt make process-urls
  CONTENT_FOLDER=/path/to/content URLS_FILE=/path/to/urls.txt make process-all

Current defaults:
  Content folder: /path/to/your/test_content
  URLs file: /path/to/your/test_content/star_trek_urls.txt
```

#### **Basic Commands**
```bash
# Setup development environment
make setup

# Start the application locally
make run

# Clean up temporary files
make clean
```

#### **Content Processing Commands**
```bash
# Process text content (default: test_content/)
make process-content

# Process HTML files (default: test_content/)
make process-html

# Process URLs from file (default: test_content/star_trek_urls.txt)
make process-urls

# Process all content types
make process-all
```

#### **Verbose Logging Commands**
```bash
# Process with detailed HTTP request logging
make process-content-verbose
make process-html-verbose
make process-urls-verbose
make process-all-verbose
```

#### **Custom Path Commands**
```bash
# Process content from custom folder
CONTENT_FOLDER=/path/to/your/content make process-content

# Process URLs from custom file
URLS_FILE=/path/to/your/urls.txt make process-urls

# Process all with custom paths
CONTENT_FOLDER=/path/to/content URLS_FILE=/path/to/urls.txt make process-all

# Verbose processing with custom paths
CONTENT_FOLDER=/path/to/content make process-content-verbose
```

## 📁 Project Structure

```
startrek-rag-llm/
├── startrek-rag/              # Main RAG application
│   ├── app.py                # Application factory and main entry point
│   ├── config.py             # Centralized configuration management
│   ├── embed.py              # Embedding generation utilities
│   ├── db_config.py          # ChromaDB configuration
│   ├── routes/               # API route blueprints
│   │   ├── __init__.py
│   │   └── api.py           # REST API endpoints
│   ├── services/             # Business logic layer
│   │   ├── __init__.py
│   │   └── rag_service.py   # RAG operations service
│   ├── requirements.txt      # Python dependencies
│   └── Dockerfile           # Container configuration
├── content_loader/           # Content processing service
│   ├── process_content.py   # Original text content processing script
│   ├── enhanced_processor.py # Enhanced processor supporting HTML and URLs
│   ├── html_processor.py    # HTML parsing and text extraction utilities
│   ├── requirements.txt     # Dependencies
│   └── Dockerfile          # Container configuration
├── test_content/            # Sample content for testing
│   ├── startrek_original_series.txt
│   ├── star_trek_wikipedia.html
│   └── star_trek_urls.txt
├── docker-compose.yml       # Service orchestration
├── Makefile                # Build and run commands
└── README.md               # This file
```

## 🔧 Configuration

### Environment Variables

The system uses the following environment variables:

#### **Database Configuration**
- `CHROMA_HOST`: ChromaDB host (default: `localhost`)
- `CHROMA_PORT`: ChromaDB port (default: `8000`)
- `COLLECTION_NAME`: ChromaDB collection name (default: `startrek`)

#### **Ollama Configuration**
- `OLLAMA_HOST`: Ollama host (default: `localhost`)
- `OLLAMA_PORT`: Ollama port (default: `11434`)
- `LLM_MODEL`: LLM model name (default: `llama3.2`)

#### **Application Configuration**
- `FLASK_HOST`: Flask host (default: `0.0.0.0`)
- `FLASK_PORT`: Flask port (default: `8080`)
- `FLASK_DEBUG`: Debug mode (default: `True`)
- `TEMP_FOLDER`: Temporary files directory (default: `./_temp`)

### Docker Configuration

The `docker-compose.yml` file configures:
- **App Service**: RAG application on port 8080
- **ChromaDB Service**: Vector database on port 8000
- **Networks**: Internal communication between services
- **Volumes**: Persistent data storage

## 🧪 Testing

### Local CI Testing 🆕

The project includes comprehensive local testing capabilities that simulate the GitHub Actions CI environment, providing fast feedback during development.

#### **Quick Test (Fast Feedback)**
For rapid feedback during development:
```bash
# Quick format, syntax, and import checks
make test-quick

# Or run the script directly
./test-quick.sh
```

**What it checks:**
- ✅ Code formatting (Black, isort)
- ✅ Python syntax validation
- ✅ Import functionality
- ✅ Docker build verification (if Docker available)

#### **Full CI Simulation**
For comprehensive testing that mirrors GitHub Actions:
```bash
# Full CI simulation (lint, security, Docker, tests)
make test-ci

# Or run the script directly
./test-ci-local.sh
```

**What it includes:**
- ✅ **Linting**: flake8 with comprehensive rules
- ✅ **Formatting**: Black and isort checks
- ✅ **Type Checking**: mypy with proper configuration
- ✅ **Security Scanning**: Bandit and Safety checks
- ✅ **Docker Builds**: Image building and compose verification
- ✅ **Code Compilation**: Python bytecode generation
- ✅ **Unit Tests**: pytest with coverage reporting
- ✅ **Integration Tests**: Basic functionality verification

#### **Individual Test Components**
Run specific test components as needed:
```bash
# Format checks only
make test-format

# Linting checks only
make test-lint

# Security scans only
make test-security

# Docker builds only
make test-docker

# Unit tests only
make test-unit
```

#### **Test Output Examples**

**Quick Test Output:**
```
⚡ Quick Test - Fast Feedback Loop
==================================
[INFO] Using existing virtual environment
[INFO] Quick format check...
[SUCCESS] Format check passed
[INFO] Quick syntax check...
[SUCCESS] Syntax check passed
[INFO] Quick import test...
✅ All imports successful
[SUCCESS] Import test passed
[INFO] Quick Docker build test...
[SUCCESS] Docker builds passed

🎉 Quick test completed successfully!
[INFO] Your code is ready for the full CI test or commit
```

**Full CI Test Output:**
```
🚀 Starting CI Local Test Simulation
=====================================
[INFO] Step 1: Running Lint and Format Check
----------------------------------------
[INFO] Installing dependencies...
[INFO] Running flake8...
[SUCCESS] flake8 passed
[INFO] Running black check...
[SUCCESS] black check passed
[INFO] Running isort check...
[SUCCESS] isort check passed
[INFO] Running mypy...
[SUCCESS] mypy completed

[INFO] Step 2: Running Security Scan
--------------------------------
[INFO] Running Bandit security scan...
[SUCCESS] Bandit scan completed
[INFO] Running Safety check...
[SUCCESS] Safety check completed

[INFO] Step 3: Building Docker Images
-----------------------------------
[INFO] Building RAG application image...
[SUCCESS] RAG application image built
[INFO] Building content loader image...
[SUCCESS] Content loader image built
[INFO] Testing Docker Compose build...
[SUCCESS] Docker Compose build completed

[INFO] Step 4: Precompiling Python Code
-------------------------------------
[INFO] Precompiling RAG application...
[SUCCESS] RAG application precompiled
[INFO] Precompiling content loader...
[SUCCESS] Content loader precompiled
[INFO] Generating bytecode files...
[SUCCESS] All Python files compiled

[INFO] Step 5: Running Unit Tests
-------------------------------
[INFO] Running unit tests...
============================= test session starts ==============================
platform linux -- Python 3.10.12, pytest-7.4.3, pluggy-1.3.0
plugins: cov-4.1.0, mock-3.12.0
collected 6 items

tests/test_imports.py::test_rag_imports PASSED                           [ 16%]
tests/test_imports.py::test_content_loader_imports PASSED                [ 33%]
tests/test_imports.py::test_config_creation PASSED                       [ 50%]
tests/test_imports.py::test_html_processor_creation PASSED               [ 66%]
tests/test_imports.py::test_enhanced_processor_creation PASSED           [ 83%]
tests/test_imports.py::test_app_creation_with_mock PASSED                [100%]

============================== 6 passed in 2.34s ==============================
[SUCCESS] Unit tests completed

[INFO] Step 6: Running Integration Tests
--------------------------------------
[INFO] Testing basic functionality without external services...
✅ Config and app imports work
✅ Config created: chroma_url=localhost:8000
✅ App created: app
✅ Content loader imports work
✅ Enhanced processor created: chunk_size=1000
✅ HTML processor created: chunk_size=1000
[SUCCESS] Integration tests completed

[INFO] Step 7: Coverage Report
----------------------------
[SUCCESS] Coverage XML report generated
[INFO] Coverage summary:
Name                           Stmts   Miss  Cover   Missing
------------------------------------------------------------
startrek_rag/__init__.py           0      0   100%
startrek_rag/app.py               45      0   100%
startrek_rag/config.py            15      0   100%
startrek_rag/embed.py             25      0   100%
content_loader/__init__.py         0      0   100%
content_loader/enhanced_processor.py   120      0   100%
content_loader/html_processor.py   85      0   100%
------------------------------------------------------------
TOTAL                             290      0   100%

🎉 CI Local Test Simulation Complete!
=====================================
[SUCCESS] All tests passed locally
[INFO] You can now push to GitHub with confidence
```

#### **Development Workflow**

**Recommended workflow for development:**
```bash
# 1. Make your changes
# ... edit files ...

# 2. Quick test for fast feedback
make test-quick

# 3. If quick test passes, run full CI simulation
make test-ci

# 4. If all tests pass, commit and push
git add .
git commit -m "Your changes"
git push
```

**Benefits:**
- 🚀 **Fast Feedback**: Quick tests run in seconds
- 🔍 **Comprehensive**: Full CI simulation catches all issues
- 🛡️ **Confidence**: Local testing prevents CI failures
- ⚡ **Efficiency**: Catch issues before pushing to GitHub
- 📊 **Coverage**: Detailed coverage reporting
- 🔧 **Modular**: Run individual test components as needed

### Test the Complete System

1. **Start all services:**
   ```bash
   docker compose up -d
   ```

2. **Process content:**
   ```bash
   make process-content
   ```

3. **Start Ollama:**
   ```bash
   OLLAMA_HOST=0.0.0.0:11434 ollama serve
   ```

4. **Test all endpoints:**
   ```bash
   # Test root endpoint
   curl http://localhost:8080/
   
   # Test health check
   curl http://localhost:8080/api/health
   
   # Test stats
   curl http://localhost:8080/api/stats
   
   # Test query
   curl -X POST http://localhost:8080/api/query \
     -H "Content-Type: application/json" \
     -d '{"query": "Who is Captain Kirk?"}'
   
   # Test embedding generation
   curl -X POST http://localhost:8080/api/embed \
     -H "Content-Type: application/json" \
     -d '{"text": "Star Trek is a science fiction franchise"}'
   ```

## 🐛 Troubleshooting

### Common Issues

1. **Ollama Connection Refused**
   - Ensure Ollama is running: `sudo systemctl status ollama`
   - Start Ollama with host binding: `OLLAMA_HOST=0.0.0.0:11434 ollama serve`

2. **ChromaDB Connection Issues**
   - Check if ChromaDB container is running: `docker compose ps`
   - Restart services: `docker compose restart`

3. **Content Processing Failures**
   - Verify content files exist in `test_content/`
   - Check container logs: `docker compose logs app`

4. **Port Conflicts**
   - Ensure ports 8080 and 8000 are available
   - Modify `docker-compose.yml` if needed

5. **Import Errors**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check Python path and virtual environment activation

### Logs and Debugging

```bash
# View application logs
docker compose logs app

# View ChromaDB logs
docker compose logs chroma

# Follow logs in real-time
docker compose logs -f app

# Check service status
docker compose ps
```

## 📚 Dependencies

### Core Dependencies
- **ChromaDB**: Vector database for embeddings
- **LangChain**: LLM orchestration framework
- **Flask**: Web framework for API
- **Ollama**: Local LLM inference
- **Python-dotenv**: Environment variable management
- **Marshmallow**: Request validation and serialization
- **Flask-restx**: API documentation (future enhancement)

### Development Dependencies
- **Docker**: Containerization
- **Docker Compose**: Service orchestration
- **Make**: Build automation

## 🔄 Architecture Evolution

### **Previous Architecture**
- Monolithic Flask application
- Mixed concerns in single files
- Direct endpoint definitions
- Limited error handling

### **Current Architecture**
- ✅ **Application Factory Pattern**: Clean app initialization
- ✅ **Service Layer**: Business logic encapsulation
- ✅ **API Blueprints**: Organized route structure
- ✅ **Centralized Configuration**: Environment-based config management
- ✅ **Comprehensive Error Handling**: Proper exception management
- ✅ **Request Validation**: Input validation with schemas
- ✅ **Modular Design**: Easy to extend and maintain

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes following the established architecture patterns
4. Test thoroughly
5. Commit your changes: `git commit -m 'Add feature'`
6. Push to the branch: `git push origin feature-name`
7. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Star Trek** content for testing
- **ChromaDB** for vector database functionality
- **LangChain** for LLM orchestration
- **Ollama** for local LLM inference
- **Flask** for the web framework foundation

---

**Happy exploring the final frontier! 🖖** 