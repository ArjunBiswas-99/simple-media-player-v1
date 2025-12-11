"""
Shared test fixtures and configuration for Simple Media Player tests
"""

import pytest
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

# Import application modules
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.gui.theme_manager import ThemeManager, Theme
from src.gui.main_window import MainWindow
from src.core.player import MediaPlayer


@pytest.fixture(scope='session')
def qapp():
    """
    Create QApplication instance for the test session.
    Required for any PyQt6 GUI testing.
    """
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app
    # Don't quit app here - let pytest-qt handle it


@pytest.fixture
def theme_manager():
    """Create a fresh ThemeManager instance for testing"""
    return ThemeManager()


@pytest.fixture
def main_window(qtbot):
    """
    Create a MainWindow instance for testing.
    qtbot is provided by pytest-qt plugin.
    """
    window = MainWindow()
    qtbot.addWidget(window)
    return window


@pytest.fixture
def media_player(qtbot):
    """Create a MediaPlayer instance for testing"""
    from PyQt6.QtWidgets import QWidget
    
    # Create a dummy video widget for the player
    video_widget = QWidget()
    qtbot.addWidget(video_widget)
    
    player = MediaPlayer()
    player.initialize(video_widget)
    
    yield player
    
    # Cleanup
    player.shutdown()


@pytest.fixture
def sample_video_path():
    """
    Return path to sample video file for testing.
    Note: You'll need to add a small test video to tests/fixtures/
    """
    fixtures_dir = Path(__file__).parent / 'fixtures'
    video_path = fixtures_dir / 'sample_video.mp4'
    
    if video_path.exists():
        return str(video_path)
    return None


@pytest.fixture
def sample_subtitle_path():
    """Return path to sample subtitle file for testing"""
    fixtures_dir = Path(__file__).parent / 'fixtures'
    subtitle_path = fixtures_dir / 'sample_subtitle.srt'
    
    if subtitle_path.exists():
        return str(subtitle_path)
    return None


@pytest.fixture
def mock_video_file(tmp_path):
    """Create a temporary mock video file for testing"""
    video_file = tmp_path / "test_video.mp4"
    video_file.write_bytes(b"fake video content")
    return str(video_file)


# Markers for pytest
def pytest_configure(config):
    """Configure custom pytest markers"""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "gui: mark test as requiring GUI"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
