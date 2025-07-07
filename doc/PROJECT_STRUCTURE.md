# Project Structure

```
Pinthenews/
├── Dockerfile                     # Docker container configuration
├── README.md                      # Project documentation
├── docker-compose.yml             # Docker Compose configuration
├── requirements.txt               # Python dependencies
├── runtime.txt                    # Python runtime version
├── run_server.py                  # Server execution script
├── start.sh                       # Startup script
├── streamlit_config.toml          # Streamlit configuration
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

- **agents/**: Contains agent-related modules for location-based functionality
- **doc/**: Project documentation and assessments
- **src/**: Main source code directory with application logic
- **test/**: Test files and test suite
- **Root files**: Configuration files for Docker, Python dependencies, and application startup