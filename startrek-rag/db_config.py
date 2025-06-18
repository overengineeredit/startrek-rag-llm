import os
import logging
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database configuration
CHROMA_HOST = os.getenv('CHROMA_HOST', 'localhost')
CHROMA_PORT = int(os.getenv('CHROMA_PORT', '8000'))
COLLECTION_NAME = "startrek"

def get_chroma_client():
    """
    Initialize and return a ChromaDB client with the latest recommended configuration.
    """
    try:
        client = chromadb.HttpClient(
            host=CHROMA_HOST,
            port=CHROMA_PORT,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        logger.info(f"Successfully initialized ChromaDB client at {CHROMA_HOST}:{CHROMA_PORT}")
        return client
    except Exception as e:
        logger.error(f"Error initializing ChromaDB client: {str(e)}")
        raise

def get_embedding_function():
    """
    Initialize and return the embedding function for ChromaDB.
    """
    try:
        embedding_function = embedding_functions.DefaultEmbeddingFunction()
        logger.info("Successfully initialized default embedding function")
        return embedding_function
    except Exception as e:
        logger.error(f"Error initializing embedding function: {str(e)}")
        raise

def get_collection():
    """
    Get or create the ChromaDB collection with the specified configuration.
    """
    try:
        client = get_chroma_client()
        embedding_function = get_embedding_function()
        
        collection = client.get_or_create_collection(
            name=COLLECTION_NAME,
            embedding_function=embedding_function,
            metadata={
                "hnsw:space": "cosine",
                "hnsw:construction_ef": 100,
                "hnsw:search_ef": 100
            }
        )
        
        logger.info(f"Successfully initialized collection: {COLLECTION_NAME}")
        return collection
    except Exception as e:
        logger.error(f"Error getting/creating collection: {str(e)}")
        raise 