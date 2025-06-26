"""
Integration tests for API endpoints.
"""

import pytest
import requests
import time
import subprocess
import sys
import os

class TestAPIIntegration:
    """Integration tests for API endpoints."""
    
    @pytest.fixture(scope="class")
    def app_server(self):
        """Start the Flask app server for testing."""
        # This would start the actual server in a real integration test
        # For now, we'll just test the endpoints if they're available
        pass
    
    def test_health_endpoint(self):
        """Test the health endpoint."""
        try:
            response = requests.get("http://localhost:8080/api/health", timeout=5)
            assert response.status_code == 200
            data = response.json()
            assert "status" in data
            assert data["status"] == "healthy"
        except requests.exceptions.ConnectionError:
            pytest.skip("Server not running - skipping integration test")
        except Exception as e:
            pytest.fail(f"Health endpoint test failed: {e}")
    
    def test_stats_endpoint(self):
        """Test the stats endpoint."""
        try:
            response = requests.get("http://localhost:8080/api/stats", timeout=5)
            assert response.status_code == 200
            data = response.json()
            assert "count" in data
            assert isinstance(data["count"], int)
        except requests.exceptions.ConnectionError:
            pytest.skip("Server not running - skipping integration test")
        except Exception as e:
            pytest.fail(f"Stats endpoint test failed: {e}")
    
    def test_root_endpoint(self):
        """Test the root endpoint."""
        try:
            response = requests.get("http://localhost:8080/", timeout=5)
            assert response.status_code == 200
            # Should return some HTML or JSON
            assert len(response.text) > 0
        except requests.exceptions.ConnectionError:
            pytest.skip("Server not running - skipping integration test")
        except Exception as e:
            pytest.fail(f"Root endpoint test failed: {e}")
    
    def test_embed_endpoint(self):
        """Test the embed endpoint."""
        try:
            test_text = "Star Trek is a science fiction franchise"
            response = requests.post(
                "http://localhost:8080/api/embed",
                json={"text": test_text},
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            assert response.status_code == 200
            data = response.json()
            assert "embedding" in data
            assert isinstance(data["embedding"], list)
            assert len(data["embedding"]) > 0
        except requests.exceptions.ConnectionError:
            pytest.skip("Server not running - skipping integration test")
        except Exception as e:
            pytest.fail(f"Embed endpoint test failed: {e}")
    
    def test_add_endpoint(self):
        """Test the add endpoint."""
        try:
            test_document = "This is a test document for integration testing."
            test_metadata = {"source": "integration_test", "test": True}
            test_id = "test_integration_001"
            
            # First get an embedding
            embed_response = requests.post(
                "http://localhost:8080/api/embed",
                json={"text": test_document},
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if embed_response.status_code == 200:
                embedding = embed_response.json()["embedding"]
                
                # Then add to ChromaDB
                add_response = requests.post(
                    "http://localhost:8080/api/add",
                    json={
                        "embedding": embedding,
                        "document": test_document,
                        "metadata": test_metadata,
                        "id": test_id
                    },
                    headers={"Content-Type": "application/json"},
                    timeout=10
                )
                
                assert add_response.status_code == 200
                data = add_response.json()
                assert "success" in data
                assert data["success"] is True
        except requests.exceptions.ConnectionError:
            pytest.skip("Server not running - skipping integration test")
        except Exception as e:
            pytest.fail(f"Add endpoint test failed: {e}")
    
    def test_query_endpoint(self):
        """Test the query endpoint."""
        try:
            test_query = "What is Star Trek?"
            response = requests.post(
                "http://localhost:8080/api/query",
                json={"query": test_query, "num_results": 3},
                headers={"Content-Type": "application/json"},
                timeout=15
            )
            assert response.status_code == 200
            data = response.json()
            assert "results" in data
            assert isinstance(data["results"], list)
        except requests.exceptions.ConnectionError:
            pytest.skip("Server not running - skipping integration test")
        except Exception as e:
            pytest.fail(f"Query endpoint test failed: {e}")

class TestDockerIntegration:
    """Integration tests for Docker services."""
    
    def test_docker_compose_services(self):
        """Test that Docker Compose services can be started."""
        try:
            # Check if docker compose is available
            result = subprocess.run(
                ["docker", "compose", "config"],
                capture_output=True,
                text=True,
                timeout=30
            )
            assert result.returncode == 0
            assert "services:" in result.stdout
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pytest.skip("Docker Compose not available - skipping test")
        except Exception as e:
            pytest.fail(f"Docker Compose test failed: {e}")
    
    def test_chroma_service_health(self):
        """Test ChromaDB service health."""
        try:
            response = requests.get("http://localhost:8000/api/v1/heartbeat", timeout=5)
            assert response.status_code == 200
        except requests.exceptions.ConnectionError:
            pytest.skip("ChromaDB not running - skipping test")
        except Exception as e:
            pytest.fail(f"ChromaDB health check failed: {e}")

class TestContentProcessingIntegration:
    """Integration tests for content processing."""
    
    def test_content_processing_script(self):
        """Test that content processing script can be run."""
        try:
            # Test if the script can be imported and has the right structure
            content_loader_path = os.path.join(os.path.dirname(__file__), '..', '..', 'content_loader')
            sys.path.insert(0, content_loader_path)
            
            # Try to import the modules
            import process_content
            from enhanced_processor import EnhancedContentProcessor
            from html_processor import HTMLProcessor
            
            assert hasattr(process_content, 'ContentProcessor')
            assert hasattr(EnhancedContentProcessor, '__init__')
            assert hasattr(HTMLProcessor, '__init__')
            
        except ImportError as e:
            pytest.skip(f"Content processing modules not available: {e}")
        except Exception as e:
            pytest.fail(f"Content processing test failed: {e}")
    
    def test_makefile_commands(self):
        """Test that Makefile commands are available."""
        try:
            # Check if Makefile exists and has expected targets
            makefile_path = os.path.join(os.path.dirname(__file__), '..', '..', 'Makefile')
            assert os.path.exists(makefile_path)
            
            # Read Makefile and check for expected targets
            with open(makefile_path, 'r') as f:
                content = f.read()
                
            expected_targets = [
                'process-content',
                'process-html', 
                'process-urls',
                'process-all',
                'help'
            ]
            
            for target in expected_targets:
                assert target in content, f"Makefile target '{target}' not found"
                
        except Exception as e:
            pytest.fail(f"Makefile test failed: {e}")

class TestErrorHandlingIntegration:
    """Integration tests for error handling."""
    
    def test_invalid_json_handling(self):
        """Test handling of invalid JSON requests."""
        try:
            response = requests.post(
                "http://localhost:8080/api/embed",
                data="invalid json",
                headers={"Content-Type": "application/json"},
                timeout=5
            )
            # Should return 400 Bad Request
            assert response.status_code == 400
        except requests.exceptions.ConnectionError:
            pytest.skip("Server not running - skipping integration test")
        except Exception as e:
            pytest.fail(f"Invalid JSON test failed: {e}")
    
    def test_missing_fields_handling(self):
        """Test handling of requests with missing required fields."""
        try:
            response = requests.post(
                "http://localhost:8080/api/embed",
                json={},  # Missing 'text' field
                headers={"Content-Type": "application/json"},
                timeout=5
            )
            # Should return 400 Bad Request
            assert response.status_code == 400
        except requests.exceptions.ConnectionError:
            pytest.skip("Server not running - skipping integration test")
        except Exception as e:
            pytest.fail(f"Missing fields test failed: {e}")
    
    def test_large_text_handling(self):
        """Test handling of very large text inputs."""
        try:
            large_text = "A" * 10000  # 10KB of text
            response = requests.post(
                "http://localhost:8080/api/embed",
                json={"text": large_text},
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            # Should handle large text gracefully
            assert response.status_code in [200, 413]  # 200 OK or 413 Payload Too Large
        except requests.exceptions.ConnectionError:
            pytest.skip("Server not running - skipping integration test")
        except Exception as e:
            pytest.fail(f"Large text test failed: {e}") 