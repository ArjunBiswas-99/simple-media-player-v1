"""
Enhanced theme system with Netflix-style aesthetics
Includes glass morphism, smooth animations, and modern design
"""

from enum import Enum
from PyQt6.QtGui import QColor


class Theme(Enum):
    """Theme options"""
    DARK = "dark"
    LIGHT = "light"


class EnhancedThemeManager:
    """Manages enhanced themes with Netflix-style aesthetics"""
    
    def __init__(self):
        self._current_theme = Theme.DARK
    
    @property
    def current_theme(self) -> Theme:
        """Get current theme"""
        return self._current_theme
    
    def toggle_theme(self):
        """Toggle between dark and light themes"""
        self._current_theme = Theme.LIGHT if self._current_theme == Theme.DARK else Theme.DARK
    
    def get_colors(self) -> dict:
        """Get color palette for current theme"""
        if self._current_theme == Theme.DARK:
            return {
                'bg_primary': '#0F0F0F',      # Netflix dark
                'bg_secondary': '#181818',     # Slightly lighter
                'bg_glass': 'rgba(24, 24, 24, 0.85)',  # Glass effect
                'text_primary': '#FFFFFF',
                'text_secondary': '#B3B3B3',
                'accent': '#E50914',          # Netflix red
                'accent_hover': '#F40612',
                'control_bg': 'rgba(20, 20, 20, 0.95)',
                'slider_bg': 'rgba(255, 255, 255, 0.3)',
                'slider_active': '#FFFFFF',
                'button_hover': 'rgba(255, 255, 255, 0.1)',
            }
        else:
            return {
                'bg_primary': '#F8F9FA',
                'bg_secondary': '#FFFFFF',
                'bg_glass': 'rgba(255, 255, 255, 0.85)',
                'text_primary': '#212529',
                'text_secondary': '#6C757D',
                'accent': '#E50914',
                'accent_hover': '#F40612',
                'control_bg': 'rgba(255, 255, 255, 0.98)',
                'slider_bg': 'rgba(0, 0, 0, 0.15)',
                'slider_active': '#E50914',
                'button_hover': 'rgba(229, 9, 20, 0.08)',
            }
    
    def get_full_stylesheet(self) -> str:
        """Get complete stylesheet with Netflix-inspired design"""
        colors = self.get_colors()
        
        return f"""
        QMainWindow {{
            background-color: {colors['bg_primary']};
        }}
        
        /* Glass Morphism Control Panel */
        QWidget#controlPanel {{
            background-color: {colors['control_bg']};
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        }}
        
        /* Modern Buttons with Hover Effects */
        QPushButton {{
            background-color: transparent;
            color: {colors['text_primary']};
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
            font-size: 14px;
            font-weight: 500;
            outline: none;
        }}
        
        QPushButton:hover {{
            background-color: {colors['button_hover']};
        }}
        
        QPushButton:pressed {{
            background-color: {colors['button_hover']};
        }}
        
        QPushButton:focus {{
            outline: none;
            border: none;
        }}
        
        /* Icon Buttons (Play/Pause/Stop) */
        QPushButton#iconButton {{
            background-color: rgba(255, 255, 255, 0.1);
            color: {colors['text_primary']};
            border: 2px solid rgba(255, 255, 255, 0.2);
            border-radius: 22px;
            min-width: 44px;
            min-height: 44px;
            max-width: 44px;
            max-height: 44px;
            font-size: 20px;
            outline: none;
        }}
        
        QPushButton#iconButton:hover {{
            background-color: {colors['accent']};
            border-color: {colors['accent']};
            outline: none;
        }}
        
        QPushButton#iconButton:pressed {{
            background-color: {colors['accent_hover']};
            outline: none;
        }}
        
        QPushButton#iconButton:focus {{
            outline: none;
            border: 2px solid {colors['accent']};
        }}
        
        /* Theme Toggle Button */
        QPushButton#themeToggle {{
            background-color: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 20px;
            min-width: 40px;
            min-height: 40px;
            max-width: 40px;
            max-height: 40px;
            font-size: 18px;
        }}
        
        QPushButton#themeToggle:hover {{
            background-color: rgba(255, 255, 255, 0.2);
            border-color: {colors['accent']};
        }}
        
        /* Modern Progress Slider */
        QSlider#progressSlider {{
            height: 8px;
        }}
        
        QSlider#progressSlider::groove:horizontal {{
            background: {colors['slider_bg']};
            height: 4px;
            border-radius: 2px;
        }}
        
        QSlider#progressSlider::sub-page:horizontal {{
            background: {colors['accent']};
            height: 4px;
            border-radius: 2px;
        }}
        
        QSlider#progressSlider::handle:horizontal {{
            background: {colors['slider_active']};
            width: 14px;
            height: 14px;
            margin: -5px 0;
            border-radius: 7px;
            border: 2px solid {colors['bg_primary']};
        }}
        
        QSlider#progressSlider::handle:horizontal:hover {{
            background: {colors['accent']};
            width: 16px;
            height: 16px;
            margin: -6px 0;
            border-radius: 8px;
        }}
        
        /* Volume Slider */
        QSlider#volumeSlider {{
            height: 6px;
        }}
        
        QSlider#volumeSlider::groove:horizontal {{
            background: {colors['slider_bg']};
            height: 3px;
            border-radius: 1.5px;
        }}
        
        QSlider#volumeSlider::sub-page:horizontal {{
            background: {colors['slider_active']};
            height: 3px;
            border-radius: 1.5px;
        }}
        
        QSlider#volumeSlider::handle:horizontal {{
            background: {colors['slider_active']};
            width: 12px;
            height: 12px;
            margin: -5px 0;
            border-radius: 6px;
        }}
        
        QSlider#volumeSlider::handle:horizontal:hover {{
            background: {colors['accent']};
            width: 14px;
            height: 14px;
            margin: -6px 0;
            border-radius: 7px;
        }}
        
        /* Labels with Better Typography */
        QLabel {{
            color: {colors['text_primary']};
            font-size: 13px;
            font-weight: 400;
        }}
        
        QLabel#timeLabel, QLabel#durationLabel {{
            color: {colors['text_secondary']};
            font-size: 12px;
            font-weight: 500;
            min-width: 50px;
        }}
        
        QLabel#volumeLabel {{
            color: {colors['text_secondary']};
            font-size: 12px;
            font-weight: 500;
        }}
        
        QLabel#volumeIcon {{
            font-size: 18px;
        }}
        
        QLabel#speedLabel {{
            color: {colors['text_secondary']};
            font-size: 13px;
            font-weight: 500;
        }}
        
        /* Menu Bar */
        QMenuBar {{
            background-color: {colors['bg_secondary']};
            color: {colors['text_primary']};
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            padding: 4px;
        }}
        
        QMenuBar::item {{
            background-color: transparent;
            padding: 6px 12px;
            border-radius: 4px;
        }}
        
        QMenuBar::item:selected {{
            background-color: {colors['button_hover']};
        }}
        
        QMenu {{
            background-color: {colors['bg_secondary']};
            color: {colors['text_primary']};
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            padding: 8px 0;
        }}
        
        QMenu::item {{
            padding: 8px 24px;
        }}
        
        QMenu::item:selected {{
            background-color: {colors['button_hover']};
        }}
        
        /* Control Button Style */
        QPushButton#controlButton {{
            background-color: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 6px;
            padding: 8px 16px;
            font-size: 13px;
            font-weight: 500;
        }}
        
        QPushButton#controlButton:hover {{
            background-color: rgba(255, 255, 255, 0.15);
            border-color: {colors['accent']};
        }}
        """
    
    def get_stylesheet(self, component: str) -> str:
        """Get stylesheet for specific component"""
        colors = self.get_colors()
        
        if component == 'control_panel':
            return f"""
            background-color: {colors['control_bg']};
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            """
        
        return ""
