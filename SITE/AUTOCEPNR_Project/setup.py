#!/usr/bin/env python3
"""
Setup script for Latam Auto-Filler
Installs dependencies and configures the application
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


def run_command(command, description):
    """
    Run a command and handle errors
    
    Args:
        command: Command to run
        description: Description of what the command does
    """
    print(f"Running: {description}")
    print(f"Command: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        if result.stdout:
            print(f"Output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed")
        print(f"Error: {e.stderr}")
        return False


def install_playwright_browsers():
    """Install Playwright browsers"""
    print("Installing Playwright browsers...")
    return run_command("python -m playwright install", "Installing Playwright browsers")


def install_dependencies():
    """Install Python dependencies"""
    print("Installing Python dependencies...")
    return run_command("pip install -r requirements.txt", "Installing dependencies")


def create_directories():
    """Create necessary directories"""
    directories = [
        "debug_images",
        "models",
        "user_networks",
        "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✓ Created directory: {directory}")


def setup_environment():
    """Setup the application environment"""
    print("Setting up Latam Auto-Filler environment...")
    
    # Create directories
    create_directories()
    
    # Install dependencies
    if not install_dependencies():
        print("Failed to install dependencies")
        return False
    
    # Install Playwright browsers
    if not install_playwright_browsers():
        print("Failed to install Playwright browsers")
        return False
    
    print("✓ Environment setup completed successfully!")
    return True


def test_installation():
    """Test the installation"""
    print("Testing installation...")
    
    try:
        # Test imports
        import easyocr
        import cv2
        import numpy as np
        from playwright.async_api import async_playwright
        import tkinter
        
        print("✓ All required modules imported successfully")
        
        # Test Playwright
        print("Testing Playwright...")
        result = subprocess.run("python -c \"import playwright; print('Playwright OK')\"", 
                              shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ Playwright working correctly")
        else:
            print("✗ Playwright test failed")
            return False
        
        # Test EasyOCR
        print("Testing EasyOCR...")
        result = subprocess.run("python -c \"import easyocr; print('EasyOCR OK')\"", 
                              shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ EasyOCR working correctly")
        else:
            print("✗ EasyOCR test failed")
            return False
        
        print("✓ All tests passed!")
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Test error: {e}")
        return False


def create_shortcut():
    """Create desktop shortcut (Windows only)"""
    if os.name == 'nt':  # Windows
        try:
            import winshell
            from win32com.client import Dispatch
            
            desktop = winshell.desktop()
            path = os.path.join(desktop, "Latam Auto-Filler.lnk")
            target = os.path.join(os.getcwd(), "main.py")
            wdir = os.getcwd()
            icon = os.path.join(os.getcwd(), "icon.ico")  # Optional icon
            
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(path)
            shortcut.Targetpath = sys.executable
            shortcut.Arguments = target
            shortcut.WorkingDirectory = wdir
            if os.path.exists(icon):
                shortcut.IconLocation = icon
            shortcut.save()
            
            print("✓ Desktop shortcut created")
            
        except ImportError:
            print("Note: winshell not available, skipping shortcut creation")
        except Exception as e:
            print(f"Warning: Could not create shortcut: {e}")
    else:
        print("Note: Desktop shortcuts only supported on Windows")


def main():
    """Main setup function"""
    parser = argparse.ArgumentParser(description="Setup Latam Auto-Filler")
    parser.add_argument('--test-only', action='store_true', help='Only run tests')
    parser.add_argument('--no-shortcut', action='store_true', help='Skip shortcut creation')
    
    args = parser.parse_args()
    
    print("Latam Auto-Filler Setup")
    print("=" * 50)
    
    if args.test_only:
        success = test_installation()
    else:
        success = setup_environment()
        if success:
            success = test_installation()
    
    if success:
        print("\n✓ Setup completed successfully!")
        print("\nTo run the application:")
        print("  python main.py")
        print("\nTo run with no UI:")
        print("  python main.py --no-ui")
        print("\nTo process an image:")
        print("  python main.py --image path/to/image.png")
        print("\nTo process from clipboard:")
        print("  python main.py --clipboard")
        
        if not args.no_shortcut and not args.test_only:
            create_shortcut()
    else:
        print("\n✗ Setup failed!")
        print("Please check the error messages above and try again.")
        sys.exit(1)


if __name__ == "__main__":
    main()