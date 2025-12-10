"""
PyMedia Player - Main entry point
A simple, lightweight media player built with Python, PyQt6, and MPV
"""

import sys
import logging
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

from gui.main_window import MainWindow


def setup_logging():
    """Configure logging for the application"""
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('pymedia_player.log', mode='w')
        ]
    )


def main():
    """Main application entry point"""
    # Set up logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("Starting PyMedia Player v1.0.0")
    
    # Enable high DPI support
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("PyMedia Player")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("PyMedia")
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Check for file argument
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        if Path(file_path).exists():
            logger.info(f"Opening file from command line: {file_path}")
            window._load_file(file_path)
    
    # Run application
    logger.info("Application started successfully")
    exit_code = app.exec()
    
    logger.info(f"Application exited with code {exit_code}")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
