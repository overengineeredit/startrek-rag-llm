# Star Trek RAG LLM System

A complete Retrieval-Augmented Generation (RAG) system built with ChromaDB, LangChain, and Ollama, designed to answer questions about Star Trek content using vector embeddings and large language models.

## 🚀 Features

- **Vector Database**: ChromaDB for efficient similarity search
- **Content Processing**: Automated text chunking and embedding generation
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

#### Process New Content
```bash
# Add your content files to test_content/
make process-content
```

#### Manual Content Processing
```bash
docker compose run --rm \
  -v $(PWD)/content_loader:/app \
  -v $(PWD)/test_content:/app/content \
  app python /app/process_content.py /app/content
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
│   ├── process_content.py   # Content processing script
│   ├── requirements.txt     # Dependencies
│   └── Dockerfile          # Container configuration
├── test_content/            # Sample content for testing
│   └── startrek_original_series.txt
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