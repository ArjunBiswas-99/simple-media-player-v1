# 🧪 Testing Guide for Simple Media Player

This directory contains unit and integration tests for the Simple Media Player application.

## 📁 Test Structure

```
tests/
├── conftest.py              # Shared fixtures and configuration
├── README.md                # This file
│
├── unit/                    # Unit tests (isolated components)
│   ├── test_theme_manager.py
│   ├── test_player.py
│   └── test_video_widget.py
│
├── integration/             # Integration tests (component interaction)
│   ├── test_main_window.py
│   └── test_playback_flow.py
│
└── fixtures/                # Test data files
    ├── sample_video.mp4     # Add small test video here
    └── sample_subtitle.srt  # Add test subtitle here
```

## 🚀 Quick Start

### Install Development Dependencies

```bash
pip install -r requirements-dev.txt
```

This installs:
- pytest (test framework)
- pytest-qt (PyQt6 testing)
- pytest-cov (code coverage)
- Code quality tools (black, flake8, mypy)

### Run All Tests

```bash
pytest
```

### Run with Coverage Report

```bash
pytest --cov=src --cov-report=html
```

Then open `htmlcov/index.html` to see detailed coverage.

## 🎯 Running Specific Tests

### Run Only Unit Tests

```bash
pytest tests/unit/
```

### Run Only Integration Tests

```bash
pytest tests/integration/
```

### Run Tests by Marker

```bash
# Run only GUI tests
pytest -m gui

# Run only unit tests
pytest -m unit

# Skip slow tests
pytest -m "not slow"
```

### Run Specific Test File

```bash
pytest tests/unit/test_theme_manager.py
```

### Run Specific Test Function

```bash
pytest tests/unit/test_theme_manager.py::TestThemeManager::test_toggle_theme_dark_to_light
```

## 📊 Test Coverage Goals

- **Target: 70%+ overall coverage**
- **Core logic (player.py): 80%+ coverage**
- **GUI components: 60%+ coverage**

### Check Current Coverage

```bash
pytest --cov=src --cov-report=term-missing
```

## ✍️ Writing Tests

### Unit Test Example

```python
import pytest
from gui.theme_manager import ThemeManager

@pytest.mark.unit
def test_theme_toggle(theme_manager):
    """Test theme switching functionality"""
    initial = theme_manager.current_theme
    theme_manager.toggle_theme()
    assert theme_manager.current_theme != initial
```

### Integration Test Example

```python
import pytest
from PyQt6.QtCore import Qt

@pytest.mark.integration
@pytest.mark.gui
def test_button_click(qtbot, main_window):
    """Test button click updates state"""
    qtbot.mouseClick(main_window.play_button, Qt.MouseButton.LeftButton)
    # Assert expected state change
```

## 🔧 Available Fixtures

Defined in `conftest.py`:

### Application Fixtures
- **qapp**: QApplication instance
- **main_window**: Complete MainWindow instance
- **media_player**: MediaPlayer instance
- **theme_manager**: ThemeManager instance

### Test Data Fixtures
- **sample_video_path**: Path to test video file
- **sample_subtitle_path**: Path to test subtitle
- **mock_video_file**: Temporary mock video file

### pytest-qt Fixtures
- **qtbot**: Simulate Qt events (clicks, keys, etc.)
- **qapp**: Qt application instance

## 🎨 Test Organization

### Use Markers

```python
@pytest.mark.unit          # Unit test
@pytest.mark.integration   # Integration test
@pytest.mark.gui          # Requires GUI
@pytest.mark.slow         # Long-running test
@pytest.mark.skip_ci      # Skip in CI environment
```

### Organize in Classes

```python
@pytest.mark.unit
class TestThemeManager:
    """Group related tests together"""
    
    def test_feature_1(self):
        pass
    
    def test_feature_2(self):
        pass
```

## 🐛 Testing Best Practices

### 1. Test Naming
```python
# Good ✅
def test_volume_increases_when_up_arrow_pressed():
    pass

# Bad ❌
def test1():
    pass
```

### 2. Arrange-Act-Assert Pattern
```python
def test_toggle_theme():
    # Arrange
    tm = ThemeManager()
    
    # Act
    tm.toggle_theme()
    
    # Assert
    assert tm.current_theme == Theme.LIGHT
```

### 3. One Assertion Per Test (when possible)
```python
# Preferred
def test_volume_minimum():
    player.volume = 0
    assert player.volume == 0

def test_volume_maximum():
    player.volume = 100
    assert player.volume == 100
```

### 4. Use Descriptive Assertions
```python
# Good ✅
assert player.is_playing, "Player should be playing after play() call"

# Okay
assert player.is_playing
```

## 🤖 Continuous Integration

Tests can run automatically on GitHub Actions. See `.github/workflows/test.yml`.

### Local CI Simulation

```bash
# Run tests like CI does
pytest tests/ --cov=src --cov-report=xml -v
```

## 🔍 Debugging Tests

### Run with Print Statements

```bash
pytest -s
```

### Run with Debugger

```bash
pytest --pdb
```

### Show Local Variables on Failure

```bash
pytest -l
```

### Verbose Output

```bash
pytest -vv
```

## 📝 Test Data

### Adding Test Fixtures

1. Add files to `tests/fixtures/`
2. Keep files small (<1MB)
3. Use Creative Commons or public domain content
4. Document source in `tests/fixtures/README.md`

### Sample Subtitle File

Create `tests/fixtures/sample_subtitle.srt`:

```srt
1
00:00:00,000 --> 00:00:05,000
Welcome to Simple Media Player

2
00:00:05,000 --> 00:00:10,000
A modern video player built with Python
```

## 🎓 Learning Resources

- **pytest docs**: https://docs.pytest.org/
- **pytest-qt docs**: https://pytest-qt.readthedocs.io/
- **PyQt6 testing**: https://www.riverbankcomputing.com/static/Docs/PyQt6/

## ❓ Common Issues

### "QApplication already created"
- Use the `qapp` fixture from conftest.py
- Don't create QApplication in individual tests

### "Cannot find module 'gui'"
- Make sure you're running pytest from project root
- conftest.py adds src/ to path

### "X server not found" (Linux)
- Install pytest-xvfb: `pip install pytest-xvfb`
- Or use: `xvfb-run pytest`

## ✅ Pre-Commit Checklist

Before committing code:

```bash
# Run tests
pytest

# Check coverage
pytest --cov=src --cov-report=term-missing

# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Lint code
flake8 src/ tests/

# Type check
mypy src/
```

## 📈 Test Metrics

Track test health:

```bash
# Total tests
pytest --collect-only

# Test duration
pytest --durations=10

# Coverage report
pytest --cov=src --cov-report=term
```

---

## 🎯 Current Test Status

- **Unit Tests**: 25+ tests covering core components
- **Integration Tests**: 15+ tests for GUI workflows
- **Coverage Target**: 70%+

Run `pytest` to see current status!
