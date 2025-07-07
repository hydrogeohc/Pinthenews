#!/usr/bin/env python3
"""
Robust Pinthenews Server Launcher
Enhanced connectivity and no timeout limits
"""
import os
import sys
import subprocess
import time
import signal
import socket
from pathlib import Path

def check_port(port, host='localhost'):
    """Check if port is available"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex((host, port))
            return result != 0  # True if port is available
    except:
        return True

def kill_existing_streamlit():
    """Kill any existing Streamlit processes"""
    try:
        subprocess.run(['pkill', '-f', 'streamlit.*app.py'], 
                      capture_output=True, check=False)
        time.sleep(2)
    except:
        pass

def main():
    """Launch Pinthenews with enhanced connectivity"""
    print("🌍 Starting Pinthenews with enhanced connectivity...")
    print("=" * 50)
    
    # Check .env file
    env_file = Path('.env')
    if not env_file.exists():
        print("⚠️  .env file not found. Creating template...")
        with open('.env', 'w') as f:
            f.write("ANTHROPIC_API_KEY=your_anthropic_api_key_here\n")
        print("📝 Please edit .env file with your API key before running again")
        sys.exit(1)
    
    # Check API key
    with open('.env', 'r') as f:
        if 'your_anthropic_api_key_here' in f.read():
            print("❌ Please configure your ANTHROPIC_API_KEY in the .env file")
            sys.exit(1)
    
    # Clean up existing processes
    print("🔄 Cleaning up existing processes...")
    kill_existing_streamlit()
    
    # Check if port is available
    port = 8501
    if not check_port(port):
        print(f"⚠️  Port {port} is still in use. Waiting...")
        time.sleep(5)
        if not check_port(port):
            print(f"❌ Port {port} is still occupied. Please manually kill processes.")
            sys.exit(1)
    
    # Install dependencies
    print("📦 Installing dependencies...")
    subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt', '-q'],
                  check=False)
    
    # Set environment variables for better connectivity
    os.environ['STREAMLIT_SERVER_MAX_MESSAGE_SIZE'] = '1000'
    os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'
    os.environ['STREAMLIT_SERVER_ENABLE_CORS'] = 'true'
    
    # Launch Streamlit
    print("🚀 Launching Pinthenews...")
    print("🌐 Application will be available at: http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop the application")
    print("=" * 50)
    
    # Streamlit command with enhanced settings
    cmd = [
        sys.executable, '-m', 'streamlit', 'run', 'src/app.py',
        '--server.port=8501',
        '--server.address=localhost', 
        '--server.headless=false',
        '--server.fileWatcherType=none',
        '--server.enableCORS=true',
        '--server.enableXsrfProtection=false',
        '--server.maxUploadSize=1000',
        '--browser.gatherUsageStats=false',
        '--client.toolbarMode=minimal',
        '--client.showErrorDetails=true'
    ]
    
    # Handle Ctrl+C gracefully
    def signal_handler(sig, frame):
        print("\n🛑 Shutting down Pinthenews...")
        kill_existing_streamlit()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        # Run Streamlit
        process = subprocess.Popen(cmd)
        process.wait()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down Pinthenews...")
        kill_existing_streamlit()
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()