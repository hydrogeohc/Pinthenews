# Pinthenews Deployment Guide

## 🚀 Deployment Options

### 1. Quick Start (Recommended)
```bash
./start.sh
```

### 2. Manual Start
```bash
python -m streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

### 3. Docker Deployment
```bash
# Build and run
docker build -t pinthenews .
docker run -p 8501:8501 --env-file .env pinthenews

# Or use Docker Compose
docker-compose up -d
```

## ⚙️ Configuration

### Environment Variables
```bash
# Required
ANTHROPIC_API_KEY=your_actual_api_key_here
```

### Optimized Settings
- **No timeout issues** - Persistent session management
- **Enhanced uploads** - Up to 5MB file processing
- **Performance tuned** - Efficient resource usage
- **Error recovery** - Comprehensive fallback mechanisms

## 🌐 Access Points

- **Local**: http://localhost:8501
- **Network**: http://0.0.0.0:8501
- **Docker**: http://localhost:8501

## 🔧 Troubleshooting

### Common Issues
```bash
# Port conflict
lsof -ti:8501 | head -1 | xargs kill -9

# Different port
python -m streamlit run app.py --server.port 8502

# Check configuration
cat streamlit_config.toml
```

### Performance Tips
- Keep articles under 10,000 characters
- Use direct news article URLs
- Clear browser cache if map doesn't load
- Check API key configuration in .env file

## 📊 Production Features

- **Zero downtime** - Optimized for continuous operation
- **Scalable** - Handles multiple concurrent users
- **Secure** - Input validation and sanitization
- **Monitored** - Comprehensive error logging