FROM python:3.9-slim

WORKDIR /app

# Install minimal system dependencies
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY src/ ./src/
COPY agents/ ./agents/
COPY streamlit_config.toml ./.streamlit/config.toml

# Set environment for local development
ENV PORT=8501
EXPOSE $PORT

# Run application in non-headless mode for local development
CMD streamlit run src/app.py --server.port=$PORT --server.address=0.0.0.0