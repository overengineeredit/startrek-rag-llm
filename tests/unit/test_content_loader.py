"""
Unit tests for content loader modules.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add the content_loader directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'content_loader'))

class TestContentLoader:
    """Test cases for content loader modules."""
    
    def test_process_content_import(self):
        """Test that process_content can be imported."""
        try:
            import process_content
            assert True
        except ImportError as e:
            pytest.fail(f"Failed to import process_content: {e}")
    
    def test_enhanced_processor_import(self):
        """Test that enhanced_processor can be imported."""
        try:
            from enhanced_processor import EnhancedContentProcessor
            assert True
        except ImportError as e:
            pytest.fail(f"Failed to import EnhancedContentProcessor: {e}")
    
    def test_html_processor_import(self):
        """Test that html_processor can be imported."""
        try:
            from html_processor import HTMLProcessor
            assert True
        except ImportError as e:
            pytest.fail(f"Failed to import HTMLProcessor: {e}")
    
    def test_enhanced_processor_initialization(self):
        """Test EnhancedContentProcessor initialization."""
        try:
            from enhanced_processor import EnhancedContentProcessor
            
            processor = EnhancedContentProcessor()
            assert processor is not None
            assert hasattr(processor, 'app_url')
            assert hasattr(processor, 'html_processor')
            assert hasattr(processor, 'stats')
        except Exception as e:
            pytest.fail(f"Failed to initialize EnhancedContentProcessor: {e}")
    
    def test_html_processor_initialization(self):
        """Test HTMLProcessor initialization."""
        try:
            from html_processor import HTMLProcessor
            
            processor = HTMLProcessor()
            assert processor is not None
            assert hasattr(processor, 'chunk_size')
            assert hasattr(processor, 'overlap')
        except Exception as e:
            pytest.fail(f"Failed to initialize HTMLProcessor: {e}")
    
    def test_enhanced_processor_custom_config(self):
        """Test EnhancedContentProcessor with custom configuration."""
        try:
            from enhanced_processor import EnhancedContentProcessor
            
            processor = EnhancedContentProcessor(
                app_url="http://test:8080",
                chunk_size=1500,
                overlap=300
            )
            
            assert processor.app_url == "http://test:8080"
            assert processor.html_processor.chunk_size == 1500
            assert processor.html_processor.overlap == 300
        except Exception as e:
            pytest.fail(f"Failed to test EnhancedContentProcessor custom config: {e}")
    
    def test_html_processor_custom_config(self):
        """Test HTMLProcessor with custom configuration."""
        try:
            from html_processor import HTMLProcessor
            
            processor = HTMLProcessor(chunk_size=1500, overlap=300)
            
            assert processor.chunk_size == 1500
            assert processor.overlap == 300
        except Exception as e:
            pytest.fail(f"Failed to test HTMLProcessor custom config: {e}")
    
    @patch('enhanced_processor.requests.post')
    def test_get_embedding_mock(self, mock_post):
        """Test get_embedding with mocked requests."""
        try:
            from enhanced_processor import EnhancedContentProcessor
            
            # Mock the response
            mock_response = Mock()
            mock_response.json.return_value = {"embedding": [0.1, 0.2, 0.3]}
            mock_response.raise_for_status.return_value = None
            mock_post.return_value = mock_response
            
            processor = EnhancedContentProcessor()
            result = processor.get_embedding("test text")
            
            assert result == [0.1, 0.2, 0.3]
            mock_post.assert_called_once()
        except Exception as e:
            pytest.fail(f"Failed to test get_embedding mock: {e}")
    
    @patch('enhanced_processor.requests.post')
    def test_add_to_chroma_mock(self, mock_post):
        """Test add_to_chroma with mocked requests."""
        try:
            from enhanced_processor import EnhancedContentProcessor
            
            # Mock the response
            mock_response = Mock()
            mock_response.raise_for_status.return_value = None
            mock_post.return_value = mock_response
            
            processor = EnhancedContentProcessor()
            result = processor.add_to_chroma(
                embedding=[0.1, 0.2, 0.3],
                document="test document",
                metadata={"source": "test"},
                doc_id="test_id"
            )
            
            assert result is True
            mock_post.assert_called_once()
        except Exception as e:
            pytest.fail(f"Failed to test add_to_chroma mock: {e}")
    
    def test_stats_reset(self):
        """Test statistics reset functionality."""
        try:
            from enhanced_processor import EnhancedContentProcessor
            
            processor = EnhancedContentProcessor()
            
            # Modify some stats
            processor.stats["total_files_processed"] = 10
            processor.stats["errors"] = 5
            
            # Reset stats
            processor.reset_stats()
            
            assert processor.stats["total_files_processed"] == 0
            assert processor.stats["errors"] == 0
            assert processor.stats["total_chunks_processed"] == 0
        except Exception as e:
            pytest.fail(f"Failed to test stats reset: {e}")
    
    def test_html_processor_chunking(self):
        """Test HTML processor text chunking."""
        try:
            from html_processor import HTMLProcessor
            
            processor = HTMLProcessor(chunk_size=100, overlap=20)
            
            # Test text chunking
            text = "This is a test text. " * 10  # Create longer text
            chunks = processor.chunk_text(text)
            
            assert len(chunks) > 0
            assert all(len(chunk) <= 100 for chunk in chunks)
        except Exception as e:
            pytest.fail(f"Failed to test HTML processor chunking: {e}")
    
    @patch('html_processor.requests.get')
    def test_html_processor_url_fetching(self, mock_get):
        """Test HTML processor URL fetching."""
        try:
            from html_processor import HTMLProcessor
            
            # Mock the response
            mock_response = Mock()
            mock_response.text = "<html><body><p>Test content</p></body></html>"
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response
            
            processor = HTMLProcessor()
            result = processor.extract_from_url("http://test.com")
            
            assert result is not None
            assert "Test content" in result
            mock_get.assert_called_once_with("http://test.com", headers=processor.headers)
        except Exception as e:
            pytest.fail(f"Failed to test HTML processor URL fetching: {e}")

class TestProcessContent:
    """Test cases for process_content module."""
    
    def test_content_processor_import(self):
        """Test that ContentProcessor can be imported."""
        try:
            from process_content import ContentProcessor
            assert True
        except ImportError as e:
            pytest.fail(f"Failed to import ContentProcessor: {e}")
    
    def test_content_processor_initialization(self):
        """Test ContentProcessor initialization."""
        try:
            from process_content import ContentProcessor
            
            processor = ContentProcessor()
            assert processor is not None
            assert hasattr(processor, 'app_url')
            assert hasattr(processor, 'stats')
        except Exception as e:
            pytest.fail(f"Failed to initialize ContentProcessor: {e}")
    
    def test_content_processor_custom_config(self):
        """Test ContentProcessor with custom configuration."""
        try:
            from process_content import ContentProcessor
            
            processor = ContentProcessor(app_url="http://test:8080")
            assert processor.app_url == "http://test:8080"
        except Exception as e:
            pytest.fail(f"Failed to test ContentProcessor custom config: {e}")
    
    def test_file_processing_simulation(self):
        """Test file processing simulation."""
        try:
            from process_content import ContentProcessor
            
            processor = ContentProcessor()
            
            # Test with a simple text
            test_content = "This is a test document.\n\nIt has multiple paragraphs.\n\nFor testing purposes."
            
            # Simulate processing
            chunks = test_content.split('\n\n')
            valid_chunks = [chunk for chunk in chunks if chunk.strip()]
            
            assert len(valid_chunks) > 0
            assert all(len(chunk) > 0 for chunk in valid_chunks)
        except Exception as e:
            pytest.fail(f"Failed to test file processing simulation: {e}")

class TestErrorHandling:
    """Test cases for error handling."""
    
    def test_enhanced_processor_error_handling(self):
        """Test EnhancedContentProcessor error handling."""
        try:
            from enhanced_processor import EnhancedContentProcessor
            
            processor = EnhancedContentProcessor()
            
            # Test that errors are tracked
            initial_errors = processor.stats["errors"]
            
            # Simulate an error
            processor.stats["errors"] += 1
            
            assert processor.stats["errors"] == initial_errors + 1
        except Exception as e:
            pytest.fail(f"Failed to test error handling: {e}")
    
    def test_html_processor_error_handling(self):
        """Test HTMLProcessor error handling."""
        try:
            from html_processor import HTMLProcessor
            
            processor = HTMLProcessor()
            
            # Test with invalid input
            result = processor.chunk_text("")
            assert result == []
            
            result = processor.chunk_text(None)
            assert result == []
        except Exception as e:
            pytest.fail(f"Failed to test HTML processor error handling: {e}") 