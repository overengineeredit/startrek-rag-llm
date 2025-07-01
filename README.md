# Star Trek RAG LLM System

[![codecov](https://codecov.io/gh/overengineeredit/startrek-rag-llm/branch/main/graph/badge.svg)](https://codecov.io/gh/overengineeredit/startrek-rag-llm)

A Retrieval-Augmented Generation (RAG) system built with ChromaDB, LangChain, and Ollama for answering Star Trek questions using vector embeddings and large language models.

## 🚀 Quick Start

### Prerequisites
- **Docker & Docker Compose**
- **Ollama** (for LLM functionality)

### Setup & Run
```bash
# 1. Clone and start services
git clone <your-repo-url>
cd startrek-rag-llm
docker compose up -d

# 2. Start Ollama with Docker compatibility
OLLAMA_HOST=0.0.0.0:11434 ollama serve

# 3. Pull the required model
ollama pull llama3.2

# 4. Process Star Trek content
make process-content

# 5. Test the system
curl -X POST http://localhost:8080/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Who is Captain Kirk?", "num_results": 5}'
```

## 🏗️ Architecture

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

# URLs from file
make process-urls

# All content types
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