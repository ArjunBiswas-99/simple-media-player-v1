# Contributing to Simple Media Player 🎬

First off, thank you for considering contributing to Simple Media Player! It's people like you that make this project great.

## 🌟 How Can I Contribute?

### Reporting Bugs 🐛

Before creating bug reports, please check existing issues. When creating a bug report, include as many details as possible:

**Bug Report Template:**
```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. See error

**Expected behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment:**
 - OS: [e.g. Windows 11, macOS 13, Ubuntu 22.04]
 - Python Version: [e.g. 3.10.5]
 - PyQt6 Version: [e.g. 6.5.0]

**Additional context**
Any other context about the problem.
```

### Suggesting Features 💡

Feature requests are welcome! Please provide:

- Clear use case
- Expected behavior
- Why this would be useful
- Possible implementation approach (optional)

### Pull Requests 🔧

1. **Fork the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/simple-media-player.git
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/AmazingFeature
   ```

3. **Make your changes**
   - Follow the coding style
   - Add comments for complex logic
   - Update documentation if needed

4. **Test your changes**
   ```bash
   python -m src.main
   # Test all affected features
   ```

5. **Commit your changes**
   ```bash
   git commit -m "Add some AmazingFeature"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/AmazingFeature
   ```

7. **Open a Pull Request**
   - Describe your changes clearly
   - Reference any related issues
   - Include screenshots if UI changes

## 💻 Development Setup

### Prerequisites
- Python 3.10 or higher
- Git
- Virtual environment (recommended)

### Setup Steps

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/simple-media-player.git
cd simple-media-player

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the player
python -m src.main
```

## 📝 Coding Guidelines

### Python Style

Follow PEP 8 with these specifics:

```python
# Good ✅
class MediaPlayer:
    """Media player with audio and video support."""
    
    def __init__(self):
        """Initialize the media player."""
        self.is_playing = False
    
    def play(self) -> bool:
        """
        Start media playback.
        
        Returns:
            bool: True if playback started successfully
        """
        if not self.is_playing:
            self.is_playing = True
            return True
        return False

# Bad ❌
class mediaplayer:
    def __init__(self):
        self.isPlaying=False
    
    def play(self):
        if not self.isPlaying:
            self.isPlaying=True
            return True
        return False
```

### Key Principles

1. **Descriptive Names**
   - Use clear, descriptive variable names
   - Methods should be verbs (`play()`, `stop()`, `seek()`)
   - Classes should be nouns (`MediaPlayer`, `VideoWidget`)

2. **Documentation**
   - Add docstrings to all classes and public methods
   - Explain complex logic with inline comments
   - Update README if adding features

3. **Error Handling**
   ```python
   # Good ✅
   try:
       self.player.load_file(filepath)
       logger.info(f"Loaded file: {filepath}")
   except Exception as e:
       logger.error(f"Failed to load file: {e}")
       raise
   
   # Bad ❌
   self.player.load_file(filepath)
   ```

4. **Logging**
   - Use appropriate log levels
   - Include context in log messages
   ```python
   logger.debug("Starting playback")
   logger.info(f"Loaded video: {filename}")
   logger.warning("Audio track not found")
   logger.error(f"Playback failed: {error}")
   ```

## 🏗️ Project Structure

```
simple-media-player/
├── src/
│   ├── main.py              # Entry point
│   ├── core/
│   │   └── player.py        # Media playback logic
│   └── gui/
│       ├── main_window.py   # Main window & UI
│       ├── video_widget.py  # Video display widget
│       ├── theme_manager.py # Theme system
│       └── fullscreen_overlay.py
├── requirements.txt
├── LICENSE
├── README.md
└── CONTRIBUTING.md
```

### Adding New Features

1. **New UI Component**
   - Add to `src/gui/`
   - Follow existing widget patterns
   - Integrate with theme system

2. **New Playback Feature**
   - Add to `src/core/player.py`
   - Emit signals for UI updates
   - Handle errors gracefully

3. **New Theme**
   - Update `src/gui/theme_manager.py`
   - Add color definitions
   - Test all UI elements

## 🧪 Testing

### Manual Testing Checklist

Before submitting PR, test:

- [ ] Basic playback (play, pause, stop)
- [ ] Seeking (progress bar, keyboard shortcuts)
- [ ] Volume control
- [ ] Fullscreen mode
- [ ] Theme switching
- [ ] Multiple video formats
- [ ] Keyboard shortcuts
- [ ] Mouse interactions
- [ ] Window resizing
- [ ] Drag and drop

### Test on Multiple Platforms

If possible, test on:
- Windows 10/11
- macOS 12+
- Ubuntu 20.04+

## 📦 Commit Message Guidelines

Use clear, descriptive commit messages:

```bash
# Good ✅
git commit -m "Add volume fade-in animation"
git commit -m "Fix fullscreen mouse cursor hiding on Windows"
git commit -m "Update README with new keyboard shortcuts"

# Bad ❌
git commit -m "fix bug"
git commit -m "updates"
git commit -m "wip"
```

### Commit Message Format

```
<type>: <subject>

<body (optional)>

<footer (optional)>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

**Examples:**
```
feat: Add playlist support

Implement basic playlist functionality with add/remove/reorder
operations. Integrates with existing player controls.

Closes #42
```

## 🎯 Priority Areas

We especially welcome contributions in these areas:

### High Priority
- 🐛 Bug fixes
- 📖 Documentation improvements
- 🎨 UI/UX enhancements
- ⚡ Performance optimizations

### Medium Priority
- ✨ New features (discuss first!)
- 🌐 Internationalization (i18n)
- 🧪 Test coverage
- 📱 Platform-specific improvements

### Low Priority
- 🎨 Additional themes
- ⌨️ More keyboard shortcuts
- 🔧 Code refactoring

## 💬 Communication

- **Issues**: For bugs and feature requests
- **Discussions**: For questions and ideas
- **Pull Requests**: For code contributions

## 📜 Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inspiring community for all.

### Expected Behavior

- Be respectful and inclusive
- Accept constructive criticism
- Focus on what's best for the community
- Show empathy towards others

### Unacceptable Behavior

- Harassment or discrimination
- Trolling or insulting comments
- Personal or political attacks
- Publishing others' private information

## 🏆 Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in the About dialog

## ❓ Questions?

Feel free to open an issue or discussion if you have questions!

---

**Thank you for contributing to Simple Media Player!** 🎉

Every contribution, no matter how small, makes a difference.
