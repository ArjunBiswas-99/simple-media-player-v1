"""
Welcome screen widget displayed when no video is loaded
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class WelcomeScreen(QWidget):
    """Welcome screen with instructions when no video is loaded"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the welcome screen UI"""
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)
        
        # App icon/logo (using emoji)
        icon_label = QLabel("🎬")
        icon_font = QFont()
        icon_font.setPointSize(80)
        icon_label.setFont(icon_font)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon_label)
        
        # App title
        title_label = QLabel("Simple Media Player")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setObjectName("welcomeTitle")
        layout.addWidget(title_label)
        
        # Subtitle
        subtitle_label = QLabel("Ready to play your media")
        subtitle_font = QFont()
        subtitle_font.setPointSize(14)
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setObjectName("welcomeSubtitle")
        layout.addWidget(subtitle_label)
        
        layout.addSpacing(30)
        
        # Instructions
        instructions = [
            "📂 Drag & drop a video file here",
            "⌨️  Press Ctrl+O to open a file",
            "🎯 Or use File → Open File menu"
        ]
        
        for instruction in instructions:
            instr_label = QLabel(instruction)
            instr_font = QFont()
            instr_font.setPointSize(13)
            instr_label.setFont(instr_font)
            instr_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            instr_label.setObjectName("welcomeInstruction")
            layout.addWidget(instr_label)
        
        layout.addSpacing(30)
        
        # Supported formats
        formats_label = QLabel("Supports: MP4, MKV, AVI, MOV, WMV, and more")
        formats_font = QFont()
        formats_font.setPointSize(11)
        formats_label.setFont(formats_font)
        formats_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        formats_label.setObjectName("welcomeFormats")
        layout.addWidget(formats_label)
    
    def get_stylesheet(self, is_dark_theme: bool) -> str:
        """Get stylesheet for the welcome screen based on theme"""
        if is_dark_theme:
            return """
            QLabel#welcomeTitle {
                color: #FFFFFF;
            }
            QLabel#welcomeSubtitle {
                color: #B3B3B3;
            }
            QLabel#welcomeInstruction {
                color: #E0E0E0;
                padding: 5px;
            }
            QLabel#welcomeFormats {
                color: #888888;
            }
            """
        else:
            return """
            QLabel#welcomeTitle {
                color: #212529;
            }
            QLabel#welcomeSubtitle {
                color: #6C757D;
            }
            QLabel#welcomeInstruction {
                color: #495057;
                padding: 5px;
            }
            QLabel#welcomeFormats {
                color: #ADB5BD;
            }
            """
