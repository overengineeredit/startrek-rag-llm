import logging

from config import config
from flask import Blueprint, jsonify, request
from marshmallow import Schema, fields
from services.rag_service import rag_service

logger = logging.getLogger(__name__)

# Create Blueprint for API routes
api_bp = Blueprint("api", __name__, url_prefix="/api")


# Create custom exception classes
class RAGServiceError(Exception):
    pass


class ValidationError(Exception):
    pass


# Add request validation
class QuerySchema(Schema):
    query = fields.Str(required=True)
    num_results = fields.Int(load_default=5, validate=lambda x: 1 <= x <= 20)


@api_bp.route("/query", methods=["POST"])
def query():
    """Handle RAG queries."""
    logger.debug("Received query request")
    try:
        data = request.get_json()
        logger.debug(f"Query data: {data}")

        if not data or "query" not in data:
            logger.error("No query in request data")
            return jsonify({"error": "No query provided"}), 400

        query_text = data.get("query")
        num_results = data.get("num_results", 5)

        logger.info(f"Processing query: {query_text}")

        response = rag_service.query(query_text, num_results)
        logger.debug(f"Query response: {response}")

        if response:
            logger.info("Query processed successfully")
            return jsonify({"message": response}), 200
        else:
            logger.error("Query returned no response")
            return jsonify({"error": "No response generated"}), 400

    except Exception as e:
        logger.exception("Error processing query")
        return jsonify({"error": f"Query error: {str(e)}"}), 500


@api_bp.route("/add", methods=["POST"])
def add_document():
    """Add a document to the vector database."""
    logger.debug("Received add document request")
    if not request.is_json:
        logger.error("Request is not JSON")
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    logger.debug(f"Add request data: {data}")

    required_fields = ["document", "metadata", "id"]
    if not all(field in data for field in required_fields):
        logger.error("Missing required fields in add request")
        return (
            jsonify(
                {"error": f"Missing required fields: {', '.join(required_fields)}"}
            ),
            400,
        )

    try:
        success = rag_service.add_document(
            document=data["document"], metadata=data["metadata"], doc_id=data["id"]
        )

        if success:
            logger.info("Document added to ChromaDB successfully")
            return jsonify({"message": "Document added to ChromaDB successfully"}), 200
        else:
            logger.error("Failed to add document to ChromaDB")
            return jsonify({"error": "Failed to add document"}), 500

    except Exception as e:
        logger.exception("Error adding document to ChromaDB")
        return jsonify({"error": f"Add error: {str(e)}"}), 500


@api_bp.route("/stats", methods=["GET"])
def get_stats():
    """Get collection statistics."""
    logger.debug("Received stats request")
    try:
        stats = rag_service.get_collection_stats()
        return jsonify(stats), 200
    except Exception as e:
        logger.exception("Error getting stats")
        return jsonify({"error": f"Stats error: {str(e)}"}), 500


@api_bp.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint to verify system status."""
    logger.debug("Received health check request")
    try:
        import requests

        # Check database connection
        stats = rag_service.get_collection_stats()
        if "error" in stats:
            raise Exception(f"Database error: {stats['error']}")

        # Check if Ollama is accessible
        ollama_url = f"{config.ollama_url}/api/tags"
        ollama_response = requests.get(ollama_url, timeout=5)

        if ollama_response.status_code == 200:
            logger.info("Health check passed - all systems operational")
            return (
                jsonify(
                    {
                        "status": "healthy",
                        "database": "connected",
                        "ollama": "accessible",
                        "model": config.ollama.model,
                        "collection_stats": stats,
                    }
                ),
                200,
            )
        else:
            logger.warning("Health check failed - Ollama not accessible")
            return (
                jsonify(
                    {
                        "status": "degraded",
                        "database": "connected",
                        "ollama": "not accessible",
                        "error": "Ollama service not responding",
                        "collection_stats": stats,
                    }
                ),
                503,
            )

    except Exception as e:
        logger.exception("Health check failed")
        return jsonify({"status": "unhealthy", "error": str(e)}), 500


@api_bp.route("/embed", methods=["POST"])
def embed():
    """Handle embedding requests."""
    logger.debug("Received embed request")
    logger.debug(f"Request headers: {dict(request.headers)}")
    logger.debug(f"Request data: {request.data}")
    logger.debug(f"Content-Type: {request.content_type}")
    logger.debug(f"Is JSON: {request.is_json}")

    # Check if this is a file upload or direct text
    if request.is_json or request.content_type == "application/json":
        data = request.get_json()
        logger.debug(f"Parsed JSON data: {data}")
        if "text" not in data:
            logger.error("No text in request data")
            return jsonify({"error": "No text provided"}), 400

        try:
            from embed import get_embedding

            embedding = get_embedding(data["text"])
            logger.info("Text embedded successfully")
            return jsonify({"embedding": embedding}), 200
        except Exception as e:
            logger.exception("Error during text embedding")
            return jsonify({"error": f"Embedding error: {str(e)}"}), 500
    else:
        # Handle file upload
        if "file" not in request.files:
            logger.error("No file part in request")
            return jsonify({"error": "No file part"}), 400

        file = request.files["file"]
        logger.debug(f"Received file: {file.filename}")

        if file.filename == "":
            logger.error("No selected file")
            return jsonify({"error": "No selected file"}), 400

        try:
            from embed import embed

            embedded = embed(file)
            if embedded:
                logger.info("File embedded successfully")
                return jsonify({"message": "File embedded successfully"}), 200
            else:
                logger.error("File embedding failed")
                return jsonify({"error": "File embedded unsuccessfully"}), 400
        except Exception as e:
            logger.exception("Error during embedding")
            return jsonify({"error": f"Embedding error: {str(e)}"}), 500
