import os
import argparse
import sys
import requests
from dotenv import load_dotenv

def get_embedding(text, app_url="http://app:8080"):
    """Get embedding from the app's embed endpoint."""
    try:
        response = requests.post(
            f"{app_url}/api/embed",
            json={"text": text},
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        return response.json()["embedding"]
    except Exception as e:
        print(f"Error getting embedding: {str(e)}", file=sys.stderr)
        raise

def process_and_add_to_chroma(file_path, source_name, app_url="http://app:8080"):
    try:
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Split the content into chunks (e.g., paragraphs)
        chunks = content.split('\n\n')

        # Process each chunk
        for i, chunk in enumerate(chunks):
            if chunk.strip():  # Skip empty chunks
                # Get embedding from app
                embedding = get_embedding(chunk, app_url)

                # Add to ChromaDB through app's API
                response = requests.post(
                    f"{app_url}/api/add",
                    json={
                        "embedding": embedding,
                        "document": chunk,
                        "metadata": {
                            "source": source_name,
                            "chunk_id": i
                        },
                        "id": f"{os.path.basename(file_path)}_{i}"
                    },
                    headers={"Content-Type": "application/json"}
                )
                response.raise_for_status()

        print(f"Content from {file_path} added to ChromaDB successfully.")
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}", file=sys.stderr)
        raise

def process_folder(folder_path, app_url="http://app:8080"):
    if not os.path.exists(folder_path):
        print(f"Error: Folder {folder_path} does not exist", file=sys.stderr)
        sys.exit(1)

    # Iterate over all files in the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            # Use the filename as the source name
            source_name = os.path.splitext(filename)[0]
            process_and_add_to_chroma(file_path, source_name, app_url)

if __name__ == "__main__":
    # Load environment variables
    load_dotenv()

    parser = argparse.ArgumentParser(description='Process files in a folder and add to ChromaDB.')
    parser.add_argument('folder_path', type=str, help='Path to the folder containing files to process.')
    parser.add_argument('--app-url', type=str, default="http://app:8080",
                      help='URL of the app service (default: http://app:8080)')
    args = parser.parse_args()

    try:
        process_folder(args.folder_path, args.app_url)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1) 