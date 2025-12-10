# Simple Media Player

A lightweight, cross-platform media player built with PyQt6 and MPV.

**Current Version:** v0.1.0-alpha (MVP)

## Features (MVP)

✅ **Core Playback**
- Play video files (MP4, MKV, AVI, MOV, WMV, FLV, WebM, M4V)
- Play audio files (MP3, WAV, FLAC, M4A, AAC, OGG, WMA)
- Play/Pause/Stop controls
- Synchronized audio and video

✅ **User Interface**
- Clean, professional GUI
- Video display with proper aspect ratio
- Progress bar with seeking capability
- Volume control (0-100%)
- Time display (current/total)
- File menu for opening media
- Resizable window

✅ **Technical**
- SOLID principles architecture
- Modular, maintainable code
- Type hints and docstrings
- Error handling
- Cross-platform compatible

## Installation

### Prerequisites

1. **Python 3.8 or higher**
2. **MPV player** (required backend)

#### Installing MPV

**macOS:**
```bash
brew install mpv
```

**Windows:**
Download from https://mpv.io/installation/ or use Chocolatey:
```bash
choco install mpv
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt install mpv libmpv-dev
```

### Install Python Dependencies

```bash
cd simple-media-player
pip install -r requirements.txt
```

## Usage

### Running the Application

```bash
cd simple-media-player
python src/main.py
```

### Opening a Media File

1. Click **File → Open File...** (or press `Ctrl+O`)
2. Select a video or audio file
3. Use the controls to play/pause/stop

### Controls

- **Play Button**: Start or resume playback
- **Pause Button**: Pause playback
- **Stop Button**: Stop playback and reset to beginning
- **Progress Bar**: Click anywhere to seek to that position
- **Volume Slider**: Adjust volume (0-100%)

## Project Structure

```
simple-media-player/
├── src/
│   ├── main.py              # Application entry point
│   ├── config/              # Configuration files
│   │   ├── version.py       # Version information
│   │   └── settings.py      # Application settings
│   ├── player/              # Media player backend
│   │   └── media_player.py  # MPV wrapper
│   ├── gui/                 # GUI components
│   │   ├── main_window.py   # Main application window
│   │   ├── video_widget.py  # Video display widget
│   │   └── control_panel.py # Playback controls
│   └── utils/               # Utility functions
│       └── formatters.py    # Time formatting
├── requirements.txt         # Python dependencies
├── MVP-STATUS.md           # Development roadmap
└── README.md               # This file
```

## Roadmap

See [MVP-STATUS.md](MVP-STATUS.md) for the complete development roadmap.

### Coming Soon

- **v0.2.0**: Keyboard shortcuts (Space, F, M, arrows, etc.)
- **v0.3.0**: Fullscreen mode, mute button, speed control
- **v0.4.0**: Playlist support
- **v0.5.0**: Subtitle support
- **v0.6.0**: Dark/Light themes
- **v1.0.0**: Full feature set from requirements

## Known Issues (v0.1.0-alpha)

- No keyboard shortcuts yet (mouse/menu only)
- No fullscreen mode
- No playlist support
- No subtitle support
- No speed control
- No mute button (use volume slider)
- Basic error handling

## Development

### Architecture Principles

This project follows SOLID principles:
- **Single Responsibility**: Each class has one clear purpose
- **Open/Closed**: Extensible without modifying existing code
- **Liskov Substitution**: Proper inheritance hierarchies
- **Interface Segregation**: Clean interfaces between components
- **Dependency Inversion**: Depends on abstractions

### Code Style

- Type hints throughout
- Comprehensive docstrings
- Clean separation of concerns
- Modular, testable code

## Contributing

This is currently an MVP. Contributions welcome after v1.0.0 release.

## License

MIT License (to be added)

## Credits

Built with:
- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) - GUI framework
- [python-mpv](https://github.com/jaseg/python-mpv) - MPV bindings
- [MPV](https://mpv.io/) - Media player backend

## Support

For bugs or feature requests, please see the project repository.

---

**Status:** MVP - Ready for testing! 🚀

See [MVP-STATUS.md](MVP-STATUS.md) for what's next.
# simple-media-player
