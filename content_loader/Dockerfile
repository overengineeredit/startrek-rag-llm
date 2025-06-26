FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install NLTK and download required NLTK data resources
RUN pip install --no-cache-dir nltk && \
    python -m nltk.downloader punkt punkt_tab averaged_perceptron_tagger averaged_perceptron_tagger_eng

# Copy the content loader code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1

# The entrypoint will be specified in docker-compose.yml
CMD ["python", "process_content.py"] 