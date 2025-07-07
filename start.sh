#!/bin/bash
# Pinthenews Quick Start Script
# Launches the application with optimized production settings

echo "🌍 Starting Pinthenews with enhanced connectivity..."
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
echo "🔄 Cleaning up existing processes..."
pkill -f "streamlit.*app.py" 2>/dev/null || true
sleep 2

# Install dependencies if needed
echo "📦 Installing dependencies..."
pip install -r requirements.txt -q

# Launch Streamlit with enhanced settings
echo "🚀 Launching Pinthenews..."
echo "🌐 Application will be available at: http://localhost:8501"
echo "⏹️  Press Ctrl+C to stop the application"
echo "================================================="

# Export environment variables for better connectivity
export STREAMLIT_SERVER_MAX_MESSAGE_SIZE=1000
export STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Run with simplified reliable settings  
exec python -m streamlit run src/app.py \
    --server.address=localhost \
    --server.port=8501 \
    --server.headless=false \
    --browser.gatherUsageStats=false