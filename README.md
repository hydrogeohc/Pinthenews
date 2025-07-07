# 🌍 Pinthenews

**Interactive News Location Analysis with AI-Powered Mapping**

Pinthenews uses AI to extract and visualize geographical locations from news articles, featuring an interactive map and AI assistant for conversational analysis.

## 📋 Table of Contents
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [API Key Configuration](#api-key-configuration)
- [Running the Application](#running-the-application)
- [Verification & Testing](#verification--testing)
- [Usage](#usage)
- [Troubleshooting](#troubleshooting)
- [Development](#development)

## 🔧 Prerequisites
- **Python**: 3.8+ (Recommended: 3.10+)
- **pip**: Python package installer
- **Git**: For cloning the repository
- **System**: 4GB+ RAM, 500MB free storage, Windows 10+/macOS 10.14+/Ubuntu 18.04+
- **Internet**: For API calls and geocoding

**Verify**:
```bash
python --version  # Should show 3.8+
pip --version
git --version
```

## 🚀 Setup
1. **Clone or Download**:
   ```bash
   git clone <repository-url>
   cd Pinthenews
   # Or download and extract ZIP, then cd to folder
   ```

2. **Create Virtual Environment**:
   ```bash
   python -m venv .venv
   # Windows: .venv\Scripts\activate
   # macOS/Linux: source .venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   # Verify: pip list | grep -E "(streamlit|anthropic|crewai|folium)"
   ```

**Expected packages**:
```
anthropic       0.57.1
crewai          0.70.0
folium          0.18.0
streamlit       1.40.0
streamlit-folium 0.25.0
```

## 🔑 API Key Configuration
1. **Get Anthropic API Key**:
   - Visit [Anthropic Console](https://console.anthropic.com/)
   - Sign up/login, navigate to "API Keys," create key (`sk-ant-...`)
   - Save securely

2. **Set Environment Variable**:
   ```bash
   # Create .env file
   echo "ANTHROPIC_API_KEY=your_key_here" > .env
   # Verify
   cat .env
   ```

3. **Verify Configuration**:
   ```bash
   python -c "from dotenv import load_dotenv; load_dotenv(); import os; print('✅ API key configured' if os.getenv('ANTHROPIC_API_KEY') else '❌ API key missing')"
   ```

## ▶️ Running the Application
**Quick Start**:
```bash
chmod +x start.sh  # macOS/Linux
./start.sh
```
- Checks .env, updates dependencies, and launches on port 8501

**Manual Start**:
```bash
source .venv/bin/activate  # macOS/Linux
# or .venv\Scripts\activate  # Windows
python -m streamlit run src/app.py --server.port 8501
```

**Using Python Launcher**:
```bash
python src/run.py
```

**Docker (Optional)**:
```bash
docker build -t pinthenews .
docker run -p 8501:8501 --env-file .env pinthenews
```

## ✅ Verification & Testing
1. **Access**: Open [http://localhost:8501](http://localhost:8501)
   - Expect: Interactive map (left), AI chat (right)

2. **Verify Setup**:
   ```bash
   python src/setup_verification.py
   ```
   - Checks Python, dependencies, and API configuration

3. **Run Tests**:
   ```bash
   python test/test_suite.py
   ```
   - Validates URL/text analysis, error handling, and performance

4. **Manual Tests**:
   - **URL Analysis**: Paste news URL (e.g., BBC), check map pins
   - **Text Analysis**: Input text with locations (e.g., "Paris, Tokyo"), verify pins
   - **AI Assistant**: Ask "What locations were mentioned?"

## 📖 Usage
- **Interface**: Map (left) for location pins; AI chat (right) for analysis
- **Input Types**:
  - **URL**: Analyze news articles (e.g., BBC, Reuters)
  - **Text**: Extract locations from pasted text
  - **Summarize**: Summarize long articles
  - **Ask Questions**: Query locations or patterns
- **Export**: Download location data as JSON

## 🆘 Troubleshooting
- **Python not found**:
  ```bash
  python3 -m pip install -r requirements.txt
  python3 -m streamlit run src/app.py
  ```
- **API key error**:
  ```bash
  cat .env  # Ensure ANTHROPIC_API_KEY=sk-ant-...
  ```
- **Port 8501 in use**:
  ```bash
  lsof -ti:8501 | xargs kill -9
  ```
- **Blank map**:
  - Clear browser cache
  - Check internet connection
  - Try incognito mode
- **Slow performance**:
  - Use shorter articles
  - Verify API key limits
  - Restart application

**Debug**:
```bash
streamlit run src/app.py --logger.level debug
```

## 👩‍💻 Development
- **Development Setup**:
  ```bash
  export STREAMLIT_ENV=development
  streamlit run src/app.py --server.runOnSave true
  ```

- **Project Structure**:
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

- **Key Files**:
  - `src/app.py`: Main application logic and UI
  - `agents/location_agents.py`: AI location extraction system
  - `requirements.txt`: Python dependencies
  - `.env`: API keys and environment variables
  - `streamlit_config.toml`: Application settings
  - `start.sh`: Automated setup and launch script

- **File Purposes**:
  | File/Directory | Purpose | When to Modify |
  |----------------|---------|----------------|
  | `src/app.py` | Main application logic | UI changes, feature updates |
  | `agents/location_agents.py` | AI extraction logic | Algorithm improvements |
  | `requirements.txt` | Dependencies | Adding new packages |
  | `.env` | Secrets and API keys | Key rotation, new APIs |
  | `streamlit_config.toml` | App configuration | Performance tuning |
  | `test/test_suite.py` | Testing framework | Adding new tests |
  | `doc/` | Documentation | Updates and guides |

## 📝 License
For educational and development purposes.

## 🔗 Quick Reference
```bash
# Setup
pip install -r requirements.txt
echo "ANTHROPIC_API_KEY=your_key" > .env

# Verify
python src/setup_verification.py

# Run
./start.sh

# Test
python test/test_suite.py

# Access
http://localhost:8501
```

### Need Help?
1. 📖 Check documentation in `doc/` folder
2. 🔧 Run `python src/setup_verification.py` for diagnosis
3. 🧪 Run `python test/test_suite.py` for functionality tests
4. 🔍 Review error messages in the app
5. 🛠️ Verify all prerequisites are met

---

**Pinthenews** - Interactive news geography with AI! 🌍✨