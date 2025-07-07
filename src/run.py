#!/usr/bin/env python3
"""
Pinthenews Application Launcher
Simple launcher script with dependency checking and browser integration
"""

import os
import sys
import subprocess
from pathlib import Path
import webbrowser
import time

def check_api_key():
    """Check if API key is configured"""
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key or api_key == "your_anthropic_api_key_here":
        print("❌ ANTHROPIC_API_KEY not configured")
        print("\n🔧 Setup Instructions:")
        print("1. Edit the .env file in this directory")
        print("2. Replace 'your_anthropic_api_key_here' with your actual API key")
        print("3. Save the file and run this script again")
        print("\nGet your API key from: https://console.anthropic.com/")
        return False
    
    print(f"✅ API key configured: {api_key[:10]}...")
    return True

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'streamlit',
        'streamlit_folium',
        'anthropic',
        'crewai',
        'folium',
        'requests',
        'beautifulsoup4',
        'geopy',
        'pandas',
        'plotly'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'streamlit_folium':
                __import__('streamlit_folium')
            else:
                __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("\n🔧 Install missing packages:")
        print(f"uv pip install {' '.join(missing_packages)}")
        return False
    
    print("✅ All dependencies installed")
    return True

def launch_application():
    """Launch the Streamlit application"""
    print("\n🚀 Launching Pinthenews...")
    print("Enhanced UI with Interactive Map + Q&A Chatbot")
    print("=" * 60)
    
    try:
        # Launch Streamlit with no timeout configuration
        cmd = [
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", "8501",
            "--server.address", "0.0.0.0",
            "--server.headless", "false",
            "--server.runOnSave", "false",
            "--server.allowRunOnSave", "false",
            "--server.maxUploadSize", "1000",
            "--server.maxRequestSize", "1000",
            "--server.enableStaticServing", "true",
            "--server.fileWatcherType", "none"
        ]
        
        print("🌐 Starting web server...")
        print("📱 The application will open automatically in your browser")
        print("🔗 URL: http://localhost:8501")
        print("\n💡 Features:")
        print("   • Interactive map with real-time location markers")
        print("   • AI-powered Q&A chatbot for location analysis")
        print("   • URL and text input for news articles")
        print("   • Export capabilities for data analysis")
        print("\n📋 Usage:")
        print("   1. Use the chatbot to analyze news articles")
        print("   2. Watch locations appear on the map in real-time")
        print("   3. Click map markers for detailed information")
        print("   4. Ask questions about the locations found")
        print("\n⏹️  Press Ctrl+C to stop the application")
        print("=" * 60)
        
        # Small delay then open browser
        def open_browser():
            time.sleep(3)
            webbrowser.open('http://localhost:8501')
        
        import threading
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        # Run Streamlit
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
        return 0
    except Exception as e:
        print(f"\n❌ Error launching application: {e}")
        return 1

def main():
    """Main launcher function"""
    print("🌍 Pinthenews - Enhanced UI Launcher")
    print("=" * 60)
    
    # Check current directory
    current_dir = Path.cwd()
    print(f"📁 Working directory: {current_dir}")
    
    # Check if we're in the right directory
    required_files = ["app.py", "agents/location_agents.py", "mcp_integration.py"]
    missing_files = []
    
    for file in required_files:
        if not (current_dir / file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        print("Please ensure you're in the correct project directory")
        return 1
    
    print("✅ All required files found")
    
    # Check API key
    print("\n🔑 Checking API configuration...")
    if not check_api_key():
        return 1
    
    # Check dependencies
    print("\n📦 Checking dependencies...")
    if not check_dependencies():
        return 1
    
    # Launch application
    return launch_application()

if __name__ == "__main__":
    sys.exit(main())