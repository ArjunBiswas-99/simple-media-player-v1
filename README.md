# PyMedia Player

A simple, lightweight media player built with Python, PyQt6, and OpenCV.

## Features

### Video Playback
- Play MP4, MKV, AVI, MOV, WMV, FLV, WebM, and more
- Support for multiple video formats
- Smooth playback with OpenCV
- Variable playback speed (0.5x, 1.0x, 1.5x, 2.0x)

### User Interface
- **Dark and Light theme modes** - Toggle in View menu
- Modern, attractive UI with vibrant colors
- Drag & drop support for video files
- Fullscreen mode

### Mouse Controls
- **Click progress bar** - Seek to any position instantly
- **Double-click video** - Toggle fullscreen
- **Click and hold video** - Fast forward (2x speed)

### Keyboard Shortcuts
- All standard media player shortcuts
- Arrow keys for seeking and volume
- Space for play/pause

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

That's it! No external libraries or system dependencies required.

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
- F - Toggle fullscreen
- Double-click video - Toggle fullscreen
- Esc - Exit fullscreen

**Volume:**
- M - Mute/Unmute
- ↑/↓ - Volume up/down

**Advanced:**
- Speed button - Cycle through playback speeds
- Click and hold video - Fast forward

**Theme:**
- View menu → Toggle between Dark and Light modes

## Building Executable

To create a standalone executable:

**Windows:**
```bash
python build.py
```

The .exe will be in `dist/PyMediaPlayer.exe`

## Technical Details

### Architecture
Built following SOLID principles:
- **Single Responsibility**: Separate modules for player logic, UI themes, and video display
- **Open/Closed**: Easy to extend with new features
- **Interface Segregation**: Clean callback interfaces
- **Dependency Inversion**: Components use abstractions

### Technologies
- **PyQt6** - Modern GUI framework
- **OpenCV** - Video processing and playback
- **Threading** - Smooth video playback without blocking UI

### Why OpenCV?
- Pure Python solution - no external system libraries needed
- Cross-platform compatibility
- Easy installation
- Reliable and well-documented
- No DLL or library path issues

## Troubleshooting

**"No module named 'cv2'"**
```bash
pip install opencv-python
```

**"No module named 'PyQt6'"**
```bash
pip install PyQt6
```

**Video won't load**
- Ensure the video file format is supported
- Check the console output for error messages
- Try a different video file to verify the player works

**Application won't start**
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (need 3.10+)

## License

This project is open source and available for personal and educational use.

## Contributing

Feel free to submit issues or pull requests to improve the player!
