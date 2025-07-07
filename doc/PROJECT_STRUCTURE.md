# Pinthenews Project Structure

## 📁 Core Files

```
Pinthenews/
  ├── .venv/                      # Virtual environment (created during setup)
  ├── .env                        # API keys (create manually)
  ├── agents/                     # AI location extraction agents
  │   ├── __init__.py            # Package initialization
  │   └── location_agents.py     # CrewAI multi-agent system
  ├── doc/                        # Documentation
  │   ├── CODE_QUALITY_ASSESSMENT.md
  │   ├── DEPLOYMENT.md
  │   ├── DOCUMENTATION_ASSESSMENT.md
  │   ├── EDGE_CASE_TESTING.md
  │   ├── PROJECT_STRUCTURE.md
  │   └── REPRODUCIBILITY_ASSESSMENT.md
  ├── src/                        # Core application code
  │   ├── app.py                 # Main Streamlit application
  │   ├── mcp_integration.py     # MCP client integration
  │   ├── run.py                 # Application launcher
  │   └── setup_verification.py  # Environment validation script
  ├── test/                       # Testing
  │   └── test_suite.py          # Comprehensive test suite
  ├── docker-compose.yml          # Docker Compose configuration
  ├── Dockerfile                  # Docker container configuration
  ├── requirements.txt            # Python dependencies
  ├── runtime.txt                 # Python runtime specification
  ├── start.sh                    # Quick start script
  └── streamlit_config.toml       # Streamlit configuration
```

## 🤖 AI Components

```
agents/
├── __init__.py              # Package initialization
└── location_agents.py       # CrewAI multi-agent system for location extraction
```

```
mcp_integration.py           # MCP client integration and context management
```

## 🐳 Deployment

```
Dockerfile                   # Docker container configuration
docker-compose.yml          # Docker Compose setup
runtime.txt                 # Python runtime specification
```

## 📚 Documentation

```
README.md                   # Main project documentation
DEPLOYMENT.md               # Deployment guide and troubleshooting
EDGE_CASE_TESTING.md       # Comprehensive testing documentation
PROJECT_STRUCTURE.md       # This file - project organization
```

## 🧪 Testing

```
test_suite.py              # Comprehensive test suite for all edge cases
```

## 🔧 Configuration Files

### `.env` (Create manually)
```bash
ANTHROPIC_API_KEY=your_api_key_here
```

### `streamlit_config.toml`
- No-timeout configuration
- Enhanced upload limits
- Production optimizations
- Security settings

## 📊 File Purposes

| File | Purpose | Status |
|------|---------|--------|
| `app.py` | Main application with UI and logic | ✅ Production ready |
| `run.py` | Launcher with checks and browser opening | ✅ Production ready |
| `start.sh` | Quick start script | ✅ Production ready |
| `agents/location_agents.py` | AI location extraction system | ✅ Production ready |
| `mcp_integration.py` | MCP client integration | ✅ Production ready |
| `test_suite.py` | Comprehensive testing | ✅ 100% pass rate |

## 🚀 Getting Started

1. **Install dependencies**: `pip install -r requirements.txt`
2. **Configure API key**: Create `.env` with your Anthropic API key
3. **Launch application**: `./start.sh` or `python run.py`
4. **Access**: Open http://localhost:8501

## 🛠️ Development

- **Main app**: Edit `app.py` for UI and functionality changes
- **AI agents**: Modify `agents/location_agents.py` for extraction logic
- **Configuration**: Update `streamlit_config.toml` for app settings
- **Testing**: Run `python test_suite.py` for validation

## 📦 Dependencies

All dependencies are managed in `requirements.txt`:
- **Streamlit**: Web framework
- **Anthropic**: AI API
- **CrewAI**: Multi-agent system
- **Folium**: Interactive mapping
- **GeoPy**: Geocoding services
- **BeautifulSoup**: Web scraping