# 🎬 Simple Media Player
### *by Arjun Biswas*

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![PyQt6](https://img.shields.io/badge/PyQt6-6.0+-green.svg)](https://pypi.org/project/PyQt6/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](https://github.com/ArjunBiswas-99/simple-media-player)

> A modern, lightweight, cross-platform video player built with Python and PyQt6. Perfect for developers learning GUI programming or users seeking a simple, elegant media player.

## ✨ Why Simple Media Player?

- 🚀 **Zero configuration** - Works out of the box with system codecs
- 🎨 **Beautiful UI** - Modern dark/light themes with smooth animations
- ⚡ **Lightweight** - Pure Python, no heavy dependencies
- 🔄 **Cross-platform** - Windows, macOS, and Linux support
- 🎓 **Clean code** - Well-structured, perfect for learning PyQt6
- 🆓 **Open source** - Free to use, modify, and learn from

## 📸 Screenshots

### Dark Theme
*Modern dark interface perfect for nighttime viewing*

### Light Theme  
*Clean, professional light mode for daytime use*
<img width="802" height="632" alt="image" src="https://github.com/user-attachments/assets/68d03cc0-6f5d-4a88-a266-1dcf073d73d3" />


### Fullscreen Mode
*Immersive fullscreen with auto-hiding controls*

> *Add screenshots here using: `![Dark Theme](screenshots/dark-theme.png)`*

## 🎯 Key Features

### 🎥 Media Playback
- ✅ **Universal format support** - MP4, MKV, AVI, MOV, WMV, FLV, WebM, and more
- ✅ **Hardware acceleration** - Uses native OS media frameworks
- ✅ **Perfect sync** - Audio and video perfectly synchronized
- ✅ **Variable speed** - 0.5x to 2.0x playback with pitch preservation
- ✅ **Subtitle support** - SRT, ASS, SSA formats

### 🎨 Modern User Interface
- 🌙 **Dark/Light themes** - Professional color schemes
- 🖱️ **Intuitive controls** - Click-to-seek, drag-and-drop support
- 🖼️ **Smart fullscreen** - Auto-hiding controls, mouse-activated
- 📐 **Auto-resize** - Window adapts to video resolution
- 🎯 **Responsive** - Smooth, lag-free interface

### ⌨️ Power User Features
- ⚡ **Keyboard shortcuts** - Complete keyboard control
- 🔄 **Fast forward** - Click and hold to skip ahead
- 🎚️ **Volume control** - Precise volume adjustment
- ⏯️ **Playback control** - Play, pause, stop, seek
- 🖼️ **Click-to-seek** - Jump anywhere instantly

## 📥 Download & Installation

### Option 1: Windows Executable (Easiest!) ⭐

**No Python installation required!**

1. Go to [Releases](https://github.com/ArjunBiswas-99/simple-media-player/releases)
2. Download `SimpleMediaPlayer.exe`
3. Double-click to run
4. That's it! 🎉

### Option 2: From Source (macOS/Linux/Windows)

**Prerequisites:**
- Python 3.10 or higher
- pip (Python package installer)

**Installation Steps:**

**Download from Release:**
1. Go to [Releases](https://github.com/ArjunBiswas-99/simple-media-player/releases)
2. Download **Source code (zip)**
3. Extract the ZIP file
4. Open Terminal/Command Prompt in the extracted folder
5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
6. Run the player:
   ```bash
   # Windows
   python -m src.main
   
   # macOS/Linux
   python3 -m src.main
   ```

**Or Clone from Git:**
```bash
git clone https://github.com/ArjunBiswas-99/simple-media-player.git
cd simple-media-player
pip install -r requirements.txt
python -m src.main
```

### Opening a Video

**Method 1: Drag and Drop**
- Simply drag a video file onto the player window

**Method 2: File Menu**
- Click `File → Open File` (or press `Ctrl+O`)

**Method 3: Command Line**
```bash
python -m src.main "path/to/video.mp4"
```

## ⌨️ Keyboard Shortcuts

### Playback Controls
| Shortcut | Action |
|----------|--------|
| `Space` | Play/Pause |
| `S` | Stop |
| `←` / `→` | Seek backward/forward (5 seconds) |
| `↑` / `↓` | Volume up/down |
| `M` | Mute/Unmute |

### Display Controls
| Shortcut | Action |
|----------|--------|
| `F` | Toggle fullscreen |
| `Esc` | Exit fullscreen |
| `Ctrl+O` | Open file |
| `Ctrl+S` | Open subtitle |
| `Ctrl+Q` | Quit |

### Mouse Controls
| Action | Result |
|--------|--------|
| Click progress bar | Seek to position |
| Double-click video | Toggle fullscreen |
| Click and hold video | Fast forward (2x speed) |
| Mouse move (fullscreen) | Show controls |

## 🏗️ Building Executable

Create a standalone application:

**Windows:**
```bash
python scripts/build.py
```
Output: `dist/PyMediaPlayer.exe`

**Cross-platform:**
```bash
pip install pyinstaller
pyinstaller --name="Simple Media Player" --windowed src/main.py
```

## 🔧 Technology Stack

### Core Technologies
- **[PyQt6](https://www.riverbankcomputing.com/software/pyqt/)** - Modern Qt6 bindings for Python
- **[PyQt6-Multimedia](https://pypi.org/project/PyQt6-Multimedia/)** - Native multimedia framework
- **Python 3.10+** - Latest Python features

### Architecture Highlights
- 🏛️ **Clean Architecture** - Separation of concerns, SOLID principles
- 🧩 **Modular Design** - Independent components with clear interfaces
- 🔒 **Thread-safe** - Proper synchronization for multimedia
- 📝 **Well-documented** - Comprehensive code comments

### How It Works

```
┌─────────────────────────────────────┐
│        PyQt6 Application           │
├─────────────────────────────────────┤
│  GUI (main_window.py)              │
│   ├─ Video Widget (video_widget.py)│
│   ├─ Controls & UI                 │
│   └─ Theme Manager                 │
├─────────────────────────────────────┤
│  Media Player (player.py)          │
│   ├─ QMediaPlayer (Qt Multimedia)  │
│   ├─ QAudioOutput (System audio)   │
│   └─ QVideoSink (Video rendering)  │
├─────────────────────────────────────┤
│  Native OS Media Frameworks        │
│   ├─ Windows: Media Foundation     │
│   ├─ macOS: AVFoundation           │
│   └─ Linux: GStreamer              │
└─────────────────────────────────────┘
```

**Why PyQt6 Multimedia?**
- ✅ Uses native OS codecs (no external libraries needed)
- ✅ Hardware acceleration support
- ✅ Perfect audio/video synchronization
- ✅ Same technology used by professional Qt applications
- ✅ Simple, unified API for all media types

## 📁 Project Structure

```
simple-media-player/
├── README.md                    # Project documentation
├── LICENSE                      # MIT License
├── requirements.txt             # Python dependencies
│
├── src/                         # Source code
│   ├── main.py                  # Application entry point
│   ├── core/
│   │   └── player.py            # Media playback engine
│   └── gui/
│       ├── main_window.py       # Main window & UI
│       ├── video_widget.py      # Video display widget
│       ├── theme_manager.py     # Theme management
│       └── fullscreen_overlay.py # Fullscreen controls
│
├── docs/                        # Documentation
│   ├── CHANGELOG.md             # Version history
│   ├── CONTRIBUTING.md          # Contribution guidelines
│   └── development/             # Developer docs
│       ├── HOW_TO_RELEASE.md    # Release process
│       └── RELEASE_NOTES_v1.0.0.md
│
├── scripts/                     # Build & utility scripts
│   ├── build.py                 # Executable builder
│   └── BUILD-EXE.bat            # Windows build script
│
└── archive/                     # Archived files
    ├── errorlog.txt
    └── media-player-requirements.md
```

## 🐛 Troubleshooting

### Installation Issues

**"No module named 'PyQt6'"**
```bash
pip install --upgrade pip
pip install PyQt6 PyQt6-Multimedia
```

**Python version error**
```bash
python --version  # Must be 3.10 or higher
```

### Playback Issues

**Video plays but no audio**
- ✅ Check PyQt6-Multimedia is installed: `pip show PyQt6-Multimedia`
- ✅ Verify video file has an audio track (test with another media player)
- ✅ Check volume slider and mute button (press M to unmute)
- ✅ Restart the application

**Video won't load**
- ✅ Check file format is supported (MP4, MKV work best)
- ✅ Look for error messages in terminal
- ✅ Try a different video file
- ✅ Ensure file isn't corrupted

**Controls hidden in fullscreen**
- ✅ Move mouse to show controls
- ✅ Controls auto-hide after 3 seconds
- ✅ Press `Esc` or double-click to exit fullscreen

## 🧪 Testing

Simple Media Player has comprehensive unit and integration tests.

### Run Tests

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html
```

### Test Structure

- **Unit Tests** (`tests/unit/`) - Test isolated components
- **Integration Tests** (`tests/integration/`) - Test component interaction
- **Coverage Target** - 70%+ overall coverage

See [tests/README.md](tests/README.md) for detailed testing documentation.

## 🤝 Contributing

Contributions are welcome! See [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

Quick start:

1. 🍴 Fork the repository
2. 🌟 Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. 💾 Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. 📤 Push to the branch (`git push origin feature/AmazingFeature`)
5. 🎉 Open a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/simple-media-player.git
cd simple-media-player

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run tests
pytest

# Run the application
python -m src.main
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Star History

If you find this project useful, please consider giving it a star! ⭐

## 📬 Contact & Support

- 🐛 **Bug Reports**: [Open an issue](https://github.com/ArjunBiswas-99/simple-media-player/issues)
- 💡 **Feature Requests**: [Open an issue](https://github.com/ArjunBiswas-99/simple-media-player/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/ArjunBiswas-99/simple-media-player/discussions)

## 🙏 Acknowledgments

- PyQt6 team for excellent Python bindings
- Qt Project for the robust multimedia framework
- Open source community for inspiration and support

---

<div align="center">

**Made by Arjun Biswas**

[⬆ Back to Top](#-simple-media-player)

</div>
