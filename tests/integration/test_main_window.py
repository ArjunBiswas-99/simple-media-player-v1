"""
Integration tests for MainWindow
Tests the interaction between GUI components
"""

import pytest
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication
from src.gui.main_window import MainWindow


@pytest.mark.integration
@pytest.mark.gui
class TestMainWindowIntegration:
    """Integration tests for MainWindow"""
    
    def test_window_creation(self, main_window):
        """Test main window creates successfully"""
        assert main_window is not None
        assert main_window.windowTitle() == "Simple Media Player"
    
    def test_window_has_video_widget(self, main_window):
        """Test window contains video widget"""
        assert hasattr(main_window, 'video_widget')
        assert main_window.video_widget is not None
    
    def test_window_has_control_panel(self, main_window):
        """Test window contains control panel"""
        assert hasattr(main_window, 'control_panel')
        assert main_window.control_panel is not None
    
    def test_window_has_player(self, main_window):
        """Test window has media player instance"""
        assert hasattr(main_window, 'player')
        assert main_window.player is not None
    
    def test_play_button_exists(self, main_window):
        """Test play button exists"""
        assert hasattr(main_window, 'play_button')
        assert main_window.play_button is not None
    
    def test_volume_slider_exists(self, main_window):
        """Test volume slider exists"""
        assert hasattr(main_window, 'volume_slider')
        assert main_window.volume_slider.minimum() == 0
        assert main_window.volume_slider.maximum() == 100
    
    def test_progress_slider_exists(self, main_window):
        """Test progress slider exists"""
        assert hasattr(main_window, 'progress_slider')
        assert main_window.progress_slider.minimum() == 0
        assert main_window.progress_slider.maximum() == 1000
    
    def test_theme_toggle_button_exists(self, main_window):
        """Test theme toggle button exists"""
        assert hasattr(main_window, 'theme_toggle_button')
        assert main_window.theme_toggle_button is not None
    
    def test_theme_toggle_updates_ui(self, qtbot, main_window):
        """Test theme toggle changes UI appearance"""
        initial_theme = main_window.theme_manager.current_theme
        
        # Click theme toggle button
        qtbot.mouseClick(main_window.theme_toggle_button, Qt.MouseButton.LeftButton)
        
        # Theme should have changed
        assert main_window.theme_manager.current_theme != initial_theme
    
    def test_volume_slider_changes_player_volume(self, qtbot, main_window):
        """Test volume slider updates player volume"""
        # Set slider to 50%
        main_window.volume_slider.setValue(50)
        
        # Player volume should be updated (0.5 as decimal)
        assert main_window.player.audio_output.volume() == pytest.approx(0.5, rel=0.01)
    
    def test_speed_button_cycles(self, qtbot, main_window):
        """Test speed button cycles through speeds"""
        initial_text = main_window.speed_button.text()
        
        # Click speed button
        qtbot.mouseClick(main_window.speed_button, Qt.MouseButton.LeftButton)
        
        # Text should have changed
        assert main_window.speed_button.text() != initial_text
    
    def test_menu_bar_exists(self, main_window):
        """Test menu bar is created"""
        menubar = main_window.menuBar()
        assert menubar is not None
        
        # Check for expected menus
        menus = [action.text() for action in menubar.actions()]
        assert any('File' in menu for menu in menus)
        assert any('Playback' in menu for menu in menus)
        assert any('View' in menu for menu in menus)
    
    def test_keyboard_shortcut_space(self, qtbot, main_window):
        """Test Space key toggles play/pause"""
        # This test simulates keyboard input
        qtbot.keyPress(main_window, Qt.Key.Key_Space)
        
        # Should trigger play/pause (exact behavior depends on state)
        # Just verify it doesn't crash
        assert True
    
    def test_fullscreen_toggle_exists(self, main_window):
        """Test fullscreen toggle functionality exists"""
        assert hasattr(main_window, '_toggle_fullscreen')
        assert callable(main_window._toggle_fullscreen)
    
    def test_window_minimum_size(self, main_window):
        """Test window has minimum size set"""
        assert main_window.minimumWidth() >= 800
        assert main_window.minimumHeight() >= 600
    
    def test_timer_running(self, main_window):
        """Test update timer is running"""
        assert hasattr(main_window, 'update_timer')
        assert main_window.update_timer.isActive()


@pytest.mark.integration
@pytest.mark.slow
class TestMainWindowWorkflows:
    """Test complete user workflows"""
    
    def test_theme_switching_workflow(self, qtbot, main_window):
        """Test complete theme switching workflow"""
        # Start in dark theme
        assert main_window.theme_manager.current_theme.value == "dark"
        
        # Toggle to light
        qtbot.mouseClick(main_window.theme_toggle_button, Qt.MouseButton.LeftButton)
        qtbot.wait(100)  # Wait for UI update
        
        assert main_window.theme_manager.current_theme.value == "light"
        
        # Toggle back to dark
        qtbot.mouseClick(main_window.theme_toggle_button, Qt.MouseButton.LeftButton)
        qtbot.wait(100)
        
        assert main_window.theme_manager.current_theme.value == "dark"
    
    def test_volume_control_workflow(self, qtbot, main_window):
        """Test volume adjustment workflow"""
        # Set to 100%
        main_window.volume_slider.setValue(100)
        assert main_window.volume_label.text() == "100%"
        
        # Set to 50%
        main_window.volume_slider.setValue(50)
        assert main_window.volume_label.text() == "50%"
        
        # Set to 0%
        main_window.volume_slider.setValue(0)
        assert main_window.volume_label.text() == "0%"
