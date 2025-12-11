"""
Audio playback component using pygame mixer with PyAV audio extraction
Handles audio stream extraction and synchronized playback
"""

import logging
import time
import tempfile
import subprocess
from pathlib import Path
import pygame.mixer
import threading

logger = logging.getLogger(__name__)


class AudioPlayer:
    """
    Manages audio playback for media files using pygame
    
    Responsibilities:
    - Extract and load audio from media files
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
        self._temp_audio_file = None
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
        Extracts audio to temporary file if needed
        
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
            
            # Clean up previous temp file
            if self._temp_audio_file and Path(self._temp_audio_file).exists():
                try:
                    Path(self._temp_audio_file).unlink()
                except:
                    pass
            
            # Try to load directly first (for simple formats)
            try:
                pygame.mixer.music.load(str(file_path))
                self._current_file = filepath
                self._temp_audio_file = None
                self._is_loaded = True
                self._start_position = 0
                self._pause_position = 0
                
                # Set initial volume
                self._set_pygame_volume()
                
                logger.info(f"Audio loaded directly: {filepath}")
                return True
                
            except:
                # Direct load failed, need to extract audio
                logger.info("Direct load failed, extracting audio track...")
                return self._extract_and_load_audio(str(file_path))
            
        except Exception as e:
            logger.error(f"Failed to load audio: {e}")
            self._is_loaded = False
            return False
    
    def _extract_and_load_audio(self, filepath: str) -> bool:
        """
        Extract audio from video file using ffmpeg and load it
        
        Args:
            filepath: Path to the media file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create temporary WAV file for extracted audio
            temp_audio = tempfile.NamedTemporaryFile(
                suffix='.wav',
                delete=False
            )
            temp_audio.close()
            self._temp_audio_file = temp_audio.name
            
            # Use ffmpeg to extract audio (bundled with PyAV)
            import av
            
            # Open input container
            input_container = av.open(filepath)
            
            # Find audio stream
            audio_stream = None
            for stream in input_container.streams.audio:
                audio_stream = stream
                break
            
            if not audio_stream:
                logger.warning(f"No audio stream found in {filepath}")
                input_container.close()
                return False
            
            # Create output container for WAV with proper format
            output_container = av.open(self._temp_audio_file, 'w', format='wav')
            output_stream = output_container.add_stream('pcm_s16le', rate=44100)
            
            # Create resampler for audio conversion
            resampler = av.audio.resampler.AudioResampler(
                format='s16',
                layout='stereo',
                rate=44100
            )
            
            # Transcode audio with resampling
            frame_count = 0
            for packet in input_container.demux(audio_stream):
                for frame in packet.decode():
                    # Resample to 44.1kHz stereo
                    resampled_frames = resampler.resample(frame)
                    for resampled_frame in resampled_frames:
                        for packet in output_stream.encode(resampled_frame):
                            output_container.mux(packet)
                        frame_count += 1
            
            # Flush remaining packets
            for packet in output_stream.encode():
                output_container.mux(packet)
            
            # Close containers
            output_container.close()
            input_container.close()
            
            logger.info(f"Extracted {frame_count} audio frames")
            
            # Load the extracted audio
            pygame.mixer.music.load(self._temp_audio_file)
            
            self._current_file = filepath
            self._is_loaded = True
            self._start_position = 0
            self._pause_position = 0
            
            # Set initial volume
            self._set_pygame_volume()
            
            logger.info(f"Audio extracted and loaded: {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to extract audio: {e}", exc_info=True)
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
                logger.info("✓ Audio is playing successfully")
            else:
                logger.error("✗ Audio failed to start - mixer not busy")
            
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
            
            # Clean up temp audio file
            if self._temp_audio_file and Path(self._temp_audio_file).exists():
                try:
                    Path(self._temp_audio_file).unlink()
                    logger.debug(f"Cleaned up temp audio file: {self._temp_audio_file}")
                except Exception as e:
                    logger.warning(f"Failed to cleanup temp file: {e}")
            
            pygame.mixer.quit()
            logger.info("Audio player shut down")
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")
