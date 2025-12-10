# Quick Start Guide - Simple Media Player MVP

Get up and running in 5 minutes!

## Step 1: Install MPV (Required)

The media player requires MPV as its backend.

### macOS
```bash
brew install mpv
```

### Windows
Option 1 - Chocolatey:
```bash
choco install mpv
```

Option 2 - Manual Download:
1. Visit https://mpv.io/installation/
2. Download MPV for Windows
3. Extract and add to PATH

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install mpv libmpv-dev
```

## Step 2: Install Python Dependencies

```bash
cd simple-media-player
pip install -r requirements.txt
```

If you encounter issues, try:
```bash
pip install --upgrade pip
pip install PyQt6 python-mpv
```

## Step 3: Run the Application

```bash
python src/main.py
```

## Step 4: Open a Media File

1. Click **File → Open File...** (or press `Ctrl+O`)
2. Browse to any video or audio file
3. Click Open

## Step 5: Test Playback

Try these actions:
- ✅ Click **Play** button
- ✅ Click **Pause** button
- ✅ Click **Stop** button
- ✅ Drag the **progress bar** to seek
- ✅ Adjust **volume slider**
- ✅ Resize the window

## Supported Formats

### Video
MP4, MKV, AVI, MOV, WMV, FLV, WebM, M4V

### Audio
MP3, WAV, FLAC, M4A, AAC, OGG, WMA

## Troubleshooting

### "Failed to initialize player"
- Ensure MPV is installed and in your PATH
- On Windows, restart your terminal after installing MPV
- Try: `mpv --version` to verify MPV is accessible

### "Module not found" errors
- Run: `pip install -r requirements.txt`
- Ensure you're using Python 3.8 or higher

### Window opens but no video displays
- This is normal before loading a file
- The black area is the video display
- Open a file from the File menu

### "Player Not Ready" warning
- Wait 1-2 seconds after the window opens
- The player needs to initialize
- Try opening the file again

## What Works in MVP

✅ Open and play common video/audio formats  
✅ Play, pause, stop controls  
✅ Seek anywhere in the video  
✅ Volume control 0-100%  
✅ Time display (current/total)  
✅ Window resizing  
✅ Menu navigation  

## What Doesn't Work Yet

❌ Keyboard shortcuts (coming in v0.2.0)  
❌ Fullscreen mode (coming in v0.3.0)  
❌ Playlists (coming in v0.4.0)  
❌ Subtitles (coming in v0.5.0)  
❌ Themes (coming in v0.6.0)  

## Next Steps

1. **Test different file formats** - Try MP4, MKV, MP3, etc.
2. **Test different resolutions** - 720p, 1080p, 4K if available
3. **Test seeking** - Click around the progress bar
4. **Test volume** - Adjust from 0 to 100%
5. **Test window resizing** - Resize and see if video scales properly

## Provide Feedback

After testing, note:
- ✅ What works perfectly
- ❌ What doesn't work
- 🐛 Any crashes or errors
- 💡 Feature suggestions
- 🐌 Performance issues

See **MVP-STATUS.md** for the complete roadmap and development plan.

---

**Ready to go?** Run `python src/main.py` and start testing! 🚀
