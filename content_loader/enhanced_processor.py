import argparse
import logging
import os
import sys
import time
from datetime import datetime
from typing import Any, Dict, List, Tuple, Union, cast

import requests
from dotenv import load_dotenv
from html_processor import HTMLProcessor

# Configure logging with more detailed format
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


class EnhancedContentProcessor:
    """Enhanced content processor supporting both text files and HTML documents."""

    def __init__(
        self,
        app_url: str = "http://app:8080",
        chunk_size: int = 1000,
        overlap: int = 200,
    ):
        """
        Initialize the enhanced content processor.

        Args:
            app_url: URL of the app service
            chunk_size: Maximum size of text chunks
            overlap: Overlap between chunks to maintain context
        """
        self.app_url = app_url
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.html_processor = HTMLProcessor(chunk_size=chunk_size, overlap=overlap)

        # Initialize stats with proper types
        self.stats: Dict[str, Union[int, float, Dict[str, int]]] = {
            "total_files_processed": 0,
            "total_urls_processed": 0,
            "total_chunks_processed": 0,
            "total_text_length": 0,
            "errors": 0,
            "processing_time": 0.0,
            "file_types": {
                "text": 0,
                "html": 0,
                "urls": 0,
            },
        }

        logger.info(f"Initialized EnhancedContentProcessor with app_url={app_url}, chunk_size={chunk_size}, overlap={overlap}")

    def reset_stats(self):
        """Reset processing statistics."""
        self.stats = {
            "total_files_processed": 0,
            "total_urls_processed": 0,
            "total_chunks_processed": 0,
            "total_text_length": 0,
            "errors": 0,
            "processing_time": 0.0,
            "file_types": {
                "text": 0,
                "html": 0,
                "urls": 0,
            },
        }

    def print_stats(self):
        """Print detailed processing statistics."""
        print("\n" + "=" * 60)
        print("ENHANCED CONTENT PROCESSING STATISTICS")
        print("=" * 60)
        print(f"Total Files Processed: {self.stats['total_files_processed']}")
        print(f"Total URLs Processed: {self.stats['total_urls_processed']}")
        print(f"Total Chunks Processed: {self.stats['total_chunks_processed']}")
        print(f"Total Text Length: {self.stats['total_text_length']}")
        print(f"Errors Encountered: {self.stats['errors']}")
        print(f"Total Processing Time: {self.stats['processing_time']:.2f} seconds")

        # Type-safe access to file_types
        file_types = self.stats.get("file_types", {})
        if isinstance(file_types, dict):
            print("\nFile Type Breakdown:")
            print(f"  Text files: {file_types.get('text', 0)}")
            print(f"  HTML files: {file_types.get('html', 0)}")
            print(f"  URLs: {file_types.get('urls', 0)}")

        # Calculate averages if we have data
        total_chunks = self.stats.get("total_chunks_processed", 0)
        if isinstance(total_chunks, int) and total_chunks > 0:
            processing_time = self.stats.get("processing_time", 0.0)
            if isinstance(processing_time, (int, float)):
                print(f"Average Time per Chunk: {processing_time/total_chunks:.3f} seconds")

            total_length = self.stats.get("total_text_length", 0)
            if isinstance(total_length, int):
                print(f"Average Chunk Size: {total_length/total_chunks:.0f} characters")

        errors = self.stats.get("errors", 0)
        if isinstance(errors, int) and errors > 0:
            print(f"\n⚠️  WARNING: {errors} errors occurred during processing")
        else:
            print("\n✅ SUCCESS: All content processed without errors")
        print("=" * 60)

    def get_embedding(self, text: str) -> List[float]:
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
            # Type-safe increment of total_text_length
            if isinstance(self.stats["total_text_length"], (int, float)):
                self.stats["total_text_length"] += len(text)
            logger.debug(f"Generated embedding in {time.time() - start_time:.3f}s (text length: {len(text)})")
            if isinstance(embedding, list):
                return embedding
            else:
                raise ValueError("Embedding is not a list")
        except Exception as e:
            logger.error(f"Error getting embedding: {str(e)}")
            # Type-safe increment of errors
            if isinstance(self.stats["errors"], int):
                self.stats["errors"] += 1
            raise

    def add_to_chroma(
        self,
        embedding: List[float],
        document: str,
        metadata: Dict[str, Any],
        doc_id: str,
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
            self.stats["total_files_processed"] += 1
            logger.debug(f"Added document to ChromaDB in {time.time() - start_time:.3f}s (doc_id: {doc_id})")
            return True
        except Exception as e:
            logger.error(f"Error adding to ChromaDB: {str(e)}")
            self.stats["errors"] += 1
            return False

    def process_text_file(self, file_path: str, source_name: str) -> int:
        """
        Process a text file and add to ChromaDB.

        Args:
            file_path: Path to the text file
            source_name: Name to use as source identifier

        Returns:
            Number of chunks processed
        """
        logger.info(f"📄 Processing text file: {os.path.basename(file_path)}")
        start_time = time.time()

        try:
            # Get file size for progress tracking
            file_size = os.path.getsize(file_path)
            logger.info(f"   File size: {file_size:,} bytes")

            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()

            logger.info(f"   Content length: {len(content):,} characters")

            # Split content into chunks
            chunks = content.split("\n\n")
            logger.info(f"   Split into {len(chunks)} potential chunks")

            processed_count = 0
            valid_chunks = [chunk for chunk in chunks if chunk.strip()]
            logger.info(f"   Found {len(valid_chunks)} non-empty chunks")

            for i, chunk in enumerate(valid_chunks):
                chunk_start = time.time()
                logger.info(f"   Processing chunk {i+1}/{len(valid_chunks)} (length: {len(chunk):,} chars)")

                try:
                    # Get embedding
                    embedding = self.get_embedding(chunk)

                    # Add to ChromaDB
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
                        logger.info(f"   ✅ Chunk {i+1} processed successfully in {time.time() - chunk_start:.3f}s")
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
            logger.error(f"❌ Error processing text file {file_path}: {str(e)}")
            self.stats["errors"] += 1
            raise

    def process_html_file(self, file_path: str, source_name: str) -> int:
        """
        Process an HTML file and add to ChromaDB.

        Args:
            file_path: Path to the HTML file
            source_name: Name to use as source identifier

        Returns:
            Number of chunks processed
        """
        logger.info(f"🌐 Processing HTML file: {os.path.basename(file_path)}")
        start_time = time.time()

        try:
            # Get file size for progress tracking
            file_size = os.path.getsize(file_path)
            logger.info(f"   File size: {file_size:,} bytes")

            # Extract chunks from HTML
            logger.info(f"   Extracting text chunks from HTML...")
            chunks = self.html_processor.extract_text_from_html_file(file_path)
            logger.info(f"   Extracted {len(chunks)} chunks from HTML")

            processed_count = 0

            for i, chunk_data in enumerate(chunks):
                chunk_start = time.time()
                # Access the chunk data properly with type checking
                if isinstance(chunk_data, dict):
                    chunk_text = cast(str, chunk_data.get("text", ""))
                    chunk_metadata = cast(Dict[str, Any], chunk_data.get("metadata", {}))
                else:
                    # Fallback if chunk_data is not a dict
                    chunk_text = str(chunk_data)
                    chunk_metadata = {"source": source_name, "chunk_id": i}

                logger.info(f"   Processing HTML chunk {i+1}/{len(chunks)} (length: {len(chunk_text):,} chars)")

                try:
                    # Get embedding
                    embedding = self.get_embedding(chunk_text)

                    # Add to ChromaDB
                    success = self.add_to_chroma(
                        embedding=embedding,
                        document=chunk_text,
                        metadata=chunk_metadata,
                        doc_id=f"{source_name}_{chunk_metadata.get('chunk_id', i)}",
                    )

                    if success:
                        processed_count += 1
                        self.stats["total_chunks_processed"] += 1
                        logger.info(f"   ✅ HTML chunk {i+1} processed successfully in {time.time() - chunk_start:.3f}s")
                    else:
                        logger.error(f"   ❌ Failed to add HTML chunk {i+1} to ChromaDB")

                except Exception as e:
                    logger.error(f"   ❌ Error processing HTML chunk {i+1}: {str(e)}")
                    self.stats["errors"] += 1
                    continue

            processing_time = time.time() - start_time
            logger.info(
                f"🌐 Completed processing {os.path.basename(file_path)}: {processed_count}/{len(chunks)} chunks in {processing_time:.2f}s"
            )
            return processed_count

        except Exception as e:
            logger.error(f"❌ Error processing HTML file {file_path}: {str(e)}")
            self.stats["errors"] += 1
            raise

    def process_url(self, url: str, source_name: str) -> int:
        """
        Process a URL and add to ChromaDB.

        Args:
            url: URL to process
            source_name: Name to use as source identifier

        Returns:
            Number of chunks processed
        """
        logger.info(f"🔗 Processing URL: {url}")
        start_time = time.time()

        try:
            # Extract chunks from URL
            logger.info(f"   Fetching and extracting text from URL...")
            chunks = self.html_processor.extract_text_from_url(url)
            logger.info(f"   Extracted {len(chunks)} chunks from URL")

            processed_count = 0

            for i, chunk_data in enumerate(chunks):
                chunk_start = time.time()
                # Access the chunk data properly with type checking
                if isinstance(chunk_data, dict):
                    chunk_text = cast(str, chunk_data.get("text", ""))
                    chunk_metadata = cast(Dict[str, Any], chunk_data.get("metadata", {}))
                else:
                    # Fallback if chunk_data is not a dict
                    chunk_text = str(chunk_data)
                    chunk_metadata = {"source": source_name, "chunk_id": i}

                logger.info(f"   Processing URL chunk {i+1}/{len(chunks)} (length: {len(chunk_text):,} chars)")

                try:
                    # Get embedding
                    embedding = self.get_embedding(chunk_text)

                    # Add to ChromaDB
                    success = self.add_to_chroma(
                        embedding=embedding,
                        document=chunk_text,
                        metadata=chunk_metadata,
                        doc_id=f"{source_name}_{chunk_metadata.get('chunk_id', i)}",
                    )

                    if success:
                        processed_count += 1
                        self.stats["total_chunks_processed"] += 1
                        logger.info(f"   ✅ URL chunk {i+1} processed successfully in {time.time() - chunk_start:.3f}s")
                    else:
                        logger.error(f"   ❌ Failed to add URL chunk {i+1} to ChromaDB")

                except Exception as e:
                    logger.error(f"   ❌ Error processing URL chunk {i+1}: {str(e)}")
                    self.stats["errors"] += 1
                    continue

            processing_time = time.time() - start_time
            logger.info(f"🔗 Completed processing URL: {processed_count}/{len(chunks)} chunks in {processing_time:.2f}s")
            return processed_count

        except Exception as e:
            logger.error(f"❌ Error processing URL {url}: {str(e)}")
            self.stats["errors"] += 1
            raise

    def process_folder(self, folder_path: str) -> Dict[str, Union[int, float]]:
        """
        Process all supported files in a folder.

        Args:
            folder_path: Path to the folder

        Returns:
            Dictionary with processing statistics (contains both int and float values)
        """
        logger.info(f"📁 Processing folder: {folder_path}")
        start_time = time.time()

        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"Folder {folder_path} does not exist")

        # Reset stats for this processing session
        self.reset_stats()

        text_extensions = [".txt", ".md", ".rst"]
        html_extensions = [".html", ".htm", ".xhtml"]

        # Count files by type first
        files_by_type: Dict[str, List[Tuple[str, str]]] = {"text": [], "html": []}
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                file_ext = os.path.splitext(filename)[1].lower()
                if file_ext in text_extensions:
                    files_by_type["text"].append((filename, file_path))
                elif file_ext in html_extensions:
                    files_by_type["html"].append((filename, file_path))

        total_files = len(files_by_type["text"]) + len(files_by_type["html"])
        logger.info(f"📁 Found {total_files} files to process:")
        logger.info(f"   Text files: {len(files_by_type['text'])}")
        logger.info(f"   HTML files: {len(files_by_type['html'])}")

        # Process text files
        for i, (filename, file_path) in enumerate(files_by_type["text"]):
            logger.info(f"\n📄 Processing text file {i+1}/{len(files_by_type['text'])}: {filename}")
            source_name = os.path.splitext(filename)[0]

            try:
                chunks = self.process_text_file(file_path, source_name)
                self.stats["file_types"]["text"] += 1
                self.stats["total_files_processed"] += 1

            except Exception as e:
                logger.error(f"❌ Failed to process {filename}: {str(e)}")
                self.stats["errors"] += 1
                continue

        # Process HTML files
        for i, (filename, file_path) in enumerate(files_by_type["html"]):
            logger.info(f"\n🌐 Processing HTML file {i+1}/{len(files_by_type['html'])}: {filename}")
            source_name = os.path.splitext(filename)[0]

            try:
                chunks = self.process_html_file(file_path, source_name)
                self.stats["file_types"]["html"] += 1
                self.stats["total_files_processed"] += 1

            except Exception as e:
                logger.error(f"❌ Failed to process {filename}: {str(e)}")
                self.stats["errors"] += 1
                continue

        self.stats["processing_time"] = time.time() - start_time
        logger.info(f"\n📁 Folder processing complete in {self.stats['processing_time']:.2f} seconds")
        self.print_stats()
        return self.stats

    def process_urls_from_file(self, urls_file: str) -> Dict[str, Union[int, float]]:
        """
        Process URLs listed in a file.

        Args:
            urls_file: Path to file containing URLs (one per line)

        Returns:
            Dictionary with processing statistics (contains both int and float values)
        """
        logger.info(f"🔗 Processing URLs from file: {urls_file}")
        start_time = time.time()

        if not os.path.exists(urls_file):
            raise FileNotFoundError(f"URLs file {urls_file} does not exist")

        # Reset stats for this processing session
        self.reset_stats()

        with open(urls_file, "r", encoding="utf-8") as file:
            urls = [line.strip() for line in file if line.strip()]

        logger.info(f"🔗 Found {len(urls)} URLs to process")

        for i, url in enumerate(urls):
            logger.info(f"\n🔗 Processing URL {i+1}/{len(urls)}: {url}")

            try:
                chunks = self.process_url(url, f"url_{i}")
                self.stats["total_urls_processed"] += 1
                self.stats["file_types"]["urls"] += 1

            except Exception as e:
                logger.error(f"❌ Failed to process URL {url}: {str(e)}")
                self.stats["errors"] += 1
                continue

        self.stats["processing_time"] = time.time() - start_time
        logger.info(f"\n🔗 URL processing complete in {self.stats['processing_time']:.2f} seconds")
        self.print_stats()
        return self.stats


