#!/usr/bin/env python3
"""
Build script for PyMedia Player
Creates a standalone Windows executable using PyInstaller
"""

import os
import sys
import shutil
import subprocess
import hashlib
from pathlib import Path

VERSION = "1.0.0"
APP_NAME = "PyMediaPlayer"


def clean():
    """Remove previous build artifacts"""
    print("🧹 Cleaning previous builds...")
    for dir_name in ['build', 'dist', '__pycache__']:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"   ✓ Removed {dir_name}/")
    
    # Remove .spec file if exists
    spec_file = f"{APP_NAME}.spec"
    if os.path.exists(spec_file):
        os.remove(spec_file)
        print(f"   ✓ Removed {spec_file}")
    
    print("✅ Clean complete\n")


def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    # Check PyQt6
    try:
        __import__('PyQt6')
        print(f"   ✓ PyQt6 installed")
    except ImportError:
        print(f"   ✗ PyQt6 NOT installed")
        print("\n❌ PyQt6 is required. Install with: pip3 install PyQt6")
        return False
    
    # Check if pyinstaller command is available (more reliable than import check)
    try:
        result = subprocess.run(['pyinstaller', '--version'], 
                              capture_output=True, 
                              text=True,
                              timeout=5)
        if result.returncode == 0:
            print(f"   ✓ pyinstaller installed")
        else:
            print(f"   ✗ pyinstaller NOT installed")
            print("\n❌ pyinstaller is required. Install with: pip3 install pyinstaller")
            return False
    except (FileNotFoundError, subprocess.TimeoutExpired):
        print(f"   ✗ pyinstaller NOT installed or not in PATH")
        print("\n❌ pyinstaller is required. Install with: pip3 install pyinstaller")
        return False
    
    print("✅ All dependencies installed\n")
    return True


