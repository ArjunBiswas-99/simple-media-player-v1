# PyMedia Player

A simple, lightweight media player built with Python, PyQt6, and PyAV with full audio and video support.

## Features

### Media Playback
- **Full audio and video playback** - Synchronized audio and video streams
- Play MP4, MKV, AVI, MOV, WMV, FLV, WebM, and more
- Support for multiple video formats and codecs
- Variable playback speed (0.5x, 1.0x, 1.5x, 2.0x) with pitch-preserved audio
- Volume control with mute functionality

### User Interface
- **Dark and Light theme modes** - Modern professional color schemes
- Rounded, modern UI with gradient buttons
- Prominent theme toggle button in control panel
- Drag & drop support for video files
- Fullscreen mode with auto-hiding controls
- Controls appear on mouse movement in fullscreen

### Mouse Controls
- **Click progress bar** - Seek to any position instantly
- **Double-click video** - Toggle fullscreen
- **Click and hold video** - Fast forward (2x speed)
- **Mouse movement in fullscreen** - Show hidden controls

### Keyboard Shortcuts
- All standard media player shortcuts
- Arrow keys for seeking and volume
- Space for play/pause
- F for fullscreen with auto-hide

## Installation

### Requirements
- Python 3.10 or newer
- Works on Windows, macOS, and Linux

### Setup

1. **Clone or download the repository**

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the player:**
   
   **Windows:**
   ```bash
   python -m src.main
   ```
   
   **macOS/Linux:**
   ```bash
   python3 -m src.main
   ```

That's it! All dependencies are pure Python packages - no external system libraries required.

## Usage

### Opening Videos
1. Click "File" → "Open File..." (or press Ctrl+O)
2. Or drag and drop a video file onto the player window
3. Or run with a file: `python -m src.main "path/to/video.mp4"`

### Controls

**Playback:**
- Space - Play/Pause
- S - Stop
- ←/→ - Seek backward/forward 5 seconds
- Click progress bar - Jump to position

**Display:**
- F - Toggle fullscreen (controls auto-hide after 3 seconds)
- Double-click video - Toggle fullscreen
- Esc - Exit fullscreen
- Move mouse - Show controls in fullscreen

**Volume:**
- M - Mute/Unmute
- ↑/↓ - Volume up/down
- Volume slider - Precise control

**Advanced:**
- Speed button - Cycle through playback speeds (audio pitch preserved)
- Click and hold video - Fast forward
- Theme toggle button (🌙/☀️) - Switch between dark and light modes

**Theme:**
- View menu → Toggle between Dark and Light modes
- Or use the prominent theme button in the control panel

## Building Executable

To create a standalone executable:

**Windows:**
```bash
python build.py
```

The .exe will be in `dist/PyMediaPlayer.exe`

## Technical Details

### Architecture

Built following software design best practices:

- **Separation of Concerns**: Distinct modules for media playback, audio, UI, and theming
- **Component Independence**: Audio and video players can operate independently
- **Clear Interfaces**: Well-defined APIs between components
- **Thread Safety**: Proper synchronization for multi-threaded playback

### Component Structure

```
src/
├── core/
│   ├── player.py        # Unified media player (audio + video)
│   └── __init__.py
├── gui/
│   ├── main_window.py   # Main application window
│   ├── video_widget.py  # Video display widget
│   ├── theme_manager.py # Theme management
│   └── __init__.py
└── main.py              # Application entry point
```

### Technologies

- **PyQt6** - Modern Qt6 bindings for Python, providing the GUI framework
- **PyQt6-Multimedia** - Qt's native multimedia framework for unified audio/video playback
- Uses OS-native codecs (Windows Media Foundation, AVFoundation on macOS, GStreamer on Linux)

### Why PyQt6 Multimedia?

**Unified Media Framework:**
- Single library handles both audio and video
- Leverages OS-native media frameworks for optimal performance
- Automatic codec support through system codecs
- Hardware acceleration where available

**OS Integration:**
- **Windows**: Uses Windows Media Foundation (WMF)
- **macOS**: Uses AVFoundation framework
- **Linux**: Uses GStreamer pipeline

**Key Benefits:**
- **Instant playback** - No audio extraction or preprocessing needed
- **Zero external dependencies** - Uses codecs already on your system
- **Perfect synchronization** - Qt handles audio/video sync automatically
- **Professional quality** - Same framework used by major Qt applications
- **Simple codebase** - One unified player instead of separate audio/video components

### How It Works

The player uses Qt's QMediaPlayer which provides:

1. **Unified playback** - QMediaPlayer handles both audio and video streams from the same file
2. **QVideoWidget** - Renders video frames directly to the GUI
3. **QAudioOutput** - Routes audio to system audio devices
4. **Automatic sync** - Qt's media framework keeps audio and video synchronized
5. **Native performance** - Leverages OS codecs for optimal playback

No manual frame timing or audio extraction required!

## Troubleshooting

**"No module named 'PyQt6'"**
```bash
pip install PyQt6 PyQt6-Multimedia
```

**Video plays but no audio**
- Ensure PyQt6-Multimedia is installed: `pip install PyQt6-Multimedia`
- Check that your video file contains an audio track
- Try adjusting volume slider or unmuting (M key)

**Audio/Video out of sync**
- This is usually caused by variable frame rate videos
- Try seeking to a different position to resync
- Check console logs for any timing warnings

**Video won't load**
- Ensure the video file format is supported by FFmpeg
- Check the console output for error messages
- Try a different video file to verify the player works
- Some exotic codecs may not be supported

**Application won't start**
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (need 3.10+)
- Look for error messages in the console

**Fullscreen controls won't show**
- Move your mouse to trigger the controls
- The controls auto-hide after 3 seconds of no movement
- Double-click or press Esc to exit fullscreen

## License

This project is open source and available for personal and educational use.

## Contributing

Feel free to submit issues or pull requests to improve the player!

## Credits

Built with modern Python technologies:
- PyQt6 for the beautiful, responsive UI
- PyQt6 Multimedia for native audio/video playback using OS frameworks
