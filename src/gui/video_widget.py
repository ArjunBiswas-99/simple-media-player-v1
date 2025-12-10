"""
Video display widget - renders video content
"""

from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor


class VideoWidget(QWidget):
    """Widget that displays video content via MPV"""
    
    def __init__(self, parent=None):
        """Initialize the video widget"""
        super().__init__(parent)
        
        # Set black background
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(0, 0, 0))
        self.setPalette(palette)
        
        # Accept drag and drop
        self.setAcceptDrops(True)
        
        # Set minimum size
        self.setMinimumSize(640, 480)
        
        # Store drop callback
        self._drop_callback = None
    
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
                # Get the first file path
                filepath = urls[0].toLocalFile()
                self._drop_callback(filepath)
            event.acceptProposedAction()
