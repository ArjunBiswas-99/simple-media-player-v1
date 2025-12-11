"""
Theme manager for handling light and dark themes with modern design
"""

from enum import Enum
from typing import Dict


class Theme(Enum):
    """Available themes"""
    DARK = "dark"
    LIGHT = "light"


class ThemeManager:
    """Manages application themes with modern, beautiful styling"""
    
    def __init__(self):
        """Initialize theme manager with dark theme as default"""
        self._current_theme = Theme.DARK
        self._theme_styles = self._initialize_themes()
    
    def _initialize_themes(self) -> Dict[Theme, Dict[str, str]]:
        """Initialize theme configurations"""
        return {
            Theme.DARK: self._get_dark_theme(),
            Theme.LIGHT: self._get_light_theme()
        }
    
    def _get_dark_theme(self) -> Dict[str, str]:
        """Modern dark theme with gradient accent"""
        return {
            'main_window': """
                QMainWindow {
                    background-color: #1a1a2e;
                    color: #e0e0e0;
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'SF Pro Display', sans-serif;
                }
            """,
            'control_panel': """
                #controlPanel {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 rgba(22, 33, 62, 0.95),
                                stop:1 rgba(26, 26, 46, 0.95));
                    border-top: 2px solid rgba(102, 126, 234, 0.3);
                }
            """,
            'button': """
                QPushButton#controlButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop:0 #667eea,
                                stop:1 #764ba2);
                    color: white;
                    border: none;
                    border-radius: 12px;
                    padding: 12px 20px;
                    font-weight: 600;
                    font-size: 14px;
                    min-width: 100px;
                }
                QPushButton#controlButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop:0 #7c94f5,
                                stop:1 #8b61b3);
                    padding: 12px 22px;
                }
                QPushButton#controlButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop:0 #5568d3,
                                stop:1 #653a91);
                }
                QPushButton#iconButton {
                    background: rgba(102, 126, 234, 0.2);
                    border: 2px solid rgba(102, 126, 234, 0.4);
                    border-radius: 24px;
                    min-width: 48px;
                    max-width: 48px;
                    min-height: 48px;
                    max-height: 48px;
                    color: white;
                }
                QPushButton#iconButton:hover {
                    background: rgba(102, 126, 234, 0.4);
                    border: 2px solid rgba(102, 126, 234, 0.6);
                }
                QPushButton#iconButton:pressed {
                    background: rgba(102, 126, 234, 0.6);
                }
                QPushButton#iconButton::icon {
                    color: white;
                }
                QPushButton#themeToggle {
                    background: rgba(0, 212, 255, 0.15);
                    border: 2px solid rgba(0, 212, 255, 0.3);
                    border-radius: 24px;
                    min-width: 48px;
                    max-width: 48px;
                    min-height: 48px;
                    max-height: 48px;
                    font-size: 20px;
                }
                QPushButton#themeToggle:hover {
                    background: rgba(0, 212, 255, 0.3);
                    border: 2px solid rgba(0, 212, 255, 0.5);
                }
            """,
            'label': """
                QLabel#timeLabel, QLabel#durationLabel {
                    color: #00d4ff;
                    font-weight: 600;
                    font-size: 14px;
                    min-width: 60px;
                }
                QLabel#volumeIcon, QLabel#speedLabel {
                    color: #b8c1ec;
                    font-weight: 500;
                    font-size: 13px;
                }
                QLabel#volumeLabel {
                    color: #00d4ff;
                    font-weight: 600;
                    font-size: 13px;
                    min-width: 45px;
                }
            """,
            'slider': """
                QSlider#progressSlider::groove:horizontal {
                    border: none;
                    height: 6px;
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 3px;
                }
                QSlider#progressSlider::sub-page:horizontal {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop:0 #667eea,
                                stop:1 #764ba2);
                    border-radius: 3px;
                }
                QSlider#progressSlider::handle:horizontal {
                    background: #00d4ff;
                    border: 3px solid #1a1a2e;
                    width: 18px;
                    margin: -7px 0;
                    border-radius: 9px;
                }
                QSlider#progressSlider::handle:horizontal:hover {
                    background: #33ddff;
                    width: 20px;
                    margin: -8px 0;
                    border-radius: 10px;
                }
                QSlider#volumeSlider::groove:horizontal {
                    border: none;
                    height: 4px;
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 2px;
                }
                QSlider#volumeSlider::sub-page:horizontal {
                    background: #00d4ff;
                    border-radius: 2px;
                }
                QSlider#volumeSlider::handle:horizontal {
                    background: #00d4ff;
                    border: 2px solid #1a1a2e;
                    width: 14px;
                    margin: -6px 0;
                    border-radius: 7px;
                }
                QSlider#volumeSlider::handle:horizontal:hover {
                    background: #33ddff;
                    width: 16px;
                    border-radius: 8px;
                }
            """,
            'menubar': """
                QMenuBar {
                    background-color: #1a1a2e;
                    color: #e0e0e0;
                    font-weight: 500;
                    font-size: 13px;
                    spacing: 8px;
                    padding: 4px;
                }
                QMenuBar::item {
                    padding: 6px 12px;
                    border-radius: 6px;
                }
                QMenuBar::item:selected {
                    background: rgba(102, 126, 234, 0.3);
                    color: #00d4ff;
                }
                QMenu {
                    background-color: #16213e;
                    color: #e0e0e0;
                    border: 2px solid rgba(102, 126, 234, 0.3);
                    border-radius: 8px;
                    padding: 4px;
                }
                QMenu::item {
                    padding: 8px 24px 8px 12px;
                    border-radius: 4px;
                }
                QMenu::item:selected {
                    background: rgba(102, 126, 234, 0.4);
                    color: #00d4ff;
                }
            """
        }
    
    def _get_light_theme(self) -> Dict[str, str]:
        """Modern light theme with vibrant accent"""
        return {
            'main_window': """
                QMainWindow {
                    background-color: #ffffff;
                    color: #2c3e50;
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'SF Pro Display', sans-serif;
                }
            """,
            'control_panel': """
                #controlPanel {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 rgba(248, 249, 250, 0.98),
                                stop:1 rgba(233, 236, 239, 0.98));
                    border-top: 2px solid rgba(74, 144, 226, 0.2);
                }
            """,
            'button': """
                QPushButton#controlButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop:0 #4A90E2,
                                stop:1 #5BA3F5);
                    color: white;
                    border: none;
                    border-radius: 12px;
                    padding: 12px 20px;
                    font-weight: 600;
                    font-size: 14px;
                    min-width: 100px;
                }
                QPushButton#controlButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop:0 #5BA3F5,
                                stop:1 #6CB4FF);
                    padding: 12px 22px;
                }
                QPushButton#controlButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop:0 #3A7DC2,
                                stop:1 #4B8ED5);
                }
                QPushButton#iconButton {
                    background: rgba(74, 144, 226, 0.1);
                    border: 2px solid rgba(74, 144, 226, 0.3);
                    border-radius: 24px;
                    min-width: 48px;
                    max-width: 48px;
                    min-height: 48px;
                    max-height: 48px;
                    color: #2c3e50;
                }
                QPushButton#iconButton:hover {
                    background: rgba(74, 144, 226, 0.2);
                    border: 2px solid rgba(74, 144, 226, 0.5);
                }
                QPushButton#iconButton:pressed {
                    background: rgba(74, 144, 226, 0.3);
                }
                QPushButton#themeToggle {
                    background: rgba(255, 107, 107, 0.1);
                    border: 2px solid rgba(255, 107, 107, 0.3);
                    border-radius: 24px;
                    min-width: 48px;
                    max-width: 48px;
                    min-height: 48px;
                    max-height: 48px;
                    font-size: 20px;
                }
                QPushButton#themeToggle:hover {
                    background: rgba(255, 107, 107, 0.2);
                    border: 2px solid rgba(255, 107, 107, 0.5);
                }
            """,
            'label': """
                QLabel#timeLabel, QLabel#durationLabel {
                    color: #4A90E2;
                    font-weight: 600;
                    font-size: 14px;
                    min-width: 60px;
                }
                QLabel#volumeIcon, QLabel#speedLabel {
                    color: #6c757d;
                    font-weight: 500;
                    font-size: 13px;
                }
                QLabel#volumeLabel {
                    color: #4A90E2;
                    font-weight: 600;
                    font-size: 13px;
                    min-width: 45px;
                }
            """,
            'slider': """
                QSlider#progressSlider::groove:horizontal {
                    border: none;
                    height: 6px;
                    background: rgba(0, 0, 0, 0.1);
                    border-radius: 3px;
                }
                QSlider#progressSlider::sub-page:horizontal {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop:0 #4A90E2,
                                stop:1 #5BA3F5);
                    border-radius: 3px;
                }
                QSlider#progressSlider::handle:horizontal {
                    background: #FF6B6B;
                    border: 3px solid white;
                    width: 18px;
                    margin: -7px 0;
                    border-radius: 9px;
                }
                QSlider#progressSlider::handle:horizontal:hover {
                    background: #ff8585;
                    width: 20px;
                    margin: -8px 0;
                    border-radius: 10px;
                }
                QSlider#volumeSlider::groove:horizontal {
                    border: none;
                    height: 4px;
                    background: rgba(0, 0, 0, 0.1);
                    border-radius: 2px;
                }
                QSlider#volumeSlider::sub-page:horizontal {
                    background: #4A90E2;
                    border-radius: 2px;
                }
                QSlider#volumeSlider::handle:horizontal {
                    background: #4A90E2;
                    border: 2px solid white;
                    width: 14px;
                    margin: -6px 0;
                    border-radius: 7px;
                }
                QSlider#volumeSlider::handle:horizontal:hover {
                    background: #5BA3F5;
                    width: 16px;
                    border-radius: 8px;
                }
            """,
            'menubar': """
                QMenuBar {
                    background-color: #ffffff;
                    color: #2c3e50;
                    font-weight: 500;
                    font-size: 13px;
                    spacing: 8px;
                    padding: 4px;
                }
                QMenuBar::item {
                    padding: 6px 12px;
                    border-radius: 6px;
                }
                QMenuBar::item:selected {
                    background: rgba(74, 144, 226, 0.15);
                    color: #4A90E2;
                }
                QMenu {
                    background-color: white;
                    color: #2c3e50;
                    border: 2px solid rgba(74, 144, 226, 0.2);
                    border-radius: 8px;
                    padding: 4px;
                }
                QMenu::item {
                    padding: 8px 24px 8px 12px;
                    border-radius: 4px;
                }
                QMenu::item:selected {
                    background: rgba(74, 144, 226, 0.15);
                    color: #4A90E2;
                }
            """
        }
    
    @property
    def current_theme(self) -> Theme:
        """Get current theme"""
        return self._current_theme
    
    def toggle_theme(self) -> Theme:
        """Toggle between light and dark themes"""
        self._current_theme = (
            Theme.LIGHT if self._current_theme == Theme.DARK else Theme.DARK
        )
        return self._current_theme
    
    def set_theme(self, theme: Theme):
        """Set specific theme"""
        self._current_theme = theme
    
    def get_stylesheet(self, component: str) -> str:
        """Get stylesheet for specific component"""
        return self._theme_styles[self._current_theme].get(component, "")
    
    def get_full_stylesheet(self) -> str:
        """Get complete stylesheet for current theme"""
        theme_config = self._theme_styles[self._current_theme]
        return "\n".join(theme_config.values())
