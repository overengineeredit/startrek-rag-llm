# Star Trek RAG System - Architecture Documentation

This directory contains comprehensive PlantUML diagrams documenting the architecture of the Star Trek Retrieval-Augmented Generation (RAG) system.

## 📋 Overview

The Star Trek RAG system is a containerized application that combines:
- **ChromaDB** for vector storage and similarity search
- **Ollama** for local LLM inference
- **Flask** for the web API
- **LangChain** for RAG orchestration
- **Docker Compose** for deployment

## 🏗️ Architecture Diagrams

### 1. System Overview
**File**: `architecture.puml` (first diagram)
- High-level system architecture
- Component relationships and dependencies
- External service integrations

### 2. Component Interactions
**File**: `architecture.puml` (second diagram)
- Detailed interaction flows between components
- API request/response patterns
- Service communication protocols

### 3. Data Flow Architecture
**File**: `architecture.puml` (third diagram)
- Content ingestion pipeline
- Vector database storage structure
- Query processing flow

### 4. Deployment Architecture
**File**: `architecture.puml` (fourth diagram)
- Docker container structure
- Service networking
- Volume mounts and port mappings

### 5. API Endpoints
**File**: `architecture.puml` (fifth diagram)
- REST API endpoint definitions
- Request/response models
- Data structures

### 6. Content Processing Flow
**File**: `architecture.puml` (sixth diagram)
- Step-by-step content ingestion process
- Text, HTML, and URL processing
- Error handling and validation

### 7. Query Processing Flow
**File**: `architecture.puml` (seventh diagram)
- RAG query processing steps
- Document retrieval and context assembly
- LLM response generation

### 8. Testing Architecture
**File**: `architecture.puml` (eighth diagram)
- Test framework organization
- CI/CD pipeline integration
- Coverage and security testing

## 🚀 Key Components

### Core Services
- **Flask Web App**: Main application server
- **RAG Service**: Orchestrates retrieval and generation
- **Embedding Service**: Handles vector generation
- **ChromaDB**: Vector database for similarity search
- **Ollama**: Local LLM for text generation

### Content Processing
- **Enhanced Processor**: Multi-format content ingestion
- **HTML Processor**: Web page parsing and extraction
- **Content Loader**: Batch processing utilities

### API Endpoints
- `GET /` - API information
- `POST /api/query` - RAG queries
- `POST /api/add` - Document addition
- `POST /api/embed` - Embedding generation
- `GET /api/stats` - Collection statistics
- `GET /api/health` - System health check

## 🔧 Technology Stack

### Backend
- **Python 3.11**
- **Flask** - Web framework
- **LangChain** - RAG orchestration
- **ChromaDB** - Vector database
- **Ollama** - Local LLM

### Content Processing
- **BeautifulSoup** - HTML parsing
- **Unstructured** - Document processing
- **Requests** - HTTP client

### Testing & Quality
- **pytest** - Testing framework
- **pytest-cov** - Coverage reporting
- **bandit** - Security scanning
- **safety** - Dependency checking

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Orchestration
- **GitHub Actions** - CI/CD
- **Codecov** - Coverage reporting

## 📊 Data Flow

### Content Ingestion
1. **Source Selection**: Text files, HTML files, or URLs
2. **Processing**: Parse, extract, and chunk content
3. **Embedding**: Generate vector representations
4. **Storage**: Store in ChromaDB with metadata

### Query Processing
1. **Query Input**: User question
2. **Retrieval**: Find relevant documents in ChromaDB
3. **Context Assembly**: Combine retrieved documents
4. **Generation**: Use LLM to generate answer
5. **Response**: Return formatted answer

## 🐳 Deployment

### Docker Services
- **app**: Flask application (port 8080)
- **chroma**: ChromaDB database (port 8000)
- **content-loader**: Content processing utilities

### External Dependencies
- **Ollama**: Must be running locally with Star Trek model
- **Network**: Services communicate via Docker network

## 🧪 Testing Strategy

### Test Types
- **Unit Tests**: Individual component testing
- **Integration Tests**: Service interaction testing
- **API Tests**: Endpoint functionality testing
- **Security Tests**: Vulnerability scanning
- **Docker Tests**: Container build verification

### CI/CD Pipeline
1. **Code Quality**: Linting and formatting
2. **Security**: Bandit and Safety scans
3. **Testing**: Unit and integration tests
4. **Coverage**: Code coverage reporting
5. **Build**: Docker image creation
6. **Deploy**: Container deployment

## 📈 Monitoring & Observability

### Health Checks
- Database connectivity
- Ollama service availability
- Collection statistics
- System status reporting

### Logging
- Structured logging with timestamps
- Debug information for troubleshooting
- Error tracking and reporting
- Performance metrics

## 🔒 Security Considerations

### Input Validation
- Request schema validation
- File upload restrictions
- SQL injection prevention
- XSS protection

### Access Control
- API rate limiting
- Input sanitization
- Error message sanitization
- Secure configuration management

## 📚 Usage Examples

### Content Processing
```bash
# Process text files
make process-content

# Process HTML files
make process-html

# Process URLs
make process-urls

# Process all content types
make process-all
```

### API Usage
```bash
# Query the system
curl -X POST http://localhost:8080/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Who is Captain Kirk?", "num_results": 5}'

# Check system health
curl http://localhost:8080/api/health

# Get collection stats
curl http://localhost:8080/api/stats
```

## 🛠️ Development

### Local Setup
```bash
# Clone repository
git clone <repository-url>
cd startrek-rag-llm

# Setup environment
make setup

# Start services
docker-compose up -d

# Run tests
make test-ci
```

### Custom Content Processing
```bash
# Process custom content folder
CONTENT_FOLDER=/path/to/content make process-content

# Process custom URLs file
URLS_FILE=/path/to/urls.txt make process-urls
```

## 📝 Contributing

When contributing to the architecture:

1. **Update Diagrams**: Modify PlantUML files to reflect changes
2. **Document Changes**: Update this README with new components
3. **Test Integration**: Ensure new components work with existing architecture
4. **Update Tests**: Add tests for new functionality

## 🔗 Related Documentation

- [Main README](../README.md) - Project overview and setup
- [API Documentation](../startrek-rag/routes/api.py) - Detailed API specifications
- [Configuration Guide](../config/) - Environment and configuration management
- [Testing Guide](../tests/) - Test suite documentation

## 📄 License

This documentation is part of the Star Trek RAG system and follows the same license as the main project. 