"""
Video display widget - renders video content
"""

from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QPalette, QColor, QMouseEvent


class VideoWidget(QWidget):
    """Widget that displays video content via MPV"""
    
    # Signals
    double_clicked = pyqtSignal()
    fast_forward_started = pyqtSignal()
    fast_forward_stopped = pyqtSignal()
    
    def __init__(self, parent=None):
        """Initialize the video widget"""
        super().__init__(parent)
        
        self._setup_appearance()
        self._setup_interaction()
        
    def _setup_appearance(self):
        """Configure widget appearance"""
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(0, 0, 0))
        self.setPalette(palette)
        self.setMinimumSize(640, 480)
    
    def _setup_interaction(self):
        """Configure interaction features"""
        self.setAcceptDrops(True)
        self._drop_callback = None
        self._is_mouse_pressed = False
        self._press_timer = QTimer()
        self._press_timer.setSingleShot(True)
        self._press_timer.timeout.connect(self._on_long_press)
        self._long_press_threshold = 500  # milliseconds
    
    def set_drop_callback(self, callback):
        """Set callback for file drops"""
        self._drop_callback = callback
    
    def dragEnterEvent(self, event):
        """Handle drag enter events"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    
    def dropEvent(self, event):
        """Handle drop events"""
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls and self._drop_callback:
                filepath = urls[0].toLocalFile()
                self._drop_callback(filepath)
            event.acceptProposedAction()
    
    def mouseDoubleClickEvent(self, event: QMouseEvent):
        """Handle double-click to toggle fullscreen"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.double_clicked.emit()
        super().mouseDoubleClickEvent(event)
    
    def mousePressEvent(self, event: QMouseEvent):
        """Handle mouse press for long-press detection"""
        if event.button() == Qt.MouseButton.LeftButton:
            self._is_mouse_pressed = True
            self._press_timer.start(self._long_press_threshold)
        super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event: QMouseEvent):
        """Handle mouse release to stop fast forward"""
        if event.button() == Qt.MouseButton.LeftButton:
            self._is_mouse_pressed = False
            self._press_timer.stop()
            if hasattr(self, '_is_fast_forwarding') and self._is_fast_forwarding:
                self._is_fast_forwarding = False
                self.fast_forward_stopped.emit()
        super().mouseReleaseEvent(event)
    
    def _on_long_press(self):
        """Handle long press to start fast forward"""
        if self._is_mouse_pressed:
            self._is_fast_forwarding = True
            self.fast_forward_started.emit()
