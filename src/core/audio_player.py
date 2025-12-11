"""
Audio playback component using pygame mixer
Handles audio stream extraction and synchronized playback
"""

import logging
import time
from pathlib import Path
import pygame.mixer
import threading

logger = logging.getLogger(__name__)


class AudioPlayer:
    """
    Manages audio playback for media files using pygame
    
    Responsibilities:
    - Load and play audio from media files
    - Control playback state (play, pause, stop)
    - Manage volume and mute state
    - Provide playback position for synchronization
    """
    
    def __init__(self):
        """Initialize audio player components"""
        # Initialize pygame mixer for audio
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=2048)
        
        # Playback state
        self._current_file = None
        self._volume = 100
        self._is_muted = False
        self._is_loaded = False
        
        # Position tracking
        self._start_position = 0  # Position when playback started (seconds)
        self._pause_position = 0  # Position when paused (seconds)
        
        logger.info("Audio player initialized with pygame mixer")
    
    def load(self, filepath: str) -> bool:
        """
        Load audio from a media file
        
        Args:
            filepath: Path to the media file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            file_path = Path(filepath)
            if not file_path.exists():
                logger.error(f"Audio file not found: {filepath}")
                return False
            
            # Stop any current playback
            self.stop()
            
            # Load the audio file
            pygame.mixer.music.load(str(file_path))
            
            # Set initial volume
            self._set_pygame_volume()
            
            self._current_file = filepath
            self._is_loaded = True
            self._start_position = 0
            self._pause_position = 0
            
            logger.info(f"Audio loaded: {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load audio: {e}")
            self._is_loaded = False
            return False
    
    def play(self):
        """Start or resume audio playback"""
        if not self._is_loaded:
            logger.warning("No audio loaded")
            return
        
        try:
            # If paused, unpause. Otherwise start from beginning
            if pygame.mixer.music.get_busy() and self._pause_position > 0:
                pygame.mixer.music.unpause()
                logger.info("Audio unpaused")
            else:
                pygame.mixer.music.play(start=self._start_position)
                logger.info(f"Audio playback started from {self._start_position}s")
            
            # Verify playback started
            time.sleep(0.1)
            if pygame.mixer.music.get_busy():
                logger.info("Audio is playing")
            else:
                logger.error("Audio failed to start - mixer not busy")
            
        except Exception as e:
            logger.error(f"Failed to start audio playback: {e}", exc_info=True)
    
    def pause(self):
        """Pause audio playback"""
        if not self._is_loaded:
            return
        
        try:
            # Get current position before pausing
            self._pause_position = self.position / 1000.0  # Convert to seconds
            pygame.mixer.music.pause()
            logger.debug("Audio playback paused")
            
        except Exception as e:
            logger.error(f"Failed to pause audio: {e}")
    
    def stop(self):
        """Stop audio playback and reset position"""
        if not self._is_loaded:
            return
        
        try:
            pygame.mixer.music.stop()
            self._start_position = 0
            self._pause_position = 0
            logger.debug("Audio playback stopped")
            
        except Exception as e:
            logger.error(f"Failed to stop audio: {e}")
    
    def seek(self, position_ms: int):
        """
        Seek to a specific position in the audio
        
        Args:
            position_ms: Target position in milliseconds
        """
        if not self._is_loaded:
            return
        
        try:
            position_seconds = position_ms / 1000.0
            
            # Store the seek position
            self._start_position = position_seconds
            self._pause_position = position_seconds
            
            # Restart playback from new position
            was_playing = self.is_playing
            pygame.mixer.music.stop()
            
            if was_playing:
                pygame.mixer.music.play(start=position_seconds)
            
            logger.debug(f"Audio seeked to {position_ms}ms")
            
        except Exception as e:
            logger.error(f"Seek failed: {e}")
    
    def set_volume(self, volume: int):
        """
        Set audio volume level
        
        Args:
            volume: Volume level (0-100)
        """
        self._volume = max(0, min(100, volume))
        self._set_pygame_volume()
        logger.debug(f"Audio volume set to {self._volume}%")
    
    def _set_pygame_volume(self):
        """Apply current volume setting to pygame mixer"""
        if self._is_muted:
            pygame.mixer.music.set_volume(0.0)
        else:
            # Convert 0-100 to 0.0-1.0
            pygame.mixer.music.set_volume(self._volume / 100.0)
    
    def set_muted(self, muted: bool):
        """
        Set audio mute state
        
        Args:
            muted: True to mute, False to unmute
        """
        self._is_muted = muted
        self._set_pygame_volume()
        logger.debug(f"Audio muted: {muted}")
    
    def toggle_mute(self):
        """Toggle audio mute state"""
        self.set_muted(not self._is_muted)
    
    def set_playback_rate(self, rate: float):
        """
        Set audio playback speed
        
        Note: pygame.mixer doesn't support playback rate changes natively
        This is a limitation of the library
        
        Args:
            rate: Playback rate multiplier (e.g., 0.5, 1.0, 1.5, 2.0)
        """
        # pygame doesn't support playback rate changes
        # This is a known limitation
        logger.debug(f"Playback rate change requested: {rate}x (not supported by pygame)")
    
    @property
    def position(self) -> int:
        """
        Get current playback position in milliseconds
        
        Note: pygame.mixer has limited position tracking
        Returns approximate position based on get_pos()
        """
        if not self._is_loaded:
            return 0
        
        try:
            # get_pos() returns milliseconds since music started
            pygame_pos = pygame.mixer.music.get_pos()
            
            if pygame_pos >= 0:
                # Add the start position we seeked to
                return int((self._start_position * 1000) + pygame_pos)
            else:
                return int(self._pause_position * 1000)
                
        except Exception:
            return 0
    
    @property
    def duration(self) -> int:
        """
        Get total audio duration in milliseconds
        
        Note: pygame.mixer doesn't provide duration directly
        Returns 0 as it's not available
        """
        # pygame doesn't provide duration info
        return 0
    
    @property
    def is_playing(self) -> bool:
        """Check if audio is currently playing"""
        return self._is_loaded and pygame.mixer.music.get_busy()
    
    @property
    def volume(self) -> int:
        """Get current volume level (0-100)"""
        return self._volume
    
    @property
    def is_muted(self) -> bool:
        """Check if audio is muted"""
        return self._is_muted
    
    def shutdown(self):
        """Clean up audio resources"""
        try:
            self.stop()
            pygame.mixer.quit()
            logger.info("Audio player shut down")
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")
