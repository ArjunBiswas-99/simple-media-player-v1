"""
Main application window with controls and menu
"""

import logging
from pathlib import Path
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QSlider, QLabel, QFileDialog, QStyle,
    QMessageBox, QMenuBar, QMenu
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QAction, QKeySequence

from .video_widget import VideoWidget
from ..core.player import MediaPlayer

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """Main application window"""
    
    # Supported video formats
    VIDEO_EXTENSIONS = (
        "*.mp4", "*.mkv", "*.avi", "*.mov", "*.wmv",
        "*.flv", "*.webm", "*.m4v", "*.mpg", "*.mpeg"
    )
    
    SUBTITLE_EXTENSIONS = ("*.srt", "*.ass", "*.ssa", "*.sub", "*.vtt")
    
    def __init__(self):
        """Initialize the main window"""
        super().__init__()
        
        self.player = MediaPlayer()
        self.current_file = None
        self.is_seeking = False
        
        self._setup_ui()
        self._create_menu()
        self._setup_shortcuts()
        self._setup_timer()
        
        logger.info("Main window initialized")
    
    def _setup_ui(self):
        """Set up the user interface"""
        self.setWindowTitle("PyMedia Player")
        self.setMinimumSize(800, 600)
        
        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Video widget
        self.video_widget = VideoWidget()
        self.video_widget.set_drop_callback(self._on_file_dropped)
        main_layout.addWidget(self.video_widget, stretch=1)
        
        # Control panel
        control_panel = self._create_control_panel()
        main_layout.addWidget(control_panel)
        
        # Initialize player with video widget
        self.player.initialize(self.video_widget)
        self.player.set_time_pos_callback(self._on_time_update)
        
        # Apply dark theme
        self._apply_dark_theme()
    
    def _create_control_panel(self):
        """Create the bottom control panel"""
        panel = QWidget()
        panel.setFixedHeight(100)
        panel.setStyleSheet("background-color: #2b2b2b;")
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(10, 5, 10, 5)
        
        # Progress bar and time labels
        progress_layout = QHBoxLayout()
        
        self.time_label = QLabel("00:00")
        self.time_label.setStyleSheet("color: white;")
        progress_layout.addWidget(self.time_label)
        
        self.progress_slider = QSlider(Qt.Orientation.Horizontal)
        self.progress_slider.setRange(0, 1000)
        self.progress_slider.setValue(0)
        self.progress_slider.sliderPressed.connect(self._on_slider_pressed)
        self.progress_slider.sliderReleased.connect(self._on_slider_released)
        self.progress_slider.sliderMoved.connect(self._on_slider_moved)
        progress_layout.addWidget(self.progress_slider, stretch=1)
        
        self.duration_label = QLabel("00:00")
        self.duration_label.setStyleSheet("color: white;")
        progress_layout.addWidget(self.duration_label)
        
        layout.addLayout(progress_layout)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        # Play/Pause button
        self.play_button = QPushButton()
        self.play_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
        self.play_button.clicked.connect(self._toggle_play_pause)
        self.play_button.setFixedSize(40, 40)
        button_layout.addWidget(self.play_button)
        
        # Stop button
        stop_button = QPushButton()
        stop_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaStop))
        stop_button.clicked.connect(self._on_stop)
        stop_button.setFixedSize(40, 40)
        button_layout.addWidget(stop_button)
        
        button_layout.addSpacing(20)
        
        # Volume control
        volume_label = QLabel("🔊")
        volume_label.setStyleSheet("color: white; font-size: 18px;")
        button_layout.addWidget(volume_label)
        
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(100)
        self.volume_slider.setFixedWidth(100)
        self.volume_slider.valueChanged.connect(self._on_volume_changed)
        button_layout.addWidget(self.volume_slider)
        
        self.volume_label = QLabel("100%")
        self.volume_label.setStyleSheet("color: white;")
        self.volume_label.setFixedWidth(40)
        button_layout.addWidget(self.volume_label)
        
        button_layout.addSpacing(20)
        
        # Speed control
        speed_label = QLabel("Speed:")
        speed_label.setStyleSheet("color: white;")
        button_layout.addWidget(speed_label)
        
        self.speed_button = QPushButton("1.0x")
        self.speed_button.clicked.connect(self._cycle_speed)
        self.speed_button.setFixedWidth(60)
        button_layout.addWidget(self.speed_button)
        
        button_layout.addStretch()
        
        # Fullscreen button
        fullscreen_button = QPushButton("Fullscreen")
        fullscreen_button.clicked.connect(self._toggle_fullscreen)
        button_layout.addWidget(fullscreen_button)
        
        layout.addLayout(button_layout)
        
        return panel
    
    def _create_menu(self):
        """Create the menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        open_action = QAction("&Open File...", self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.triggered.connect(self._on_open_file)
        file_menu.addAction(open_action)
        
        open_subtitle_action = QAction("Open &Subtitle...", self)
        open_subtitle_action.setShortcut("Ctrl+S")
        open_subtitle_action.triggered.connect(self._on_open_subtitle)
        file_menu.addAction(open_subtitle_action)
        
        file_menu.addSeparator()
        
        quit_action = QAction("&Quit", self)
        quit_action.setShortcut(QKeySequence.StandardKey.Quit)
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)
        
        # Playback menu
        playback_menu = menubar.addMenu("&Playback")
        
        play_pause_action = QAction("&Play/Pause", self)
        play_pause_action.setShortcut("Space")
        play_pause_action.triggered.connect(self._toggle_play_pause)
        playback_menu.addAction(play_pause_action)
        
        stop_action = QAction("&Stop", self)
        stop_action.setShortcut("S")
        stop_action.triggered.connect(self._on_stop)
        playback_menu.addAction(stop_action)
        
        # Help menu
        help_menu = menubar.addMenu("&Help")
        
        about_action = QAction("&About", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)
        
        shortcuts_action = QAction("&Keyboard Shortcuts", self)
        shortcuts_action.triggered.connect(self._show_shortcuts)
        help_menu.addAction(shortcuts_action)
    
    def _setup_shortcuts(self):
        """Set up keyboard shortcuts"""
        # Fullscreen
        self.fullscreen_shortcut = QAction(self)
        self.fullscreen_shortcut.setShortcut("F")
        self.fullscreen_shortcut.triggered.connect(self._toggle_fullscreen)
        self.addAction(self.fullscreen_shortcut)
        
        # Mute
        self.mute_shortcut = QAction(self)
        self.mute_shortcut.setShortcut("M")
        self.mute_shortcut.triggered.connect(self._toggle_mute)
        self.addAction(self.mute_shortcut)
        
        # Seek forward
        self.seek_forward_shortcut = QAction(self)
        self.seek_forward_shortcut.setShortcut("Right")
        self.seek_forward_shortcut.triggered.connect(lambda: self.player.seek(5, relative=True))
        self.addAction(self.seek_forward_shortcut)
        
        # Seek backward
        self.seek_backward_shortcut = QAction(self)
        self.seek_backward_shortcut.setShortcut("Left")
        self.seek_backward_shortcut.triggered.connect(lambda: self.player.seek(-5, relative=True))
        self.addAction(self.seek_backward_shortcut)
        
        # Volume up
        self.volume_up_shortcut = QAction(self)
        self.volume_up_shortcut.setShortcut("Up")
        self.volume_up_shortcut.triggered.connect(self._volume_up)
        self.addAction(self.volume_up_shortcut)
        
        # Volume down
        self.volume_down_shortcut = QAction(self)
        self.volume_down_shortcut.setShortcut("Down")
        self.volume_down_shortcut.triggered.connect(self._volume_down)
        self.addAction(self.volume_down_shortcut)
    
    def _setup_timer(self):
        """Set up update timer"""
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self._update_ui)
        self.update_timer.start(100)  # Update every 100ms
    
    def _apply_dark_theme(self):
        """Apply dark theme to the application"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
            QPushButton {
                background-color: #3c3c3c;
                color: white;
                border: 1px solid #555;
                border-radius: 3px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #4a4a4a;
            }
            QPushButton:pressed {
                background-color: #2a2a2a;
            }
            QSlider::groove:horizontal {
                border: 1px solid #555;
                height: 8px;
                background: #3c3c3c;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #2196F3;
                border: 1px solid #1976D2;
                width: 16px;
                margin: -4px 0;
                border-radius: 8px;
            }
            QSlider::handle:horizontal:hover {
                background: #42A5F5;
            }
            QMenuBar {
                background-color: #2b2b2b;
                color: white;
            }
            QMenuBar::item:selected {
                background-color: #3c3c3c;
            }
            QMenu {
                background-color: #2b2b2b;
                color: white;
                border: 1px solid #555;
            }
            QMenu::item:selected {
                background-color: #3c3c3c;
            }
        """)
    
    def _on_open_file(self):
        """Handle open file action"""
        file_filter = f"Video Files ({' '.join(self.VIDEO_EXTENSIONS)});;All Files (*.*)"
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Open Video File",
            "",
            file_filter
        )
        
        if filename:
            self._load_file(filename)
    
    def _on_open_subtitle(self):
        """Handle open subtitle action"""
        if not self.current_file:
            QMessageBox.warning(self, "No Video", "Please open a video file first.")
            return
        
        file_filter = f"Subtitle Files ({' '.join(self.SUBTITLE_EXTENSIONS)});;All Files (*.*)"
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Open Subtitle File",
            "",
            file_filter
        )
        
        if filename:
            self.player.load_subtitle(filename)
            logger.info(f"Loaded subtitle: {filename}")
    
    def _on_file_dropped(self, filepath):
        """Handle file dropped on video widget"""
        self._load_file(filepath)
    
    def _load_file(self, filepath):
        """Load and play a media file"""
        if self.player.load_file(filepath):
            self.current_file = filepath
            self.setWindowTitle(f"PyMedia Player - {Path(filepath).name}")
            self.player.play()
            self._update_play_button()
            logger.info(f"Playing: {filepath}")
        else:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to load file:\n{filepath}"
            )
    
    def _toggle_play_pause(self):
        """Toggle play/pause state"""
        if not self.current_file:
            self._on_open_file()
            return
        
        self.player.toggle_pause()
        self._update_play_button()
    
    def _on_stop(self):
        """Handle stop button"""
        self.player.stop()
        self._update_play_button()
    
    def _update_play_button(self):
        """Update play/pause button icon"""
        if self.player.is_paused:
            self.play_button.setIcon(
                self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay)
            )
        else:
            self.play_button.setIcon(
                self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPause)
            )
    
    def _on_volume_changed(self, value):
        """Handle volume slider change"""
        self.player.volume = value
        self.volume_label.setText(f"{value}%")
    
    def _volume_up(self):
        """Increase volume by 5%"""
        new_volume = min(100, self.volume_slider.value() + 5)
        self.volume_slider.setValue(new_volume)
    
    def _volume_down(self):
        """Decrease volume by 5%"""
        new_volume = max(0, self.volume_slider.value() - 5)
        self.volume_slider.setValue(new_volume)
    
    def _toggle_mute(self):
        """Toggle mute state"""
        self.player.toggle_mute()
    
    def _toggle_fullscreen(self):
        """Toggle fullscreen mode"""
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()
    
    def _cycle_speed(self):
        """Cycle through playback speeds"""
        speeds = [0.5, 1.0, 1.5, 2.0]
        current_text = self.speed_button.text()
        current_speed = float(current_text.replace("x", ""))
        
        try:
            current_index = speeds.index(current_speed)
            next_index = (current_index + 1) % len(speeds)
        except ValueError:
            next_index = 1  # Default to 1.0x
        
        new_speed = speeds[next_index]
        self.player.set_speed(new_speed)
        self.speed_button.setText(f"{new_speed}x")
    
    def _on_slider_pressed(self):
        """Handle slider press"""
        self.is_seeking = True
    
    def _on_slider_released(self):
        """Handle slider release"""
        self.is_seeking = False
        # Seek to the position
        position = self.progress_slider.value() / 1000.0
        duration = self.player.duration
        if duration > 0:
            self.player.seek(position * duration)
    
    def _on_slider_moved(self, value):
        """Handle slider movement"""
        # Update time label during seek
        position = value / 1000.0
        duration = self.player.duration
        if duration > 0:
            time_seconds = position * duration
            self.time_label.setText(self._format_time(time_seconds))
    
    def _on_time_update(self, time_pos):
        """Handle time position updates from player"""
        if not self.is_seeking:
            # Update progress slider
            duration = self.player.duration
            if duration > 0:
                position = int((time_pos / duration) * 1000)
                self.progress_slider.setValue(position)
            
            # Update time label
            self.time_label.setText(self._format_time(time_pos))
    
    def _update_ui(self):
        """Update UI elements"""
        # Update duration label
        duration = self.player.duration
        if duration > 0:
            self.duration_label.setText(self._format_time(duration))
        
        # Update play button
        self._update_play_button()
    
    def _format_time(self, seconds):
        """Format time in seconds to MM:SS or HH:MM:SS"""
        seconds = int(seconds)
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes:02d}:{secs:02d}"
    
    def _show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            "About PyMedia Player",
            "<h3>PyMedia Player v1.0.0</h3>"
            "<p>A simple, lightweight media player built with Python.</p>"
            "<p><b>Features:</b></p>"
            "<ul>"
            "<li>Play video and audio files</li>"
            "<li>Support for multiple formats (MP4, MKV, AVI, etc.)</li>"
            "<li>External subtitle support (SRT, ASS, etc.)</li>"
            "<li>Keyboard shortcuts for easy control</li>"
            "<li>Dark theme interface</li>"
            "</ul>"
            "<p>Built with PyQt6 and python-mpv</p>"
        )
    
    def _show_shortcuts(self):
        """Show keyboard shortcuts dialog"""
        shortcuts_text = """
        <h3>Keyboard Shortcuts</h3>
        <table>
        <tr><td><b>Space</b></td><td>Play/Pause</td></tr>
        <tr><td><b>S</b></td><td>Stop</td></tr>
        <tr><td><b>F</b></td><td>Toggle Fullscreen</td></tr>
        <tr><td><b>Esc</b></td><td>Exit Fullscreen</td></tr>
        <tr><td><b>M</b></td><td>Mute/Unmute</td></tr>
        <tr><td><b>←/→</b></td><td>Seek Backward/Forward (5s)</td></tr>
        <tr><td><b>↑/↓</b></td><td>Volume Up/Down</td></tr>
        <tr><td><b>Ctrl+O</b></td><td>Open File</td></tr>
        <tr><td><b>Ctrl+S</b></td><td>Open Subtitle</td></tr>
        <tr><td><b>Ctrl+Q</b></td><td>Quit</td></tr>
        </table>
        """
        QMessageBox.information(self, "Keyboard Shortcuts", shortcuts_text)
    
    def keyPressEvent(self, event):
        """Handle key press events"""
        # Handle Escape to exit fullscreen
        if event.key() == Qt.Key.Key_Escape and self.isFullScreen():
            self.showNormal()
            event.accept()
        else:
            super().keyPressEvent(event)
    
    def closeEvent(self, event):
        """Handle window close event"""
        self.player.shutdown()
        event.accept()
        logger.info("Application closed")
