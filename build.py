"""
Build script for creating executable versions of Simple Media Player.

This script uses PyInstaller to create standalone executables for different platforms.
"""

import os
import sys
import shutil
import platform
from pathlib import Path

try:
    import PyInstaller.__main__
except ImportError:
    print("PyInstaller is not installed.")
    print("Install it with: pip install pyinstaller")
    sys.exit(1)


def clean_build_dirs():
    """Remove previous build directories."""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"Cleaning {dir_name}...")
            shutil.rmtree(dir_name)


def build_executable():
    """Build the executable using PyInstaller."""
    print("=" * 60)
    print("Building Simple Media Player Executable")
    print("=" * 60)
    print()
    
    # Clean previous builds
    clean_build_dirs()
    
    # Determine the platform
    system = platform.system()
    print(f"Platform: {system}")
    print()
    
    # Common PyInstaller arguments
    args = [
        'src/main.py',
        '--name=SimpleMediaPlayer',
        '--windowed',  # Don't show console window
        '--onefile',   # Create a single executable file
        '--clean',
        '--noconfirm',
        # Add application icon (if available)
        # '--icon=icon.ico',  # Uncomment if you have an icon
    ]
    
    # Add hidden imports that PyInstaller might miss
    hidden_imports = [
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'mpv',
    ]
    
    for module in hidden_imports:
        args.extend(['--hidden-import', module])
    
    # Add data files
    # args.extend(['--add-data', 'README.md:.',
    #              '--add-data', 'MVP-STATUS.md:.'])
    
    print("PyInstaller arguments:")
    for arg in args:
        print(f"  {arg}")
    print()
    
    # Run PyInstaller
    try:
        print("Running PyInstaller...")
        PyInstaller.__main__.run(args)
        print()
        print("=" * 60)
        print("Build completed successfully!")
        print("=" * 60)
        print()
        print(f"Executable location: dist/SimpleMediaPlayer")
        if system == "Windows":
            print("  -> dist/SimpleMediaPlayer.exe")
        elif system == "Darwin":  # macOS
            print("  -> dist/SimpleMediaPlayer")
        else:  # Linux
            print("  -> dist/SimpleMediaPlayer")
        print()
        print("IMPORTANT: Before distributing, test the executable!")
        print()
        
    except Exception as e:
        print(f"Error during build: {e}")
        sys.exit(1)


def main():
    """Main entry point."""
    print()
    print("Simple Media Player - Executable Builder")
    print("Version: 0.1.0-alpha")
    print()
    
    # Check if we're in the right directory
    if not os.path.exists('src/main.py'):
        print("Error: src/main.py not found!")
        print("Please run this script from the project root directory.")
        sys.exit(1)
    
    # Build the executable
    build_executable()
    
    print("Next steps:")
    print("1. Test the executable: ./dist/SimpleMediaPlayer")
    print("2. Create a GitHub release")
    print("3. Upload the executable to the release")
    print()


if __name__ == "__main__":
    main()
