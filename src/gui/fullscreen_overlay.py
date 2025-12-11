"""
Transparent overlay widget for capturing mouse movements in fullscreen mode
Used when video is paused to detect mouse movements for showing/hiding controls
"""

import logging
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QMouseEvent

logger = logging.getLogger(__name__)


class FullscreenMouseOverlay(QWidget):
    """
    Transparent widget that captures mouse movements when video is paused
    
    Responsibilities:
    - Detect mouse movements in fullscreen when video is paused
    - Emit signal to notify parent window of mouse activity
    - Remain transparent and non-intrusive
    """
    
    mouse_moved = pyqtSignal()
    
    def __init__(self, parent=None):
        """
        Initialize the overlay widget
        
        Args:
            parent: Parent widget (typically main window)
        """
        super().__init__(parent)
        self._setup_appearance()
        self._setup_behavior()
        logger.debug("Fullscreen mouse overlay initialized")
    
    def _setup_appearance(self):
        """Configure visual appearance to be completely transparent"""
        self.setStyleSheet("background: transparent;")
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, True)
    
    def _setup_behavior(self):
        """Configure interaction behavior"""
        self.setMouseTracking(True)
        self.hide()  # Hidden by default, shown only when needed
    
    def mouseMoveEvent(self, event: QMouseEvent):
        """
        Capture mouse movement and emit signal
        
        Args:
            event: Mouse movement event information
        """
        self.mouse_moved.emit()
        super().mouseMoveEvent(event)
    
    def activate(self):
        """Make overlay visible and active for capturing mouse movements"""
        self.show()
        self.raise_()
        logger.debug("Overlay activated")
    
    def deactivate(self):
        """Hide overlay when not needed"""
        self.hide()
        logger.debug("Overlay deactivated")
