# Star Trek RAG LLM System

[![codecov](https://codecov.io/gh/overengineeredit/startrek-rag-llm/branch/main/graph/badge.svg)](https://codecov.io/gh/overengineeredit/startrek-rag-llm)

A Retrieval-Augmented Generation (RAG) system built with ChromaDB, LangChain, and Ollama for answering Star Trek questions using vector embeddings and large language models.

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

### **📊 Detailed Architecture Documentation**

For comprehensive architecture diagrams and detailed system documentation, see:
- **[📋 Architecture Diagrams](docs/README.md)** - 14 PlantUML diagrams covering system overview, component interactions, data flows, deployment, API endpoints, and processing workflows
- **🔧 Diagram Generation** - Automated CI/CD diagram generation with syntax validation
- **📈 Visual Documentation** - Color-coded component diagrams and workflow visualizations

## Prerequisites
- **Docker & Docker Compose**
- **Ollama** (for LLM functionality)

- **Git**

## 🛠️ Quick Start

### 1. Clone and Setup
```bash
git clone <your-repo-url>
cd startrek-rag-llm
```

### 2. Start Ollama (Required for LLM functionality)
```bash
# Stop any existing Ollama service
sudo systemctl stop ollama

# Start Ollama with Docker compatibility (listens on all interfaces)
nohup bash -c 'OLLAMA_HOST=0.0.0.0:11434 ollama serve' > ollama.log 2>&1 &

# Pull the required model
ollama pull llama3.2

# Verify Ollama is accessible
curl -s http://localhost:11434/api/tags
```

### 3. Start Docker Services
```bash
# Start the application and ChromaDB
docker compose up -d

# Verify services are running
docker compose ps
```

### 4. Process Content (Optional)
```bash
# Add Star Trek content to the vector database
make process-content

# Check database stats
curl -s http://localhost:8080/api/stats
```

### 5. Test the System
```bash
# Ask a Star Trek question
curl -X POST http://localhost:8080/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Who is Captain Kirk?", "num_results": 5}'
```

### 6. Shutdown (When Done)
```bash
# Stop Docker containers
docker compose down

# Stop Ollama processes
pkill ollama

# Verify everything is stopped
docker compose ps
ps aux | grep ollama
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

#### **Custom Folder Support**

The system supports processing content from custom folders and URLs from custom files:

```bash
# Process content from a custom folder
CONTENT_FOLDER=/path/to/your/content make process-content

# Process URLs from a custom file
URLS_FILE=/path/to/your/urls.txt make process-urls

# Process both with custom paths
CONTENT_FOLDER=/path/to/content URLS_FILE=/path/to/urls.txt make process-all
```

**Examples:**
```bash
# Process content from your documents folder
CONTENT_FOLDER=/home/user/star_trek_docs make process-content

# Process URLs from a different file
URLS_FILE=/home/user/my_urls.txt make process-urls
```

**Default Paths:**
- **Content Folder**: `$(PWD)/test_content` (your current test_content folder)
- **URLs File**: `$(PWD)/test_content/star_trek_urls.txt`

#### **Process New Content**

```bash
# Add your content files to test_content/
make process-content

# Or use a custom folder
CONTENT_FOLDER=/path/to/your/content make process-content
```

#### **Process HTML Files**
```bash
# Process HTML files in test_content/
make process-html

# Or use a custom folder
CONTENT_FOLDER=/path/to/your/html make process-html
```

#### **Process URLs from File**
```bash
# Process URLs listed in test_content/star_trek_urls.txt
make process-urls

# Or use a custom URLs file
URLS_FILE=/path/to/your/urls.txt make process-urls
```

#### **Process All Content Types**
```bash
# Process text, HTML, and URLs in one command
make process-all

# Or use custom paths for all
CONTENT_FOLDER=/path/to/content URLS_FILE=/path/to/urls.txt make process-all
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
```

- **RAG Application** (`startrek-rag/`): Flask API with service layer architecture
- **Content Loader** (`content_loader/`): Multi-format content processing (text, HTML, URLs)
- **Vector Database**: ChromaDB for similarity search
- **LLM Integration**: Ollama for local inference

For detailed architecture diagrams, see [📋 Architecture Documentation](docs/README.md).

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

## 📋 API Endpoints

All endpoints are under `/api/` prefix:

```bash
# Query the RAG system
curl -X POST http://localhost:8080/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Your question", "num_results": 5}'

# Health check
curl http://localhost:8080/api/health

# Get collection stats
curl http://localhost:8080/api/stats
```

## 📁 Content Processing

### Process Different Content Types
```bash
# Text files
make process-content

# HTML files
make process-html
```

### Local CI Testing
# All content types
```
make process-all
```

### Custom Content Paths
```bash
# Process content from custom folder
CONTENT_FOLDER=/path/to/your/content make process-content

# Process URLs from custom file
URLS_FILE=/path/to/your/urls.txt make process-urls
```

## 🧪 Testing

### Quick Development Testing
```bash
# Fast feedback loop
make test-quick

# Full CI simulation
make test-ci
```

### Individual Test Components
```bash
make test-format    # Code formatting
make test-lint      # Linting
make test-security  # Security scans
make test-docker    # Docker builds
make test-unit      # Unit tests
```

## 🐳 Docker Services

- **app**: Flask RAG application (port 8080)
- **chroma**: ChromaDB database (port 8000)
- **content-loader**: Content processing utilities

## 🔧 Configuration

### Environment Variables
```bash
# Database
CHROMA_HOST=localhost
CHROMA_PORT=8000
COLLECTION_NAME=startrek

# Ollama
OLLAMA_HOST=localhost
OLLAMA_PORT=11434
LLM_MODEL=llama3.2

# Application
FLASK_HOST=0.0.0.0
FLASK_PORT=8080
```

## 🐛 Troubleshooting

### Common Issues
1. **Ollama Connection**: Ensure `OLLAMA_HOST=0.0.0.0:11434 ollama serve`
2. **Port Conflicts**: Check ports 8080 and 8000 are available
3. **Content Processing**: Verify files exist in `test_content/`

### Debug Commands
```bash
# View logs
docker compose logs app

# Check service status
docker compose ps

# Restart services
docker compose restart
```

## 📚 Dependencies

- **ChromaDB**: Vector database
- **LangChain**: LLM orchestration
- **Flask**: Web framework
- **Ollama**: Local LLM inference
- **Docker**: Containerization

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Run tests: `make test-ci`
4. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

---

**Happy exploring the final frontier! 🖖** 