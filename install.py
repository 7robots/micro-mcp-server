#!/usr/bin/env python3
"""Install script for the Micro.blog Books MCP Server dependencies."""

import subprocess
import sys
from pathlib import Path


def install_dependencies():
    """Install required dependencies."""
    requirements_file = Path(__file__).parent / "requirements.txt"
    
    print("Installing dependencies...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
        ])
        print("✓ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install dependencies: {e}")
        return False
    
    return True


def test_server():
    """Test that the server can be imported and created."""
    try:
        from micro_mcp_server.server import create_server
        server = create_server("test_token")
        print("✓ Server can be created successfully")
        return True
    except Exception as e:
        print(f"✗ Server test failed: {e}")
        print("  Make sure you've installed the dependencies with pip install -r requirements.txt")
        return False


if __name__ == "__main__":
    print("Setting up Micro.blog Books MCP Server...")
    
    if install_dependencies() and test_server():
        print("\n✓ Setup complete! The server is ready to use.")
        print("\nNext steps:")
        print("1. Set your bearer token: export MICRO_BLOG_BEARER_TOKEN='your_token'")
        print("2. Generate Claude Desktop configuration: python get_config.py")
        print("3. Add the configuration to Claude Desktop and restart")
    else:
        print("\n✗ Setup failed. Please check the errors above.")
        sys.exit(1)