#!/bin/bash
# Pinthenews Quick Start Script
# Launches the application with optimized production settings

echo "🌍 Starting Pinthenews with no timeout configuration..."
echo "================================================="

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating template..."
    echo "ANTHROPIC_API_KEY=your_anthropic_api_key_here" > .env
    echo "📝 Please edit .env file with your API key before running again"
    exit 1
fi

# Check for API key
if grep -q "your_anthropic_api_key_here" .env; then
    echo "❌ Please configure your ANTHROPIC_API_KEY in the .env file"
    exit 1
fi

# Kill any existing process on port 8501
echo "🔄 Checking for existing processes..."
lsof -ti:8501 | head -1 | xargs kill -9 2>/dev/null || true

# Install dependencies if needed
echo "📦 Checking dependencies..."
pip install -r requirements.txt -q

# Launch Streamlit with no timeout configuration
echo "🚀 Launching Pinthenews..."
echo "🌐 Application will be available at: http://localhost:8501"
echo "⏹️  Press Ctrl+C to stop the application"
echo "================================================="

# Run with optimized settings for no timeout
python -m streamlit run src\app.py \
    --server.port 8501 \
    --server.address 0.0.0.0 \
    --server.headless false \
    --server.runOnSave false \
    --server.allowRunOnSave false \
    --server.maxUploadSize 1000 \
    --server.fileWatcherType none \
    --client.toolbarMode minimal \
    --client.showErrorDetails false \
    --global.dataFrameSerialization legacy