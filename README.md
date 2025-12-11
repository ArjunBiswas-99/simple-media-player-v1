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
│   ├── player.py        # Main media player coordinator
│   ├── audio_player.py  # Audio playback component
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
- **PyAV** - Python bindings for FFmpeg, handles video decoding with excellent format support
- **PyQt6-Multimedia** - Audio playback engine with native OS integration
- **NumPy** - Efficient array operations for video frame handling
- **Threading** - Smooth video playback without blocking UI

### Why PyAV + PyQt6 Multimedia?

**PyAV for Video:**
- Excellent codec support (uses FFmpeg)
- Pure Python solution - no system dependencies
- Cross-platform compatibility
- Frame-accurate seeking
- Efficient memory usage

**PyQt6 Multimedia for Audio:**
- Native OS audio integration
- Low latency playback
- Built-in volume and speed control
- Robust error handling
- Already included with PyQt6

**Benefits of This Approach:**
- Full audio/video synchronization
- No external libraries or DLLs needed
- Easy installation
- Reliable cross-platform playback
- Professional media player capabilities

### Audio/Video Synchronization

The player uses presentation timestamps (PTS) to synchronize video frames with audio:

1. Audio plays continuously via QMediaPlayer
2. Video frames are decoded and displayed based on their timestamps
3. Frame timing is adjusted to match audio position
4. Seeking updates both audio and video positions atomically

This ensures lip-sync accuracy and smooth playback at any speed.

## Troubleshooting

**"No module named 'av'"**
```bash
pip install av
```

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
- PyAV (FFmpeg) for professional-grade video decoding
- PyQt6 Multimedia for high-quality audio playback
