"""
Theme manager for handling light and dark themes
"""

from enum import Enum
from typing import Dict


class Theme(Enum):
    """Available themes"""
    DARK = "dark"
    LIGHT = "light"


class ThemeManager:
    """Manages application themes and provides theme-specific styles"""
    
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
        """Get dark theme configuration"""
        return {
            'main_window': """
                QMainWindow {
                    background-color: #1e1e1e;
                }
            """,
            'control_panel': "background-color: #2b2b2b;",
            'button': """
                QPushButton {
                    background-color: #0d7377;
                    color: white;
                    border: 2px solid #14FFEC;
                    border-radius: 5px;
                    padding: 8px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #14FFEC;
                    color: #0d7377;
                    border: 2px solid #0d7377;
                }
                QPushButton:pressed {
                    background-color: #0a5f62;
                }
            """,
            'label': "color: #14FFEC; font-weight: bold;",
            'slider': """
                QSlider::groove:horizontal {
                    border: 1px solid #555;
                    height: 10px;
                    background: #3c3c3c;
                    border-radius: 5px;
                }
                QSlider::handle:horizontal {
                    background: #14FFEC;
                    border: 2px solid #0d7377;
                    width: 18px;
                    margin: -5px 0;
                    border-radius: 9px;
                }
                QSlider::handle:horizontal:hover {
                    background: #42A5F5;
                    border: 2px solid #14FFEC;
                }
            """,
            'menubar': """
                QMenuBar {
                    background-color: #2b2b2b;
                    color: #14FFEC;
                    font-weight: bold;
                }
                QMenuBar::item:selected {
                    background-color: #0d7377;
                }
                QMenu {
                    background-color: #2b2b2b;
                    color: #14FFEC;
                    border: 2px solid #0d7377;
                }
                QMenu::item:selected {
                    background-color: #0d7377;
                }
            """
        }
    
    def _get_light_theme(self) -> Dict[str, str]:
        """Get light theme configuration"""
        return {
            'main_window': """
                QMainWindow {
                    background-color: #f5f5f5;
                }
            """,
            'control_panel': "background-color: #e0e0e0;",
            'button': """
                QPushButton {
                    background-color: #2196F3;
                    color: white;
                    border: 2px solid #1976D2;
                    border-radius: 5px;
                    padding: 8px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #1976D2;
                    border: 2px solid #0D47A1;
                }
                QPushButton:pressed {
                    background-color: #0D47A1;
                }
            """,
            'label': "color: #1976D2; font-weight: bold;",
            'slider': """
                QSlider::groove:horizontal {
                    border: 1px solid #bbb;
                    height: 10px;
                    background: #d0d0d0;
                    border-radius: 5px;
                }
                QSlider::handle:horizontal {
                    background: #2196F3;
                    border: 2px solid #1976D2;
                    width: 18px;
                    margin: -5px 0;
                    border-radius: 9px;
                }
                QSlider::handle:horizontal:hover {
                    background: #42A5F5;
                    border: 2px solid #2196F3;
                }
            """,
            'menubar': """
                QMenuBar {
                    background-color: #e0e0e0;
                    color: #1976D2;
                    font-weight: bold;
                }
                QMenuBar::item:selected {
                    background-color: #2196F3;
                    color: white;
                }
                QMenu {
                    background-color: #f5f5f5;
                    color: #333;
                    border: 2px solid #2196F3;
                }
                QMenu::item:selected {
                    background-color: #2196F3;
                    color: white;
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
