# Dockerfile for Pinthenews - Optimized for Google Cloud Run
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies including curl for health checks
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p .streamlit

# Copy Streamlit config
COPY streamlit_config.toml .streamlit/config.toml

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash app && chown -R app:app /app
USER app

# Use PORT environment variable for Cloud Run
ENV PORT=8080
EXPOSE $PORT

# Health check for Cloud Run
HEALTHCHECK --interval=30s --timeout=30s --start-period=40s --retries=3 \
    CMD curl --fail http://localhost:$PORT/_stcore/health || exit 1

# Run the application optimized for Cloud Run
CMD streamlit run src/app.py \
    --server.port=$PORT \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --server.runOnSave=false \
    --server.allowRunOnSave=false \
    --server.maxUploadSize=1000 \
    --server.maxRequestSize=1000 \
    --server.enableStaticServing=true \
    --server.fileWatcherType=none \
    --server.enableCORS=false \
    --server.enableXsrfProtection=true