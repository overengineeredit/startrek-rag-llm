import logging
import os
import re
import time
from typing import Any, Dict, List, Union

import nltk
import requests
from bs4 import BeautifulSoup

try:
    from unstructured.partition.html import partition_html
except ImportError:
    partition_html = None

# Configure logging with more detailed format
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# Download NLTK resources at module import time
try:
    nltk.download("punkt", quiet=True)
    nltk.download("punkt_tab", quiet=True)
    logger.info("NLTK resources downloaded successfully")
except Exception as e:
    logger.warning(f"Could not download NLTK resources: {e}")


class HTMLProcessor:
    """Process HTML documents and extract meaningful text content."""

    def __init__(self, chunk_size: int = 1000, overlap: int = 200):
        """
        Initialize the HTML processor.

        Args:
            chunk_size: Maximum size of text chunks
            overlap: Overlap between chunks to maintain context
        """
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.stats = {
            "total_files_processed": 0,
            "total_urls_processed": 0,
            "total_chunks_extracted": 0,
            "total_text_length": 0,
            "errors": 0,
            "processing_time": 0,
            "extraction_methods": {
                "unstructured": 0,
                "beautifulsoup": 0,
                "fallback": 0,
            },
        }
        logger.info(
            f"Initialized HTMLProcessor with chunk_size={chunk_size}, overlap={overlap}"
        )

    def reset_stats(self):
        """Reset processing statistics."""
        self.stats = {
            "total_files_processed": 0,
            "total_urls_processed": 0,
            "total_chunks_extracted": 0,
            "total_text_length": 0,
            "errors": 0,
            "processing_time": 0,
            "extraction_methods": {
                "unstructured": 0,
                "beautifulsoup": 0,
                "fallback": 0,
            },
        }

    def print_stats(self):
        """Print detailed processing statistics."""
        print("\n" + "=" * 60)
        print("HTML PROCESSING STATISTICS")
        print("=" * 60)
        print(f"Total Files Processed: {self.stats['total_files_processed']}")
        print(f"Total URLs Processed: {self.stats['total_urls_processed']}")
        print(f"Total Chunks Extracted: {self.stats['total_chunks_extracted']}")
        print(f"Total Text Length: {self.stats['total_text_length']:,} characters")
        print(f"Errors Encountered: {self.stats['errors']}")
        print(f"Total Processing Time: {self.stats['processing_time']:.2f} seconds")
        if self.stats["total_chunks_extracted"] > 0:
            print(
                f"Average Time per Chunk: {self.stats['processing_time']/self.stats['total_chunks_extracted']:.3f} seconds"
            )
            print(
                f"Average Chunk Size: {self.stats['total_text_length']/self.stats['total_chunks_extracted']:.0f} characters"
            )

        print("\nExtraction Method Breakdown:")
        print(f"  Unstructured: {self.stats['extraction_methods']['unstructured']}")
        print(f"  BeautifulSoup: {self.stats['extraction_methods']['beautifulsoup']}")
        print(f"  Fallback: {self.stats['extraction_methods']['fallback']}")

        if self.stats["errors"] > 0:
            print(
                f"\n⚠️  WARNING: {self.stats['errors']} errors occurred during processing"
            )
        else:
            print("\n✅ SUCCESS: All content processed without errors")
        print("=" * 60)

    def clean_text(self, text: str) -> str:
        """Clean and normalize text content."""
        if not text:
            return ""

        # Remove extra whitespace
        text = re.sub(r"\s+", " ", text)

        # Remove special characters but keep punctuation
        text = re.sub(r"[^\w\s\.\,\!\?\;\:\-\(\)\[\]\{\}]", "", text)

        # Strip leading/trailing whitespace
        text = text.strip()

        return text

    def extract_text_from_html_file(
        self, file_path: str
    ) -> List[Dict[str, Union[str, Dict[str, Any]]]]:
        """
        Extract text content from an HTML file.

        Args:
            file_path: Path to the HTML file

        Returns:
            List of dictionaries containing text chunks and metadata
        """
        logger.info(f"📄 Extracting text from HTML file: {os.path.basename(file_path)}")
        start_time = time.time()

        try:
            # Get file size for progress tracking
            file_size = os.path.getsize(file_path)
            logger.info(f"   File size: {file_size:,} bytes")

            with open(file_path, "r", encoding="utf-8") as file:
                html_content = file.read()

            logger.info(f"   HTML content length: {len(html_content):,} characters")

            chunks = self._process_html_content(
                html_content, source=f"file:{file_path}"
            )

            processing_time = time.time() - start_time
            logger.info(
                f"📄 Completed extracting from {os.path.basename(file_path)}: {len(chunks)} chunks in {processing_time:.2f}s"
            )

            return chunks

        except Exception as e:
            logger.error(f"❌ Error processing HTML file {file_path}: {str(e)}")
            self.stats["errors"] += 1
            raise

    def extract_text_from_url(
        self, url: str
    ) -> List[Dict[str, Union[str, Dict[str, Any]]]]:
        """
        Extract text content from a web URL.

        Args:
            url: URL to fetch and process

        Returns:
            List of dictionaries containing text chunks and metadata
        """
        logger.info(f"🔗 Extracting text from URL: {url}")
        start_time = time.time()

        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }

            logger.info(f"   Fetching content from URL...")
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()

            html_content = response.text
            logger.info(f"   Fetched {len(html_content):,} characters from URL")

            chunks = self._process_html_content(html_content, source=f"url:{url}")

            processing_time = time.time() - start_time
            logger.info(
                f"🔗 Completed extracting from URL: {len(chunks)} chunks in {processing_time:.2f}s"
            )

            return chunks

        except Exception as e:
            logger.error(f"❌ Error processing URL {url}: {str(e)}")
            self.stats["errors"] += 1
            raise

    def _process_html_content(
        self, html_content: str, source: str
    ) -> List[Dict[str, Union[str, Dict[str, Any]]]]:
        """
        Process HTML content and extract meaningful text chunks.

        Args:
            html_content: Raw HTML content
            source: Source identifier (file path or URL)

        Returns:
            List of dictionaries containing text chunks and metadata
        """
        chunks = []
        extraction_start = time.time()

        try:
            logger.info(
                "   Processing HTML content using multiple extraction methods..."
            )

            # Use unstructured to partition HTML
            logger.info(f"   Attempting extraction with unstructured library...")
            try:
                if partition_html is not None:
                    elements = partition_html(text=html_content)
                    logger.info(f"   Unstructured extracted {len(elements)} elements")

                    # Extract text from elements
                    text_content = []
                    for i, element in enumerate(elements):
                        if hasattr(element, "text") and element.text:
                            cleaned_text = self.clean_text(element.text)
                            if (
                                cleaned_text and len(cleaned_text) > 50
                            ):  # Filter out very short content
                                text_content.append(cleaned_text)
                                logger.debug(f"   Element {i+1}: {len(cleaned_text)} chars")

                    logger.info(
                        f"   Unstructured extracted {len(text_content)} text segments"
                    )
                    self.stats["extraction_methods"]["unstructured"] += 1
                else:
                    logger.warning("   Unstructured library not available")
                    text_content = []

            except Exception as e:
                logger.warning(f"   Unstructured extraction failed: {str(e)}")
                text_content = []

            # Also try BeautifulSoup for additional content extraction
            logger.info(f"   Attempting extraction with BeautifulSoup...")
            try:
                soup = BeautifulSoup(html_content, "html.parser")

                # Remove script and style elements
                for script in soup(["script", "style"]):
                    script.decompose()

                # Extract text from body
                body_text = soup.get_text()
                if body_text:
                    cleaned_body = self.clean_text(body_text)
                    if cleaned_body and len(cleaned_body) > 100:
                        text_content.append(cleaned_body)
                        logger.info(
                            f"   BeautifulSoup extracted {len(cleaned_body):,} chars from body"
                        )

                # Extract title
                title = soup.find("title")
                if title and title.get_text():
                    title_text = self.clean_text(title.get_text())
                    if title_text:
                        text_content.append(f"Title: {title_text}")
                        logger.info(f"   BeautifulSoup extracted title: {title_text}")

                # Extract headings
                headings_found = 0
                for heading in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]):
                    heading_text = self.clean_text(heading.get_text())
                    if heading_text and len(heading_text) > 10:
                        text_content.append(f"Heading: {heading_text}")
                        headings_found += 1

                logger.info(f"   BeautifulSoup extracted {headings_found} headings")
                self.stats["extraction_methods"]["beautifulsoup"] += 1

            except Exception as e:
                logger.warning(f"   BeautifulSoup extraction failed: {str(e)}")

            # Create chunks from extracted content
            if text_content:
                full_text = " ".join(text_content)
                logger.info(f"   Combined text length: {len(full_text):,} characters")

                text_chunks = self._create_chunks(full_text)
                logger.info(f"   Created {len(text_chunks)} chunks from combined text")

                # Create chunk metadata
                for i, chunk in enumerate(text_chunks):
                    chunks.append(
                        {
                            "text": chunk,
                            "metadata": {
                                "source": source,
                                "chunk_id": i,
                                "content_type": "html",
                                "chunk_size": len(chunk),
                                "extraction_method": "combined",
                            },
                        }
                    )

                self.stats["total_chunks_extracted"] += len(chunks)
                self.stats["total_text_length"] += len(full_text)

            else:
                logger.warning(
                    f"   No text content extracted, trying fallback method..."
                )
                # Fallback to simple text extraction
                fallback_chunks = self._fallback_text_extraction(html_content, source)
                chunks.extend(fallback_chunks)

            extraction_time = time.time() - extraction_start
            logger.info(
                f"   HTML processing completed in {extraction_time:.2f}s: {len(chunks)} chunks extracted"
            )
            return chunks

        except Exception as e:
            logger.error(f"   ❌ Error processing HTML content: {str(e)}")
            self.stats["errors"] += 1
            # Fallback to simple text extraction
            return self._fallback_text_extraction(html_content, source)

    def _fallback_text_extraction(
        self, html_content: str, source: str
    ) -> List[Dict[str, Union[str, Dict[str, Any]]]]:
        """Fallback method for text extraction if structured parsing fails."""
        logger.info(f"   Using fallback text extraction method...")
        fallback_start = time.time()

        try:
            soup = BeautifulSoup(html_content, "html.parser")

            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()

            # Get text content
            text = soup.get_text()
            cleaned_text = self.clean_text(text)

            if not cleaned_text:
                logger.warning(f"   Fallback extraction: no text content found")
                return []

            logger.info(f"   Fallback extracted {len(cleaned_text):,} characters")

            # Create chunks
            text_chunks = self._create_chunks(cleaned_text)
            logger.info(f"   Fallback created {len(text_chunks)} chunks")

            chunks = []
            for i, chunk in enumerate(text_chunks):
                chunks.append(
                    {
                        "text": chunk,
                        "metadata": {
                            "source": source,
                            "chunk_id": i,
                            "content_type": "html_fallback",
                            "chunk_size": len(chunk),
                            "extraction_method": "fallback",
                        },
                    }
                )

            fallback_time = time.time() - fallback_start
            logger.info(
                f"   Fallback extraction completed in {fallback_time:.2f}s: {len(chunks)} chunks"
            )

            self.stats["extraction_methods"]["fallback"] += 1
            self.stats["total_chunks_extracted"] += len(chunks)
            self.stats["total_text_length"] += len(cleaned_text)

            return chunks

        except Exception as e:
            logger.error(f"   ❌ Fallback extraction failed: {str(e)}")
            self.stats["errors"] += 1
            return []

    def _create_chunks(self, text: str) -> List[str]:
        """
        Create overlapping chunks from text.

        Args:
            text: Input text to chunk

        Returns:
            List of text chunks
        """
        if len(text) <= self.chunk_size:
            return [text]

        chunks = []
        start = 0

        while start < len(text):
            end = start + self.chunk_size

            # Try to break at sentence boundaries
            if end < len(text):
                # Look for sentence endings
                sentence_endings = [". ", "! ", "? ", "\n\n"]
                for ending in sentence_endings:
                    last_ending = text.rfind(ending, start, end)
                    if (
                        last_ending > start + self.chunk_size * 0.7
                    ):  # Only break if we're at least 70% through
                        end = last_ending + 1
                        break

            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)

            start = end - self.overlap
            if start >= len(text):
                break

        return chunks

    def process_html_folder(
        self, folder_path: str
    ) -> List[Dict[str, Union[str, Dict[str, Any]]]]:
        """
        Process all HTML files in a folder.

        Args:
            folder_path: Path to folder containing HTML files

        Returns:
            List of all extracted chunks from all HTML files
        """
        logger.info(f"📁 Processing HTML folder: {folder_path}")
        start_time = time.time()

        # Reset stats for this processing session
        self.reset_stats()

        all_chunks = []

        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"Folder {folder_path} does not exist")

        html_extensions = [".html", ".htm", ".xhtml"]

        # Count files first
        html_files = []
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                file_ext = os.path.splitext(filename)[1].lower()
                if file_ext in html_extensions:
                    html_files.append((filename, file_path))

        logger.info(f"📁 Found {len(html_files)} HTML files to process")

        for i, (filename, file_path) in enumerate(html_files):
            logger.info(
                f"\n📄 Processing HTML file {i+1}/{len(html_files)}: {filename}"
            )

            try:
                chunks = self.extract_text_from_html_file(file_path)
                all_chunks.extend(chunks)
                self.stats["total_files_processed"] += 1

            except Exception as e:
                logger.error(f"❌ Failed to process {filename}: {str(e)}")
                self.stats["errors"] += 1
                continue

        self.stats["processing_time"] = time.time() - start_time
        logger.info(
            f"\n📁 HTML folder processing complete in {self.stats['processing_time']:.2f} seconds"
        )
        logger.info(f"📁 Total chunks extracted from HTML folder: {len(all_chunks)}")
        self.print_stats()
        return all_chunks

    def process_urls(
        self, urls: List[str]
    ) -> List[Dict[str, Union[str, Dict[str, Any]]]]:
        """
        Process multiple URLs.

        Args:
            urls: List of URLs to process

        Returns:
            List of all extracted chunks from all URLs
        """
        logger.info(f"🔗 Processing {len(urls)} URLs")
        start_time = time.time()

        # Reset stats for this processing session
        self.reset_stats()

        all_chunks = []

        for i, url in enumerate(urls):
            logger.info(f"\n🔗 Processing URL {i+1}/{len(urls)}: {url}")

            try:
                chunks = self.extract_text_from_url(url)
                all_chunks.extend(chunks)
                self.stats["total_urls_processed"] += 1

            except Exception as e:
                logger.error(f"❌ Failed to process URL {url}: {str(e)}")
                self.stats["errors"] += 1
                continue

        self.stats["processing_time"] = time.time() - start_time
        logger.info(
            f"\n🔗 URL processing complete in {self.stats['processing_time']:.2f} seconds"
        )
        logger.info(f"🔗 Total chunks extracted from URLs: {len(all_chunks)}")
        self.print_stats()
        return all_chunks
