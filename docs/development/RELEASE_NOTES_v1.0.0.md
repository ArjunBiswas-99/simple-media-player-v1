# Simple Media Player v1.0.0 - Initial Release

**First stable MVP release!** 🎉

A modern, lightweight, cross-platform video player built with Python and PyQt6 by Arjun Biswas.

---

## ✨ Features

### 🎥 Media Playback
- ✅ **Universal format support** - MP4, MKV, AVI, MOV, WMV, FLV, WebM, and more
- ✅ **Hardware acceleration** - Uses native OS frameworks (Media Foundation, AVFoundation, GStreamer)
- ✅ **Perfect audio/video sync** - Qt Multimedia ensures smooth playback
- ✅ **Variable playback speeds** - 0.5x, 1.0x, 1.5x, 2.0x with pitch preservation
- ✅ **Subtitle support** - Load SRT, ASS, SSA subtitle files

### 🎨 User Interface
- 🌙 **Beautiful themes** - Modern dark and light color schemes
- 🖱️ **Intuitive controls** - Click-to-seek on progress bar
- 🖼️ **Smart fullscreen** - Auto-hiding controls, mouse-activated
- 📐 **Auto-resize** - Window adapts to video resolution (limited to 90% screen size)
- 🎯 **Drag and drop** - Simply drop video files to play

### ⌨️ Power Features
- ⚡ **Complete keyboard shortcuts** - Control everything from keyboard
- 🔄 **Fast forward** - Click and hold video to skip ahead (2x speed)
- 🎚️ **Precise volume** - Slider and keyboard control
- ⏯️ **Full playback control** - Play, pause, stop, seek

---

## 📥 Installation

### Windows (Recommended) ⭐

**No Python required!**

1. Download **SimpleMediaPlayer.exe** (below, under Assets)
2. Double-click to run
3. Enjoy! 🎉

### macOS / Linux

**Download Source Code:**
1. Download **Source code (zip)** (below, under Assets)
2. Extract ZIP file
3. Open Terminal in extracted folder
4. Install dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```
5. Run player:
   ```bash
   python3 -m src.main
   ```

**Or Clone from Git:**
```bash
git clone https://github.com/ArjunBiswas-99/simple-media-player.git
cd simple-media-player
pip3 install -r requirements.txt
python3 -m src.main
```

---

## 🎯 System Requirements

### Windows
- Windows 10 or newer
- No additional software needed (for .exe)

### macOS
- macOS 11 (Big Sur) or newer
- Python 3.10 or higher

### Linux
- Ubuntu 20.04+ or equivalent
- Python 3.10 or higher
- GStreamer (usually pre-installed)

---

## ⌨️ Quick Reference

### Essential Shortcuts
- **Space** - Play/Pause
- **F** - Fullscreen
- **M** - Mute
- **←/→** - Seek ±5 seconds
- **↑/↓** - Volume up/down

### Mouse Controls
- **Click progress bar** - Jump to position
- **Double-click video** - Toggle fullscreen
- **Click & hold video** - Fast forward

[Full keyboard shortcuts in README](https://github.com/ArjunBiswas-99/simple-media-player#-keyboard-shortcuts)

---

## 🔧 Technology

Built with modern Python technologies:
- **PyQt6** - Modern Qt6 bindings
- **PyQt6-Multimedia** - Native media framework
- **Python 3.10+** - Latest language features

Uses **native OS codecs** for maximum compatibility and performance.

---

## 🐛 Known Issues

None currently! This is a stable release. Please [report any issues](https://github.com/ArjunBiswas-99/simple-media-player/issues) you encounter.

---

## 📝 Documentation

- **README**: [View full documentation](https://github.com/ArjunBiswas-99/simple-media-player#readme)
- **Contributing**: [How to contribute](https://github.com/ArjunBiswas-99/simple-media-player/blob/main/CONTRIBUTING.md)
- **Changelog**: [Version history](https://github.com/ArjunBiswas-99/simple-media-player/blob/main/CHANGELOG.md)

---

## 💬 Feedback & Support

- 🐛 Found a bug? [Open an issue](https://github.com/ArjunBiswas-99/simple-media-player/issues)
- 💡 Have an idea? [Share it](https://github.com/ArjunBiswas-99/simple-media-player/issues)
- ⭐ Like the project? [Give it a star!](https://github.com/ArjunBiswas-99/simple-media-player)

---

## 🙏 Thank You

Thank you for trying Simple Media Player! Your feedback helps make it better.

**Made by Arjun Biswas** with ❤️ using Python and PyQt6
