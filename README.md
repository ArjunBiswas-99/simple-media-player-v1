# PyMedia Player

A simple media player built with Python, PyQt6, and MPV.

## Features

- Play MP4, MKV, AVI, MOV, WMV, FLV, WebM videos
- Play MP3, AAC, FLAC, WAV, OGG audio files
- Load SRT, ASS, SSA, VTT subtitles
- Dark theme interface
- Keyboard shortcuts (Space, F, M, arrows)
- Drag & drop videos
- Volume control, speed control (0.5x-2.0x)
- Fullscreen mode

## Installation

### Requirements
- Python 3.10 or newer
- Windows 10/11 (64-bit)

### Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Get MPV library:**
   - Download from: https://mpv.io/installation/
   - Extract `libmpv-2.dll`
   - Place in project folder or system PATH

3. **Run the player:**
   ```bash
   python src/main.py
   ```

## Building Executable

To create a standalone .exe file:

```bash
python build.py
```

The .exe will be in `dist/PyMediaPlayer.exe`

**Note:** You must place `libmpv-2.dll` in the same folder as the .exe for it to work.

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| Space | Play/Pause |
| F | Fullscreen |
| M | Mute |
| ←/→ | Seek ±5s |
| ↑/↓ | Volume ±5% |
| Ctrl+O | Open file |
| Ctrl+S | Load subtitle |

## Troubleshooting

**"libmpv-2.dll not found"**
- Download from mpv.io and place with the .exe or in PATH

**"pip not recognized"**
- Install Python from python.org with "Add to PATH" checked

**Windows blocks the app**
- Click "More info" → "Run anyway" (normal for unsigned apps)
