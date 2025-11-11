#!/usr/bin/env python3
"""
Simple launcher script for the Python Web Browser
This script handles dependency checking and provides a clean startup experience
"""

import sys
import subprocess
import os

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = [
        'requests',
        'beautifulsoup4',
        'Pillow'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    return missing_packages

def install_dependencies(packages):
    """Install missing dependencies"""
    print("Installing missing dependencies...")
    for package in packages:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    print("All dependencies installed successfully!")

def main():
    """Main launcher function"""
    print("Python Web Browser Launcher")
    print("=" * 30)
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("Error: Python 3.7 or higher is required")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    
    print(f"Python version: {sys.version.split()[0]} ✓")
    
    # Check dependencies
    missing = check_dependencies()
    
    if missing:
        print(f"Missing dependencies: {', '.join(missing)}")
        response = input("Would you like to install them automatically? (y/n): ")
        
        if response.lower() in ['y', 'yes']:
            try:
                install_dependencies(missing)
            except subprocess.CalledProcessError as e:
                print(f"Error installing dependencies: {e}")
                print("Please install manually using: pip install -r requirements.txt")
                sys.exit(1)
        else:
            print("Please install dependencies manually:")
            print("pip install -r requirements.txt")
            sys.exit(1)
    else:
        print("All dependencies found ✓")
    
    # Launch the browser
    print("\nStarting Python Web Browser...")
    print("-" * 30)
    
    try:
        # Import and run the browser
        from web_browser import main as browser_main
        browser_main()
    except ImportError as e:
        print(f"Error importing browser: {e}")
        print("Make sure web_browser.py is in the same directory")
        sys.exit(1)
    except Exception as e:
        print(f"Error starting browser: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
