"""
Video display widget using PyQt6 Multimedia
Handles video rendering and user interaction
"""

import logging
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QMouseEvent

logger = logging.getLogger(__name__)


class VideoWidget(QVideoWidget):
    """
    Widget for video display and user interaction
    
    Responsibilities:
    - Display video content via Qt Multimedia
    - Handle drag and drop for media files
    - Detect user interactions (double-click, long-press)
    - Emit signals for UI coordination
    """
    
    # Signals for user interactions
    single_clicked = pyqtSignal()
    double_clicked = pyqtSignal()
    fast_forward_started = pyqtSignal()
    fast_forward_stopped = pyqtSignal()
    mouse_moved_in_fullscreen = pyqtSignal()
    
    def __init__(self, parent=None):
        """Initialize the video widget"""
        super().__init__(parent)
        
        self._setup_appearance()
        self._setup_interaction()
        self._main_window = None
        
        logger.debug("Video widget initialized")
    
    def set_main_window(self, main_window):
        """Set reference to main window for fullscreen handling"""
        self._main_window = main_window
    
    def _setup_appearance(self):
        """Configure widget appearance"""
        self.setMinimumSize(640, 480)
        self.setAspectRatioMode(Qt.AspectRatioMode.KeepAspectRatio)
    
    def _setup_interaction(self):
        """Configure interaction features"""
        # Enable drag and drop
        self.setAcceptDrops(True)
        self._drop_callback = None
        
        # Long-press detection for fast forward
        self._is_mouse_pressed = False
        self._is_fast_forwarding = False
        self._press_timer = QTimer()
        self._press_timer.setSingleShot(True)
        self._press_timer.timeout.connect(self._on_long_press)
        self._long_press_threshold = 500  # milliseconds
    
    def set_drop_callback(self, callback):
        """
        Set callback function for file drops
        
        Args:
            callback: Function to call with dropped file path
        """
        self._drop_callback = callback
    
    def dragEnterEvent(self, event):
        """
        Handle drag enter events for files
        
        Args:
            event: QDragEnterEvent with mime data
        """
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    
    def dropEvent(self, event):
        """
        Handle file drop events
        
        Args:
            event: QDropEvent with dropped file data
        """
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls and self._drop_callback:
                filepath = urls[0].toLocalFile()
                self._drop_callback(filepath)
                logger.info(f"File dropped: {filepath}")
            event.acceptProposedAction()
    
    def mouseDoubleClickEvent(self, event: QMouseEvent):
        """
        Handle double-click to toggle fullscreen
        
        Args:
            event: Mouse event with click information
        """
        if event.button() == Qt.MouseButton.LeftButton:
            self.double_clicked.emit()
            logger.debug("Video double-clicked")
        super().mouseDoubleClickEvent(event)
    
    def mousePressEvent(self, event: QMouseEvent):
        """
        Handle mouse press for long-press detection
        
        Args:
            event: Mouse event with press information
        """
        if event.button() == Qt.MouseButton.LeftButton:
            self._is_mouse_pressed = True
            self._press_timer.start(self._long_press_threshold)
        super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event: QMouseEvent):
        """
        Handle mouse release to detect single clicks or stop fast forward
        
        Args:
            event: Mouse event with release information
        """
        if event.button() == Qt.MouseButton.LeftButton:
            was_fast_forwarding = self._is_fast_forwarding
            
            self._is_mouse_pressed = False
            self._press_timer.stop()
            
            # Stop fast forward if active
            if was_fast_forwarding:
                self._is_fast_forwarding = False
                self.fast_forward_stopped.emit()
                logger.debug("Fast forward stopped")
            # Don't emit single click here - it interferes with double-click
            # The single click should only happen if no double-click follows
        
        super().mouseReleaseEvent(event)
    
    def mouseMoveEvent(self, event: QMouseEvent):
        """
        Handle mouse movement - emit signal for fullscreen handling
        
        Args:
            event: Mouse event with movement information
        """
        if self._main_window and self._main_window.isFullScreen():
            logger.debug("Mouse moved in fullscreen - emitting signal")
            self.mouse_moved_in_fullscreen.emit()
        super().mouseMoveEvent(event)
    
    def _on_long_press(self):
        """Handle long press to start fast forward"""
        if self._is_mouse_pressed:
            self._is_fast_forwarding = True
            self.fast_forward_started.emit()
            logger.debug("Fast forward started")
