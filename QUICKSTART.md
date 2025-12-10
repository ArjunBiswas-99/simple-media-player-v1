# 🚀 Quick Start Guide - PyMedia Player

Get up and running with PyMedia Player in 5 minutes!

## 📋 What You Need

- **Windows 10 or 11** (64-bit)
- **4GB RAM** minimum
- **500MB free disk space**
- **Internet connection** (for downloading MPV library)

## 🎯 Step-by-Step Setup

### Step 1: Download PyMedia Player

1. Go to the [Releases page](https://github.com/yourusername/pymedia-player/releases)
2. Download `PyMediaPlayer-v1.0.0-Windows-x64.zip`
3. Extract the ZIP file to a folder of your choice (e.g., `C:\PyMediaPlayer`)

### Step 2: Download MPV Library

PyMedia Player needs the MPV library to play videos. Here's how to get it:

**Option A: Download from MPV Website (Recommended)**

1. Visit: https://mpv.io/installation/
2. Scroll to "Windows builds"
3. Click on **"mpv.io/installation"** or **"shinchiro builds"**
4. Download the latest `mpv-x86_64-*.7z` file
5. Extract the archive (you'll need 7-Zip: https://www.7-zip.org/)
6. Find `libmpv-2.dll` in the extracted folder
7. Copy `libmpv-2.dll` to the same folder as `PyMediaPlayer.exe`

**Option B: Install Full MPV Player**

1. Visit: https://mpv.io/installation/
2. Download and install the full MPV player
3. The required library will be available system-wide

### Step 3: Run the Application

1. Navigate to your PyMedia Player folder
2. Double-click `PyMediaPlayer.exe`
3. **If you see a Windows security warning:**
   - Click **"More info"**
   - Click **"Run anyway"**
   - This is normal for unsigned applications

### Step 4: Open Your First Video

1. Click **File → Open** (or press `Ctrl+O`)
2. Browse to a video file
3. Double-click to open and play
4. **Or simply drag & drop** a video file onto the window!

## 🎬 Basic Controls

### Using Your Mouse

- **Play/Pause**: Click the ▶/⏸ button
- **Seek**: Click anywhere on the progress bar
- **Volume**: Drag the volume slider
- **Speed**: Click the speed button to cycle (0.5x → 1.0x → 1.5x → 2.0x)
- **Fullscreen**: Click the "Fullscreen" button

### Using Your Keyboard

- **Space**: Play/Pause
- **F**: Fullscreen (press `Esc` to exit)
- **M**: Mute/Unmute
- **←/→**: Skip backward/forward 5 seconds
- **↑/↓**: Volume up/down 5%

## 🎵 Playing Different File Types

PyMedia Player supports:

- **Videos**: MP4, MKV, AVI, MOV, WMV, FLV, WebM
- **Audio**: MP3, AAC, FLAC, WAV, OGG, WMA
- **Subtitles**: SRT, ASS, SSA, VTT, SUB

Just open the file and it will play!

## 📝 Adding Subtitles

1. Make sure a video is playing
2. Click **File → Open Subtitle** (or press `Ctrl+S`)
3. Browse to your subtitle file (.srt, .ass, etc.)
4. Select and open
5. Subtitles will appear on the video!

## ⚡ Pro Tips

### Drag & Drop
Just drag video files onto the window to play them instantly!

### Command Line
You can also open videos from the command line:
```cmd
PyMediaPlayer.exe "C:\path\to\video.mp4"
```

### Playback Speed
Click the speed button repeatedly to cycle through:
- 0.5x (slow motion)
- 1.0x (normal)
- 1.5x (faster)
- 2.0x (double speed)

### Keyboard Shortcuts
Press `Help → Keyboard Shortcuts` in the menu to see all shortcuts!

## ❓ Common Issues

### "Application failed to start"
**Solution**: Make sure `libmpv-2.dll` is in the same folder as `PyMediaPlayer.exe`

### "Video won't play"
**Solutions**:
- Check if the file format is supported
- Try a different video file to test
- Make sure the video file isn't corrupted

### "No sound"
**Solutions**:
- Check the volume slider in PyMedia Player
- Check your computer's volume settings
- Make sure the video has an audio track

### "Windows SmartScreen blocks the app"
**Solution**: 
1. Click "More info"
2. Click "Run anyway"

This happens because the app isn't signed with an expensive certificate. The app is safe to use!

## 🎉 You're All Set!

Enjoy using PyMedia Player! If you have any questions or issues:

- 📖 Check the [README](README.md) for more details
- 🐛 Report bugs on [GitHub Issues](https://github.com/yourusername/pymedia-player/issues)
- 💡 Request features on GitHub

---

**Happy Watching! 🍿**
