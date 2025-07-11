import pytest
import sys
import os
from unittest.mock import patch, MagicMock

def test_rag_imports():
    """Test that RAG modules can be imported"""
    try:
        # Add the startrek-rag directory to the path
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'startrek-rag'))
        
        # Mock ChromaDB to avoid connection issues
        with patch('chromadb.Client'):
            # Test imports
            from config import Config
            from app import create_app
            from embed import get_embedding
            from services.rag_service import RAGService
            
            assert True
    except ImportError as e:
        pytest.fail(f"Failed to import RAG modules: {e}")

def test_content_loader_imports():
    """Test that content loader modules can be imported"""
    try:
        # Add the content_loader directory to the path
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'content_loader'))
        
        # Test imports
        import process_content
        from enhanced_processor import EnhancedContentProcessor
        from html_processor import HTMLProcessor
        
        assert True
    except ImportError as e:
        pytest.fail(f"Failed to import content loader modules: {e}")

def test_config_creation():
    """Test Config class creation"""
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'startrek-rag'))
        from config import Config
        
        config = Config()
        assert config is not None
        assert hasattr(config, 'chroma_url')
        assert hasattr(config.database, 'collection_name')
    except Exception as e:
        pytest.fail(f"Failed to create Config: {e}")

def test_html_processor_creation():
    """Test HTMLProcessor creation"""
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'content_loader'))
        from html_processor import HTMLProcessor
        
        processor = HTMLProcessor()
        assert processor is not None
        assert hasattr(processor, 'chunk_size')
        assert hasattr(processor, 'overlap')
    except Exception as e:
        pytest.fail(f"Failed to create HTMLProcessor: {e}")

def test_enhanced_processor_creation():
    """Test EnhancedContentProcessor creation"""
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'content_loader'))
        from enhanced_processor import EnhancedContentProcessor
        
        processor = EnhancedContentProcessor()
        assert processor is not None
        assert hasattr(processor, 'app_url')
        assert hasattr(processor, 'chunk_size')
    except Exception as e:
        pytest.fail(f"Failed to create EnhancedContentProcessor: {e}")

def test_app_creation_with_mock():
    """Test app creation with mocked dependencies"""
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'startrek-rag'))
        
        # Mock all ChromaDB dependencies
        with patch('chromadb.Client'), \
             patch('chromadb.PersistentClient'), \
             patch('services.rag_service.RAGService'):
            
            from app import create_app
            app = create_app()
            assert app is not None
            assert app.name == 'app'
    except Exception as e:
        pytest.fail(f"Failed to create app with mocks: {e}")
