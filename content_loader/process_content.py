import argparse
import logging
import os
import sys
import time
from datetime import datetime

import requests
from dotenv import load_dotenv

# Configure logging with more detailed format
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


class ContentProcessor:
    """Simple content processor for text files with detailed logging."""

    def __init__(self, app_url: str = "http://app:8080"):
        """
        Initialize the content processor.

        Args:
            app_url: URL of the app service
        """
        self.app_url = app_url
        self.stats = {
            "total_files_processed": 0,
            "total_chunks_processed": 0,
            "total_embeddings_generated": 0,
            "total_documents_added": 0,
            "errors": 0,
            "processing_time": 0.0,
            "total_text_length": 0,
        }
        logger.info(f"Initialized ContentProcessor with app_url={app_url}")

    def reset_stats(self):
        """Reset processing statistics."""
        self.stats = {
            "total_files_processed": 0,
            "total_chunks_processed": 0,
            "total_embeddings_generated": 0,
            "total_documents_added": 0,
            "errors": 0,
            "processing_time": 0.0,
            "total_text_length": 0,
        }

    def print_stats(self):
        """Print detailed processing statistics."""
        print("\n" + "=" * 60)
        print("CONTENT PROCESSING STATISTICS")
        print("=" * 60)
        print(f"Total Files Processed: {self.stats['total_files_processed']}")
        print(f"Total Chunks Processed: {self.stats['total_chunks_processed']}")
        print(f"Total Embeddings Generated: {self.stats['total_embeddings_generated']}")
        print(
            f"Total Documents Added to ChromaDB: {self.stats['total_documents_added']}"
        )
        print(f"Total Text Length: {self.stats['total_text_length']:,} characters")
        print(f"Errors Encountered: {self.stats['errors']}")
        print(f"Total Processing Time: {self.stats['processing_time']:.2f} seconds")
        if self.stats["total_chunks_processed"] > 0:
            print(
                f"Average Time per Chunk: {self.stats['processing_time']/self.stats['total_chunks_processed']:.3f} seconds"
            )
            print(
                f"Average Chunk Size: {self.stats['total_text_length']/self.stats['total_chunks_processed']:.0f} characters"
            )

        if self.stats["errors"] > 0:
            print(
                f"\n⚠️  WARNING: {self.stats['errors']} errors occurred during processing"
            )
        else:
            print(f"\n✅ SUCCESS: All content processed without errors")
        print("=" * 60)

    def get_embedding(self, text: str) -> list:
        """Get embedding from the app's embed endpoint."""
        try:
            start_time = time.time()
            response = requests.post(
                f"{self.app_url}/api/embed",
                json={"text": text},
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()
            embedding = response.json()["embedding"]
            self.stats["total_embeddings_generated"] += 1
            logger.debug(
                f"Generated embedding in {time.time() - start_time:.3f}s (text length: {len(text)})"
            )
            return embedding
        except Exception as e:
            logger.error(f"Error getting embedding: {str(e)}")
            self.stats["errors"] += 1
            raise

    def add_to_chroma(
        self, embedding: list, document: str, metadata: dict, doc_id: str
    ) -> bool:
        """Add document to ChromaDB through app's API."""
        try:
            start_time = time.time()
            response = requests.post(
                f"{self.app_url}/api/add",
                json={
                    "embedding": embedding,
                    "document": document,
                    "metadata": metadata,
                    "id": doc_id,
                },
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()
            self.stats["total_documents_added"] += 1
            logger.debug(
                f"Added document to ChromaDB in {time.time() - start_time:.3f}s (doc_id: {doc_id})"
            )
            return True
        except Exception as e:
            logger.error(f"Error adding to ChromaDB: {str(e)}")
            self.stats["errors"] += 1
            return False

    def process_file(self, file_path: str, source_name: str) -> int:
        """
        Process a single file and add to ChromaDB.

        Args:
            file_path: Path to the file to process
            source_name: Name to use as source identifier

        Returns:
            Number of chunks processed
        """
        logger.info(f"📄 Processing file: {os.path.basename(file_path)}")
        start_time = time.time()

        try:
            # Get file size for progress tracking
            file_size = os.path.getsize(file_path)
            logger.info(f"   File size: {file_size:,} bytes")

            # Read the file
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()

            logger.info(f"   Content length: {len(content):,} characters")

            # Split the content into chunks (e.g., paragraphs)
            chunks = content.split("\n\n")
            logger.info(f"   Split into {len(chunks)} potential chunks")

            # Filter out empty chunks
            valid_chunks = [chunk for chunk in chunks if chunk.strip()]
            logger.info(f"   Found {len(valid_chunks)} non-empty chunks")

            processed_count = 0

            # Process each chunk
            for i, chunk in enumerate(valid_chunks):
                chunk_start = time.time()
                logger.info(
                    f"   Processing chunk {i+1}/{len(valid_chunks)} (length: {len(chunk):,} chars)"
                )

                try:
                    # Get embedding from app
                    embedding = self.get_embedding(chunk)

                    # Add to ChromaDB through app's API
                    success = self.add_to_chroma(
                        embedding=embedding,
                        document=chunk,
                        metadata={
                            "source": source_name,
                            "chunk_id": i,
                            "content_type": "text",
                            "file_path": file_path,
                            "chunk_size": len(chunk),
                        },
                        doc_id=f"{os.path.basename(file_path)}_{i}",
                    )

                    if success:
                        processed_count += 1
                        self.stats["total_chunks_processed"] += 1
                        self.stats["total_text_length"] += len(chunk)
                        logger.info(
                            f"   ✅ Chunk {i+1} processed successfully in {time.time() - chunk_start:.3f}s"
                        )
                    else:
                        logger.error(f"   ❌ Failed to add chunk {i+1} to ChromaDB")

                except Exception as e:
                    logger.error(f"   ❌ Error processing chunk {i+1}: {str(e)}")
                    self.stats["errors"] += 1
                    continue

            processing_time = time.time() - start_time
            logger.info(
                f"📄 Completed processing {os.path.basename(file_path)}: {processed_count}/{len(valid_chunks)} chunks in {processing_time:.2f}s"
            )
            return processed_count

        except Exception as e:
            logger.error(f"❌ Error processing file {file_path}: {str(e)}")
            self.stats["errors"] += 1
            raise

    def process_folder(self, folder_path: str) -> dict:
        """
        Process all files in a folder.

        Args:
            folder_path: Path to the folder containing files to process

        Returns:
            Dictionary with processing statistics
        """
        logger.info(f"📁 Processing folder: {folder_path}")
        start_time = time.time()

        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"Folder {folder_path} does not exist")

        # Reset stats for this processing session
        self.reset_stats()

        # Count files first
        files = []
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                files.append((filename, file_path))

        logger.info(f"📁 Found {len(files)} files to process")

        # Process each file
        for i, (filename, file_path) in enumerate(files):
            logger.info(f"\n📄 Processing file {i+1}/{len(files)}: {filename}")

            try:
                # Use the filename as the source name
                source_name = os.path.splitext(filename)[0]
                chunks = self.process_file(file_path, source_name)
                self.stats["total_files_processed"] += 1

            except Exception as e:
                logger.error(f"❌ Failed to process {filename}: {str(e)}")
                self.stats["errors"] += 1
                continue

        self.stats["processing_time"] = time.time() - start_time
        logger.info(
            f"\n📁 Folder processing complete in {self.stats['processing_time']:.2f} seconds"
        )
        self.print_stats()
        return self.stats


def main():
    """Main function for command-line usage."""
    load_dotenv()

    parser = argparse.ArgumentParser(
        description="Process files in a folder and add to ChromaDB."
    )
    parser.add_argument(
        "folder_path", type=str, help="Path to the folder containing files to process."
    )
    parser.add_argument(
        "--app-url",
        type=str,
        default="http://app:8080",
        help="URL of the app service (default: http://app:8080)",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    print(
        f"🚀 Starting Content Processor at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    print(f"   App URL: {args.app_url}")
    print(f"   Folder: {args.folder_path}")

    try:
        processor = ContentProcessor(app_url=args.app_url)
        stats = processor.process_folder(args.folder_path)

        print(
            f"\n🎉 Processing completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )

    except Exception as e:
        logger.error(f"❌ Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
