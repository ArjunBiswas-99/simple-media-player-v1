"""Main window for Simple Media Player."""

from typing import Optional
from pathlib import Path
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QFileDialog, 
    QMessageBox, QMenuBar, QMenu
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QAction

from gui.video_widget import VideoWidget
from gui.control_panel import ControlPanel
from player.media_player import MediaPlayer
from config.settings import (
    DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT,
    MINIMUM_WINDOW_WIDTH, MINIMUM_WINDOW_HEIGHT,
    FILE_FILTER, DEFAULT_VOLUME
)
from config.version import VERSION


class MainWindow(QMainWindow):
    """Main application window for Simple Media Player."""
    
    def __init__(self):
        """Initialize the main window."""
        super().__init__()
        
        self._player: Optional[MediaPlayer] = None
        self._player_initialized = False
        
        self._setup_ui()
        self._setup_menu()
        self._setup_player()
        
    def _setup_ui(self) -> None:
        """Set up the user interface."""
        self.setWindowTitle(f"Simple Media Player v{VERSION}")
        self.resize(DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT)
        self.setMinimumSize(MINIMUM_WINDOW_WIDTH, MINIMUM_WINDOW_HEIGHT)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Video widget
        self._video_widget = VideoWidget()
        self._video_widget.initialized.connect(self._on_video_widget_initialized)
        layout.addWidget(self._video_widget, stretch=1)
        
        # Control panel
        self._control_panel = ControlPanel()
        layout.addWidget(self._control_panel)
        
        # Connect control panel signals
        self._control_panel.play_clicked.connect(self._on_play_clicked)
        self._control_panel.pause_clicked.connect(self._on_pause_clicked)
        self._control_panel.stop_clicked.connect(self._on_stop_clicked)
        self._control_panel.seek_requested.connect(self._on_seek_requested)
        self._control_panel.volume_changed.connect(self._on_volume_changed)
        
    def _setup_menu(self) -> None:
        """Set up the menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        open_action = QAction("&Open File...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self._on_open_file)
        file_menu.addAction(open_action)
        
        file_menu.addSeparator()
        
        quit_action = QAction("&Quit", self)
        quit_action.setShortcut("Ctrl+Q")
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)
        
        # Help menu
        help_menu = menubar.addMenu("&Help")
        
        about_action = QAction("&About", self)
        about_action.triggered.connect(self._on_about)
        help_menu.addAction(about_action)
        
    def _setup_player(self) -> None:
        """Set up the media player."""
        self._player = MediaPlayer(self)
        
        # Connect player signals
        self._player.position_changed.connect(self._on_position_changed)
        self._player.state_changed.connect(self._on_state_changed)
        self._player.file_loaded.connect(self._on_file_loaded)
        self._player.error_occurred.connect(self._on_error)
        
    def _on_video_widget_initialized(self, wid: int) -> None:
        """Handle video widget initialization."""
        if self._player and not self._player_initialized:
            self._player.initialize(wid)
            self._player.set_volume(DEFAULT_VOLUME)
            self._control_panel.set_volume(DEFAULT_VOLUME)
            self._player_initialized = True
            
    def _on_open_file(self) -> None:
        """Handle open file action."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Media File",
            "",
            FILE_FILTER
        )
        
        if file_path:
            self._load_file(file_path)
            
    def _load_file(self, file_path: str) -> None:
        """
        Load a media file.
        
        Args:
            file_path: Path to the media file
        """
        if not self._player_initialized:
            QMessageBox.warning(
                self,
                "Player Not Ready",
                "Please wait for the player to initialize."
            )
            return
            
        if self._player:
            success = self._player.load_file(file_path)
            if success:
                self._control_panel.set_media_loaded(True)
                file_name = Path(file_path).name
                self.setWindowTitle(f"{file_name} - Simple Media Player v{VERSION}")
                
    def _on_play_clicked(self) -> None:
        """Handle play button click."""
        if self._player:
            self._player.play()
            
    def _on_pause_clicked(self) -> None:
        """Handle pause button click."""
        if self._player:
            self._player.pause()
            
    def _on_stop_clicked(self) -> None:
        """Handle stop button click."""
        if self._player:
            self._player.stop()
            self._control_panel.update_position(0.0, 0.0)
            
    def _on_seek_requested(self, position: float) -> None:
        """Handle seek request."""
        if self._player:
            self._player.seek(position)
            
    def _on_volume_changed(self, volume: int) -> None:
        """Handle volume change."""
        if self._player:
            self._player.set_volume(volume)
            
    def _on_position_changed(self, position: float, duration: float) -> None:
        """Handle position change from player."""
        self._control_panel.update_position(position, duration)
        
    def _on_state_changed(self, is_playing: bool, is_paused: bool) -> None:
        """Handle state change from player."""
        self._control_panel.set_playing_state(is_playing, is_paused)
        
    def _on_file_loaded(self, file_path: str) -> None:
        """Handle file loaded event."""
        pass  # Already handled in _load_file
        
    def _on_error(self, error_message: str) -> None:
        """Handle error from player."""
        QMessageBox.critical(
            self,
            "Player Error",
            error_message
        )
        
    def _on_about(self) -> None:
        """Show about dialog."""
        QMessageBox.about(
            self,
            "About Simple Media Player",
            f"<h2>Simple Media Player</h2>"
            f"<p>Version: {VERSION}</p>"
            f"<p>A simple, lightweight media player built with PyQt6 and MPV.</p>"
            f"<p><b>MVP Features:</b></p>"
            f"<ul>"
            f"<li>Play video and audio files</li>"
            f"<li>Basic playback controls</li>"
            f"<li>Progress bar with seeking</li>"
            f"<li>Volume control</li>"
            f"</ul>"
            f"<p>For more features, see the MVP-STATUS.md roadmap.</p>"
        )
        
    def closeEvent(self, event) -> None:
        """Handle window close event."""
        if self._player:
            self._player.cleanup()
        event.accept()
