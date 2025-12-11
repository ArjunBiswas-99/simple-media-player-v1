"""
Visual feedback animations for user interactions
YouTube-style overlay animations for play, pause, seek, etc.
"""

import logging
from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import QTimer, QPropertyAnimation, QEasingCurve, Qt, QRect
from PyQt6.QtGui import QFont

logger = logging.getLogger(__name__)


class FeedbackAnimation:
    """
    YouTube-style visual feedback animations
    Shows large temporary icons for user actions like play, pause, seek, etc.
    """
    
    def __init__(self, parent_widget):
        """
        Initialize animation system
        
        Args:
            parent_widget: Widget to display animations on (video widget)
        """
        self.parent = parent_widget
        self._create_feedback_label()
        logger.info("YouTube-style animation system initialized")
    
    def _create_feedback_label(self):
        """Create the overlay label for feedback icons"""
        self.feedback_label = QLabel("", self.parent)
        self.feedback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Style like YouTube overlays
        self.feedback_label.setStyleSheet("""
            QLabel {
                background-color: rgba(0, 0, 0, 160);
                color: white;
                border-radius: 40px;
                font-size: 72px;
                font-weight: bold;
                padding: 40px;
            }
        """)
        
        # Start hidden
        self.feedback_label.hide()
        self.feedback_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        
        logger.debug("Feedback label created")
    
    def show_play_pause(self, is_playing: bool):
        """Show play ▶ or pause ⏸ icon"""
        icon = "⏸" if is_playing else "▶"
        logger.info(f"Showing {'pause' if is_playing else 'play'} animation")
        self._show_feedback(icon, 72)
    
    def show_seek_forward(self):
        """Show seek forward ⏩ icon"""
        logger.info("Showing seek forward animation")
        self._show_feedback("⏩", 72)
    
    def show_seek_backward(self):
        """Show seek backward ⏪ icon"""
        logger.info("Showing seek backward animation")
        self._show_feedback("⏪", 72)
    
    def show_volume(self, volume: int):
        """Show volume icon with percentage"""
        if volume == 0:
            icon = "🔇"
        elif volume < 33:
            icon = "🔈"
        elif volume < 67:
            icon = "🔉"
        else:
            icon = "🔊"
        logger.info(f"Showing volume animation: {volume}%")
        self._show_feedback(f"{icon}\n{volume}%", 56)
    
    def show_speed(self, speed: float):
        """Show playback speed"""
        logger.info(f"Showing speed animation: {speed}x")
        self._show_feedback(f"{speed}x", 56)
    
    def _show_feedback(self, text: str, font_size: int):
        """
        Display feedback animation - YouTube style
        
        Args:
            text: Icon or text to display
            font_size: Font size in pixels
        """
        try:
            logger.info(f"Displaying animation: '{text}' (size: {font_size})")
            
            # Update text and style
            self.feedback_label.setText(text)
            self.feedback_label.setStyleSheet(f"""
                QLabel {{
                    background-color: rgba(0, 0, 0, 160);
                    color: white;
                    border-radius: 40px;
                    font-size: {font_size}px;
                    font-weight: bold;
                    padding: 40px;
                }}
            """)
            
            # Calculate size and position at center
            self.feedback_label.adjustSize()
            parent_rect = self.parent.rect()
            label_width = self.feedback_label.width()
            label_height = self.feedback_label.height()
            
            x = (parent_rect.width() - label_width) // 2
            y = (parent_rect.height() - label_height) // 2
            
            self.feedback_label.setGeometry(x, y, label_width, label_height)
            
            # Show and bring to front
            self.feedback_label.show()
            self.feedback_label.raise_()
            
            logger.info(f"Animation positioned at ({x}, {y}) size ({label_width}x{label_height})")
            logger.info(f"Parent size: {parent_rect.width()}x{parent_rect.height()}")
            logger.info(f"Label visible: {self.feedback_label.isVisible()}")
            
            # Auto-hide after 800ms
            QTimer.singleShot(800, self.feedback_label.hide)
            
        except Exception as e:
            logger.error(f"Error showing animation: {e}", exc_info=True)
