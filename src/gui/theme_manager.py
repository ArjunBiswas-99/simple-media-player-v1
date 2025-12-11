"""
Theme Manager Module

Manages application-wide theme configuration and styling with Netflix-inspired aesthetics.
Provides dark and light theme options with consistent color schemes across all UI components.

Design Principles:
    - Open/Closed Principle: Easy to extend with new themes without modifying existing code
    - Single Responsibility: Only handles theme-related styling and configuration
    - Interface Segregation: Provides specific methods for different styling needs
"""

from enum import Enum
from typing import Dict


class Theme(Enum):
    """Available themes"""
    DARK = "dark"
    LIGHT = "light"


class ThemeManager:
    """
    Manages application themes with Netflix-inspired styling
    
    Provides a centralized theme management system that can be easily extended
    with new themes. Follows Open/Closed Principle - open for extension (new themes),
    closed for modification (existing theme logic).
    
    Attributes:
        _current_theme: Currently active theme (Dark or Light)
        _theme_styles: Dictionary mapping themes to their style configurations
    """
    
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
        """
        Netflix-inspired dark theme configuration
        
        Colors:
            - Background: Pure black (#000000) - Netflix signature
            - Text: Pure white (#FFFFFF) for maximum contrast
            - Accent: Netflix red (#E50914) for interactive elements
            - Control Panel: Gradient overlay (transparent → 95% black)
            
        Returns:
            Dict[str, str]: Component name to stylesheet mapping
        """
        return {
            'main_window': """
                QMainWindow {
                    background-color: #000000;
                    color: #FFFFFF;
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Netflix Sans', 'Helvetica Neue', sans-serif;
                }
            """,
            'control_panel': """
                #controlPanel {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 rgba(0, 0, 0, 0.0),
                                stop:0.3 rgba(0, 0, 0, 0.3),
                                stop:1 rgba(0, 0, 0, 0.95));
                    border: none;
                }
            """,
            'button': """
                QPushButton#controlButton {
                    background: #E50914;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 10px 24px;
                    font-weight: 600;
                    font-size: 14px;
                    min-width: 100px;
                }
                QPushButton#controlButton:hover {
                    background: #F40612;
                }
                QPushButton#controlButton:pressed {
                    background: #B20710;
                }
                QPushButton#iconButton {
                    background: transparent;
                    border: none;
                    border-radius: 20px;
                    min-width: 40px;
                    max-width: 40px;
                    min-height: 40px;
                    max-height: 40px;
                    color: white;
                    font-size: 18px;
                }
                QPushButton#iconButton:hover {
                    background: rgba(255, 255, 255, 0.1);
                }
                QPushButton#iconButton:pressed {
                    background: rgba(255, 255, 255, 0.2);
                }
                QPushButton#themeToggle {
                    background: transparent;
                    border: 1px solid rgba(255, 255, 255, 0.3);
                    border-radius: 20px;
                    min-width: 40px;
                    max-width: 40px;
                    min-height: 40px;
                    max-height: 40px;
                    font-size: 16px;
                }
                QPushButton#themeToggle:hover {
                    background: rgba(255, 255, 255, 0.1);
                    border: 1px solid rgba(255, 255, 255, 0.5);
                }
            """,
            'label': """
                QLabel#timeLabel, QLabel#durationLabel {
                    color: #FFFFFF;
                    font-weight: 500;
                    font-size: 13px;
                    min-width: 60px;
                }
                QLabel#volumeIcon, QLabel#speedLabel {
                    color: #B3B3B3;
                    font-weight: 400;
                    font-size: 13px;
                }
                QLabel#volumeLabel {
                    color: #FFFFFF;
                    font-weight: 500;
                    font-size: 12px;
                    min-width: 40px;
                }
            """,
            'slider': """
                QSlider#progressSlider::groove:horizontal {
                    border: none;
                    height: 3px;
                    background: rgba(255, 255, 255, 0.3);
                    border-radius: 2px;
                }
                QSlider#progressSlider::sub-page:horizontal {
                    background: #E50914;
                    border-radius: 2px;
                }
                QSlider#progressSlider::handle:horizontal {
                    background: #E50914;
                    border: none;
                    width: 12px;
                    height: 12px;
                    margin: -5px 0;
                    border-radius: 6px;
                }
                QSlider#progressSlider::handle:horizontal:hover {
                    background: #F40612;
                    width: 14px;
                    height: 14px;
                    margin: -6px 0;
                    border-radius: 7px;
                }
                QSlider#volumeSlider::groove:horizontal {
                    border: none;
                    height: 3px;
                    background: rgba(255, 255, 255, 0.3);
                    border-radius: 2px;
                }
                QSlider#volumeSlider::sub-page:horizontal {
                    background: #FFFFFF;
                    border-radius: 2px;
                }
                QSlider#volumeSlider::handle:horizontal {
                    background: #FFFFFF;
                    border: none;
                    width: 12px;
                    height: 12px;
                    margin: -5px 0;
                    border-radius: 6px;
                }
                QSlider#volumeSlider::handle:horizontal:hover {
                    background: #FFFFFF;
                    width: 14px;
                    height: 14px;
                    margin: -6px 0;
                    border-radius: 7px;
                }
            """,
            'menubar': """
                QMenuBar {
                    background-color: #000000;
                    color: #FFFFFF;
                    font-weight: 500;
                    font-size: 13px;
                    spacing: 8px;
                    padding: 4px;
                }
                QMenuBar::item {
                    padding: 6px 12px;
                    border-radius: 4px;
                }
                QMenuBar::item:selected {
                    background: rgba(255, 255, 255, 0.1);
                }
                QMenu {
                    background-color: #141414;
                    color: #FFFFFF;
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    border-radius: 4px;
                    padding: 4px;
                }
                QMenu::item {
                    padding: 8px 24px 8px 12px;
                    border-radius: 2px;
                }
                QMenu::item:selected {
                    background: rgba(229, 9, 20, 0.8);
                }
            """
        }
    
    def _get_light_theme(self) -> Dict[str, str]:
        """
        Netflix-inspired light theme configuration
        
        Colors:
            - Background: Pure white (#FFFFFF)
            - Text: Dark gray (#141414) for readability
            - Accent: Netflix red (#E50914) consistent with dark theme
            - Control Panel: Gradient overlay (transparent → 98% white)
            
        Returns:
            Dict[str, str]: Component name to stylesheet mapping
        """
        return {
            'main_window': """
                QMainWindow {
                    background-color: #FFFFFF;
                    color: #141414;
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Netflix Sans', 'Helvetica Neue', sans-serif;
                }
            """,
            'control_panel': """
                #controlPanel {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                stop:0 rgba(255, 255, 255, 0.0),
                                stop:0.3 rgba(255, 255, 255, 0.5),
                                stop:1 rgba(255, 255, 255, 0.98));
                    border: none;
                }
            """,
            'button': """
                QPushButton#controlButton {
                    background: #E50914;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 10px 24px;
                    font-weight: 600;
                    font-size: 14px;
                    min-width: 100px;
                }
                QPushButton#controlButton:hover {
                    background: #F40612;
                }
                QPushButton#controlButton:pressed {
                    background: #B20710;
                }
                QPushButton#iconButton {
                    background: transparent;
                    border: none;
                    border-radius: 20px;
                    min-width: 40px;
                    max-width: 40px;
                    min-height: 40px;
                    max-height: 40px;
                    color: #141414;
                    font-size: 18px;
                }
                QPushButton#iconButton:hover {
                    background: rgba(0, 0, 0, 0.05);
                }
                QPushButton#iconButton:pressed {
                    background: rgba(0, 0, 0, 0.1);
                }
                QPushButton#themeToggle {
                    background: transparent;
                    border: 1px solid rgba(0, 0, 0, 0.3);
                    border-radius: 20px;
                    min-width: 40px;
                    max-width: 40px;
                    min-height: 40px;
                    max-height: 40px;
                    font-size: 16px;
                }
                QPushButton#themeToggle:hover {
                    background: rgba(0, 0, 0, 0.05);
                    border: 1px solid rgba(0, 0, 0, 0.5);
                }
            """,
            'label': """
                QLabel#timeLabel, QLabel#durationLabel {
                    color: #141414;
                    font-weight: 500;
                    font-size: 13px;
                    min-width: 60px;
                }
                QLabel#volumeIcon, QLabel#speedLabel {
                    color: #6C6C6C;
                    font-weight: 400;
                    font-size: 13px;
                }
                QLabel#volumeLabel {
                    color: #141414;
                    font-weight: 500;
                    font-size: 12px;
                    min-width: 40px;
                }
            """,
            'slider': """
                QSlider#progressSlider::groove:horizontal {
                    border: none;
                    height: 3px;
                    background: rgba(0, 0, 0, 0.2);
                    border-radius: 2px;
                }
                QSlider#progressSlider::sub-page:horizontal {
                    background: #E50914;
                    border-radius: 2px;
                }
                QSlider#progressSlider::handle:horizontal {
                    background: #E50914;
                    border: none;
                    width: 12px;
                    height: 12px;
                    margin: -5px 0;
                    border-radius: 6px;
                }
                QSlider#progressSlider::handle:horizontal:hover {
                    background: #F40612;
                    width: 14px;
                    height: 14px;
                    margin: -6px 0;
                    border-radius: 7px;
                }
                QSlider#volumeSlider::groove:horizontal {
                    border: none;
                    height: 3px;
                    background: rgba(0, 0, 0, 0.2);
                    border-radius: 2px;
                }
                QSlider#volumeSlider::sub-page:horizontal {
                    background: #141414;
                    border-radius: 2px;
                }
                QSlider#volumeSlider::handle:horizontal {
                    background: #141414;
                    border: none;
                    width: 12px;
                    height: 12px;
                    margin: -5px 0;
                    border-radius: 6px;
                }
                QSlider#volumeSlider::handle:horizontal:hover {
                    background: #141414;
                    width: 14px;
                    height: 14px;
                    margin: -6px 0;
                    border-radius: 7px;
                }
            """,
            'menubar': """
                QMenuBar {
                    background-color: #FFFFFF;
                    color: #141414;
                    font-weight: 500;
                    font-size: 13px;
                    spacing: 8px;
                    padding: 4px;
                }
                QMenuBar::item {
                    padding: 6px 12px;
                    border-radius: 4px;
                }
                QMenuBar::item:selected {
                    background: rgba(0, 0, 0, 0.05);
                }
                QMenu {
                    background-color: #F5F5F5;
                    color: #141414;
                    border: 1px solid rgba(0, 0, 0, 0.1);
                    border-radius: 4px;
                    padding: 4px;
                }
                QMenu::item {
                    padding: 8px 24px 8px 12px;
                    border-radius: 2px;
                }
                QMenu::item:selected {
                    background: rgba(229, 9, 20, 0.8);
                    color: white;
                }
            """
        }
    
    @property
    def current_theme(self) -> Theme:
        """
        Get the currently active theme
        
        Returns:
            Theme: Current theme (DARK or LIGHT)
        """
        return self._current_theme
    
    def toggle_theme(self) -> Theme:
        """
        Toggle between light and dark themes
        
        Returns:
            Theme: The newly activated theme
        """
        self._current_theme = (
            Theme.LIGHT if self._current_theme == Theme.DARK else Theme.DARK
        )
        return self._current_theme
    
    def set_theme(self, theme: Theme):
        """
        Set a specific theme
        
        Args:
            theme: The theme to activate (DARK or LIGHT)
        """
        self._current_theme = theme
    
    def get_stylesheet(self, component: str) -> str:
        """
        Get stylesheet for a specific UI component
        
        Args:
            component: Component identifier (e.g., 'control_panel', 'button')
            
        Returns:
            str: CSS stylesheet for the specified component
        """
        return self._theme_styles[self._current_theme].get(component, "")
    
    def get_full_stylesheet(self) -> str:
        """
        Get complete stylesheet for current theme
        
        Combines all component stylesheets into a single string for
        application-wide styling.
        
        Returns:
            str: Complete CSS stylesheet for all components
        """
        theme_config = self._theme_styles[self._current_theme]
        return "\n".join(theme_config.values())
