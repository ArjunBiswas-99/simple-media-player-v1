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
from PyQt6.QtCore import Qt, QTimer, QEvent
from PyQt6.QtGui import QAction, QKeySequence

from .video_widget import VideoWidget
from .theme_manager import ThemeManager, Theme
from .fullscreen_overlay import FullscreenMouseOverlay
from ..core.player import MediaPlayer

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """Main application window"""
    
    VIDEO_EXTENSIONS = (
        "*.mp4", "*.mkv", "*.avi", "*.mov", "*.wmv",
        "*.flv", "*.webm", "*.m4v", "*.mpg", "*.mpeg"
    )
    
    SUBTITLE_EXTENSIONS = ("*.srt", "*.ass", "*.ssa", "*.sub", "*.vtt")
    
    def __init__(self):
        """Initialize the main window"""
        super().__init__()
        
        self._initialize_components()
        self._create_menu()
        self._setup_ui()
        self._setup_shortcuts()
        self._setup_timer()
        self._connect_signals()
        
        logger.info("Main window initialized")
    
    def _initialize_components(self):
        """Initialize core components"""
        self.player = MediaPlayer()
        self.theme_manager = ThemeManager()
        self.current_file = None
        self.is_seeking = False
        self._fast_forward_timer = None
        self._is_fast_forwarding = False
        
        # Fullscreen control hiding system
        self._fullscreen_hide_timer = None
        self._cursor_hidden = False
        self._controls_visible = True
        self._last_mouse_pos = None  # For frame-based detection
        self.setMouseTracking(True)
    
    def _setup_ui(self):
        """Set up the user interface"""
        self.setWindowTitle("PyMedia Player")
        self.setMinimumSize(800, 600)
        
        # Create a custom central widget that tracks mouse
        class MouseTrackingWidget(QWidget):
            def __init__(self, parent_window):
                super().__init__()
                self.parent_window = parent_window
                self.setMouseTracking(True)
            
            def mouseMoveEvent(self, event):
                if self.parent_window.isFullScreen():
                    if self.parent_window._cursor_hidden:
                        self.parent_window._show_controls()
                    else:
                        self.parent_window._start_hide_timer()
                super().mouseMoveEvent(event)
        
        central_widget = MouseTrackingWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Video widget for displaying media
        self.video_widget = VideoWidget()
        self.video_widget.setMouseTracking(True)
        self.video_widget.set_main_window(self)
        self.video_widget.set_drop_callback(self._on_file_dropped)
        main_layout.addWidget(self.video_widget, stretch=1)
        
        # Create fullscreen overlay (hidden by default, activated when paused in fullscreen)
        self.fullscreen_overlay = FullscreenMouseOverlay(self.video_widget)
        self.fullscreen_overlay.mouse_moved.connect(self._on_overlay_mouse_move)
        
        self.control_panel = self._create_control_panel()
        self.control_panel.setMouseTracking(True)
        main_layout.addWidget(self.control_panel)
        
        self.player.initialize(self.video_widget)
        
        # Connect player signals for thread-safe communication
        self.player.signals.time_update.connect(self._on_time_update)
        self.player.signals.duration_changed.connect(self._on_duration_changed)
        self.player.signals.playback_ended.connect(self._on_playback_ended)
        self.player.signals.error_occurred.connect(self._on_player_error)
        
        self._apply_theme()
    
    def _create_control_panel(self):
        """Create the bottom control panel with modern design"""
        panel = QWidget()
        panel.setFixedHeight(120)
        panel.setObjectName("controlPanel")
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(16, 10, 16, 10)
        layout.setSpacing(12)
        
        layout.addLayout(self._create_progress_bar())
        layout.addLayout(self._create_control_buttons())
        
        return panel
    
    def _create_progress_bar(self):
        """Create progress bar with time labels"""
        progress_layout = QHBoxLayout()
        
        self.time_label = QLabel("00:00")
        self.time_label.setObjectName("timeLabel")
        progress_layout.addWidget(self.time_label)
        
        self.progress_slider = QSlider(Qt.Orientation.Horizontal)
        self.progress_slider.setRange(0, 1000)
        self.progress_slider.setValue(0)
        self.progress_slider.setObjectName("progressSlider")
        
        # Enable mouse tracking for click-to-seek
        self.progress_slider.setMouseTracking(True)
        self.progress_slider.installEventFilter(self)
        
        self.progress_slider.sliderPressed.connect(self._on_slider_pressed)
        self.progress_slider.sliderReleased.connect(self._on_slider_released)
        self.progress_slider.sliderMoved.connect(self._on_slider_moved)
        progress_layout.addWidget(self.progress_slider, stretch=1)
        
        self.duration_label = QLabel("00:00")
        self.duration_label.setObjectName("durationLabel")
        progress_layout.addWidget(self.duration_label)
        
        return progress_layout
    
    def _create_control_buttons(self):
        """Create control buttons layout with modern design"""
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        
        # Playback controls (larger icon buttons)
        self.play_button = self._create_icon_button(
            QStyle.StandardPixmap.SP_MediaPlay,
            self._toggle_play_pause,
            "Play/Pause"
        )
        button_layout.addWidget(self.play_button)
        
        stop_button = self._create_icon_button(
            QStyle.StandardPixmap.SP_MediaStop,
            self._on_stop,
            "Stop"
        )
        button_layout.addWidget(stop_button)
        
        button_layout.addSpacing(16)
        
        # Volume controls
        button_layout.addLayout(self._create_volume_controls())
        
        button_layout.addSpacing(16)
        
        # Speed control
        button_layout.addLayout(self._create_speed_control())
        
        button_layout.addStretch()
        
        # Theme toggle button (prominent)
        self.theme_toggle_button = QPushButton("🌙")
        self.theme_toggle_button.clicked.connect(self._toggle_theme)
        self.theme_toggle_button.setObjectName("themeToggle")
        self.theme_toggle_button.setToolTip("Toggle Dark/Light Mode")
        button_layout.addWidget(self.theme_toggle_button)
        
        button_layout.addSpacing(8)
        
        # Fullscreen button
        fullscreen_button = QPushButton("Fullscreen")
        fullscreen_button.clicked.connect(self._toggle_fullscreen)
        fullscreen_button.setObjectName("controlButton")
        button_layout.addWidget(fullscreen_button)
        
        return button_layout
    
    def _create_button(self, icon: QStyle.StandardPixmap, callback, tooltip: str):
        """Create a styled button with icon"""
        button = QPushButton()
        button.setIcon(self.style().standardIcon(icon))
        button.clicked.connect(callback)
        button.setFixedSize(40, 40)
        button.setToolTip(tooltip)
        button.setObjectName("controlButton")
        return button
    
    def _create_icon_button(self, icon: QStyle.StandardPixmap, callback, tooltip: str):
        """Create a large circular icon button"""
        button = QPushButton()
        
        # Map standard icons to Unicode symbols for better color control
        icon_map = {
            QStyle.StandardPixmap.SP_MediaPlay: "▶",
            QStyle.StandardPixmap.SP_MediaPause: "⏸",
            QStyle.StandardPixmap.SP_MediaStop: "⏹"
        }
        
        if icon in icon_map:
            button.setText(icon_map[icon])
            button.setStyleSheet("font-size: 20px;")
        else:
            button.setIcon(self.style().standardIcon(icon))
        
        button.clicked.connect(callback)
        button.setToolTip(tooltip)
        button.setObjectName("iconButton")
        return button
    
    def _create_volume_controls(self):
        """Create volume control widgets"""
        layout = QHBoxLayout()
        layout.setSpacing(8)
        
        volume_icon = QLabel("🔊")
        volume_icon.setObjectName("volumeIcon")
        volume_icon.setFixedWidth(25)
        layout.addWidget(volume_icon)
        
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(100)
        self.volume_slider.setFixedWidth(100)
        self.volume_slider.setObjectName("volumeSlider")
        self.volume_slider.valueChanged.connect(self._on_volume_changed)
        layout.addWidget(self.volume_slider)
        
        self.volume_label = QLabel("100%")
        self.volume_label.setFixedWidth(45)
        self.volume_label.setObjectName("volumeLabel")
        layout.addWidget(self.volume_label)
        
        return layout
    
    def _create_speed_control(self):
        """Create speed control widgets"""
        layout = QHBoxLayout()
        
        speed_label = QLabel("Speed:")
        speed_label.setObjectName("speedLabel")
        layout.addWidget(speed_label)
        
        self.speed_button = QPushButton("1.0x")
        self.speed_button.clicked.connect(self._cycle_speed)
        self.speed_button.setFixedWidth(60)
        self.speed_button.setObjectName("controlButton")
        layout.addWidget(self.speed_button)
        
        return layout
    
    def _create_menu(self):
        """Create the menu bar"""
        menubar = self.menuBar()
        
        self._create_file_menu(menubar)
        self._create_playback_menu(menubar)
        self._create_view_menu(menubar)
        self._create_help_menu(menubar)
    
    def _create_file_menu(self, menubar):
        """Create file menu"""
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
    
    def _create_playback_menu(self, menubar):
        """Create playback menu"""
        playback_menu = menubar.addMenu("&Playback")
        
        play_pause_action = QAction("&Play/Pause", self)
        play_pause_action.setShortcut("Space")
        play_pause_action.triggered.connect(self._toggle_play_pause)
        playback_menu.addAction(play_pause_action)
        
        stop_action = QAction("&Stop", self)
        stop_action.setShortcut("S")
        stop_action.triggered.connect(self._on_stop)
        playback_menu.addAction(stop_action)
    
    def _create_view_menu(self, menubar):
        """Create view menu with theme toggle"""
        view_menu = menubar.addMenu("&View")
        
        self.theme_action = QAction("🌙 Dark Mode", self)
        self.theme_action.triggered.connect(self._toggle_theme)
        view_menu.addAction(self.theme_action)
        
        fullscreen_action = QAction("&Fullscreen", self)
        fullscreen_action.setShortcut("F")
        fullscreen_action.triggered.connect(self._toggle_fullscreen)
        view_menu.addAction(fullscreen_action)
    
    def _create_help_menu(self, menubar):
        """Create help menu"""
        help_menu = menubar.addMenu("&Help")
        
        about_action = QAction("&About", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)
        
        shortcuts_action = QAction("&Keyboard Shortcuts", self)
        shortcuts_action.triggered.connect(self._show_shortcuts)
        help_menu.addAction(shortcuts_action)
    
    def _setup_shortcuts(self):
        """Set up keyboard shortcuts - work even in fullscreen"""
        shortcuts = {
            "Space": self._toggle_play_pause,  # Add Space here for fullscreen
            "F": self._toggle_fullscreen,
            "M": self._toggle_mute,
            "Right": lambda: self.player.seek(5, relative=True),
            "Left": lambda: self.player.seek(-5, relative=True),
            "Up": self._volume_up,
            "Down": self._volume_down,
        }
        
        for key, callback in shortcuts.items():
            action = QAction(self)
            action.setShortcut(key)
            action.triggered.connect(callback)
            self.addAction(action)
    
    def _setup_timer(self):
        """Set up update timer"""
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self._update_ui)
        self.update_timer.start(100)
    
    def _connect_signals(self):
        """Connect video widget signals"""
        self.video_widget.single_clicked.connect(self._toggle_play_pause)
        self.video_widget.double_clicked.connect(self._toggle_fullscreen)
        self.video_widget.fast_forward_started.connect(self._start_fast_forward)
        self.video_widget.fast_forward_stopped.connect(self._stop_fast_forward)
        self.video_widget.mouse_moved_in_fullscreen.connect(self._on_mouse_move_fullscreen)
    
    def _on_mouse_move_fullscreen(self):
        """Handle mouse movement in fullscreen from video widget"""
        logger.debug(f"Mouse move signal received - cursor_hidden: {self._cursor_hidden}")
        if self._cursor_hidden:
            logger.debug("Showing controls due to mouse movement")
            self._show_controls()
        else:
            logger.debug("Restarting hide timer")
            self._start_hide_timer()
    
    def eventFilter(self, obj, event):
        """Filter events for custom slider behavior and video widget mouse moves"""
        # Handle progress slider clicks (only if slider exists)
        if hasattr(self, 'progress_slider') and obj == self.progress_slider and event.type() == QEvent.Type.MouseButtonPress:
            if event.button() == Qt.MouseButton.LeftButton:
                # Calculate click position and seek
                value = QStyle.sliderValueFromPosition(
                    self.progress_slider.minimum(),
                    self.progress_slider.maximum(),
                    int(event.position().x()),
                    self.progress_slider.width()
                )
                self.progress_slider.setValue(value)
                # Trigger seek
                position = value / 1000.0
                duration = self.player.duration
                if duration > 0:
                    self.player.seek(position * duration)
                return True
        
        # Handle video widget mouse movements in fullscreen
        if hasattr(self, 'video_widget') and obj == self.video_widget and event.type() == QEvent.Type.MouseMove:
            if self.isFullScreen():
                if self._cursor_hidden:
                    self._show_controls()
                else:
                    self._start_hide_timer()
        
        return super().eventFilter(obj, event)
    
    def _apply_theme(self):
        """Apply current theme to the application"""
        stylesheet = self.theme_manager.get_full_stylesheet()
        self.setStyleSheet(stylesheet)
        
        # Update control panel background
        panel_style = self.theme_manager.get_stylesheet('control_panel')
        self.control_panel.setStyleSheet(panel_style)
        
        # Update theme toggle button and menu action
        if self.theme_manager.current_theme == Theme.DARK:
            self.theme_action.setText("☀️ Light Mode")
            self.theme_toggle_button.setText("🌙")
            self.theme_toggle_button.setToolTip("Switch to Light Mode")
        else:
            self.theme_action.setText("🌙 Dark Mode")
            self.theme_toggle_button.setText("☀️")
            self.theme_toggle_button.setToolTip("Switch to Dark Mode")
    
    def _toggle_theme(self):
        """Toggle between light and dark themes"""
        self.theme_manager.toggle_theme()
        self._apply_theme()
        logger.info(f"Theme changed to {self.theme_manager.current_theme.value}")
    
    def _start_fast_forward(self):
        """Start fast forwarding"""
        if not self.current_file:
            return
        
        self._is_fast_forwarding = True
        self._fast_forward_timer = QTimer()
        self._fast_forward_timer.timeout.connect(lambda: self.player.seek(2, relative=True))
        self._fast_forward_timer.start(100)
        logger.info("Fast forward started")
    
    def _stop_fast_forward(self):
        """Stop fast forwarding"""
        if self._fast_forward_timer:
            self._fast_forward_timer.stop()
            self._fast_forward_timer = None
        self._is_fast_forwarding = False
        logger.info("Fast forward stopped")
    
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
            
            # Resize window to match video resolution
            self._resize_to_video()
            
            logger.info(f"Playing: {filepath}")
        else:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to load file:\n{filepath}"
            )
    
    def _resize_to_video(self):
        """Resize main window to match video resolution (with reasonable limits)"""
        try:
            from PyQt6.QtCore import QSize
            from PyQt6.QtGui import QGuiApplication
            
            # Get video size from player
            video_size = self.player.get_video_size()
            
            if video_size and isinstance(video_size, QSize) and video_size.isValid():
                # Add control panel and menu bar height
                menu_height = self.menuBar().height() if self.menuBar().isVisible() else 0
                total_height = video_size.height() + self.control_panel.height() + menu_height
                
                # Limit to 90% of screen size
                screen = QGuiApplication.primaryScreen().availableGeometry()
                max_width = int(screen.width() * 0.9)
                max_height = int(screen.height() * 0.9)
                
                # Calculate final size
                final_width = min(video_size.width(), max_width)
                final_height = min(total_height, max_height)
                
                # Resize and center window
                self.resize(final_width, final_height)
                
                # Center on screen
                screen_center = screen.center()
                window_rect = self.frameGeometry()
                window_rect.moveCenter(screen_center)
                self.move(window_rect.topLeft())
                
                logger.info(f"Resized window to {final_width}x{final_height} (video: {video_size.width()}x{video_size.height()})")
            else:
                logger.debug("Video size not yet available, will retry")
                # Retry after more time for metadata to load
                QTimer.singleShot(500, self._resize_to_video)
        except Exception as e:
            logger.warning(f"Could not resize to video: {e}")
    
    def _toggle_play_pause(self):
        """
        Toggle play/pause state
        Manages overlay activation based on playback state
        """
        if not self.current_file:
            self._on_open_file()
            return
        
        self.player.toggle_pause()
        self._update_play_button()
        self._update_overlay_state()
    
    def _update_overlay_state(self):
        """
        Update overlay visibility based on playback and fullscreen state
        Overlay is active when paused in fullscreen, inactive when playing
        """
        if not self.isFullScreen():
            self.fullscreen_overlay.deactivate()
            return
        
        if self.player.is_playing:
            # Video playing: use frame-based detection, hide overlay
            self.fullscreen_overlay.deactivate()
        else:
            # Video paused: activate overlay to catch mouse movements
            self.fullscreen_overlay.setGeometry(self.video_widget.rect())
            self.fullscreen_overlay.activate()
    
    def _on_stop(self):
        """Handle stop button"""
        self.player.stop()
        self._update_play_button()
    
    def _update_play_button(self):
        """Update play/pause button icon"""
        if self.player.is_playing:
            self.play_button.setText("⏸")
        else:
            self.play_button.setText("▶")
    
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
        """
        Toggle fullscreen mode with automatic control hiding
        Manages overlay state based on playback status
        """
        # Activate transition lock FIRST to block any trailing mouse events
        self.video_widget.start_fullscreen_transition()
        
        if self.isFullScreen():
            # Exit fullscreen
            self._stop_fast_forward()  # Stop any fast-forward in progress
            self.showNormal()
            self.menuBar().show()
            self.control_panel.show()
            self._stop_hide_timer()
            self.setCursor(Qt.CursorShape.ArrowCursor)
            self._cursor_hidden = False
            self.fullscreen_overlay.deactivate()
        else:
            # Enter fullscreen
            self.showFullScreen()
            self.menuBar().hide()
            self._start_hide_timer()
            self._update_overlay_state()
    
    def _start_hide_timer(self):
        """Start timer to hide controls after inactivity"""
        if self._fullscreen_hide_timer:
            self._fullscreen_hide_timer.stop()
        
        self._fullscreen_hide_timer = QTimer()
        self._fullscreen_hide_timer.timeout.connect(self._hide_controls)
        self._fullscreen_hide_timer.start(3000)  # Hide after 3 seconds of inactivity
    
    def _stop_hide_timer(self):
        """Stop the hide timer"""
        if self._fullscreen_hide_timer:
            self._fullscreen_hide_timer.stop()
            self._fullscreen_hide_timer = None
    
    def _hide_controls(self):
        """Hide controls and cursor in fullscreen"""
        if self.isFullScreen():
            self.control_panel.hide()
            self.setCursor(Qt.CursorShape.BlankCursor)
            self._cursor_hidden = True
    
    def _show_controls(self):
        """Show controls and cursor in fullscreen"""
        if self.isFullScreen():
            self.control_panel.show()
            self.setCursor(Qt.CursorShape.ArrowCursor)
            self._cursor_hidden = False
            # Restart hide timer
            self._start_hide_timer()
    
    def event(self, event):
        """Handle all events including mouse movements"""
        if event.type() == QEvent.Type.MouseMove and self.isFullScreen():
            if self._cursor_hidden:
                self._show_controls()
            else:
                # Reset hide timer on mouse movement
                self._start_hide_timer()
        return super().event(event)
    
    def mouseMoveEvent(self, event):
        """Handle mouse movement in fullscreen"""
        if self.isFullScreen():
            if self._cursor_hidden:
                self._show_controls()
            else:
                # Reset hide timer on mouse movement
                self._start_hide_timer()
        super().mouseMoveEvent(event)
    
    def _cycle_speed(self):
        """Cycle through playback speeds"""
        speeds = [0.5, 1.0, 1.5, 2.0]
        current_text = self.speed_button.text()
        current_speed = float(current_text.replace("x", ""))
        
        try:
            current_index = speeds.index(current_speed)
            next_index = (current_index + 1) % len(speeds)
        except ValueError:
            next_index = 1
        
        new_speed = speeds[next_index]
        self.player.set_speed(new_speed)
        self.speed_button.setText(f"{new_speed}x")
    
    def _on_slider_pressed(self):
        """Handle slider press"""
        self.is_seeking = True
    
    def _on_slider_released(self):
        """Handle slider release"""
        self.is_seeking = False
        position = self.progress_slider.value() / 1000.0
        duration = self.player.duration
        if duration > 0:
            self.player.seek(position * duration)
    
    def _on_slider_moved(self, value):
        """Handle slider movement"""
        position = value / 1000.0
        duration = self.player.duration
        if duration > 0:
            time_seconds = position * duration
            self.time_label.setText(self._format_time(time_seconds))
    
    def _on_frame_update(self, frame):
        """Handle frame updates from player"""
        self.video_widget.display_frame(frame)
    
    def _on_time_update(self, time_pos):
        """
        Handle time position updates from player
        Also performs frame-based mouse detection when video is playing
        """
        if not self.is_seeking:
            duration = self.player.duration
            if duration > 0:
                position = int((time_pos / duration) * 1000)
                self.progress_slider.setValue(position)
            
            self.time_label.setText(self._format_time(time_pos))
        
        # Frame-based mouse detection (when video is playing in fullscreen)
        self._check_mouse_movement_while_playing()
    
    def _check_mouse_movement_while_playing(self):
        """
        Check for mouse movement while video is playing
        This provides mouse detection when QVideoWidget doesn't emit events
        """
        if not self.isFullScreen() or not self.player.is_playing:
            return
        
        from PyQt6.QtGui import QCursor
        current_pos = QCursor.pos()
        
        # Check if mouse has moved since last check
        if self._last_mouse_pos is not None and current_pos != self._last_mouse_pos:
            if self._cursor_hidden:
                self._show_controls()
            else:
                self._start_hide_timer()
        
        self._last_mouse_pos = current_pos
    
    def _on_overlay_mouse_move(self):
        """
        Handle mouse movement from overlay widget (when paused)
        Overlay is only active when video is paused in fullscreen
        """
        if self._cursor_hidden:
            self._show_controls()
        else:
            self._start_hide_timer()
    
    def _on_duration_changed(self, duration):
        """Handle duration change when file loads"""
        self.duration_label.setText(self._format_time(duration))
        # Resize window after video metadata is loaded
        QTimer.singleShot(100, self._resize_to_video)
    
    def _on_player_error(self, error_message):
        """Handle player errors"""
        QMessageBox.critical(
            self,
            "Playback Error",
            f"An error occurred during playback:\n\n{error_message}"
        )
        logger.error(f"Player error: {error_message}")
    
    def _on_playback_ended(self):
        """Handle playback end"""
        self._update_play_button()
        logger.info("Playback ended")
    
    def _update_ui(self):
        """Update UI elements"""
        duration = self.player.duration
        if duration > 0:
            self.duration_label.setText(self._format_time(duration))
        
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
            "<li>Mouse click-to-seek on progress bar</li>"
            "<li>Keyboard shortcuts for easy control</li>"
            "<li>Dark and Light theme modes</li>"
            "<li>Double-click video for fullscreen</li>"
            "<li>Click and hold video to fast forward</li>"
            "<li>Variable playback speeds (0.5x - 2.0x)</li>"
            "</ul>"
            "<p>Built with PyQt6 Multimedia</p>"
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
        <h3>Mouse Controls</h3>
        <table>
        <tr><td><b>Double-click video</b></td><td>Toggle Fullscreen</td></tr>
        <tr><td><b>Click and hold video</b></td><td>Fast Forward</td></tr>
        <tr><td><b>Click progress bar</b></td><td>Seek to position</td></tr>
        </table>
        """
        QMessageBox.information(self, "Keyboard Shortcuts", shortcuts_text)
    
    def keyPressEvent(self, event):
        """Handle key press events"""
        if event.key() == Qt.Key.Key_Escape and self.isFullScreen():
            self.showNormal()
            event.accept()
        else:
            super().keyPressEvent(event)
    
    def closeEvent(self, event):
        """Handle window close event"""
        self._stop_fast_forward()
        self.player.shutdown()
        event.accept()
        logger.info("Application closed")
