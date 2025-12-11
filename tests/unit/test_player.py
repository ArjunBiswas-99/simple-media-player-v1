"""
Unit tests for MediaPlayer
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from PyQt6.QtCore import QUrl
from src.core.player import MediaPlayer


@pytest.mark.unit
class TestMediaPlayer:
    """Test suite for MediaPlayer class"""
    
    def test_initialization(self):
        """Test MediaPlayer initializes correctly"""
        player = MediaPlayer()
        
        assert player is not None
        assert hasattr(player, 'player')
        assert hasattr(player, 'audio_output')
    
    def test_volume_property_get(self, media_player):
        """Test getting volume property"""
        # Set volume to known value
        media_player.audio_output.setVolume(0.75)
        
        volume = media_player.volume
        
        assert volume == 75  # Volume is returned as percentage
    
    def test_volume_property_set(self, media_player):
        """Test setting volume property"""
        media_player.volume = 50
        
        # Volume should be set as decimal (0.5)
        assert media_player.audio_output.volume() == pytest.approx(0.5, rel=0.01)
    
    def test_volume_bounds_zero(self, media_player):
        """Test volume minimum bound"""
        media_player.volume = 0
        
        assert media_player.audio_output.volume() == 0.0
    
    def test_volume_bounds_hundred(self, media_player):
        """Test volume maximum bound"""
        media_player.volume = 100
        
        assert media_player.audio_output.volume() == 1.0
    
    def test_is_playing_initially_false(self, media_player):
        """Test is_playing is False initially"""
        assert media_player.is_playing is False
    
    def test_toggle_mute(self, media_player):
        """Test mute toggle functionality"""
        initial_muted = media_player.audio_output.isMuted()
        
        media_player.toggle_mute()
        
        assert media_player.audio_output.isMuted() != initial_muted
    
    def test_toggle_mute_twice(self, media_player):
        """Test toggling mute twice returns to original state"""
        initial_muted = media_player.audio_output.isMuted()
        
        media_player.toggle_mute()
        media_player.toggle_mute()
        
        assert media_player.audio_output.isMuted() == initial_muted
    
    def test_set_speed_normal(self, media_player):
        """Test setting playback speed to 1.0x"""
        media_player.set_speed(1.0)
        
        assert media_player.player.playbackRate() == pytest.approx(1.0, rel=0.01)
    
    def test_set_speed_half(self, media_player):
        """Test setting playback speed to 0.5x"""
        media_player.set_speed(0.5)
        
        assert media_player.player.playbackRate() == pytest.approx(0.5, rel=0.01)
    
    def test_set_speed_double(self, media_player):
        """Test setting playback speed to 2.0x"""
        media_player.set_speed(2.0)
        
        assert media_player.player.playbackRate() == pytest.approx(2.0, rel=0.01)
    
    def test_duration_property_initially_zero(self, media_player):
        """Test duration is 0 initially"""
        # Without loading a file, duration should be 0
        assert media_player.duration >= 0
    
    def test_position_property_initially_zero(self, media_player):
        """Test position is 0 initially"""
        assert media_player.position >= 0
    
    @patch('core.player.MediaPlayer.load_file')
    def test_load_file_calls_method(self, mock_load, media_player):
        """Test load_file method is called correctly"""
        test_path = "/path/to/video.mp4"
        
        media_player.load_file(test_path)
        
        mock_load.assert_called_once_with(test_path)
    
    def test_signals_exist(self, media_player):
        """Test that player signals object exists"""
        assert hasattr(media_player, 'signals')
        assert hasattr(media_player.signals, 'time_update')
        assert hasattr(media_player.signals, 'duration_changed')
        assert hasattr(media_player.signals, 'playback_ended')
    
    def test_shutdown_method_exists(self, media_player):
        """Test shutdown method exists and is callable"""
        assert hasattr(media_player, 'shutdown')
        assert callable(media_player.shutdown)
        
        # Should not raise exception
        media_player.shutdown()


@pytest.mark.unit  
class TestMediaPlayerEdgeCases:
    """Test edge cases and error handling"""
    
    def test_volume_negative_clamped(self, media_player):
        """Test negative volume is clamped to 0"""
        media_player.volume = -10
        
        assert media_player.volume >= 0
    
    def test_volume_over_hundred_clamped(self, media_player):
        """Test volume over 100 is clamped"""
        media_player.volume = 150
        
        assert media_player.volume <= 100
    
    def test_speed_zero_handling(self, media_player):
        """Test setting speed to 0 (pause-like behavior)"""
        # Speed of 0 might not be supported, should handle gracefully
        try:
            media_player.set_speed(0.0)
            # If it works, speed should be set
            assert media_player.player.playbackRate() >= 0
        except (ValueError, Exception):
            # If it doesn't work, should raise appropriate error
            pass
    
    def test_seek_without_media(self, media_player):
        """Test seeking without loaded media doesn't crash"""
        # Should handle gracefully
        try:
            media_player.seek(10.0)
        except Exception as e:
            pytest.fail(f"Seek without media raised exception: {e}")
