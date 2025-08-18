#!/usr/bin/env python3
"""
Build script to package the Python DXT extension with bundled dependencies.
"""

import os
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

def main():
    """Build the Python DXT extension."""
    print("Building Python DXT extension...")
    
    # Get current directory
    current_dir = Path(__file__).parent
    output_path = current_dir / "micro-blog-books-python.dxt"
    
    # Remove existing package
    if output_path.exists():
        output_path.unlink()
    
    print("Installing dependencies to temporary directory...")
    
    # Create a temporary directory for the build
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        lib_path = temp_path / "lib"
        
        # Install dependencies directly to lib directory
        print("Installing Python packages...")
        subprocess.run([
            sys.executable, "-m", "pip", "install", 
            "-r", str(current_dir / "requirements.txt"),
            "--target", str(lib_path),
            "--no-deps"  # Install without dependencies to avoid conflicts
        ], check=True)
        
        # Then install with dependencies
        subprocess.run([
            sys.executable, "-m", "pip", "install", 
            "-r", str(current_dir / "requirements.txt"),
            "--target", str(lib_path)
        ], check=True)
        
        # Create the DXT package
        print("Creating DXT package...")
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
            # Add manifest.json
            zf.write(current_dir / "manifest.json", "manifest.json")
            print("  Added: manifest.json")
            
            # Add requirements.txt
            zf.write(current_dir / "requirements.txt", "requirements.txt")
            print("  Added: requirements.txt")
            
            # Add server files
            zf.write(current_dir / "server" / "main.py", "server/main.py")
            print("  Added: server/main.py")
            
            # Add README if it exists
            readme_path = current_dir / "README.md"
            if readme_path.exists():
                zf.write(readme_path, "README.md")
                print("  Added: README.md")
            
            # Add icon if it exists
            icon_path = current_dir / "icon.svg"
            if icon_path.exists():
                zf.write(icon_path, "icon.svg")
                print("  Added: icon.svg")
            
            # Add compatibility checker
            compat_path = current_dir / "check_compatibility.py"
            if compat_path.exists():
                zf.write(compat_path, "check_compatibility.py")
                print("  Added: check_compatibility.py")
            
            # Bundle the dependencies from lib directory
            if lib_path.exists():
                print("  Bundling Python dependencies...")
                for item in lib_path.iterdir():
                    # Skip unnecessary files
                    if item.name in ['pip', 'setuptools', 'wheel', '_distutils_hack', 'distutils-precedence.pth']:
                        continue
                    if item.name.startswith('pip-') or item.name.startswith('setuptools-'):
                        continue
                    if item.suffix in ['.pth', '.pyc']:
                        continue
                    
                    if item.is_file():
                        zf.write(item, f"lib/{item.name}")
                    elif item.is_dir():
                        for root, dirs, files in os.walk(item):
                            # Skip __pycache__ directories
                            dirs[:] = [d for d in dirs if d != '__pycache__']
                            
                            for file in files:
                                # Skip .pyc files
                                if file.endswith('.pyc'):
                                    continue
                                
                                file_path = Path(root) / file
                                arcname = f"lib/{file_path.relative_to(lib_path)}"
                                zf.write(file_path, arcname)
                
                print("  ✓ Bundled all Python dependencies")
            else:
                print("  ⚠ Warning: Could not find lib directory")
    
    print(f"✓ Extension packaged: {output_path.name}")
    print(f"  Total size: {output_path.stat().st_size:,} bytes")
    print(f"  Location: {output_path}")
    print("\nTo install:")
    print("1. Open Claude Desktop")
    print("2. Go to Settings → Extensions")
    print("3. Click 'Install Extension'")
    print(f"4. Select: {output_path}")

if __name__ == "__main__":
    main()