import os
from datetime import datetime
from typing import Any, List, Union

from db_config import get_collection, get_embedding_function
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from werkzeug.utils import secure_filename

TEMP_FOLDER = os.getenv("TEMP_FOLDER", "./_temp")


def get_embedding(text: str) -> Union[List[float], Any]:
    """Get embedding for a single text string."""
    embedding_function = get_embedding_function()
    if embedding_function is None:
        raise RuntimeError("Embedding function not initialized")
    result = embedding_function([text])
    if isinstance(result, list) and len(result) > 0:
        return result[0]
    raise RuntimeError("Failed to generate embedding")


# Function to check if the uploaded file is allowed (only PDF files)
def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in {"pdf"}


# Function to save the uploaded file to the temporary folder
def save_file(file: Any) -> str:
    # Save the uploaded file with a secure filename and return the file path
    ct = datetime.now()
    ts = ct.timestamp()
    filename = str(ts) + "_" + secure_filename(file.filename)
    file_path = os.path.join(TEMP_FOLDER, filename)
    file.save(file_path)

    return file_path


# Function to load and split the data from the PDF file
def load_and_split_data(file_path: str) -> List[Any]:
    # Load the PDF file and split the data into chunks
    loader = UnstructuredPDFLoader(file_path=file_path)
    data = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=7500, chunk_overlap=100)
    chunks = text_splitter.split_documents(data)

    return chunks


# Main function to handle the embedding process
def embed(file: Any) -> bool:
    # Check if the file is valid, save it, load and split the data, add to the database, and remove the temporary file
    if file.filename != "" and file and allowed_file(file.filename):
        file_path = save_file(file)
        chunks = load_and_split_data(file_path)
        collection = get_collection()
        # Use the correct method for adding documents to ChromaDB
        collection.add(
            documents=[chunk.page_content for chunk in chunks],
            metadatas=[chunk.metadata for chunk in chunks],
            ids=[f"pdf_{i}" for i in range(len(chunks))],
        )
        os.remove(file_path)

        return True

    return False
