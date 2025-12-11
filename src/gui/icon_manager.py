"""
Icon Manager Module

Manages SVG icon loading and provides theme-aware icons for the application.
All icons use 'currentColor' which automatically adapts to the theme's text color.
"""

import logging
from pathlib import Path
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtCore import QSize, Qt

logger = logging.getLogger(__name__)


class IconManager:
    """
    Manages application icons with theme-aware coloring
    
    Handles loading SVG icons and providing them with appropriate colors
    based on the current theme. Uses 'currentColor' in SVG files to enable
    dynamic color changes.
    
    Attributes:
        icon_dir: Path to the icons directory
        _icon_cache: Cache of loaded icons to avoid redundant file operations
    """
    
    def __init__(self):
        """Initialize icon manager"""
        self.icon_dir = Path(__file__).parent / 'icons'
        self._icon_cache = {}
        
        # Verify icons directory exists
        if not self.icon_dir.exists():
            logger.error(f"Icons directory not found: {self.icon_dir}")
        else:
            logger.info(f"Icon manager initialized with directory: {self.icon_dir}")
    
    def get_icon(self, icon_name: str, color: str = "white", size: int = 40) -> QIcon:
        """
        Get a theme-aware icon
        
        Args:
            icon_name: Name of the icon file (without .svg extension)
            color: Color to render the icon (e.g., 'white', '#FFFFFF', '#E50914')
            size: Size of the icon in pixels
            
        Returns:
            QIcon: The loaded and colored icon
        """
        cache_key = f"{icon_name}_{color}_{size}"
        
        # Check cache first
        if cache_key in self._icon_cache:
            return self._icon_cache[cache_key]
        
        # Load SVG file
        svg_path = self.icon_dir / f"{icon_name}.svg"
        
        if not svg_path.exists():
            logger.warning(f"Icon file not found: {svg_path}")
            return QIcon()  # Return empty icon
        
        # Read SVG content
        with open(svg_path, 'r', encoding='utf-8') as f:
            svg_content = f.read()
        
        # Replace 'currentColor' with the specified color
        svg_content = svg_content.replace('currentColor', color)
        
        # Create renderer and render to pixmap
        renderer = QSvgRenderer(svg_content.encode('utf-8'))
        pixmap = QPixmap(QSize(size, size))
        pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        
        # Create icon and cache it
        icon = QIcon(pixmap)
        self._icon_cache[cache_key] = icon
        
        return icon
    
    def get_play_icon(self, color: str = "white", size: int = 40) -> QIcon:
        """Get play button icon"""
        return self.get_icon("play", color, size)
    
    def get_pause_icon(self, color: str = "white", size: int = 40) -> QIcon:
        """Get pause button icon"""
        return self.get_icon("pause", color, size)
    
    def get_stop_icon(self, color: str = "white", size: int = 40) -> QIcon:
        """Get stop button icon"""
        return self.get_icon("stop", color, size)
    
    def get_fullscreen_icon(self, color: str = "white", size: int = 40) -> QIcon:
        """Get fullscreen expand icon"""
        return self.get_icon("fullscreen", color, size)
    
    def get_exit_fullscreen_icon(self, color: str = "white", size: int = 40) -> QIcon:
        """Get fullscreen collapse icon"""
        return self.get_icon("exit_fullscreen", color, size)
    
    def get_forward_icon(self, color: str = "white", size: int = 40) -> QIcon:
        """Get forward/skip icon"""
        return self.get_icon("forward", color, size)
    
    def get_backward_icon(self, color: str = "white", size: int = 40) -> QIcon:
        """Get backward/rewind icon"""
        return self.get_icon("backward", color, size)
    
    def get_speed_icon(self, color: str = "white", size: int = 40) -> QIcon:
        """Get speed control icon"""
        return self.get_icon("speed", color, size)
    
    def get_theme_icon(self, is_dark_mode: bool, color: str = "white", size: int = 40) -> QIcon:
        """
        Get theme toggle icon based on current theme
        
        Args:
            is_dark_mode: True if currently in dark mode
            color: Icon color
            size: Icon size
            
        Returns:
            QIcon: Moon icon for dark mode, sun icon for light mode
        """
        icon_name = "theme_moon" if is_dark_mode else "theme_sun"
        return self.get_icon(icon_name, color, size)
    
    def clear_cache(self):
        """Clear the icon cache (useful when changing themes)"""
        self._icon_cache.clear()
        logger.info("Icon cache cleared")
    
    def get_themed_color(self, is_dark_mode: bool) -> str:
        """
        Get the appropriate icon color for the current theme
        
        Args:
            is_dark_mode: True if currently in dark mode
            
        Returns:
            str: Color hex code for icons
        """
        return "#FFFFFF" if is_dark_mode else "#141414"
