#!/usr/bin/env python3
"""
Compatibility checker for Micro.blog Books Python DXT extension.
Run this before installing to verify your system meets the requirements.
"""

import sys
import subprocess
import platform

def check_python_version():
    """Check if Python version meets requirements."""
    print("🐍 Checking Python version...")
    
    required = (3, 10)
    current = sys.version_info[:2]
    
    print(f"   Current: Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    print(f"   Required: Python {required[0]}.{required[1]}+")
    
    if current >= required:
        print("   ✅ Python version compatible")
        return True
    else:
        print("   ❌ Python version too old")
        return False

def check_packages():
    """Check if required packages can be imported."""
    print("\n📦 Checking required packages...")
    
    packages = ["fastmcp", "httpx", "click"]
    all_available = True
    
    for package in packages:
        try:
            __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} (will be bundled in extension)")
            # This is OK - packages are bundled
    
    return True

def get_upgrade_instructions():
    """Get platform-specific upgrade instructions."""
    system = platform.system().lower()
    
    print("\n📋 Python upgrade instructions:")
    
    if system == "darwin":  # macOS
        print("   Option 1: Download from python.org")
        print("   Option 2: Use Homebrew: brew install python@3.10")
        print("   Option 3: Use pyenv: pyenv install 3.10.12 && pyenv global 3.10.12")
    elif system == "windows":
        print("   Option 1: Download from python.org")
        print("   Option 2: Use Microsoft Store")
        print("   Option 3: Use Chocolatey: choco install python310")
    elif system == "linux":
        print("   Ubuntu/Debian: sudo apt update && sudo apt install python3.10")
        print("   CentOS/RHEL: sudo yum install python3.10")
        print("   Fedora: sudo dnf install python3.10")
        print("   Arch: sudo pacman -S python")
    else:
        print("   Please install Python 3.10+ from python.org")

def main():
    """Run compatibility checks."""
    print("🔍 Micro.blog Books Extension - Compatibility Check")
    print("=" * 50)
    
    python_ok = check_python_version()
    packages_ok = check_packages()
    
    print("\n📊 Results:")
    print("=" * 20)
    
    if python_ok:
        print("✅ Your system is compatible with this extension!")
        print("\nYou can now install the extension:")
        print("1. Open Claude Desktop")
        print("2. Go to Settings → Extensions")
        print("3. Click 'Install Extension'")
        print("4. Select the .dxt file")
    else:
        print("❌ Your system needs updates before installing this extension.")
        get_upgrade_instructions()
        print(f"\nAfter upgrading, run this script again to verify compatibility.")
    
    return 0 if python_ok else 1

if __name__ == "__main__":
    sys.exit(main())