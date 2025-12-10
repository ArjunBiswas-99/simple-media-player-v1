"""Video display widget for Simple Media Player."""

from typing import Optional
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPalette, QColor


class VideoWidget(QWidget):
    """
    Widget for displaying video content.
    
    This widget provides a window ID (WID) for MPV to render video into.
    """
    
    initialized = pyqtSignal(int)  # Emits the window ID when ready
    
    def __init__(self, parent: Optional[QWidget] = None):
        """Initialize the video widget."""
        super().__init__(parent)
        
        # Set black background
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(0, 0, 0))
        self.setAutoFillBackground(True)
        self.setPalette(palette)
        
        # Set size policy to expand
        from PyQt6.QtWidgets import QSizePolicy
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        
        # Minimum size for usability
        self.setMinimumSize(320, 240)
        
    def showEvent(self, event):
        """Handle widget show event."""
        super().showEvent(event)
        # Emit window ID once widget is shown
        if self.winId():
            self.initialized.emit(int(self.winId()))
