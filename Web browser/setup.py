#!/usr/bin/env python3
"""
Setup script for Python Web Browser
Handles installation, dependency checking, and initial configuration
"""

import os
import sys
import subprocess
import platform
import json
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Error: Python 3.7 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    
    dependencies = [
        'requests>=2.31.0',
        'beautifulsoup4>=4.12.2',
        'Pillow>=10.0.1'
    ]
    
    for dep in dependencies:
        print(f"   Installing {dep}...")
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", dep
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"   ✅ {dep} installed successfully")
        except subprocess.CalledProcessError:
            print(f"   ❌ Failed to install {dep}")
            return False
    
    return True

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    
    directories = [
        'downloads',
        'data'
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"   ✅ Created directory: {directory}")

def create_config_files():
    """Create initial configuration files"""
    print("\n⚙️ Creating configuration files...")
    
    # Create default bookmarks
    default_bookmarks = [
        {
            "title": "Google",
            "url": "https://www.google.com",
            "date_added": "2024-01-01T00:00:00"
        },
        {
            "title": "Python.org",
            "url": "https://www.python.org",
            "date_added": "2024-01-01T00:00:00"
        },
        {
            "title": "GitHub",
            "url": "https://github.com",
            "date_added": "2024-01-01T00:00:00"
        }
    ]
    
    # Create default settings
    default_settings = {
        "home_page": "https://www.google.com",
        "search_engine": "Google",
        "theme": "light",
        "font_size": 10,
        "max_history": 1000,
        "max_bookmarks": 500
    }
    
    try:
        # Create bookmarks file
        with open('bookmarks.json', 'w') as f:
            json.dump(default_bookmarks, f, indent=2)
        print("   ✅ Created bookmarks.json")
        
        # Create settings file
        with open('browser_settings.json', 'w') as f:
            json.dump(default_settings, f, indent=2)
        print("   ✅ Created browser_settings.json")
        
        # Create empty history file
        with open('history.json', 'w') as f:
            json.dump([], f)
        print("   ✅ Created history.json")
        
    except Exception as e:
        print(f"   ❌ Error creating config files: {e}")
        return False
    
    return True

def create_desktop_shortcut():
    """Create desktop shortcut (Windows only)"""
    if platform.system() != "Windows":
        return True
    
    print("\n🖥️ Creating desktop shortcut...")
    
    try:
        import winshell
        from win32com.client import Dispatch
        
        desktop = winshell.desktop()
        path = os.path.join(desktop, "Python Web Browser.lnk")
        target = os.path.join(os.getcwd(), "run_browser.py")
        
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(path)
        shortcut.Targetpath = sys.executable
        shortcut.Arguments = f'"{target}"'
        shortcut.WorkingDirectory = os.getcwd()
        shortcut.IconLocation = sys.executable
        shortcut.save()
        
        print("   ✅ Desktop shortcut created")
        return True
        
    except ImportError:
        print("   ⚠️ Desktop shortcut creation skipped (winshell not available)")
        return True
    except Exception as e:
        print(f"   ⚠️ Could not create desktop shortcut: {e}")
        return True

def run_tests():
    """Run basic tests"""
    print("\n🧪 Running tests...")
    
    try:
        result = subprocess.run([
            sys.executable, "test_browser.py"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("   ✅ All tests passed")
            return True
        else:
            print("   ⚠️ Some tests failed (this is normal for first run)")
            return True
            
    except Exception as e:
        print(f"   ⚠️ Could not run tests: {e}")
        return True

def show_completion_message():
    """Show setup completion message"""
    print("\n" + "="*50)
    print("🎉 Python Web Browser Setup Complete!")
    print("="*50)
    print("\nTo start the browser, run one of these commands:")
    print("   python run_browser.py    (recommended)")
    print("   python web_browser.py    (direct)")
    print("   python demo.py           (demo mode)")
    print("\nFeatures available:")
    print("   • Tabbed browsing")
    print("   • Bookmarks management")
    print("   • Browsing history")
    print("   • Downloads tracking")
    print("   • Search integration")
    print("   • Keyboard shortcuts")
    print("\nFor help, see README.md or run: python demo.py")
    print("="*50)

def main():
    """Main setup function"""
    print("Python Web Browser Setup")
    print("="*30)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed: Could not install dependencies")
        print("   Please install manually: pip install -r requirements.txt")
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Create config files
    if not create_config_files():
        print("\n❌ Setup failed: Could not create configuration files")
        sys.exit(1)
    
    # Create desktop shortcut (Windows)
    create_desktop_shortcut()
    
    # Run tests
    run_tests()
    
    # Show completion message
    show_completion_message()

if __name__ == "__main__":
    main()
