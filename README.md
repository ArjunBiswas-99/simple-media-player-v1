# PyMedia Player 🎬

A simple, lightweight media player built with Python, PyQt6, and MPV. Clean interface, powerful playback, zero complexity.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.10+-green)
![License](https://img.shields.io/badge/license-MIT-blue)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey)

## ✨ Features

- 🎥 **Play video and audio files** - MP4, MKV, AVI, MOV, and more
- 📝 **External subtitle support** - SRT, ASS, SSA, VTT formats
- ⚡ **Playback speed control** - 0.5x, 1.0x, 1.5x, 2.0x
- ⌨️ **Keyboard shortcuts** - Full keyboard control for power users
- 🎨 **Dark theme interface** - Easy on the eyes
- 🖱️ **Drag & drop support** - Just drop your video files
- 🔊 **Volume control** - 0-100% with smooth slider
- 📺 **Fullscreen mode** - Distraction-free viewing

## 🚀 Quick Start

### For End Users (Windows)

1. **Download** the latest release from [Releases](https://github.com/yourusername/pymedia-player/releases)
2. **Extract** the ZIP file
3. **Download MPV library**:
   - Visit [mpv.io/installation](https://mpv.io/installation/)
   - Download `mpv-x86_64-*.7z`
   - Extract `libmpv-2.dll`
   - Place it next to `PyMediaPlayer.exe`
4. **Run** `PyMediaPlayer.exe`
5. **Open a video** (File → Open or Ctrl+O)
6. **Enjoy!** 🎉

### For Developers

#### Prerequisites
- Python 3.10 or higher
- Windows 10/11 (64-bit)

#### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/pymedia-player.git
cd pymedia-player/simple-media-player

# Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt

# Download MPV library
# Visit https://mpv.io/installation/ and download libmpv-2.dll
# Place it in your system PATH or in the project directory
```

#### Running from Source

```bash
# From the simple-media-player directory
python src/main.py
```

#### Building the Executable

```bash
# Run the build script
python build.py

# The executable will be in dist/PyMediaPlayer.exe
# The distribution package will be in dist/PyMediaPlayer-v1.0.0-Windows-x64.zip
```

## 🎮 Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| **Space** | Play/Pause |
| **S** | Stop |
| **F** | Toggle Fullscreen |
| **Esc** | Exit Fullscreen |
| **M** | Mute/Unmute |
| **←/→** | Seek Backward/Forward (5 seconds) |
| **↑/↓** | Volume Up/Down (5%) |
| **Ctrl+O** | Open File |
| **Ctrl+S** | Open Subtitle File |
| **Ctrl+Q** | Quit Application |

## 📦 Supported Formats

### Video Formats
MP4, MKV, AVI, MOV, WMV, FLV, WebM, M4V, MPG, MPEG

### Audio Formats
MP3, AAC, FLAC, WAV, OGG, WMA, ALAC

### Subtitle Formats
SRT, ASS, SSA, VTT, SUB

## 🏗️ Project Structure

```
simple-media-player/
├── src/
│   ├── main.py              # Entry point
│   ├── core/
│   │   └── player.py        # MPV player wrapper
│   └── gui/
│       ├── main_window.py   # Main application window
│       └── video_widget.py  # Video display widget
├── requirements.txt         # Python dependencies
├── build.py                 # Build script for .exe
└── README.md               # This file
```

## 🛠️ Technical Details

### Built With
- **[PyQt6](https://www.riverbankcomputing.com/software/pyqt/)** - Modern Qt6 bindings for Python
- **[python-mpv](https://github.com/jaseg/python-mpv)** - Python bindings for libmpv
- **[MPV](https://mpv.io/)** - Powerful media player backend
- **[PyInstaller](https://pyinstaller.org/)** - Packaging Python apps

### Architecture
- **MVC Pattern**: Clean separation of model, view, and controller
- **Event-Driven**: Responsive UI with Qt signals/slots
- **Modular Design**: Easy to extend and maintain

## 🐛 Troubleshooting

### "libmpv-2.dll not found" Error
**Solution**: Download libmpv-2.dll from [mpv.io](https://mpv.io/installation/) and place it in the same folder as the executable or in your system PATH.

### Video Won't Play
**Solution**: 
- Ensure the video format is supported
- Try re-downloading the video (it might be corrupted)
- Check if MPV library is properly installed

### No Audio
**Solution**:
- Check the volume slider in the player
- Check your system volume settings
- Ensure audio track exists in the video

### Windows SmartScreen Warning
**Solution**: Click "More info" → "Run anyway". This warning appears because the app is not signed with an expensive code signing certificate.

## 🗺️ Roadmap

### v1.1.0 (Next Release)
- [ ] Playlist support
- [ ] Remember last window size/position
- [ ] Recently played files list
- [ ] Auto-load subtitle files with matching names

### v1.2.0
- [ ] Streaming URL support (HTTP, RTSP)
- [ ] Audio equalizer
- [ ] Video filters (brightness, contrast, etc.)

### v2.0.0
- [ ] macOS support
- [ ] Settings/preferences window
- [ ] Multiple audio/subtitle track selection

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [MPV](https://mpv.io/) - Excellent media player and library
- [Qt Project](https://www.qt.io/) - Powerful cross-platform framework
- [PyInstaller](https://pyinstaller.org/) - Making Python apps portable

## 📧 Contact

- GitHub: [@yourusername](https://github.com/yourusername)
- Issues: [GitHub Issues](https://github.com/yourusername/pymedia-player/issues)

---

**Made with ❤️ using Python**
