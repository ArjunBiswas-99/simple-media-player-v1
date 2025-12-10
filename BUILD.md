# Building Executables - Simple Media Player

This guide explains how to build standalone executables for distribution.

## Prerequisites

1. **Install build dependencies:**
   ```bash
   pip install pyinstaller
   ```

2. **Ensure MPV is installed** (required for the executable to work):
   - macOS: `brew install mpv`
   - Windows: Download from https://mpv.io/installation/
   - Linux: `sudo apt install mpv libmpv-dev`

## Building

### Quick Build

Run the build script:

```bash
python3 build.py
```

This will:
- Clean previous builds
- Create a standalone executable in the `dist/` directory
- Package all dependencies

### Manual Build

If you prefer to build manually:

```bash
pyinstaller src/main.py \
    --name=SimpleMediaPlayer \
    --windowed \
    --onefile \
    --clean \
    --noconfirm \
    --hidden-import=PyQt6.QtCore \
    --hidden-import=PyQt6.QtGui \
    --hidden-import=PyQt6.QtWidgets \
    --hidden-import=mpv
```

## Output

After building, you'll find:

- **Executable**: `dist/SimpleMediaPlayer` (or `SimpleMediaPlayer.exe` on Windows)
- **Build files**: `build/` directory (can be deleted)
- **Spec file**: `SimpleMediaPlayer.spec` (PyInstaller configuration)

## Testing the Executable

Before distributing, test the executable:

```bash
# macOS/Linux
./dist/SimpleMediaPlayer

# Windows
dist\SimpleMediaPlayer.exe
```

**Test checklist:**
- [ ] Application launches without errors
- [ ] Can open File dialog
- [ ] Can load and play a video file
- [ ] Play/pause/stop controls work
- [ ] Volume control works
- [ ] Seeking works
- [ ] Window resizes properly

## Creating a Release

### 1. Tag the version

```bash
git tag -a v0.1.0-alpha -m "Release v0.1.0-alpha - MVP"
git push origin v0.1.0-alpha
```

### 2. Create GitHub Release

1. Go to your repository on GitHub
2. Click "Releases" → "Create a new release"
3. Select the tag: `v0.1.0-alpha`
4. Release title: `v0.1.0-alpha - MVP Release`
5. Description:

```markdown
# Simple Media Player v0.1.0-alpha

**First MVP Release** 🚀

## Features
- ✅ Play video/audio files (MP4, MKV, AVI, MOV, WMV, MP3, etc.)
- ✅ Play/Pause/Stop controls
- ✅ Progress bar with seeking
- ✅ Volume control (0-100%)
- ✅ Time display
- ✅ Resizable window

## Installation

### Prerequisites
- **MPV** must be installed on your system

**macOS:**
```bash
brew install mpv
```

**Windows:**
Download from https://mpv.io/installation/

**Linux:**
```bash
sudo apt install mpv libmpv-dev
```

### Running
1. Download the executable for your platform
2. Run the executable
3. Open a media file via File → Open File

## Known Issues
- No keyboard shortcuts yet
- No fullscreen mode
- No playlist support

See [MVP-STATUS.md](MVP-STATUS.md) for the complete roadmap.

## What's Next
- v0.2.0: Keyboard shortcuts
- v0.3.0: Fullscreen, speed control
- v0.4.0: Playlist support
```

6. **Upload executables:**
   - Drag and drop `dist/SimpleMediaPlayer` (macOS)
   - Or `dist/SimpleMediaPlayer.exe` (Windows)
   - Or create a ZIP: `zip -r SimpleMediaPlayer-v0.1.0-alpha-macOS.zip dist/SimpleMediaPlayer`

7. Click "Publish release"

## Platform-Specific Notes

### macOS

The executable may be blocked by Gatekeeper. Users need to:
1. Right-click the executable
2. Select "Open"
3. Click "Open" in the dialog

Or disable Gatekeeper (not recommended):
```bash
xattr -d com.apple.quarantine SimpleMediaPlayer
```

### Windows

Users might see a Windows Defender SmartScreen warning. They need to:
1. Click "More info"
2. Click "Run anyway"

### Linux

Make the executable executable:
```bash
chmod +x SimpleMediaPlayer
```

## Troubleshooting

### "Failed to initialize player"
- Ensure MPV is installed and in PATH
- Test: `mpv --version`

### "Module not found" errors
- Rebuild with all hidden imports
- Check the build log for missing modules

### Large executable size
- This is normal for PyInstaller (includes Python + dependencies)
- Typical size: 50-100MB

### Application doesn't start
- Check console output for errors
- Ensure all system dependencies are installed
- Try running from terminal to see error messages

## Distribution

When distributing executables:

1. **Include README** with:
   - System requirements (MPV installation)
   - Basic usage instructions
   - Known issues

2. **Test on clean systems** without development tools

3. **Provide multiple formats:**
   - Standalone executable
   - ZIP archive with README
   - Source code (for advanced users)

4. **Sign executables** (recommended for production):
   - macOS: `codesign`
   - Windows: Code signing certificate

## Next Steps

After v0.1.0-alpha, future releases will include:
- Auto-update mechanism
- Better error messages
- Installation wizard
- Desktop integration (file associations)

---

**Questions?** See the main README.md or open an issue on GitHub.
