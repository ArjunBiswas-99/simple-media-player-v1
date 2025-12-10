# 🔨 How to Build the .exe File

## What You Have Right Now

✅ **Complete working code** for the media player
❌ **No .exe file yet** - you need to build it

## Why No .exe Yet?

I wrote all the code, but I cannot run commands on your computer to create the .exe file. You need to build it yourself (it's easy!).

## 🚀 Super Simple Build Process

### Prerequisites
- Make sure you have Python 3.10+ installed
- Open a command prompt in the `simple-media-player` folder

### Build the .exe (2 Simple Ways)

**Option 1: Double-click the batch file** ✨ EASIEST
```
Just double-click: BUILD-EXE.bat
```
This will:
1. Install all dependencies
2. Build the .exe automatically
3. Tell you where to find it

**Option 2: Manual commands**
```cmd
# Install dependencies
pip install -r requirements.txt

# Build the executable
python build.py
```

### That's It! 🎉

After building, you'll find:
- **dist/PyMediaPlayer.exe** - Your standalone executable (~50-80MB)
- **dist/PyMediaPlayer-v1.0.0-Windows-x64.zip** - Distribution package

## 📦 What About MPV Library?

**MPV is not MY library** - it's a free, open-source video player engine (like VLC's engine).

Your app uses python-mpv (a Python wrapper) which needs the MPV library (libmpv-2.dll) to actually play videos.

### Get the MPV Library:

1. **Download**: Go to https://mpv.io/installation/
2. **Extract**: Get `libmpv-2.dll` from the download
3. **Place**: Put it next to `PyMediaPlayer.exe`

OR install full MPV player and it will be system-wide.

## 🎯 After Building

Your folder will look like:
```
dist/
├── PyMediaPlayer.exe               <- Your standalone app!
├── PyMediaPlayer-v1.0.0-Windows-x64.zip  <- Ready to distribute
└── SHA256SUMS.txt                  <- File checksums
```

## 🚀 To Distribute on GitHub

1. Create a new release on GitHub
2. Upload the .zip file from dist/
3. Users download, extract, get libmpv-2.dll, and run!

## ❓ Troubleshooting

**"pip not recognized"**
- Make sure Python is installed and in PATH
- Try: `python -m pip install -r requirements.txt`

**"pyinstaller not found"**
- Run: `pip install pyinstaller`

**Build takes a long time**
- Normal! PyInstaller bundles Python + all libraries
- First build: 2-5 minutes
- Subsequent builds: faster

**"libmpv-2.dll not found" when running**
- Download from mpv.io and place with the .exe
- This is normal - MPV library is separate

## 💡 Understanding the Stack

```
Your Media Player (PyMediaPlayer.exe)
    ↓ uses
Python + PyQt6 (GUI framework)
    ↓ uses
python-mpv (Python bindings)
    ↓ uses
libmpv-2.dll (MPV library - the actual video engine)
```

Think of it like:
- **Your app** = The car body and controls
- **MPV library** = The engine that makes it go

Both are needed, but they're separate files.
