#!/usr/bin/env python3
"""Generate Claude Desktop configuration for the Micro.blog Books MCP Server."""

import json
import os
import shutil
import sys
from pathlib import Path


def get_python_path():
    """Get the full path to the Python executable."""
    # Try different Python executables in order of preference
    # FastMCP has lower requirements (Python 3.8+)
    python_candidates = [
        shutil.which("python3"),  # Current environment Python (usually newer)
        sys.executable,           # The Python running this script
        shutil.which("python"),
        "/usr/bin/python3",      # System Python
    ]
    
    for python_path in python_candidates:
        if python_path and Path(python_path).exists():
            # Test if this Python version supports FastMCP
            try:
                import subprocess
                result = subprocess.run(
                    [python_path, "-c", "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"],
                    capture_output=True, text=True, timeout=5
                )
                if result.returncode == 0:
                    version = result.stdout.strip()
                    major, minor = map(int, version.split('.'))
                    if major > 3 or (major == 3 and minor >= 8):
                        print(f"Found compatible Python {version} at: {python_path}")
                        return python_path
                    else:
                        print(f"Python {version} at {python_path} is too old (need 3.8+)")
            except Exception as e:
                print(f"Failed to test Python at {python_path}: {e}")
                continue
    
    raise RuntimeError("No compatible Python executable found (need Python 3.8+)")


def generate_config():
    """Generate the Claude Desktop configuration."""
    python_path = get_python_path()
    server_path = str(Path(__file__).parent / "run_server.py")
    
    config = {
        "mcpServers": {
            "micro-books": {
                "command": python_path,
                "args": [server_path],
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
        print("3. Add it to your Claude Desktop config file:")
        print("   - macOS: ~/Library/Application Support/Claude/claude_desktop_config.json")
        print("   - Windows: %APPDATA%\\Claude\\claude_desktop_config.json")
        print("4. Restart Claude Desktop")
        
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