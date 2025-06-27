import os
from dataclasses import dataclass


@dataclass
class DatabaseConfig:
    host: str
    port: int
    collection_name: str


@dataclass
class OllamaConfig:
    host: str
    port: int
    model: str


@dataclass
class AppConfig:
    temp_folder: str
    debug: bool
    host: str
    port: int


class Config:
    def __init__(self):
        self.database = DatabaseConfig(
            host=os.getenv("CHROMA_HOST", "localhost"),
            port=int(os.getenv("CHROMA_PORT", "8000")),
            collection_name=os.getenv("COLLECTION_NAME", "startrek"),
        )

        self.ollama = OllamaConfig(
            host=os.getenv("OLLAMA_HOST", "localhost"),
            port=int(os.getenv("OLLAMA_PORT", "11434")),
            model=os.getenv("LLM_MODEL", "llama3.2"),
        )

        self.app = AppConfig(
            temp_folder=os.getenv("TEMP_FOLDER", "./_temp"),
            debug=os.getenv("FLASK_DEBUG", "True").lower() == "true",
            host=os.getenv("FLASK_HOST", "0.0.0.0"),
            port=int(os.getenv("FLASK_PORT", "8080")),
        )

    @property
    def ollama_url(self) -> str:
        return f"http://{self.ollama.host}:{self.ollama.port}"

    @property
    def chroma_url(self) -> str:
        return f"http://{self.database.host}:{self.database.port}"


# Global config instance
config = Config()
