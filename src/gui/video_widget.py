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
        
        # Single-click detection (delayed to distinguish from double-click)
        self._click_timer = QTimer()
        self._click_timer.setSingleShot(True)
        self._click_timer.timeout.connect(self._on_single_click_confirmed)
        self._click_delay = 250  # Wait 250ms to confirm it's not a double-click
        
        # Track if we're in a potential double-click scenario
        self._expecting_double_click = False
        self._double_click_prevention_timer = QTimer()
        self._double_click_prevention_timer.setSingleShot(True)
        self._double_click_prevention_timer.timeout.connect(self._reset_double_click_flag)
        
        # Fullscreen transition lock - blocks ALL mouse events during fullscreen transitions
        self._fullscreen_transition_active = False
        self._fullscreen_transition_timer = QTimer()
        self._fullscreen_transition_timer.setSingleShot(True)
        self._fullscreen_transition_timer.timeout.connect(self._end_fullscreen_transition)
        self._fullscreen_transition_duration = 350  # Block events for 350ms
    
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
            logger.info("=== DOUBLE-CLICK EVENT ===")
            logger.info(f"Timers before cancel - press: {self._press_timer.isActive()}, click: {self._click_timer.isActive()}, prevention: {self._double_click_prevention_timer.isActive()}")
            
            # Cancel ALL pending timers
            self._is_mouse_pressed = False
            self._press_timer.stop()
            self._click_timer.stop()  # Cancel pending single-click - CRITICAL!
            self._double_click_prevention_timer.stop()
            
            # SET FLAG TO PREVENT SUBSEQUENT EVENTS (release events come after double-click)
            self._expecting_double_click = True
            self._double_click_prevention_timer.start(300)  # Prevent any events for 300ms after double-click
            logger.info("Set double-click prevention flag to block subsequent events")
            
            # Stop any active fast-forward
            if self._is_fast_forwarding:
                self._is_fast_forwarding = False
                self.fast_forward_stopped.emit()
                logger.info("Fast forward stopped by double-click")
            
            logger.info("All timers cancelled - emitting double_clicked signal")
            self.double_clicked.emit()
        super().mouseDoubleClickEvent(event)
    
    def mousePressEvent(self, event: QMouseEvent):
        """
        Handle mouse press for long-press detection
        
        Args:
            event: Mouse event with press information
        """
        if event.button() == Qt.MouseButton.LeftButton:
            logger.info(f"=== MOUSE PRESS === transition_active: {self._fullscreen_transition_active}, expecting_double_click: {self._expecting_double_click}")
            
            # Block ALL events during fullscreen transition
            if self._fullscreen_transition_active:
                logger.info("BLOCKED - fullscreen transition active")
                return
            
            # Don't start timer if we're expecting a double-click
            if not self._expecting_double_click:
                self._is_mouse_pressed = True
                self._press_timer.start(self._long_press_threshold)
                logger.info("Started long-press timer (500ms)")
            else:
                logger.info("Ignoring press - expecting double-click")
        super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event: QMouseEvent):
        """
        Handle mouse release to detect single clicks or stop fast forward
        
        Args:
            event: Mouse event with release information
        """
        if event.button() == Qt.MouseButton.LeftButton:
            logger.info(f"=== MOUSE RELEASE === transition_active: {self._fullscreen_transition_active}, was_fast_forwarding: {self._is_fast_forwarding}")
            
            # Block ALL events during fullscreen transition
            if self._fullscreen_transition_active:
                logger.info("BLOCKED - fullscreen transition active")
                return
            
            was_fast_forwarding = self._is_fast_forwarding
            
            self._is_mouse_pressed = False
            self._press_timer.stop()
            logger.info("Stopped long-press timer")
            
            # Stop fast forward if active
            if was_fast_forwarding:
                self._is_fast_forwarding = False
                self.fast_forward_stopped.emit()
                logger.info("Fast forward stopped")
            else:
                # Start timer for single-click detection (wait to see if double-click follows)
                self._click_timer.start(self._click_delay)
                logger.info(f"Started click confirmation timer ({self._click_delay}ms)")
                # Set flag to prevent next press from starting long-press timer
                self._expecting_double_click = True
                self._double_click_prevention_timer.start(self._click_delay)
                logger.info(f"Set double-click prevention flag (expires in {self._click_delay}ms)")
        
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
            logger.info("!!! FAST FORWARD STARTED (long-press timer fired) !!!")
    
    def _on_single_click_confirmed(self):
        """Emit single-click signal after delay confirms it's not a double-click"""
        logger.info("!!! SINGLE CLICK CONFIRMED - emitting signal (will toggle pause) !!!")
        self.single_clicked.emit()
    
    def _reset_double_click_flag(self):
        """Reset the double-click expectation flag"""
        self._expecting_double_click = False
        logger.info("Double-click prevention window expired")
    
    def start_fullscreen_transition(self):
        """
        Start fullscreen transition lock
        Blocks all mouse press/release events for a short period
        Called by main_window when toggling fullscreen
        """
        logger.info(">>> FULLSCREEN TRANSITION LOCK ACTIVATED <<<")
        self._fullscreen_transition_active = True
        self._fullscreen_transition_timer.start(self._fullscreen_transition_duration)
        
        # Also cancel any pending interactions
        self.cancel_pending_interactions()
    
    def _end_fullscreen_transition(self):
        """End fullscreen transition lock"""
        self._fullscreen_transition_active = False
        logger.info(">>> FULLSCREEN TRANSITION LOCK RELEASED <<<")
    
    def cancel_pending_interactions(self):
        """
        Cancel any pending mouse interactions (long-press timer, etc.)
        Called when changing fullscreen state to prevent stuck timers
        """
        logger.info("=== CANCEL PENDING INTERACTIONS ===")
        logger.info(f"Active timers - press: {self._press_timer.isActive()}, click: {self._click_timer.isActive()}, prevention: {self._double_click_prevention_timer.isActive()}")
        
        self._is_mouse_pressed = False
        self._press_timer.stop()
        self._click_timer.stop()
        self._double_click_prevention_timer.stop()
        self._expecting_double_click = False
        
        # Stop any active fast-forward
        if self._is_fast_forwarding:
            self._is_fast_forwarding = False
            self.fast_forward_stopped.emit()
            logger.info("Fast-forward cancelled")
        
        logger.info("All pending interactions cancelled")
