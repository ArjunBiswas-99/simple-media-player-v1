"""
Main Application Window Module

This module defines the MainWindow class which serves as the primary UI controller
for the media player application. It coordinates between the video display, playback
controls, and user interactions while maintaining a Netflix-inspired aesthetic.

Responsibilities:
    - UI layout and widget management
    - User input handling (keyboard, mouse)
    - Theme application and switching
    - Fullscreen mode management
    - File operations (open, drop)
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
from .welcome_screen import WelcomeScreen
from .buffering_widget import BufferingWidget
from .network_stream_dialog import NetworkStreamDialog
from ..core.player import MediaPlayer
from ..core.network_stream_handler import NetworkStreamHandler

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """
    Main application window with Netflix-inspired UI
    
    This class coordinates all UI components and handles user interactions.
    It follows the Single Responsibility Principle by delegating specific tasks
    to specialized components (MediaPlayer for playback, ThemeManager for styling).
    
    Attributes:
        VIDEO_EXTENSIONS: Supported video file formats
        SUBTITLE_EXTENSIONS: Supported subtitle file formats
    """
    
    # Supported file formats
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
        """
        Initialize core application components and state variables
        
        Sets up the media player, theme manager, and fullscreen control system.
        Follows Dependency Inversion Principle by depending on abstractions
        (MediaPlayer, ThemeManager) rather than concrete implementations.
        """
        # Core components (abstractions following DIP)
        self.player = MediaPlayer()
        self.theme_manager = ThemeManager()
        self.stream_handler = NetworkStreamHandler()
        
        # Playback state
        self.current_file = None
        self.is_seeking = False
        
        # Network stream state
        self.is_network_stream = False
        self.network_stream_url = None
        self.current_quality = '480p'
        
        # Fast forward feature state
        self._fast_forward_timer = None
        self._is_fast_forwarding = False
        
        # Fullscreen control auto-hide system
        self._fullscreen_hide_timer = None
        self._cursor_hidden = False
        self._controls_visible = True
        self._last_mouse_pos = None  # For frame-based mouse detection
        
        # Enable mouse tracking for fullscreen interactions
        self.setMouseTracking(True)
    
    def _setup_ui(self):
        """
        Configure and build the user interface layout
        
        Creates the main window structure with video display area and control panel.
        Uses composition pattern to build complex UI from simpler components.
        """
        self.setWindowTitle("Simple Media Player by Arjun Biswas")
        self.setMinimumSize(800, 600)
        
        # Set application icon
        self._set_window_icon()
        
        # Custom widget for fullscreen mouse tracking (Inner class following SRP)
        class MouseTrackingWidget(QWidget):
            """Specialized widget that tracks mouse movement for fullscreen mode"""
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
        
        # Create welcome screen overlay (shown when no video is loaded)
        self.welcome_screen = WelcomeScreen(self.video_widget)
        self.welcome_screen.setGeometry(self.video_widget.rect())
        self.welcome_screen.show()
        
        # Create buffering widget overlay (shown during stream extraction/buffering)
        self.buffering_widget = BufferingWidget(self.video_widget)
        self.buffering_widget.setGeometry(self.video_widget.rect())
        self.buffering_widget.hide()
        
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
        """
        Create the bottom control panel with Netflix-style gradient overlay
        
        Returns:
            QWidget: Configured control panel with progress bar and buttons
        """
        panel = QWidget()
        panel.setFixedHeight(90)
        panel.setObjectName("controlPanel")
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 10, 20, 12)
        layout.setSpacing(8)
        
        layout.addLayout(self._create_progress_bar())
        layout.addLayout(self._create_control_buttons())
        
        return panel
    
    def _create_progress_bar(self):
        """
        Create ultra-thin Netflix-style progress bar with time display
        
        Returns:
            QHBoxLayout: Layout containing time label, slider, and duration
        """
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
        """
        Create control buttons with Netflix minimalist design
        
        Layout: [Play] [Stop] | [Volume] | [Speed] | [stretch] | [Theme] [Fullscreen]
        
        Returns:
            QHBoxLayout: Layout containing all control buttons
        """
        button_layout = QHBoxLayout()
        button_layout.setSpacing(8)
        
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
        
        button_layout.addSpacing(12)
        
        # Volume controls
        button_layout.addLayout(self._create_volume_controls())
        
        button_layout.addSpacing(12)
        
        # Speed control
        button_layout.addLayout(self._create_speed_control())
        
        button_layout.addSpacing(12)
        
        # Quality selector (for network streams only)
        button_layout.addLayout(self._create_quality_selector())
        
        button_layout.addStretch()
        
        # Theme toggle button
        self.theme_toggle_button = QPushButton("🌙")
        self.theme_toggle_button.clicked.connect(self._toggle_theme)
        self.theme_toggle_button.setObjectName("themeToggle")
        self.theme_toggle_button.setToolTip("Toggle Dark/Light Mode")
        button_layout.addWidget(self.theme_toggle_button)
        
        button_layout.addSpacing(4)
        
        # Fullscreen button (icon-only for Netflix style)
        fullscreen_button = QPushButton("⛶")
        fullscreen_button.setObjectName("iconButton")
        fullscreen_button.clicked.connect(self._toggle_fullscreen)
        fullscreen_button.setToolTip("Fullscreen (F)")
        fullscreen_button.setAttribute(Qt.WidgetAttribute.WA_MacShowFocusRect, False)
        fullscreen_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
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
        """
        Create a circular icon button with Netflix styling
        
        Args:
            icon: Qt standard icon identifier
            callback: Function to call on button click
            tooltip: Tooltip text for the button
            
        Returns:
            QPushButton: Configured icon button (40px circular, transparent background)
        """
        button = QPushButton()
        
        # Map standard icons to Unicode symbols for better color control
        icon_map = {
            QStyle.StandardPixmap.SP_MediaPlay: "▶",
            QStyle.StandardPixmap.SP_MediaPause: "⏸",
            QStyle.StandardPixmap.SP_MediaStop: "⏹"
        }
        
        if icon in icon_map:
            button.setText(icon_map[icon])
        else:
            button.setIcon(self.style().standardIcon(icon))
        
        button.clicked.connect(callback)
        button.setToolTip(tooltip)
        button.setObjectName("iconButton")
        
        # Disable macOS focus rectangle
        button.setAttribute(Qt.WidgetAttribute.WA_MacShowFocusRect, False)
        button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        
        return button
    
    def _create_volume_controls(self):
        """
        Create Netflix-style volume control with dynamic icon and inline slider
        
        Features:
            - Clickable volume icon for mute/unmute
            - Dynamic icon updates based on volume level
            - Compact inline slider (80px width)
            
        Returns:
            QHBoxLayout: Layout containing volume icon, slider, and percentage label
        """
        layout = QHBoxLayout()
        layout.setSpacing(6)
        
        # Volume icon button (mute toggle) - centered vertically
        self.volume_icon_button = QPushButton("🔊")
        self.volume_icon_button.setObjectName("iconButton")
        self.volume_icon_button.clicked.connect(self._toggle_mute)
        self.volume_icon_button.setToolTip("Mute/Unmute (M)")
        layout.addWidget(self.volume_icon_button)
        
        # Volume slider - centered vertically
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(100)
        self.volume_slider.setFixedWidth(80)
        self.volume_slider.setFixedHeight(40)
        self.volume_slider.setObjectName("volumeSlider")
        self.volume_slider.valueChanged.connect(self._on_volume_changed)
        layout.addWidget(self.volume_slider)
        
        # Volume percentage label - centered vertically
        self.volume_label = QLabel("100%")
        self.volume_label.setFixedWidth(35)
        self.volume_label.setFixedHeight(40)
        self.volume_label.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
        self.volume_label.setObjectName("volumeLabel")
        layout.addWidget(self.volume_label)
        
        return layout
    
    def _create_speed_control(self):
        """
        Create speed control for cycling through playback rates
        
        Cycles through: 0.5x → 1.0x → 1.5x → 2.0x
        
        Returns:
            QHBoxLayout: Layout containing speed label and cycle button
        """
        layout = QHBoxLayout()
        layout.setSpacing(6)
        
        # Speed label - centered vertically
        speed_label = QLabel("Speed:")
        speed_label.setFixedHeight(40)
        speed_label.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
        speed_label.setObjectName("speedLabel")
        layout.addWidget(speed_label)
        
        # Speed button - matches icon button height
        self.speed_button = QPushButton("1.0x")
        self.speed_button.clicked.connect(self._cycle_speed)
        self.speed_button.setFixedWidth(55)
        self.speed_button.setObjectName("iconButton")
        layout.addWidget(self.speed_button)
        
        return layout
    
    def _create_quality_selector(self):
        """
        Create quality selector dropdown for network streams
        
        Only visible when playing network streams (YouTube, etc.).
        Hidden for local files to avoid confusion.
        
        Returns:
            QHBoxLayout: Layout containing quality label and dropdown
        """
        from PyQt6.QtWidgets import QComboBox
        
        layout = QHBoxLayout()
        layout.setSpacing(6)
        
        # Quality label
        self.quality_label = QLabel("Quality:")
        self.quality_label.setFixedHeight(40)
        self.quality_label.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
        self.quality_label.setObjectName("speedLabel")
        self.quality_label.hide()  # Initially hidden
        layout.addWidget(self.quality_label)
        
        # Quality dropdown
        self.quality_combo = QComboBox()
        self.quality_combo.addItems([
            "360p",
            "480p",
            "720p",
            "1080p"
        ])
        self.quality_combo.setCurrentText("480p")
        self.quality_combo.currentTextChanged.connect(self._on_quality_changed)
        self.quality_combo.setObjectName("iconButton")
        self.quality_combo.setFixedWidth(80)
        self.quality_combo.setFixedHeight(40)
        self.quality_combo.hide()  # Initially hidden
        layout.addWidget(self.quality_combo)
        
        return layout
    
    def _set_window_icon(self):
        """Set the window icon from the icons directory"""
        try:
            from PyQt6.QtGui import QIcon
            from pathlib import Path
            
            # Get path to icon file
            icon_dir = Path(__file__).parent / 'icons'
            
            # Try PNG first (cross-platform), then ICO (Windows)
            icon_path = icon_dir / 'icon_256x256.png'
            if not icon_path.exists():
                icon_path = icon_dir / 'app_icon.ico'
            
            if icon_path.exists():
                icon = QIcon(str(icon_path))
                self.setWindowIcon(icon)
                logger.info(f"Window icon set: {icon_path.name}")
            else:
                logger.warning("Icon file not found")
        except Exception as e:
            logger.warning(f"Could not set window icon: {e}")
    
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
        
        # Network stream action
        open_stream_action = QAction("Open &Network Stream...", self)
        open_stream_action.setShortcut("Ctrl+N")
        open_stream_action.triggered.connect(self._on_open_network_stream)
        file_menu.addAction(open_stream_action)
        
        file_menu.addSeparator()
        
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
        
        # Update welcome screen styling
        if hasattr(self, 'welcome_screen'):
            is_dark = self.theme_manager.current_theme == Theme.DARK
            welcome_style = self.welcome_screen.get_stylesheet(is_dark)
            self.welcome_screen.setStyleSheet(welcome_style)
        
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
    
    def _on_open_network_stream(self):
        """Handle open network stream action"""
        dialog = NetworkStreamDialog(self)
        dialog.url_accepted.connect(self._load_network_stream)
        dialog.exec()
    
    def _load_network_stream(self, url: str):
        """
        Load and play a network stream from URL
        
        Args:
            url: The network stream URL (YouTube, Dailymotion, etc.)
        """
        from PyQt6.QtCore import QThread, QTimer
        
        # Show buffering widget immediately
        self.buffering_widget.show_loading("Extracting video stream...")
        
        # Extract stream in background to avoid UI freeze
        def extract_stream():
            """Background thread function for stream extraction"""
            return self.stream_handler.extract_stream_info(url)
        
        # Use QTimer to run extraction without blocking
        QTimer.singleShot(100, lambda: self._perform_stream_extraction(url))
    
    def _perform_stream_extraction(self, url: str, quality: str = '480p'):
        """
        Perform stream extraction and load into player
        
        Args:
            url: The network stream URL
            quality: Quality to extract (default: 480p)
        """
        try:
            # Extract stream information at specified quality
            stream_info = self.stream_handler.extract_stream_info(url, quality)
            
            if not stream_info:
                self.buffering_widget.hide_loading()
                QMessageBox.critical(
                    self,
                    "Stream Extraction Failed",
                    "Failed to extract video stream from the provided URL.\n\n"
                    "Possible reasons:\n"
                    "• Invalid or unsupported URL\n"
                    "• Video is private or restricted\n"
                    "• Network connection issue\n"
                    "• Platform blocked access"
                )
                return
            
            # Update buffering message
            self.buffering_widget.set_status("Loading stream...")
            
            # Load stream into player
            if self.player.load_network_stream(stream_info['url'], stream_info['title']):
                # Update window title
                self.setWindowTitle(f"Simple Media Player - {stream_info['title']} | by Arjun Biswas")
                
                # Set network stream state
                self.current_file = stream_info['title']
                self.is_network_stream = True
                self.network_stream_url = url
                self.current_quality = quality
                
                # Hide welcome screen
                if hasattr(self, 'welcome_screen'):
                    self.welcome_screen.hide()
                
                # Start playback
                self.player.play()
                self._update_play_button()
                
                # Show quality selector for network streams (after playback starts)
                QTimer.singleShot(100, self._update_quality_selector_visibility)
                
                # Hide buffering widget after short delay
                QTimer.singleShot(1000, self.buffering_widget.hide_loading)
                
                logger.info(f"Playing network stream: {stream_info['title']} ({stream_info['platform']}) at {quality}")
            else:
                self.buffering_widget.hide_loading()
                QMessageBox.critical(
                    self,
                    "Playback Error",
                    f"Failed to load video stream.\n\n"
                    f"Title: {stream_info['title']}\n"
                    f"Platform: {stream_info['platform']}"
                )
        
        except Exception as e:
            self.buffering_widget.hide_loading()
            logger.error(f"Error loading network stream: {e}", exc_info=True)
            QMessageBox.critical(
                self,
                "Error",
                f"An error occurred while loading the stream:\n\n{str(e)}"
            )
    
    def _load_file(self, filepath):
        """Load and play a media file"""
        if self.player.load_file(filepath):
            self.current_file = filepath
            self.is_network_stream = False
            self.network_stream_url = None
            self.setWindowTitle(f"Simple Media Player - {Path(filepath).name} | by Arjun Biswas")
            
            # Hide welcome screen when video loads
            if hasattr(self, 'welcome_screen'):
                self.welcome_screen.hide()
            
            self.player.play()
            self._update_play_button()
            
            # Hide quality selector for local files
            self._update_quality_selector_visibility()
            
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
        
        # Update quality selector visibility when play/pause changes
        self._update_quality_selector_visibility()
    
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
        
        # Hide quality selector when stopped
        self._update_quality_selector_visibility()
    
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
        self._update_volume_icon()
    
    def _volume_up(self):
        """Increase volume by 5%"""
        new_volume = min(100, self.volume_slider.value() + 5)
        self.volume_slider.setValue(new_volume)
    
    def _volume_down(self):
        """Decrease volume by 5%"""
        new_volume = max(0, self.volume_slider.value() - 5)
        self.volume_slider.setValue(new_volume)
    
    def _toggle_mute(self):
        """Toggle mute state and update volume icon"""
        self.player.toggle_mute()
        self._update_volume_icon()
    
    def _update_volume_icon(self):
        """Update volume icon based on mute state and volume level"""
        if self.player.muted:
            self.volume_icon_button.setText("🔇")
        else:
            volume = self.volume_slider.value()
            if volume == 0:
                self.volume_icon_button.setText("🔇")
            elif volume < 50:
                self.volume_icon_button.setText("🔉")
            else:
                self.volume_icon_button.setText("🔊")
    
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
    
    def _update_quality_selector_visibility(self):
        """Show/hide quality selector based on stream state"""
        should_show = (
            self.is_network_stream and 
            self.current_file is not None and
            (self.player.is_playing or self.player.is_paused)
        )
        
        self.quality_label.setVisible(should_show)
        self.quality_combo.setVisible(should_show)
        
        logger.info(f"Quality selector visibility: {should_show} (is_network_stream={self.is_network_stream}, current_file={self.current_file is not None}, playing={self.player.is_playing}, paused={self.player.is_paused})")
    
    def _on_quality_changed(self, quality_text):
        """Handle quality selection change"""
        if not self.is_network_stream or not self.network_stream_url:
            return
        
        new_quality = quality_text  # Already just "480p", "720p", etc.
        
        if new_quality == self.current_quality:
            return  # No change
        
        logger.info(f"Changing quality from {self.current_quality} to {new_quality}")
        
        # Save current position and playback state
        current_pos = self.player.time_pos
        was_playing = self.player.is_playing
        
        # Show buffering with quality info
        self.buffering_widget.show_loading(f"Switching to {quality_text}...")
        
        # Re-extract and load at new quality
        QTimer.singleShot(100, lambda: self._reload_stream_with_quality(
            self.network_stream_url,
            new_quality,
            current_pos,
            was_playing
        ))
    
    def _reload_stream_with_quality(self, url: str, quality: str, seek_to: float, auto_play: bool):
        """
        Reload network stream with different quality
        
        Args:
            url: Original network stream URL
            quality: New quality to load
            seek_to: Position to seek to after loading
            auto_play: Whether to auto-play after loading
        """
        try:
            logger.info(f"Reloading stream at {quality}")
            
            # Extract with new quality
            stream_info = self.stream_handler.extract_stream_info(url, quality)
            
            if not stream_info:
                self.buffering_widget.hide_loading()
                QMessageBox.warning(
                    self,
                    "Quality Change Failed",
                    f"Could not load stream at {quality}.\n"
                    "Keeping current quality."
                )
                # Revert dropdown selection
                self.quality_combo.setCurrentText(self.current_quality)
                return
            
            # Load new stream
            if self.player.load_network_stream(stream_info['url'], stream_info['title']):
                self.current_quality = quality
                
                # Seek to previous position
                if seek_to > 0:
                    QTimer.singleShot(500, lambda: self.player.seek(seek_to))
                
                # Resume playback if was playing
                if auto_play:
                    QTimer.singleShot(600, self.player.play)
                    self._update_play_button()
                
                self.buffering_widget.hide_loading()
                logger.info(f"Successfully changed to {quality}")
            else:
                self.buffering_widget.hide_loading()
                QMessageBox.warning(
                    self,
                    "Quality Change Failed",
                    f"Failed to load stream at {quality}.\n"
                    "Keeping current quality."
                )
                # Revert dropdown selection
                self.quality_combo.setCurrentText(self.current_quality)
                
        except Exception as e:
            self.buffering_widget.hide_loading()
            logger.error(f"Error changing quality: {e}", exc_info=True)
            QMessageBox.warning(
                self,
                "Quality Change Failed",
                f"An error occurred:\n{str(e)}\n\n"
                "Keeping current quality."
            )
            # Revert dropdown selection
            self.quality_combo.setCurrentText(self.current_quality)
    
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
            "About Simple Media Player",
            "<h3>Simple Media Player v1.0.0</h3>"
            "<p>by Arjun Biswas</p>"
            "<p>A modern, lightweight media player with Netflix-inspired design.</p>"
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
