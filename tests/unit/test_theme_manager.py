"""
Unit tests for ThemeManager
"""

import pytest
from src.gui.theme_manager import ThemeManager, Theme


@pytest.mark.unit
class TestThemeManager:
    """Test suite for ThemeManager class"""
    
    def test_initialization(self, theme_manager):
        """Test ThemeManager initializes with dark theme"""
        assert theme_manager.current_theme == Theme.DARK
        assert isinstance(theme_manager, ThemeManager)
    
    def test_toggle_theme_dark_to_light(self, theme_manager):
        """Test toggling from dark to light theme"""
        assert theme_manager.current_theme == Theme.DARK
        
        theme_manager.toggle_theme()
        
        assert theme_manager.current_theme == Theme.LIGHT
    
    def test_toggle_theme_light_to_dark(self, theme_manager):
        """Test toggling from light to dark theme"""
        theme_manager.current_theme = Theme.LIGHT
        
        theme_manager.toggle_theme()
        
        assert theme_manager.current_theme == Theme.DARK
    
    def test_toggle_theme_multiple_times(self, theme_manager):
        """Test toggling theme multiple times"""
        initial_theme = theme_manager.current_theme
        
        theme_manager.toggle_theme()
        theme_manager.toggle_theme()
        
        assert theme_manager.current_theme == initial_theme
    
    def test_get_full_stylesheet_returns_string(self, theme_manager):
        """Test get_full_stylesheet returns a non-empty string"""
        stylesheet = theme_manager.get_full_stylesheet()
        
        assert isinstance(stylesheet, str)
        assert len(stylesheet) > 0
    
    def test_get_full_stylesheet_dark_theme(self, theme_manager):
        """Test stylesheet contains dark theme colors"""
        theme_manager.current_theme = Theme.DARK
        stylesheet = theme_manager.get_full_stylesheet()
        
        # Check for dark theme characteristics
        assert '#2b2b2b' in stylesheet.lower() or 'dark' in stylesheet.lower()
    
    def test_get_full_stylesheet_light_theme(self, theme_manager):
        """Test stylesheet contains light theme colors"""
        theme_manager.current_theme = Theme.LIGHT
        stylesheet = theme_manager.get_full_stylesheet()
        
        # Check for light theme characteristics
        assert '#f5f5f5' in stylesheet.lower() or 'light' in stylesheet.lower()
    
    def test_get_stylesheet_with_component(self, theme_manager):
        """Test get_stylesheet returns component-specific styles"""
        control_style = theme_manager.get_stylesheet('control_panel')
        
        assert isinstance(control_style, str)
        # Control panel should have styling
        assert len(control_style) > 0
    
    def test_theme_enum_values(self):
        """Test Theme enum has correct values"""
        assert Theme.DARK.value == "dark"
        assert Theme.LIGHT.value == "light"
    
    def test_theme_consistency_after_toggle(self, theme_manager):
        """Test stylesheet changes after theme toggle"""
        dark_stylesheet = theme_manager.get_full_stylesheet()
        
        theme_manager.toggle_theme()
        light_stylesheet = theme_manager.get_full_stylesheet()
        
        # Stylesheets should be different
        assert dark_stylesheet != light_stylesheet
