"""
Buffering Widget Module

Provides a Netflix-style loading indicator for stream extraction and video buffering.
Displays an animated spinner with status messages and progress percentage.
"""

import logging
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QPainter, QPen, QColor

logger = logging.getLogger(__name__)


class BufferingWidget(QWidget):
    """
    Netflix-style buffering indicator overlay
    
    Displays an animated rotating spinner with status text and optional
    progress percentage. Auto-positions itself centered on the parent widget.
    """
    
    def __init__(self, parent=None):
        """Initialize the buffering widget"""
        super().__init__(parent)
        
        self._rotation_angle = 0
        self._status_text = "Loading..."
        self._progress = -1  # -1 means no progress (indeterminate)
        
        self._setup_ui()
        self._setup_animation()
        
        # Initially hidden
        self.hide()
    
    def _setup_ui(self):
        """Setup the user interface"""
        # Make widget semi-transparent overlay
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        
        # Create layout
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Status label
        self.status_label = QLabel(self._status_text)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 16px;
                font-weight: 500;
                background: transparent;
                padding: 10px;
            }
        """)
        layout.addWidget(self.status_label)
        
        # Progress label (hidden by default)
        self.progress_label = QLabel("")
        self.progress_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.8);
                font-size: 14px;
                background: transparent;
                padding: 5px;
            }
        """)
        self.progress_label.hide()
        layout.addWidget(self.progress_label)
        
        # Set minimum size
        self.setMinimumSize(200, 200)
    
    def _setup_animation(self):
        """Setup rotation animation timer"""
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self._rotate_spinner)
        self.animation_timer.setInterval(50)  # 20 FPS
    
    def _rotate_spinner(self):
        """Rotate the spinner animation"""
        self._rotation_angle = (self._rotation_angle + 10) % 360
        self.update()  # Trigger repaint
    
    def paintEvent(self, event):
        """Draw the spinning loading indicator"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw semi-transparent background
        painter.fillRect(self.rect(), QColor(0, 0, 0, 150))
        
        # Draw spinner in center
        center_x = self.width() // 2
        center_y = self.height() // 2 - 40  # Offset up for text
        
        # Spinner properties
        radius = 30
        pen_width = 4
        
        # Draw spinner arc (Netflix red)
        pen = QPen(QColor(229, 9, 20))  # Netflix red
        pen.setWidth(pen_width)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        
        # Save painter state
        painter.save()
        
        # Move to center and rotate
        painter.translate(center_x, center_y)
        painter.rotate(self._rotation_angle)
        
        # Draw arc (270 degrees)
        painter.drawArc(-radius, -radius, radius * 2, radius * 2, 0, 270 * 16)
        
        # Restore painter state
        painter.restore()
    
    def show_loading(self, message: str = "Loading..."):
        """
        Show buffering widget with loading message
        
        Args:
            message: Status message to display
        """
        self._status_text = message
        self._progress = -1
        self.status_label.setText(self._status_text)
        self.progress_label.hide()
        
        # Position in center of parent
        if self.parent():
            parent_rect = self.parent().rect()
            self.setGeometry(parent_rect)
        
        self.show()
        self.raise_()  # Bring to front
        self.animation_timer.start()
        
        logger.debug(f"Buffering widget shown: {message}")
    
    def update_progress(self, progress: int, message: str = None):
        """
        Update buffering progress
        
        Args:
            progress: Progress percentage (0-100), or -1 for indeterminate
            message: Optional status message update
        """
        self._progress = progress
        
        if message:
            self._status_text = message
            self.status_label.setText(self._status_text)
        
        if progress >= 0:
            self.progress_label.setText(f"{progress}%")
            self.progress_label.show()
        else:
            self.progress_label.hide()
        
        self.update()  # Trigger repaint
    
    def hide_loading(self):
        """Hide buffering widget"""
        self.animation_timer.stop()
        self.hide()
        logger.debug("Buffering widget hidden")
    
    def set_status(self, message: str):
        """
        Update status message
        
        Args:
            message: New status message
        """
        self._status_text = message
        self.status_label.setText(self._status_text)
