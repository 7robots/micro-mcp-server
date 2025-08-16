#!/usr/bin/env python3
"""Generate Claude Desktop configuration for the Micro.blog Books MCP Server."""

import json
import os
import shutil
import sys
from pathlib import Path


def get_uv_path():
    """Get the full path to the uv executable."""
    uv_path = shutil.which("uv")
    if not uv_path:
        raise RuntimeError("uv not found. Please install uv: https://docs.astral.sh/uv/getting-started/installation/")
    
    # Test if uv is working
    try:
        import subprocess
        result = subprocess.run([uv_path, "--version"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"Found uv at: {uv_path}")
            print(f"uv version: {result.stdout.strip()}")
            return uv_path
        else:
            raise RuntimeError(f"uv is not working properly: {result.stderr}")
    except Exception as e:
        raise RuntimeError(f"Failed to test uv: {e}")


def generate_config():
    """Generate the Claude Desktop configuration."""
    uv_path = get_uv_path()
    project_path = str(Path(__file__).parent)
    server_path = str(Path(__file__).parent / "run_server.py")
    
    config = {
        "mcpServers": {
            "micro-books": {
                "command": uv_path,
                "args": ["run", "--directory", project_path, "python", server_path],
                "env": {
                    "MICRO_BLOG_BEARER_TOKEN": os.environ.get("MICRO_BLOG_BEARER_TOKEN", "your_token_here")
                }
            }
        }
    }
    
    return config


def main():
    """Main function."""
    try:
        config = generate_config()
        print("Claude Desktop Configuration:")
        print("=" * 50)
        print(json.dumps(config, indent=2))
        print("=" * 50)
        print("\nInstructions:")
        print("1. Copy the configuration above")
        print("2. If you see 'your_token_here', set MICRO_BLOG_BEARER_TOKEN environment variable first")
        print("3. Make sure uv is installed and available in your PATH")
        print("4. Add the configuration to your Claude Desktop config file:")
        print("   - macOS: ~/Library/Application Support/Claude/claude_desktop_config.json")
        print("   - Windows: %APPDATA%\\Claude\\claude_desktop_config.json")
        print("5. Restart Claude Desktop")
        
        # Also save to file
        config_file = Path(__file__).parent / "claude_desktop_config.json"
        with open(config_file, "w") as f:
            json.dump(config, f, indent=2)
        print(f"\n✓ Configuration also saved to: {config_file}")
        
    except Exception as e:
        print(f"Error generating configuration: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()