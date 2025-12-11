"""
Visual feedback animations for user interactions
Provides non-intrusive visual cues for actions like play/pause, seek, and fullscreen
"""

import logging
from PyQt6.QtWidgets import QLabel, QGraphicsOpacityEffect
from PyQt6.QtCore import QTimer, QPropertyAnimation, QEasingCurve, Qt
from PyQt6.QtGui import QFont

logger = logging.getLogger(__name__)


class FeedbackAnimation:
    """
    Manages visual feedback animations for user actions
    
    Responsibilities:
    - Display temporary overlay icons for actions
    - Animate icon appearance and disappearance
    - Provide non-intrusive visual feedback
    """
    
    def __init__(self, parent_widget):
        """
        Initialize animation system
        
        Args:
            parent_widget: Widget to display animations on (typically video widget)
        """
        self.parent = parent_widget
        self._create_feedback_label()
        logger.debug("Animation system initialized")
    
    def _create_feedback_label(self):
        """Create the label widget for displaying feedback icons"""
        self.feedback_label = QLabel(self.parent)
        self.feedback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.feedback_label.setStyleSheet("""
            QLabel {
                background-color: rgba(0, 0, 0, 180);
                color: white;
                border-radius: 50px;
                font-size: 64px;
                padding: 30px;
            }
        """)
        self.feedback_label.hide()
        
        # Opacity effect for fade animations
        self.opacity_effect = QGraphicsOpacityEffect()
        self.feedback_label.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(1.0)
    
    def show_play_pause(self, is_playing: bool):
        """
        Show play or pause icon animation
        
        Args:
            is_playing: True if playing (show pause icon), False if paused (show play icon)
        """
        icon = "⏸" if is_playing else "▶"
        self._show_feedback(icon)
    
    def show_seek_forward(self):
        """Show seek forward animation"""
        self._show_feedback("⏩")
    
    def show_seek_backward(self):
        """Show seek backward animation"""
        self._show_feedback("⏪")
    
    def show_fullscreen(self, entering: bool):
        """
        Show fullscreen toggle animation
        
        Args:
            entering: True if entering fullscreen, False if exiting
        """
        icon = "⛶" if entering else "⧉"
        self._show_feedback(icon)
    
    def show_volume(self, volume: int):
        """
        Show volume change animation
        
        Args:
            volume: Current volume level (0-100)
        """
        if volume == 0:
            icon = "🔇"
        elif volume < 33:
            icon = "🔈"
        elif volume < 67:
            icon = "🔉"
        else:
            icon = "🔊"
        self._show_feedback(f"{icon}\n{volume}%", font_size=48)
    
    def show_speed(self, speed: float):
        """
        Show playback speed change animation
        
        Args:
            speed: Current playback speed (0.5, 1.0, 1.5, 2.0)
        """
        self._show_feedback(f"{speed}x", font_size=48)
    
    def _show_feedback(self, text: str, font_size: int = 64):
        """
        Display feedback animation with fade in/out effect
        
        Args:
            text: Text or icon to display
            font_size: Font size for the display
        """
        # Update label
        self.feedback_label.setText(text)
        self.feedback_label.setStyleSheet(f"""
            QLabel {{
                background-color: rgba(0, 0, 0, 180);
                color: white;
                border-radius: 50px;
                font-size: {font_size}px;
                padding: 30px;
            }}
        """)
        
        # Position at center of parent
        self.feedback_label.adjustSize()
        parent_rect = self.parent.rect()
        x = (parent_rect.width() - self.feedback_label.width()) // 2
        y = (parent_rect.height() - self.feedback_label.height()) // 2
        self.feedback_label.move(x, y)
        
        # Show with fade in
        self.feedback_label.show()
        self.feedback_label.raise_()
        
        # Fade in animation
        self.opacity_effect.setOpacity(0.0)
        fade_in = QPropertyAnimation(self.opacity_effect, b"opacity")
        fade_in.setDuration(150)
        fade_in.setStartValue(0.0)
        fade_in.setEndValue(1.0)
        fade_in.setEasingCurve(QEasingCurve.Type.OutCubic)
        fade_in.start()
        
        # Store animation reference to prevent garbage collection
        self._current_animation = fade_in
        
        # Auto-hide after delay with fade out
        QTimer.singleShot(800, self._fade_out_feedback)
    
    def _fade_out_feedback(self):
        """Fade out and hide the feedback label"""
        fade_out = QPropertyAnimation(self.opacity_effect, b"opacity")
        fade_out.setDuration(200)
        fade_out.setStartValue(1.0)
        fade_out.setEndValue(0.0)
        fade_out.setEasingCurve(QEasingCurve.Type.InCubic)
        fade_out.finished.connect(self.feedback_label.hide)
        fade_out.start()
        
        # Store animation reference
        self._current_animation = fade_out