def build_executable():
    """Build standalone executable with PyInstaller"""
    print(f"🔨 Building {APP_NAME}.exe...")
    
    # PyInstaller command
    cmd = [
        'pyinstaller',
        '--onefile',                    # Single file
        '--windowed',                   # No console window
        f'--name={APP_NAME}',           # Output name
        '--clean',                      # Clean cache
        '--noconfirm',                  # Overwrite without asking
        # Hide imports that PyInstaller might miss
        '--hidden-import=PyQt6',
        '--hidden-import=PyQt6.QtCore',
        '--hidden-import=PyQt6.QtGui',
        '--hidden-import=PyQt6.QtWidgets',
        '--hidden-import=PyQt6.QtMultimedia',
        '--hidden-import=PyQt6.QtMultimediaWidgets',
        # Entry point
        'src/main.py'
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Build successful\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed with error:\n{e.stderr}")
        return False


def create_package():
    """Create ZIP package with documentation"""
    print("📦 Creating distribution package...")
    
    package_name = f"{APP_NAME}-v{VERSION}-Windows-x64"
    package_dir = Path('dist') / package_name
    
    # Create directory
    package_dir.mkdir(exist_ok=True)
    
    # Copy executable
    exe_source = Path('dist') / f'{APP_NAME}.exe'
    if exe_source.exists():
        shutil.copy(exe_source, package_dir)
        print(f"   ✓ Copied {APP_NAME}.exe")
    else:
        print(f"   ✗ {APP_NAME}.exe not found!")
        return False
    
    # Create README
    readme_content = f"""PyMedia Player v{VERSION} - Windows Edition

QUICK START
-----------
1. Double-click {APP_NAME}.exe to launch
2. File → Open (or Ctrl+O) to select a video
3. Press Space to play/pause
4. Press F for fullscreen

FIRST RUN
---------
Windows may show a security warning:
1. Click "More info"
2. Click "Run anyway"

This is normal for unsigned applications.

SYSTEM REQUIREMENTS
-------------------
- Windows 10/11 (64-bit)
- 4GB RAM minimum
- 500MB free disk space

IMPORTANT: MPV LIBRARY REQUIRED
--------------------------------
This application requires the MPV library (libmpv-2.dll).

Option 1: Download MPV (Recommended)
   1. Visit: https://mpv.io/installation/
   2. Download "mpv-x86_64-*.7z"
   3. Extract libmpv-2.dll
   4. Place it in the same folder as {APP_NAME}.exe

Option 2: Install MPV Player
   Installing the full MPV player will provide the required library.

SUPPORTED FORMATS
-----------------
Video: MP4, MKV, AVI, MOV, WMV, FLV, WebM, MPEG
Audio: MP3, AAC, FLAC, WAV, OGG, WMA, ALAC
Subtitles: SRT, ASS, SSA, VTT, SUB

KEYBOARD SHORTCUTS
------------------
Space    - Play/Pause
S        - Stop
F        - Fullscreen (Esc to exit)
M        - Mute/Unmute
←/→      - Seek backward/forward 5 seconds
↑/↓      - Volume up/down 5%
Ctrl+O   - Open file
Ctrl+S   - Open subtitle file
Ctrl+Q   - Quit

FEATURES
--------
✓ Play video and audio files
✓ Support for multiple formats
✓ External subtitle support (SRT, ASS, etc.)
✓ Playback speed control (0.5x, 1.0x, 1.5x, 2.0x)
✓ Keyboard shortcuts for easy control
✓ Dark theme interface
✓ Drag & drop file support

TROUBLESHOOTING
---------------
Problem: "libmpv-2.dll not found" error
Solution: Download libmpv-2.dll (see "MPV LIBRARY REQUIRED" above)

Problem: Video won't play
Solution: Make sure the video format is supported and not corrupted

Problem: No audio
Solution: Check volume slider and system volume settings

Problem: Application won't start
Solution: Try running as administrator or reinstalling

NEED HELP?
----------
GitHub: https://github.com/yourusername/pymedia-player
Issues: https://github.com/yourusername/pymedia-player/issues

LICENSE
-------
This software is provided as-is without warranty.
Built with PyQt6 and python-mpv.

---
PyMedia Player v{VERSION}
"""
    
    readme_path = package_dir / 'README.txt'
    readme_path.write_text(readme_content, encoding='utf-8')
    print("   ✓ Created README.txt")
    
    # Create ZIP
    archive_path = shutil.make_archive(str(package_dir), 'zip', package_dir)
    print(f"   ✓ Created {Path(archive_path).name}")
    
    print("✅ Package created\n")
    return True


def generate_checksums():
    """Generate SHA256 checksums for verification"""
    print("🔐 Generating checksums...")
    
    files_to_hash = [
        Path('dist') / f'{APP_NAME}.exe',
        Path('dist') / f'{APP_NAME}-v{VERSION}-Windows-x64.zip'
    ]
    
    checksum_file = Path('dist') / 'SHA256SUMS.txt'
    
    with open(checksum_file, 'w') as f:
        for filepath in files_to_hash:
            if filepath.exists():
                sha256 = hashlib.sha256()
                with open(filepath, 'rb') as file:
                    for chunk in iter(lambda: file.read(4096), b""):
                        sha256.update(chunk)
                
                checksum = sha256.hexdigest()
                f.write(f"{checksum}  {filepath.name}\n")
                print(f"   ✓ {filepath.name}: {checksum[:16]}...")
            else:
                print(f"   ✗ {filepath.name} not found")
    
    print("✅ Checksums generated\n")


def print_summary():
    """Print build summary"""
    exe_path = Path('dist') / f'{APP_NAME}.exe'
    zip_path = Path('dist') / f'{APP_NAME}-v{VERSION}-Windows-x64.zip'
    
    print("=" * 60)
    print("🎉 BUILD COMPLETE!")
    print("=" * 60)
    
    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"\n📦 Standalone Executable:")
        print(f"   Location: {exe_path}")
        print(f"   Size: {size_mb:.1f} MB")
    
    if zip_path.exists():
        size_mb = zip_path.stat().st_size / (1024 * 1024)
        print(f"\n📦 Distribution Package:")
        print(f"   Location: {zip_path}")
        print(f"   Size: {size_mb:.1f} MB")
    
    print("\n📋 Next Steps:")
    print("   1. Test the executable locally")
    print("   2. Download libmpv-2.dll and place it with the .exe")
    print("   3. Test video playback")
    print("   4. Create a GitHub release")
    print("   5. Upload the .zip file as a release asset")
    
    print("\n💡 To test now:")
    print(f"   cd dist")
    print(f"   .\\{APP_NAME}.exe")
    print("\n")


def main():
    """Main build process"""
    print("\n" + "=" * 60)
    print(f"  PyMedia Player v{VERSION} - Build Script")
    print("=" * 60 + "\n")
    
    # Step 1: Clean
    clean()
    
    # Step 2: Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Step 3: Build executable
    if not build_executable():
        print("\n❌ Build failed. Check errors above.")
        sys.exit(1)
    
    # Step 4: Create package
    if not create_package():
        print("\n❌ Package creation failed.")
        sys.exit(1)
    
    # Step 5: Generate checksums
    generate_checksums()
    
    # Step 6: Summary
    print_summary()


if __name__ == '__main__':
    main()
