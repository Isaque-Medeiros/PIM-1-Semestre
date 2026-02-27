#!/usr/bin/env python3
"""
Build script for creating Windows executable
Uses PyInstaller to create standalone .exe file
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


def check_pyinstaller():
    """Check if PyInstaller is installed"""
    try:
        import PyInstaller
        return True
    except ImportError:
        return False


def install_pyinstaller():
    """Install PyInstaller"""
    print("Installing PyInstaller...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        return True
    except subprocess.CalledProcessError:
        return False


def create_spec_file():
    """Create PyInstaller spec file for better control"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('docs/', 'docs/'),
        ('rules/', 'rules/'),
        ('src/', 'src/'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='LatamAutoFiller',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico'
)
'''
    
    with open('LatamAutoFiller.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("Created PyInstaller spec file")


def build_executable(use_spec=False):
    """Build the Windows executable"""
    print("Building Windows executable...")
    
    if use_spec and Path('LatamAutoFiller.spec').exists():
        cmd = [sys.executable, "-m", "PyInstaller", "LatamAutoFiller.spec"]
    else:
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--name=LatamAutoFiller",
            "--windowed",  # Remove this if you want console
            "--onefile",
            "--add-data=docs;docs",
            "--add-data=rules;rules", 
            "--add-data=src;src",
            "--hidden-import=easyocr",
            "--hidden-import=playwright",
            "main.py"
        ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✓ Executable built successfully!")
        print(f"Output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Build failed: {e}")
        print(f"Error: {e.stderr}")
        return False


def main():
    """Main build function"""
    parser = argparse.ArgumentParser(description="Build Latam Auto-Filler Windows executable")
    parser.add_argument('--spec', action='store_true', help='Use spec file for build')
    parser.add_argument('--no-spec', action='store_true', help='Build without spec file')
    
    args = parser.parse_args()
    
    print("Latam Auto-Filler Build Script")
    print("=" * 50)
    
    # Check if PyInstaller is available
    if not check_pyinstaller():
        print("PyInstaller not found, installing...")
        if not install_pyinstaller():
            print("Failed to install PyInstaller")
            sys.exit(1)
    
    # Create spec file if requested
    if args.spec or not args.no_spec:
        create_spec_file()
        use_spec = True
    else:
        use_spec = False
    
    # Build executable
    if build_executable(use_spec):
        print("\n✓ Build completed successfully!")
        print("\nTo run the executable:")
        print("  dist/LatamAutoFiller.exe")
        print("\nNote: First run will be slower as Playwright browsers install")
    else:
        print("\n✗ Build failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()