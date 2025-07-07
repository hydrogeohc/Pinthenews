#!/usr/bin/env python3
"""
Pinthenews Setup Verification Script
Comprehensive checks to ensure the environment is properly configured
"""

import sys
import os
import subprocess
import importlib
from pathlib import Path

def print_header(title):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"🔍 {title}")
    print("=" * 60)

def print_status(check, status, details=""):
    """Print check status with consistent formatting"""
    icon = "✅" if status else "❌"
    print(f"{icon} {check}")
    if details:
        print(f"   {details}")

def check_python_version():
    """Check Python version compatibility"""
    print_header("Python Environment Check")
    
    version = sys.version_info
    python_version = f"{version.major}.{version.minor}.{version.micro}"
    
    # Check minimum Python version (3.8+)
    is_compatible = version >= (3, 8)
    
    print_status(
        f"Python Version: {python_version}",
        is_compatible,
        "Minimum required: Python 3.8+" if not is_compatible else "Compatible"
    )
    
    # Check pip availability
    try:
        import pip
        pip_version = pip.__version__
        print_status(f"pip Version: {pip_version}", True)
    except ImportError:
        print_status("pip Installation", False, "pip not found - install with: python -m ensurepip")
    
    return is_compatible

def check_project_structure():
    """Verify project files are present"""
    print_header("Project Structure Check")
    
    required_files = [
        "app.py",
        "requirements.txt", 
        "start.sh",
        "run.py",
        "streamlit_config.toml",
        "agents/location_agents.py",
        "mcp_integration.py"
    ]
    
    all_present = True
    current_dir = Path.cwd()
    
    for file_path in required_files:
        file_exists = (current_dir / file_path).exists()
        print_status(f"File: {file_path}", file_exists)
        if not file_exists:
            all_present = False
    
    return all_present

def check_dependencies():
    """Check if all required packages are installed"""
    print_header("Dependencies Check")
    
    required_packages = [
        ("streamlit", "1.40.0"),
        ("anthropic", "0.57.1"),
        ("crewai", "0.70.0"),
        ("folium", "0.18.0"),
        ("streamlit_folium", "0.25.0"),
        ("geopy", "2.4.0"),
        ("pandas", "2.2.0"),
        ("requests", "2.32.0"),
        ("beautifulsoup4", "4.12.0"),
        ("python-dotenv", "1.1.1"),
        ("plotly", "5.18.0")
    ]
    
    all_installed = True
    
    for package, min_version in required_packages:
        try:
            # Import the package
            if package == "beautifulsoup4":
                import bs4 as imported_package
            elif package == "python-dotenv":
                import dotenv as imported_package
            elif package == "streamlit_folium":
                import streamlit_folium as imported_package
            else:
                imported_package = importlib.import_module(package)
            
            # Try to get version
            try:
                if hasattr(imported_package, "__version__"):
                    version = imported_package.__version__
                else:
                    version = "unknown"
                print_status(f"{package}: {version}", True)
            except:
                print_status(f"{package}: installed", True, "Version check failed but package is available")
                
        except ImportError:
            print_status(f"{package}: NOT INSTALLED", False, f"Install with: pip install {package}>={min_version}")
            all_installed = False
    
    return all_installed

def check_api_configuration():
    """Check API key configuration"""
    print_header("API Configuration Check")
    
    # Check .env file existence
    env_file = Path(".env")
    if not env_file.exists():
        print_status(".env file", False, "Run ./start.sh to create template or create manually")
        return False
    
    print_status(".env file exists", True)
    
    # Load and check API key
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv("ANTHROPIC_API_KEY")
        
        if not api_key:
            print_status("ANTHROPIC_API_KEY", False, "Key not found in .env file")
            return False
        elif api_key == "your_anthropic_api_key_here" or api_key == "your_actual_api_key_here":
            print_status("ANTHROPIC_API_KEY", False, "Please replace with your actual API key")
            return False
        elif api_key.startswith("sk-ant-"):
            print_status("ANTHROPIC_API_KEY format", True, f"Key starts with: {api_key[:15]}...")
            return True
        else:
            print_status("ANTHROPIC_API_KEY format", False, "Key should start with 'sk-ant-'")
            return False
            
    except Exception as e:
        print_status("API key validation", False, f"Error: {str(e)}")
        return False

