# Use Python 3.9 slim image for smaller size
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY *.py .

# Create input and output directories
RUN mkdir -p /app/input /app/output

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Create entry point script
RUN echo '#!/bin/bash' > /app/entrypoint.sh && \
    echo 'if [ $# -lt 2 ]; then' >> /app/entrypoint.sh && \
    echo '    echo "Usage: docker run <image> <input_json_path> <output_json_path>"' >> /app/entrypoint.sh && \
    echo '    exit 1' >> /app/entrypoint.sh && \
    echo 'fi' >> /app/entrypoint.sh && \
    echo 'python main.py "$1" "$2"' >> /app/entrypoint.sh && \
    chmod +x /app/entrypoint.sh

# Set entry point
ENTRYPOINT ["/app/entrypoint.sh"] 