def main():
    """Main function for command-line usage."""
    load_dotenv()

    parser = argparse.ArgumentParser(description="Enhanced content processor supporting text and HTML files.")
    parser.add_argument("--folder", type=str, help="Path to folder containing files to process")
    parser.add_argument(
        "--urls-file",
        type=str,
        help="Path to file containing URLs to process (one per line)",
    )
    parser.add_argument(
        "--app-url",
        type=str,
        default="http://app:8080",
        help="URL of the app service (default: http://app:8080)",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=1000,
        help="Maximum size of text chunks (default: 1000)",
    )
    parser.add_argument("--overlap", type=int, default=200, help="Overlap between chunks (default: 200)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    if not args.folder and not args.urls_file:
        parser.error("Either --folder or --urls-file must be specified")

    print(f"🚀 Starting Enhanced Content Processor at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   App URL: {args.app_url}")
    print(f"   Chunk Size: {args.chunk_size}")
    print(f"   Overlap: {args.overlap}")

    try:
        processor = EnhancedContentProcessor(app_url=args.app_url, chunk_size=args.chunk_size, overlap=args.overlap)

        if args.folder:
            stats = processor.process_folder(args.folder)

        if args.urls_file:
            stats = processor.process_urls_from_file(args.urls_file)

        print(f"\n🎉 Processing completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    except Exception as e:
        logger.error(f"❌ Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
