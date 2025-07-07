# Project Structure

```
Pinthenews/
├── Dockerfile                     # Docker container configuration
├── PROJECT STRUCTURE.md           # Root-level project structure
├── README.md                      # Project documentation
├── docker-compose.yml             # Docker Compose configuration
├── livedemo_notebook.ipynb        # Interactive demo notebook
├── requirements.txt               # Python dependencies
├── runtime.txt                    # Python runtime version
├── run_server.py                  # Server execution script
├── service-deployed.yaml          # Service deployment configuration
├── start.sh                       # Startup script
├── streamlit_config.toml          # Streamlit configuration
├── .env                           # Environment variables (user-created)
├── .venv/                         # Virtual environment directory
├── agents/                        # Agent modules
│   ├── __init__.py               # Package initialization
│   └── location_agents.py        # Location-based agents
├── doc/                          # Documentation
│   ├── CODE_QUALITY_ASSESSMENT.md
│   ├── DEPLOYMENT.md
│   ├── DOCUMENTATION_ASSESSMENT.md
│   ├── EDGE_CASE_TESTING.md
│   ├── PROJECT_STRUCTURE.md      # This file
│   └── REPRODUCIBILITY_ASSESSMENT.md
├── src/                          # Source code
│   ├── app.py                    # Main application
│   ├── mcp_integration.py        # MCP integration module
│   ├── run.py                    # Application runner
│   └── setup_verification.py    # Setup verification utilities
└── test/                         # Test files
    └── test_suite.py             # Test suite
```

## Directory Descriptions

### Core Directories
- **agents/**: Contains agent-related modules for location-based functionality
- **doc/**: Project documentation and assessments
- **src/**: Main source code directory with application logic
- **test/**: Test files and test suite
- **.venv/**: Virtual environment directory (created during setup)

### Key Files

#### Application Files
- **src/app.py**: Main Streamlit web interface
- **src/run.py**: Direct application runner script
- **src/mcp_integration.py**: MCP (Model Context Protocol) integration
- **src/setup_verification.py**: Environment and setup validation
- **agents/location_agents.py**: AI-powered location extraction logic

#### Launch Scripts
- **start.sh**: Quick automated launch script
- **run_server.py**: Enhanced connectivity launcher with improved error handling
- **src/run.py**: Direct application runner

#### Configuration Files
- **requirements.txt**: Python package dependencies
- **runtime.txt**: Python runtime version specification
- **streamlit_config.toml**: Streamlit application configuration
- **.env**: Environment variables and API keys (user must create)
- **service-deployed.yaml**: Service deployment configuration

#### Documentation Files
- **README.md**: Main project documentation and setup guide
- **PROJECT STRUCTURE.md**: Root-level project organization overview
- **livedemo_notebook.ipynb**: Interactive Jupyter notebook tutorial
- **doc/\*.md**: Detailed documentation files for various aspects

#### Deployment Files
- **Dockerfile**: Docker container build configuration
- **docker-compose.yml**: Multi-container deployment setup
- **service-deployed.yaml**: Service deployment configuration

#### Testing Files
- **test/test_suite.py**: Comprehensive test suite for the application

## Entry Points

| File | Purpose | Usage |
|------|---------|-------|
| `start.sh` | Quick launch | `./start.sh` |
| `src/app.py` | Direct Streamlit | `streamlit run src/app.py` |
| `src/run.py` | App runner | `python src/run.py` |
| `run_server.py` | Enhanced launch | `python run_server.py` |
| `livedemo_notebook.ipynb` | Interactive demo | `jupyter notebook` |

## Development Workflow

1. **Setup**: Use `start.sh` for initial setup and launch
2. **Development**: Use `streamlit run src/app.py` for development with hot reload
3. **Testing**: Run `python test/test_suite.py` for comprehensive testing
4. **Production**: Use `docker-compose up` for containerized deployment
5. **Learning**: Open `livedemo_notebook.ipynb` for interactive tutorials