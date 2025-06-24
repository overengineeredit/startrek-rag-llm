import os
import logging
from dotenv import load_dotenv
import datetime
import requests

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()

from flask import Flask, request, jsonify
from embed import embed, get_embedding
from query import query
from db_config import get_collection

TEMP_FOLDER = os.getenv('TEMP_FOLDER', './_temp')
OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'localhost')
LLM_MODEL = os.getenv('LLM_MODEL', 'llama3.2')

logger.info(f"Configuration: TEMP_FOLDER={TEMP_FOLDER}, OLLAMA_HOST={OLLAMA_HOST}, LLM_MODEL={LLM_MODEL}")

os.makedirs(TEMP_FOLDER, exist_ok=True)

app = Flask(__name__)

# Initialize database connection at startup
try:
    collection = get_collection()
    logger.info("Database connection initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize database connection: {str(e)}")
    raise

@app.route('/embed', methods=['POST'])
def route_embed():
    logger.debug("Received embed request")
    logger.debug(f"Request headers: {dict(request.headers)}")
    logger.debug(f"Request data: {request.data}")
    logger.debug(f"Content-Type: {request.content_type}")
    logger.debug(f"Is JSON: {request.is_json}")
    
    # Check if this is a file upload or direct text
    if request.is_json or request.content_type == 'application/json':
        data = request.get_json()
        logger.debug(f"Parsed JSON data: {data}")
        if 'text' not in data:
            logger.error("No text in request data")
            return jsonify({"error": "No text provided"}), 400
        
        try:
            embedding = get_embedding(data['text'])
            logger.info("Text embedded successfully")
            return jsonify({"embedding": embedding}), 200
        except Exception as e:
            logger.exception("Error during text embedding")
            return jsonify({"error": f"Embedding error: {str(e)}"}), 500
    else:
        # Handle file upload
        if 'file' not in request.files:
            logger.error("No file part in request")
            return jsonify({"error": "No file part"}), 400

        file = request.files['file']
        logger.debug(f"Received file: {file.filename}")

        if file.filename == '':
            logger.error("No selected file")
            return jsonify({"error": "No selected file"}), 400

        try:
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

@app.route('/query', methods=['POST'])
def route_query():
    logger.debug("Received query request")
    try:
        data = request.get_json()
        logger.debug(f"Query data: {data}")
        
        if not data or 'query' not in data:
            logger.error("No query in request data")
            return jsonify({"error": "No query provided"}), 400
            
        query_text = data.get('query')
        logger.info(f"Processing query: {query_text}")
        
        response = query(query_text)
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

@app.route('/add', methods=['POST'])
def route_add():
    logger.debug("Received add request")
    if not request.is_json:
        logger.error("Request is not JSON")
        return jsonify({"error": "Request must be JSON"}), 400
    data = request.get_json()
    logger.debug(f"Add request data: {data}")
    required_fields = ["embedding", "document", "metadata", "id"]
    if not all(field in data for field in required_fields):
        logger.error("Missing required fields in add request")
        return jsonify({"error": "Missing required fields: embedding, document, metadata, id"}), 400
    try:
        collection = get_collection()
        collection.add(
            embeddings=[data["embedding"]],
            documents=[data["document"]],
            metadatas=[data["metadata"]],
            ids=[data["id"]]
        )
        logger.info("Document added to ChromaDB successfully")
        return jsonify({"message": "Document added to ChromaDB successfully"}), 200
    except Exception as e:
        logger.exception("Error adding document to ChromaDB")
        return jsonify({"error": f"Add error: {str(e)}"}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify system status"""
    logger.debug("Received health check request")
    try:
        # Check database connection
        collection = get_collection()
        # Try a simple operation to verify connection
        collection.count()
        
        # Check if Ollama is accessible
        ollama_url = f"http://{OLLAMA_HOST}:11434/api/tags"
        ollama_response = requests.get(ollama_url, timeout=5)
        
        if ollama_response.status_code == 200:
            logger.info("Health check passed - all systems operational")
            return jsonify({
                "status": "healthy",
                "database": "connected",
                "ollama": "accessible",
                "model": LLM_MODEL,
                "timestamp": str(datetime.datetime.now())
            }), 200
        else:
            logger.warning("Health check failed - Ollama not accessible")
            return jsonify({
                "status": "degraded",
                "database": "connected",
                "ollama": "not accessible",
                "error": "Ollama service not responding"
            }), 503
    except Exception as e:
        logger.exception("Health check failed")
        return jsonify({
            "status": "unhealthy",
            "error": str(e),
            "timestamp": str(datetime.datetime.now())
        }), 500

if __name__ == '__main__':
    logger.info("Starting Flask application")
    app.run(host="0.0.0.0", port=8080, debug=True)

    