def check_network_connectivity():
    """Check internet connectivity and API access"""
    print_header("Network Connectivity Check")
    
    # Test basic internet connectivity
    try:
        import urllib.request
        urllib.request.urlopen('https://www.google.com', timeout=5)
        print_status("Internet connectivity", True)
    except:
        print_status("Internet connectivity", False, "Check your internet connection")
        return False
    
    # Test API connectivity (if key is configured)
    try:
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.getenv("ANTHROPIC_API_KEY")
        
        if api_key and api_key.startswith("sk-ant-"):
            import anthropic
            client = anthropic.Anthropic(api_key=api_key)
            # Simple API test
            response = client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=10,
                messages=[{"role": "user", "content": "Hello"}]
            )
            print_status("Anthropic API access", True, "API key working correctly")
            return True
        else:
            print_status("Anthropic API access", False, "Configure API key first")
            return False
            
    except Exception as e:
        print_status("Anthropic API access", False, f"API error: {str(e)}")
        return False

def check_port_availability():
    """Check if port 8501 is available"""
    print_header("Port Availability Check")
    
    import socket
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('127.0.0.1', 8501))
        sock.close()
        
        if result == 0:
            print_status("Port 8501", False, "Port is in use - run: lsof -ti:8501 | xargs kill -9")
            return False
        else:
            print_status("Port 8501", True, "Available for use")
            return True
    except:
        print_status("Port 8501", True, "Available for use")
        return True

def run_basic_import_test():
    """Test basic application imports"""
    print_header("Application Import Test")
    
    try:
        # Test core application imports
        import streamlit as st
        print_status("Streamlit import", True)
        
        import folium
        print_status("Folium import", True)
        
        from streamlit_folium import st_folium
        print_status("Streamlit-Folium import", True)
        
        import anthropic
        print_status("Anthropic import", True)
        
        from agents.location_agents import NewsLocationMappingCrew
        print_status("Location agents import", True)
        
        return True
        
    except ImportError as e:
        print_status("Application imports", False, f"Import error: {str(e)}")
        return False
    except Exception as e:
        print_status("Application imports", False, f"Error: {str(e)}")
        return False

def generate_setup_report(checks_passed, total_checks):
    """Generate final setup report"""
    print_header("Setup Verification Report")
    
    success_rate = (checks_passed / total_checks) * 100
    
    print(f"📊 Checks Passed: {checks_passed}/{total_checks} ({success_rate:.1f}%)")
    
    if success_rate == 100:
        print("🎉 SETUP COMPLETE! Your environment is ready to run Pinthenews.")
        print("\n🚀 Next steps:")
        print("   1. Run: ./start.sh")
        print("   2. Open: http://localhost:8501")
        print("   3. Test with a news article URL")
        return True
    elif success_rate >= 80:
        print("⚠️  SETUP MOSTLY COMPLETE - Minor issues detected")
        print("\n🔧 Fix the failed checks above, then run Pinthenews")
        return False
    else:
        print("❌ SETUP INCOMPLETE - Major issues detected")
        print("\n🔧 Please fix the failed checks above before proceeding")
        return False

def main():
    """Main verification function"""
    print("🌍 Pinthenews Setup Verification")
    print("This script will check if your environment is properly configured")
    
    checks = []
    
    # Run all verification checks
    checks.append(check_python_version())
    checks.append(check_project_structure())
    checks.append(check_dependencies())
    checks.append(check_api_configuration())
    checks.append(check_network_connectivity())
    checks.append(check_port_availability())
    checks.append(run_basic_import_test())
    
    # Generate report
    checks_passed = sum(checks)
    total_checks = len(checks)
    
    setup_complete = generate_setup_report(checks_passed, total_checks)
    
    # Provide specific guidance if setup is not complete
    if not setup_complete:
        print("\n📋 Common Solutions:")
        print("   • Install dependencies: pip install -r requirements.txt")
        print("   • Configure API key: echo 'ANTHROPIC_API_KEY=your_key' > .env")
        print("   • Check internet connection")
        print("   • Free port 8501: lsof -ti:8501 | xargs kill -9")
        print("\n📖 For detailed help, see README.md")
    
    return 0 if setup_complete else 1

if __name__ == "__main__":
    sys.exit(main())