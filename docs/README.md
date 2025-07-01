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

The system architecture is documented through 14 comprehensive PlantUML diagrams:

### System Architecture
- **`system_overview_architecture.puml`** - High-level system architecture with color-coded components and external integrations

### Component & Interaction Diagrams
- **`component_interactions.puml`** - Component interaction patterns and dependencies
- **`component_interaction_flow.puml`** - Detailed interaction flows between components

### Data Flow Diagrams
- **`data_flow.puml`** - Data flow patterns and information exchange
- **`data_flow_architecture.puml`** - Comprehensive data flow architecture

### Deployment & Infrastructure
- **`deployment_architecture.puml`** - Docker container structure and service networking
- **`docker_deployment_architecture.puml`** - Detailed Docker deployment with volume mounts and port mappings

### API & Endpoints
- **`api_endpoints.puml`** - API endpoint overview and structure
- **`rest_api_endpoints.puml`** - Detailed REST API endpoints with request/response models

### Processing Workflows
- **`content_processing_flow.puml`** - Content ingestion and processing flow
- **`content_processing_workflow.puml`** - Comprehensive content processing workflow
- **`query_processing_flow.puml`** - RAG query processing steps
- **`query_processing_workflow.puml`** - Detailed query processing workflow

### Testing & Quality
- **`testing_architecture.puml`** - Test framework organization and CI/CD integration

## 🚀 Diagram Generation System

### Automated Generation
- **CI/CD Integration**: Diagrams are automatically generated on every PR and push
- **Required Check**: Diagram generation is a required CI check that blocks PRs if it fails
- **Artifact Upload**: Generated PNG files are uploaded as GitHub Actions artifacts
- **Parallel Execution**: Diagram generation runs in parallel with lint and security checks

### Local Generation
```bash
# Generate all diagrams
make diagrams-setup
make diagrams-generate

# Generate specific diagram
make diagrams-setup
java -jar docs/plantuml.jar -tpng -o ./images diagram_name.puml
```

### Generation Script Features
- **Error Detection**: Properly identifies and reports PlantUML syntax errors
- **Status Reporting**: Shows success/failure counts and detailed error messages
- **Clean Output**: Generates diagrams to `docs/images/` directory
- **Git Integration**: Generated images are gitignored (CI/CD only)

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

### Documentation & Diagrams
- **PlantUML** - Architecture diagram generation
- **Java 17** - PlantUML runtime
- **Graphviz** - Diagram rendering

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
- **Diagram Tests**: PlantUML syntax validation

### CI/CD Pipeline
1. **Code Quality**: Linting and formatting (parallel)
2. **Security**: Bandit and Safety scans (parallel)
3. **Architecture**: PlantUML diagram generation (parallel)
4. **Testing**: Unit and integration tests
5. **Coverage**: Code coverage reporting
6. **Build**: Docker image creation
7. **Deploy**: Container deployment

### Architecture Validation
- **Syntax Checking**: All PlantUML files must generate successfully
- **Required Check**: Diagram generation failure blocks PRs
- **Artifact Preservation**: Generated diagrams available for 30 days
- **Parallel Execution**: Diagram generation doesn't block other checks

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

### Diagram Development
```bash
# Generate diagrams locally
make diagrams-setup
make diagrams-generate

# Check diagram syntax
make diagrams-setup
java -jar docs/plantuml.jar -tpng -o ./images diagram_name.puml

# View generated diagrams
ls -la docs/images/*.png
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
2. **Test Generation**: Ensure diagrams generate successfully locally
3. **CI Validation**: Diagrams must pass CI/CD generation check
4. **Document Changes**: Update this README with new components
5. **Test Integration**: Ensure new components work with existing architecture
6. **Update Tests**: Add tests for new functionality

### Diagram Guidelines
- **Syntax Validation**: All .puml files must generate without errors
- **Naming Convention**: Use descriptive names for diagram files
- **Documentation**: Update this README when adding new diagrams
- **CI Integration**: New diagrams automatically included in CI checks

## 🔗 Related Documentation

- [Main README](../README.md) - Project overview, setup, and usage
- [API Documentation](../startrek-rag/routes/api.py) - Detailed API specifications
- [Configuration Guide](../config/) - Environment and configuration management
- [Testing Guide](../tests/) - Test suite documentation

## 📄 License

This documentation is part of the Star Trek RAG system and follows the same license as the main project. 