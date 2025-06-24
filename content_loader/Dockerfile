FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content loader code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1

# The entrypoint will be specified in docker-compose.yml
CMD ["python", "process_content.py"] 