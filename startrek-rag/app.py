import os
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()

from flask import Flask, request, jsonify
from embed import embed
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

if __name__ == '__main__':
    logger.info("Starting Flask application")
    app.run(host="0.0.0.0", port=8080, debug=True)

    
