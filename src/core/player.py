"""
Core player module - handles video/audio playback using OpenCV
"""

import logging
import cv2
import threading
import time
from typing import Optional, Callable
from pathlib import Path

logger = logging.getLogger(__name__)


class MediaPlayer:
    """Media player using OpenCV for video playback"""
    
    def __init__(self):
        """Initialize the media player"""
        self._video_capture: Optional[cv2.VideoCapture] = None
        self._current_file: Optional[str] = None
        self._is_playing = False
        self._is_paused = True
        self._playback_thread: Optional[threading.Thread] = None
        self._stop_flag = threading.Event()
        
        # Playback state
        self._current_frame_number = 0
        self._total_frames = 0
        self._fps = 30.0
        self._frame_delay = 0.033  # ~30 fps default
        
        # Audio/Video properties
        self._volume = 100
        self._muted = False
        self._playback_speed = 1.0
        
        # Callbacks
        self._frame_callback: Optional[Callable] = None
        self._time_pos_callback: Optional[Callable] = None
        self._end_callback: Optional[Callable] = None
        
        logger.info("OpenCV media player initialized")
    
    def initialize(self, video_widget):
        """
        Initialize player with video widget
        
        Args:
            video_widget: Qt widget that will display video frames
        """
        self._video_widget = video_widget
        logger.info("Player initialized with video widget")
        return True
    
    def load_file(self, filepath: str) -> bool:
        """
        Load a media file
        
        Args:
            filepath: Path to the media file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Stop current playback if any
            self.stop()
            
            # Open video file
            self._video_capture = cv2.VideoCapture(filepath)
            
            if not self._video_capture.isOpened():
                logger.error(f"Failed to open video file: {filepath}")
                return False
            
            # Get video properties
            self._total_frames = int(self._video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
            self._fps = self._video_capture.get(cv2.CAP_PROP_FPS)
            
            if self._fps <= 0:
                self._fps = 30.0  # Default fallback
            
            self._frame_delay = 1.0 / self._fps
            self._current_frame_number = 0
            self._current_file = filepath
            
            logger.info(f"Loaded video: {filepath}")
            logger.info(f"Properties - Frames: {self._total_frames}, FPS: {self._fps}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to load file: {e}")
            return False
    
    def play(self):
        """Start or resume playback"""
        if not self._video_capture:
            logger.warning("No video loaded")
            return
        
        self._is_paused = False
        
        if not self._is_playing:
            self._is_playing = True
            self._stop_flag.clear()
            self._playback_thread = threading.Thread(target=self._playback_loop, daemon=True)
            self._playback_thread.start()
            logger.info("Playback started")
    
    def pause(self):
        """Pause playback"""
        self._is_paused = True
        logger.info("Playback paused")
    
    def toggle_pause(self):
        """Toggle play/pause"""
        if self._is_paused:
            self.play()
        else:
            self.pause()
    
    def stop(self):
        """Stop playback"""
        self._is_playing = False
        self._is_paused = True
        self._stop_flag.set()
        
        if self._playback_thread and self._playback_thread.is_alive():
            self._playback_thread.join(timeout=1.0)
        
        if self._video_capture:
            self._current_frame_number = 0
            self._video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
        
        logger.info("Playback stopped")
    
    def seek(self, seconds: float, relative: bool = False):
        """
        Seek to a position
        
        Args:
            seconds: Target position in seconds (or offset if relative=True)
            relative: If True, seek relative to current position
        """
        if not self._video_capture:
            return
        
        try:
            if relative:
                current_pos = self._current_frame_number / self._fps
                target_seconds = current_pos + seconds
            else:
                target_seconds = seconds
            
            # Clamp to valid range
            target_seconds = max(0, min(target_seconds, self.duration))
            
            target_frame = int(target_seconds * self._fps)
            self._video_capture.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
            self._current_frame_number = target_frame
            
            logger.debug(f"Seeked to {target_seconds:.2f}s (frame {target_frame})")
            
        except Exception as e:
            logger.error(f"Seek failed: {e}")
    
    def set_speed(self, speed: float):
        """
        Set playback speed
        
        Args:
            speed: Playback speed multiplier (e.g., 0.5, 1.0, 1.5, 2.0)
        """
        self._playback_speed = max(0.1, min(speed, 4.0))
        self._frame_delay = (1.0 / self._fps) / self._playback_speed
        logger.info(f"Playback speed set to {self._playback_speed}x")
    
    def load_subtitle(self, subtitle_path: str):
        """
        Load an external subtitle file
        
        Args:
            subtitle_path: Path to subtitle file
        """
        # OpenCV doesn't have built-in subtitle support
        # This would need to be implemented separately if needed
        logger.info(f"Subtitle loading not yet implemented for OpenCV backend: {subtitle_path}")
    
    def set_frame_callback(self, callback: Callable):
        """Set callback for frame updates"""
        self._frame_callback = callback
    
    def set_time_pos_callback(self, callback: Callable):
        """Set callback for time position updates"""
        self._time_pos_callback = callback
    
    def set_end_file_callback(self, callback: Callable):
        """Set callback for end of file"""
        self._end_callback = callback
    
    @property
    def volume(self) -> int:
        """Get current volume (0-100)"""
        return self._volume
    
    @volume.setter
    def volume(self, value: int):
        """Set volume (0-100)"""
        self._volume = max(0, min(100, value))
        # Note: OpenCV doesn't handle audio directly
        # Audio control would need a separate audio library
    
    @property
    def is_paused(self) -> bool:
        """Check if playback is paused"""
        return self._is_paused
    
    @property
    def is_playing(self) -> bool:
        """Check if media is playing"""
        return self._is_playing and not self._is_paused
    
    @property
    def duration(self) -> float:
        """Get total duration in seconds"""
        if self._video_capture and self._total_frames > 0 and self._fps > 0:
            return self._total_frames / self._fps
        return 0.0
    
    @property
    def time_pos(self) -> float:
        """Get current playback position in seconds"""
        if self._fps > 0:
            return self._current_frame_number / self._fps
        return 0.0
    
    @property
    def muted(self) -> bool:
        """Check if audio is muted"""
        return self._muted
    
    @muted.setter
    def muted(self, value: bool):
        """Mute or unmute audio"""
        self._muted = value
    
    def toggle_mute(self):
        """Toggle mute state"""
        self._muted = not self._muted
    
    def toggle_fullscreen(self):
        """Toggle fullscreen mode - handled by GUI"""
        pass
    
    def shutdown(self):
        """Clean up resources"""
        self.stop()
        
        if self._video_capture:
            self._video_capture.release()
            self._video_capture = None
        
        logger.info("Player shut down")
    
    def _playback_loop(self):
        """Main playback loop running in separate thread"""
        logger.info("Playback loop started")
        
        while self._is_playing and not self._stop_flag.is_set():
            if self._is_paused:
                time.sleep(0.1)
                continue
            
            if not self._video_capture:
                break
            
            # Read next frame
            ret, frame = self._video_capture.read()
            
            if not ret:
                # End of video
                logger.info("End of video reached")
                self._is_playing = False
                if self._end_callback:
                    self._end_callback()
                break
            
            # Update frame number
            self._current_frame_number = int(self._video_capture.get(cv2.CAP_PROP_POS_FRAMES))
            
            # Call frame callback to update display
            if self._frame_callback:
                self._frame_callback(frame)
            
            # Call time position callback
            if self._time_pos_callback:
                self._time_pos_callback(self.time_pos)
            
            # Sleep to maintain frame rate
            time.sleep(self._frame_delay)
        
        logger.info("Playback loop ended")
