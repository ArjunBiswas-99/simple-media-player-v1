"""
Enhanced theme system with modern aesthetics
Clean, professional design without UI bugs
"""

from enum import Enum


class Theme(Enum):
    """Theme options"""
    DARK = "dark"
    LIGHT = "light"


class EnhancedThemeManager:
    """Manages enhanced themes with modern aesthetics"""
    
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
                'bg_primary': '#1a1a2e',
                'bg_secondary': '#16213e',
                'text_primary': '#e0e0e0',
                'text_secondary': '#b8c1ec',
                'accent': '#667eea',
                'accent_end': '#764ba2',
                'accent_hover': '#7c94f5',
                'accent_hover_end': '#8b61b3',
                'time_color': '#00d4ff',
                'border_color': 'rgba(102, 126, 234, 0.3)',
            }
        else:
            return {
                'bg_primary': '#f5f7fa',
                'bg_secondary': '#ffffff',
                'text_primary': '#2c3e50',
                'text_secondary': '#6c757d',
                'accent': '#4A90E2',
                'accent_end': '#5BA3F5',
                'accent_hover': '#5BA3F5',
                'accent_hover_end': '#6CB4FF',
                'time_color': '#4A90E2',
                'border_color': 'rgba(52, 152, 219, 0.3)',
            }
    
    def get_full_stylesheet(self) -> str:
        """Get complete stylesheet for current theme"""
        colors = self.get_colors()
        
        if self._current_theme == Theme.DARK:
            control_bg = """
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 rgba(22, 33, 62, 0.95),
                            stop:1 rgba(26, 26, 46, 0.95));
            """
            main_bg = f"background-color: {colors['bg_primary']};"
        else:
            control_bg = """
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 rgba(255, 255, 255, 0.95),
                            stop:1 rgba(240, 244, 248, 0.95));
            """
            main_bg = f"""
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 {colors['bg_primary']},
                            stop:1 #e8ecf1);
            """
        
        return f"""
        QMainWindow {{
            {main_bg}
            color: {colors['text_primary']};
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'SF Pro Display', sans-serif;
        }}
        
        #controlPanel {{
            {control_bg}
            border-top: 2px solid {colors['border_color']};
        }}
        
        /* Regular Control Buttons */
        QPushButton#controlButton {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 {colors['accent']},
                        stop:1 {colors['accent_end']});
            color: white;
            border: none;
            border-radius: 12px;
            padding: 12px 20px;
            font-weight: 600;
            font-size: 14px;
            min-width: 100px;
        }}
        
        QPushButton#controlButton:hover {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 {colors['accent_hover']},
                        stop:1 {colors['accent_hover_end']});
            padding: 12px 22px;
        }}
        
        QPushButton#controlButton:pressed {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 {colors['accent']},
                        stop:1 {colors['accent_end']});
        }}
        
        /* Icon Buttons (Play/Pause/Stop) - Perfect Circles */
        QPushButton#iconButton {{
            background: rgba(102, 126, 234, 0.2);
            border: 2px solid rgba(102, 126, 234, 0.4);
            border-radius: 24px;
            min-width: 48px;
            max-width: 48px;
            min-height: 48px;
            max-height: 48px;
            color: white;
        }}
        
        QPushButton#iconButton:hover {{
            background: rgba(102, 126, 234, 0.4);
            border: 2px solid rgba(102, 126, 234, 0.6);
        }}
        
        QPushButton#iconButton:pressed {{
            background: rgba(102, 126, 234, 0.6);
        }}
        
        /* Theme Toggle Button */
        QPushButton#themeToggle {{
            background: rgba(0, 212, 255, 0.15);
            border: 2px solid rgba(0, 212, 255, 0.3);
            border-radius: 24px;
            min-width: 48px;
            max-width: 48px;
            min-height: 48px;
            max-height: 48px;
            font-size: 20px;
        }}
        
        QPushButton#themeToggle:hover {{
            background: rgba(0, 212, 255, 0.3);
            border: 2px solid rgba(0, 212, 255, 0.5);
        }}
        
        /* Time Labels */
        QLabel#timeLabel, QLabel#durationLabel {{
            color: {colors['time_color']};
            font-weight: 600;
            font-size: 14px;
            min-width: 60px;
        }}
        
        QLabel#volumeIcon, QLabel#speedLabel {{
            color: {colors['text_secondary']};
            font-weight: 500;
            font-size: 13px;
        }}
        
        QLabel#volumeLabel {{
            color: {colors['time_color']};
            font-weight: 600;
            font-size: 13px;
            min-width: 45px;
        }}
        
        /* Progress Slider */
        QSlider#progressSlider::groove:horizontal {{
            border: none;
            height: 6px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 3px;
        }}
        
        QSlider#progressSlider::sub-page:horizontal {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 {colors['accent']},
                        stop:1 {colors['accent_end']});
            border-radius: 3px;
        }}
        
        QSlider#progressSlider::handle:horizontal {{
            background: {colors['time_color']};
            border: 3px solid {colors['bg_primary']};
            width: 18px;
            margin: -7px 0;
            border-radius: 9px;
        }}
        
        QSlider#progressSlider::handle:horizontal:hover {{
            background: #33ddff;
            width: 20px;
            margin: -8px 0;
            border-radius: 10px;
        }}
        
        /* Volume Slider */
        QSlider#volumeSlider::groove:horizontal {{
            border: none;
            height: 4px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 2px;
        }}
        
        QSlider#volumeSlider::sub-page:horizontal {{
            background: {colors['time_color']};
            border-radius: 2px;
        }}
        
        QSlider#volumeSlider::handle:horizontal {{
            background: {colors['time_color']};
            border: 2px solid {colors['bg_primary']};
            width: 14px;
            margin: -6px 0;
            border-radius: 7px;
        }}
        
        QSlider#volumeSlider::handle:horizontal:hover {{
            background: #33ddff;
            width: 16px;
            border-radius: 8px;
        }}
        
        /* Menu Bar */
        QMenuBar {{
            background-color: {colors['bg_primary']};
            color: {colors['text_primary']};
            font-weight: 500;
            font-size: 13px;
            spacing: 8px;
            padding: 4px;
        }}
        
        QMenuBar::item {{
            padding: 6px 12px;
            border-radius: 6px;
        }}
        
        QMenuBar::item:selected {{
            background: rgba(102, 126, 234, 0.3);
            color: {colors['time_color']};
        }}
        
        QMenu {{
            background-color: {colors['bg_secondary']};
            color: {colors['text_primary']};
            border: 2px solid {colors['border_color']};
            border-radius: 8px;
            padding: 4px;
        }}
        
        QMenu::item {{
            padding: 8px 24px 8px 12px;
            border-radius: 4px;
        }}
        
        QMenu::item:selected {{
            background: rgba(102, 126, 234, 0.4);
            color: {colors['time_color']};
        }}
        """
    
    def get_stylesheet(self, component: str) -> str:
        """Get stylesheet for specific component"""
        colors = self.get_colors()
        
        if component == 'control_panel':
            if self._current_theme == Theme.DARK:
                return """
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 rgba(22, 33, 62, 0.95),
                            stop:1 rgba(26, 26, 46, 0.95));
                border-top: 2px solid rgba(102, 126, 234, 0.3);
                """
            else:
                return """
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 rgba(255, 255, 255, 0.95),
                            stop:1 rgba(240, 244, 248, 0.95));
                border-top: 2px solid rgba(52, 152, 219, 0.3);
                """
        
        return ""
