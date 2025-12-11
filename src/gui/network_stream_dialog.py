"""
Network Stream Dialog Module

Provides a user interface for entering and validating streaming video URLs
from platforms like YouTube, Dailymotion, Vimeo, and others.
"""

import logging
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from ..core.network_stream_handler import NetworkStreamHandler, StreamPlatform

logger = logging.getLogger(__name__)


class NetworkStreamDialog(QDialog):
    """
    Dialog for entering and validating streaming video URLs
    
    Provides real-time URL validation with visual feedback and supports
    multiple streaming platforms including YouTube, Dailymotion, Vimeo, etc.
    """
    
    # Signal emitted when user confirms a valid URL
    url_accepted = pyqtSignal(str)
    
    def __init__(self, parent=None):
        """Initialize the network stream dialog"""
        super().__init__(parent)
        
        self.stream_handler = NetworkStreamHandler()
        self._current_platform = StreamPlatform.UNKNOWN
        
        self._setup_ui()
        self._apply_styling()
        
        logger.debug("Network stream dialog initialized")
    
    def _setup_ui(self):
        """Setup the user interface"""
        self.setWindowTitle("Open Network Stream")
        self.setModal(True)
        self.setMinimumWidth(500)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title_label = QLabel("Open Network Stream")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        # Description
        desc_label = QLabel("Enter video URL:")
        layout.addWidget(desc_label)
        
        # URL input with validation indicator
        url_layout = QHBoxLayout()
        url_layout.setSpacing(8)
        
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://youtube.com/watch?v=...")
        self.url_input.textChanged.connect(self._on_url_changed)
        self.url_input.returnPressed.connect(self._on_open_clicked)
        url_layout.addWidget(self.url_input, stretch=1)
        
        # Validation indicator
        self.validation_label = QLabel("")
        self.validation_label.setFixedWidth(80)
        self.validation_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        url_layout.addWidget(self.validation_label)
        
        layout.addLayout(url_layout)
        
        # Supported platforms info
        platforms_label = QLabel(
            "<b>Supported platforms:</b><br>"
            "• YouTube • Dailymotion • Vimeo<br>"
            "• Twitch • Direct video links<br>"
            "• And 1000+ more sites"
        )
        platforms_label.setWordWrap(True)
        platforms_label.setStyleSheet("color: #666; font-size: 11px; padding: 10px 0;")
        layout.addWidget(platforms_label)
        
        # Example URLs (collapsed by default)
        examples_label = QLabel(
            "<small><b>Example URLs:</b><br>"
            "• youtube.com/watch?v=...<br>"
            "• youtu.be/...<br>"
            "• dailymotion.com/video/...<br>"
            "• vimeo.com/...</small>"
        )
        examples_label.setWordWrap(True)
        examples_label.setStyleSheet("color: #888; font-size: 10px;")
        layout.addWidget(examples_label)
        
        layout.addStretch()
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setFixedWidth(100)
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)
        
        self.open_button = QPushButton("Open")
        self.open_button.setFixedWidth(100)
        self.open_button.clicked.connect(self._on_open_clicked)
        self.open_button.setEnabled(False)  # Disabled until valid URL entered
        self.open_button.setDefault(True)
        button_layout.addWidget(self.open_button)
        
        layout.addLayout(button_layout)
        
        # Set focus to URL input
        self.url_input.setFocus()
    
    def _apply_styling(self):
        """Apply Netflix-style theming"""
        self.setStyleSheet("""
            QDialog {
                background-color: #141414;
                color: white;
            }
            QLabel {
                color: white;
            }
            QLineEdit {
                background-color: #333;
                border: 2px solid #555;
                border-radius: 4px;
                padding: 8px;
                color: white;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 2px solid #E50914;
            }
            QPushButton {
                background-color: #E50914;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px 20px;
                font-weight: 600;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #F40612;
            }
            QPushButton:pressed {
                background-color: #B20710;
            }
            QPushButton:disabled {
                background-color: #555;
                color: #999;
            }
            QPushButton#cancelButton {
                background-color: #333;
                color: white;
            }
            QPushButton#cancelButton:hover {
                background-color: #444;
            }
        """)
        
        self.cancel_button.setObjectName("cancelButton")
    
    def _on_url_changed(self, text: str):
        """
        Handle URL input changes with real-time validation
        
        Args:
            text: Current URL text
        """
        if not text.strip():
            # Empty input
            self.validation_label.setText("")
            self.open_button.setEnabled(False)
            self._current_platform = StreamPlatform.UNKNOWN
            return
        
        # Validate URL
        is_valid, platform = self.stream_handler.validate_url(text)
        
        self._current_platform = platform
        
        if is_valid:
            # Valid URL
            platform_name = self.stream_handler.get_platform_name(platform)
            
            if platform == StreamPlatform.UNKNOWN:
                self.validation_label.setText("✓ Valid")
                self.validation_label.setStyleSheet("color: #4CAF50; font-weight: 600;")
            else:
                self.validation_label.setText(f"✓ {platform_name}")
                self.validation_label.setStyleSheet("color: #4CAF50; font-weight: 600;")
            
            self.open_button.setEnabled(True)
        else:
            # Invalid URL
            self.validation_label.setText("✗ Invalid")
            self.validation_label.setStyleSheet("color: #f44336; font-weight: 600;")
            self.open_button.setEnabled(False)
    
    def _on_open_clicked(self):
        """Handle Open button click"""
        url = self.url_input.text().strip()
        
        if not url:
            return
        
        # Final validation
        is_valid, platform = self.stream_handler.validate_url(url)
        
        if not is_valid:
            QMessageBox.warning(
                self,
                "Invalid URL",
                "Please enter a valid video URL.\n\n"
                "Supported platforms include YouTube, Dailymotion, "
                "Vimeo, Twitch, and many others."
            )
            return
        
        # Check if yt-dlp is available
        if not self.stream_handler.is_ytdlp_available():
            QMessageBox.critical(
                self,
                "Missing Dependency",
                "yt-dlp is not installed.\n\n"
                "Please install it with:\n"
                "pip install yt-dlp\n\n"
                "Then restart the application."
            )
            return
        
        # Emit signal and close dialog
        logger.info(f"User accepted URL: {url} ({platform.value})")
        self.url_accepted.emit(url)
        self.accept()
    
    def get_url(self) -> str:
        """
        Get the entered URL
        
        Returns:
            The URL entered by the user
        """
        return self.url_input.text().strip()
    
    def set_url(self, url: str):
        """
        Set the URL in the input field
        
        Args:
            url: URL to set
        """
        self.url_input.setText(url)
