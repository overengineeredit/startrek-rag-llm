"""
Unit tests for RAG service module.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add the startrek-rag directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'startrek-rag'))

class TestRAGService:
    """Test cases for RAGService class."""
    
    def test_rag_service_import(self):
        """Test that RAG service can be imported."""
        try:
            from services.rag_service import RAGService
            assert True
        except ImportError as e:
            pytest.fail(f"Failed to import RAGService: {e}")
    
    def test_rag_service_initialization(self):
        """Test RAGService initialization."""
        try:
            from services.rag_service import RAGService
            from config import Config
            
            config = Config()
            rag_service = RAGService(config)
            assert rag_service is not None
            assert hasattr(rag_service, 'config')
        except Exception as e:
            pytest.fail(f"Failed to initialize RAGService: {e}")
    
    @patch('services.rag_service.ChromaClient')
    def test_rag_service_with_mock_chroma(self, mock_chroma):
        """Test RAGService with mocked ChromaDB client."""
        try:
            from services.rag_service import RAGService
            from config import Config
            
            # Mock ChromaDB client
            mock_client = Mock()
            mock_collection = Mock()
            mock_client.get_collection.return_value = mock_collection
            mock_chroma.return_value = mock_client
            
            config = Config()
            rag_service = RAGService(config)
            
            assert rag_service is not None
            assert hasattr(rag_service, 'collection')
        except Exception as e:
            pytest.fail(f"Failed to test RAGService with mock: {e}")
    
    def test_config_import(self):
        """Test that config can be imported."""
        try:
            from config import Config
            config = Config()
            assert config is not None
            assert hasattr(config, 'chroma_host')
            assert hasattr(config, 'chroma_port')
            assert hasattr(config, 'collection_name')
        except ImportError as e:
            pytest.fail(f"Failed to import Config: {e}")
    
    def test_app_import(self):
        """Test that app can be imported."""
        try:
            from app import create_app
            app = create_app()
            assert app is not None
            assert hasattr(app, 'config')
        except ImportError as e:
            pytest.fail(f"Failed to import create_app: {e}")
    
    def test_embed_import(self):
        """Test that embed module can be imported."""
        try:
            from embed import get_embedding
            assert callable(get_embedding)
        except ImportError as e:
            pytest.fail(f"Failed to import get_embedding: {e}")
    
    @patch('services.rag_service.get_embedding')
    def test_get_embedding_function(self, mock_get_embedding):
        """Test the get_embedding function."""
        try:
            from embed import get_embedding
            
            # Mock the embedding function
            mock_embedding = [0.1, 0.2, 0.3, 0.4, 0.5]
            mock_get_embedding.return_value = mock_embedding
            
            result = get_embedding("test text")
            assert result == mock_embedding
            mock_get_embedding.assert_called_once_with("test text")
        except Exception as e:
            pytest.fail(f"Failed to test get_embedding: {e}")
    
    def test_db_config_import(self):
        """Test that db_config can be imported."""
        try:
            from db_config import get_chroma_client
            assert callable(get_chroma_client)
        except ImportError as e:
            pytest.fail(f"Failed to import get_chroma_client: {e}")
    
    def test_routes_import(self):
        """Test that routes can be imported."""
        try:
            from routes.api import api_bp
            assert api_bp is not None
        except ImportError as e:
            pytest.fail(f"Failed to import api_bp: {e}")

class TestConfig:
    """Test cases for Config class."""
    
    def test_config_defaults(self):
        """Test Config class default values."""
        try:
            from config import Config
            
            config = Config()
            
            # Test default values
            assert config.chroma_host == 'localhost'
            assert config.chroma_port == 8000
            assert config.collection_name == 'startrek'
            assert config.ollama_host == 'localhost'
            assert config.ollama_port == 11434
            assert config.llm_model == 'llama3.2'
        except Exception as e:
            pytest.fail(f"Failed to test Config defaults: {e}")
    
    def test_config_environment_override(self):
        """Test Config class environment variable override."""
        try:
            from config import Config
            
            # Test with environment variables
            with patch.dict(os.environ, {
                'CHROMA_HOST': 'test-host',
                'CHROMA_PORT': '9000',
                'COLLECTION_NAME': 'test-collection'
            }):
                config = Config()
                assert config.chroma_host == 'test-host'
                assert config.chroma_port == 9000
                assert config.collection_name == 'test-collection'
        except Exception as e:
            pytest.fail(f"Failed to test Config environment override: {e}")

class TestApp:
    """Test cases for Flask application."""
    
    def test_app_creation(self):
        """Test Flask app creation."""
        try:
            from app import create_app
            
            app = create_app()
            assert app is not None
            assert app.name == 'startrek_rag'
        except Exception as e:
            pytest.fail(f"Failed to test app creation: {e}")
    
    def test_app_config(self):
        """Test Flask app configuration."""
        try:
            from app import create_app
            
            app = create_app()
            
            # Test that app has expected configuration
            assert 'TESTING' in app.config
            assert 'DEBUG' in app.config
        except Exception as e:
            pytest.fail(f"Failed to test app config: {e}")
    
    def test_blueprint_registration(self):
        """Test that blueprints are registered."""
        try:
            from app import create_app
            
            app = create_app()
            
            # Check if API blueprint is registered
            assert 'api' in app.blueprints
        except Exception as e:
            pytest.fail(f"Failed to test blueprint registration: {e}") 