"""
Simple Media Player - Main Entry Point
Version: 0.1.0-alpha

This is the MVP with basic playback functionality.
See MVP-STATUS.md for what's included and what's coming next.
"""

import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent))

from gui.main_window import MainWindow
from config.version import VERSION


def main() -> int:
    """Main entry point for Simple Media Player."""
    # Enable high DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("Simple Media Player")
    app.setApplicationVersion(VERSION)
    app.setOrganizationName("Simple Media Player")
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Start event loop
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
