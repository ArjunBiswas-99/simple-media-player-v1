"""
Video display widget - renders video content from OpenCV frames
"""

import numpy as np
from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QSize
from PyQt6.QtGui import QPalette, QColor, QMouseEvent, QImage, QPixmap


class VideoWidget(QWidget):
    """Widget that displays video content from OpenCV frames"""
    
    # Signals
    double_clicked = pyqtSignal()
    fast_forward_started = pyqtSignal()
    fast_forward_stopped = pyqtSignal()
    
    def __init__(self, parent=None):
        """Initialize the video widget"""
        super().__init__(parent)
        
        self._setup_appearance()
        self._setup_interaction()
        self._setup_display()
        
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
    
    def _setup_display(self):
        """Setup display label for video frames"""
        self._display_label = QLabel(self)
        self._display_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._display_label.setScaledContents(False)
        self._display_label.setStyleSheet("background-color: black;")
        
        # Store current frame for display
        self._current_pixmap = None
    
    def set_drop_callback(self, callback):
        """Set callback for file drops"""
        self._drop_callback = callback
    
    def display_frame(self, frame: np.ndarray):
        """
        Display an OpenCV frame
        
        Args:
            frame: OpenCV frame (BGR format)
        """
        if frame is None:
            return
        
        try:
            # Convert BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Get frame dimensions
            height, width, channels = frame_rgb.shape
            bytes_per_line = channels * width
            
            # Create QImage
            q_image = QImage(
                frame_rgb.data,
                width,
                height,
                bytes_per_line,
                QImage.Format.Format_RGB888
            )
            
            # Convert to pixmap
            pixmap = QPixmap.fromImage(q_image)
            
            # Scale to fit widget while maintaining aspect ratio
            scaled_pixmap = pixmap.scaled(
                self.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            
            self._current_pixmap = scaled_pixmap
            self._display_label.setPixmap(scaled_pixmap)
            
        except Exception as e:
            import logging
            logging.getLogger(__name__).error(f"Error displaying frame: {e}")
    
    def clear_display(self):
        """Clear the video display"""
        self._display_label.clear()
        self._current_pixmap = None
    
    def resizeEvent(self, event):
        """Handle widget resize"""
        super().resizeEvent(event)
        # Resize display label to fill widget
        self._display_label.resize(self.size())
        
        # Rescale current pixmap if available
        if self._current_pixmap:
            scaled_pixmap = self._current_pixmap.scaled(
                self.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self._display_label.setPixmap(scaled_pixmap)
    
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


# Import cv2 at module level for frame conversion
import cv2
