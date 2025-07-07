# 🌍 Pinthenews

> **Interactive News Location Analysis with AI-Powered Mapping**

Transform news articles into interactive geographic insights! Pinthenews uses advanced AI to extract and visualize locations from news content, featuring real-time mapping and conversational analysis with enhanced connectivity and no timeout limits.

## ⚡ Quick Start

```bash
# 1. Clone and setup
git clone <repository-url> && cd Pinthenews
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2. Install dependencies  
pip install -r requirements.txt

# 3. Configure API key
echo "ANTHROPIC_API_KEY=your_key_here" > .env

# 4. Launch application
./start.sh
# Open: http://localhost:8501
```

## 📋 Table of Contents

### 🚀 Getting Started
- [Prerequisites](#-prerequisites)
- [Installation](#-installation) 
- [Configuration](#-configuration)
- [Running the App](#️-running-the-app)

### 📖 Using Pinthenews
- [Features](#-features)
- [Usage Guide](#-usage-guide)
- [Examples](#-examples)

### 🔧 Advanced
- [Enhanced Connectivity](#-enhanced-connectivity)
- [Troubleshooting](#-troubleshooting)
- [Development](#-development)
- [Project Structure](#-project-structure)

## 🔧 Prerequisites

| Requirement | Version | Purpose |
|-------------|---------|---------|
| **Python** | 3.8+ (Recommended: 3.10+) | Core runtime |
| **pip** | Latest | Package management |
| **Git** | Any | Repository cloning |
| **System** | 4GB+ RAM, 500MB storage | Performance |
| **Internet** | Stable connection | API calls & geocoding |

**Quick Verification:**
```bash
python --version && pip --version && git --version
```

### Option 1: Automated Setup (Recommended)
```bash
git clone <repository-url> && cd Pinthenews
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate  
pip install -r requirements.txt
```

### Option 2: Manual Step-by-Step
```bash
# 1. Get the code
git clone <repository-url>
cd Pinthenews

# 2. Create isolated environment  
python -m venv .venv

# 3. Activate environment
source .venv/bin/activate  # macOS/Linux
# OR
.venv\Scripts\activate     # Windows

# 4. Install dependencies
pip install -r requirements.txt
```

### 📋 Core Dependencies
| Package | Version | Purpose |
|---------|---------|---------|
| `streamlit` | 1.46+ | Web interface |
| `anthropic` | 0.57+ | AI processing |
| `crewai` | 0.70+ | Multi-agent system |
| `folium` | 0.18+ | Interactive maps |
| `streamlit-folium` | 0.25+ | Map integration |

### 🔐 API Key Setup
1. **Get Your Key** → [Anthropic Console](https://console.anthropic.com/)
   - Sign up/login → "API Keys" → Create new key (starts with `sk-ant-`)

2. **Configure Locally**:
   ```bash
   # Quick setup
   echo "ANTHROPIC_API_KEY=your_actual_key_here" > .env
   
   # Verify setup
   python -c "from dotenv import load_dotenv; load_dotenv(); import os; print('✅ Configured' if os.getenv('ANTHROPIC_API_KEY') else '❌ Missing')"
   ```

### 🚀 Launch Options

| Method | Command | Best For |
|--------|---------|----------|
| **Quick Start** | `./start.sh` | First-time users |
| **Manual** | `streamlit run src/app.py` | Development |
| **Python Launcher** | `python run_server.py` | Enhanced connectivity |
| **Docker** | `docker-compose up` | Production |

### 🏃‍♂️ Quick Launch
```bash
# Automated launch (recommended)
chmod +x start.sh && ./start.sh

# Manual launch
source .venv/bin/activate
python -m streamlit run src/app.py --server.address=localhost --server.port=8501

# Enhanced connectivity launcher
python run_server.py
```

**🌐 Access:** [http://localhost:8501](http://localhost:8501)

## ✅ Verification

### 🔍 Quick Health Check
```bash
# 1. Verify installation
python src/setup_verification.py

# 2. Run test suite  
python test/test_suite.py

# 3. Access interface
open http://localhost:8501  # macOS
# or visit manually in browser
```

### 🧪 Manual Testing
| Test | Action | Expected Result |
|------|--------|----------------|
| **URL Analysis** | Paste BBC/Reuters URL | Map shows location pins |
| **Text Analysis** | Enter "Paris, Tokyo, London" | 3 pins on map |
| **AI Chat** | Ask "What locations were found?" | Detailed response |
| **Export** | Click download button | JSON file downloads |

### 🎯 Core Capabilities
| Feature | Description | Use Case |
|---------|-------------|----------|
| **🗺️ Interactive Mapping** | Real-time location visualization | See geography of news events |
| **🤖 AI Analysis** | Intelligent location extraction | Understand geographic context |
| **💬 Chat Interface** | Conversational queries | Ask questions about patterns |
| **📄 Multi-Input** | URLs, text, summarization | Flexible content analysis |
| **📊 Data Export** | JSON download | Further analysis |
| **⚡ Enhanced Connectivity** | No timeout limits | Reliable processing |

### 🎮 Usage Guide

#### 📰 Analyze News Articles
```
1. Select "📰 Analyze URL"
2. Paste news article link (BBC, Reuters, etc.)
3. Watch locations appear on map
4. Click markers for details
```

#### 📝 Process Text Content  
```
1. Select "📝 Analyze Text"
2. Paste article content
3. View extracted locations
4. Explore geographic patterns
```

#### 💬 Interactive Questions
```
Example queries:
• "What locations were mentioned?"
• "Which areas have the most events?"
• "Are there any geographic patterns?"
• "What's the significance of these locations?"
```

## ⚡ Enhanced Connectivity

### 🚀 New Features
- **No Timeout Limits** - Extended request timeouts (60s → 120s with retry)
- **Auto-Retry Logic** - Automatic retry on connection failures
- **Better Error Handling** - Improved connection resilience  
- **Socket Optimization** - Enhanced network operation handling
- **Robust Launcher** - `run_server.py` for maximum reliability

### 🔧 Connection Enhancements
```bash
# Enhanced launcher with better connectivity
python run_server.py

# Manual with optimized settings
python -m streamlit run src/app.py \
  --server.address=localhost \
  --server.port=8501 \
  --server.headless=false
```

### ⚙️ Configuration
The app now includes:
- Extended socket timeouts (60s default)
- HTTP request retry mechanism  
- Enhanced error recovery
- Improved connection stability

## 🆘 Troubleshooting

### 🐛 Common Issues
| Issue | Solution | Command |
|-------|----------|---------|
| **Python not found** | Use python3 | `python3 -m streamlit run src/app.py` |
| **API key error** | Check .env file | `cat .env` |
| **Port occupied** | Kill processes | `pkill -f streamlit` |
| **Blank map** | Clear cache | Try incognito mode |
| **Connection timeout** | Use enhanced launcher | `python run_server.py` |

### 🔍 Debug Mode
```bash
# Enable debug logging
streamlit run src/app.py --logger.level debug

# Test connectivity  
python -c "import requests; print(requests.get('https://google.com').status_code)"
```

```
Pinthenews/
├── 🎯 Core Application
│   ├── src/app.py                 # Main Streamlit interface
│   ├── src/mcp_integration.py     # MCP client integration  
│   ├── src/setup_verification.py  # Environment validation
│   └── agents/location_agents.py  # AI location extraction
│
├── 🚀 Deployment & Setup
│   ├── start.sh                   # Quick launch script
│   ├── run_server.py              # Enhanced connectivity launcher
│   ├── requirements.txt           # Python dependencies
│   ├── .env                       # API keys (create manually)
│   └── .venv/                     # Virtual environment
│
├── 🧪 Testing & Validation  
│   ├── test/test_suite.py         # Comprehensive tests
│   └── src/setup_verification.py  # Health checks
│
├── 📚 Documentation
│   ├── README.md                  # This file
│   └── doc/                       # Detailed documentation
│
└── 🐳 Deployment Options
    ├── Dockerfile                 # Container setup
    ├── docker-compose.yml         # Multi-service deployment
    ├── service-deployed.yaml      # Service deployment configuration
    └── streamlit_config.toml       # App configuration
```

### 🔧 Key Components
| Component | Purpose | Modify When |
|-----------|---------|-------------|
| **src/app.py** | Main UI & logic | Adding features |
| **agents/location_agents.py** | AI extraction | Algorithm updates |
| **start.sh** | Quick deployment | Launch optimization |
| **run_server.py** | Enhanced launcher | Connectivity issues |
| **.env** | API configuration | Key updates |

## 👩‍💻 Development

### 🛠️ Development Mode
```bash
# Enable hot reload
export STREAMLIT_ENV=development
streamlit run src/app.py --server.runOnSave true

# Debug mode
streamlit run src/app.py --logger.level debug
```

## 📋 Examples

### 🌍 Real-World Use Cases
```bash
# Analyze breaking news
URL: https://www.bbc.com/news/world-europe-67890123
Result: Shows European conflict locations on map

# Track global events  
Text: "Protests in Paris, meetings in Geneva, floods in Bangladesh"
Result: 3 pins showing event locations + context

# Research geographic patterns
Query: "Which regions are mentioned most frequently?"
Result: AI analysis of geographic distribution
```

## 🔗 Quick Reference Card

### ⚡ Express Setup
```bash
git clone <repo> && cd Pinthenews
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
echo "ANTHROPIC_API_KEY=your_key" > .env
./start.sh  # → http://localhost:8501
```

### 🆘 Emergency Commands
```bash
pkill -f streamlit              # Stop server
python src/setup_verification.py  # Diagnose issues  
python test/test_suite.py       # Run tests
python run_server.py            # Enhanced launch
```

### 📞 Support Checklist
- [ ] ✅ Python 3.8+ installed
- [ ] 🔑 API key in .env file  
- [ ] 📦 Dependencies installed
- [ ] 🌐 Internet connection active
- [ ] 🚀 Port 8501 available

---

## 📝 License
Educational and development use.

**🌍 Pinthenews** - *Transform news into geographic insights with AI!* ✨