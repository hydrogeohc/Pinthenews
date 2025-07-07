# 📁 Project Structure

This document outlines the complete directory structure and file organization of the Pinthenews project.

## 🎯 Core Application
```
src/
├── app.py                 # Main Streamlit interface
├── mcp_integration.py     # MCP client integration  
├── setup_verification.py  # Environment validation
└── agents/
    └── location_agents.py  # AI location extraction
```

## 🚀 Deployment & Setup
```
├── start.sh                   # Quick launch script
├── run_server.py              # Enhanced connectivity launcher
├── requirements.txt           # Python dependencies
├── .env                       # API keys (create manually)
└── .venv/                     # Virtual environment
```

## 🧪 Testing & Validation
```
test/
├── test_suite.py         # Comprehensive tests
└── src/
    └── setup_verification.py  # Health checks
```

## 📚 Documentation
```
├── README.md                  # Main project documentation
├── PROJECT STRUCTURE.md       # This file
└── doc/                       # Detailed documentation
```

## 🐳 Deployment Options
```
├── Dockerfile                 # Container setup
├── docker-compose.yml         # Multi-service deployment
├── service-deployed.yaml      # Service deployment configuration
└── streamlit_config.toml       # App configuration
```

## 📋 File Descriptions

### Core Files
| File | Purpose | Status |
|------|---------|--------|
| **src/app.py** | Main Streamlit interface | Core |
| **agents/location_agents.py** | AI location extraction | Core |
| **start.sh** | Quick launch script | Core |
| **run_server.py** | Enhanced connectivity launcher | Core |

### Configuration Files
| File | Purpose | Status |
|------|---------|--------|
| **requirements.txt** | Python dependencies | Core |
| **.env** | API keys configuration | User-created |
| **service-deployed.yaml** | Service deployment configuration | Deployment |
| **streamlit_config.toml** | App configuration | Optional |

### Deployment Files
| File | Purpose | Status |
|------|---------|--------|
| **Dockerfile** | Container setup | Deployment |
| **docker-compose.yml** | Multi-service deployment | Deployment |
| **service-deployed.yaml** | Service deployment configuration | Deployment |

### Documentation Files
| File | Purpose | Status |
|------|---------|--------|
| **README.md** | Main project documentation | Core |
| **PROJECT STRUCTURE.md** | Project structure documentation | Core |