import logging
import os

from flask import Flask, jsonify

from flask import Flask, jsonify
from routes.api import api_bp

from config import config

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if config.app.debug else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def create_app():
    """Application factory pattern."""
    app = Flask(__name__)

    # Register blueprints
    app.register_blueprint(api_bp)

    @app.route("/", methods=["GET"])
    def index():
        """Root endpoint with API information."""
        return (
            jsonify(
                {
                    "name": "Star Trek RAG API",
                    "version": "1.0.0",
                    "endpoints": {
                        "query": "/api/query (POST)",
                        "add": "/api/add (POST)",
                        "stats": "/api/stats (GET)",
                        "health": "/api/health (GET)",
                        "embed": "/api/embed (POST)",
                    },
                    "documentation": "See README.md for usage instructions",
                }
            ),
            200,
        )

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Endpoint not found"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Internal server error"}), 500

    return app


def main():
    """Main application entry point."""
    # Create temp folder
    os.makedirs(config.app.temp_folder, exist_ok=True)

    # Create and run the app
    app = create_app()

    logger.info(f"Starting Flask application on {config.app.host}:{config.app.port}")
    logger.info(f"Debug mode: {config.app.debug}")
    logger.info(f"Configuration: TEMP_FOLDER={config.app.temp_folder}")
    logger.info(f"Ollama: {config.ollama_url}, Model: {config.ollama.model}")
    logger.info(f"ChromaDB: {config.chroma_url}")

    app.run(host=config.app.host, port=config.app.port, debug=config.app.debug)


if __name__ == "__main__":
    main()
