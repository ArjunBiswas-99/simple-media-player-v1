# Changelog

All notable changes to Simple Media Player will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-12-11

### 🎉 Initial Release

First stable release of Simple Media Player!

### ✨ Added

#### Media Playback
- Universal video format support (MP4, MKV, AVI, MOV, WMV, FLV, WebM, and more)
- Hardware-accelerated video playback using native OS frameworks
- Perfect audio/video synchronization
- Variable playback speeds (0.5x, 1.0x, 1.5x, 2.0x) with pitch preservation
- Subtitle support (SRT, ASS, SSA formats)
- Drag and drop file support

#### User Interface
- Modern dark and light theme modes
- Rounded, gradient-styled control panel
- Intuitive progress bar with click-to-seek
- Smart window auto-resizing to video resolution
- Smooth, responsive interface

#### Fullscreen Features
- Double-click video to toggle fullscreen
- Auto-hiding controls (3-second delay)
- Mouse movement detection to show controls
- Hybrid tracking system (frame-based when playing, overlay when paused)
- Cursor auto-hiding

#### Mouse Controls
- Single click on video to pause/play
- Double-click for fullscreen toggle
- Click and hold video for fast-forward (2x speed)
- Click progress bar to seek instantly

#### Keyboard Shortcuts
- Space: Play/Pause (works in all modes)
- F: Toggle fullscreen
- M: Mute/Unmute
- S: Stop playback
- Arrow keys: Seek (←/→) and volume (↑/↓)
- Ctrl+O: Open file
- Ctrl+S: Open subtitle
- Ctrl+Q: Quit
- Esc: Exit fullscreen

#### Advanced Features
- Volume control with precise slider
- Speed control cycling
- Fullscreen transition lock (prevents accidental actions)
- Comprehensive logging for debugging

### 🔧 Technical Highlights
- Built with PyQt6 and PyQt6-Multimedia
- Uses native OS codecs (Media Foundation, AVFoundation, GStreamer)
- Clean architecture with separation of concerns
- Thread-safe media playback
- Modular, well-documented code

### 🐛 Bug Fixes
- Fixed fullscreen mouse interaction edge cases
- Resolved double-click vs single-click conflicts
- Fixed fast-forward timer in fullscreen transitions
- Proper cleanup of pending mouse events

### 📝 Documentation
- Comprehensive README with installation guide
- Contributing guidelines
- MIT License
- Keyboard shortcuts reference
- Troubleshooting guide

---

## Release Notes

This changelog will be updated with each new version. For detailed commit history, see the [GitHub repository](https://github.com/ArjunBiswas-99/simple-media-player).
