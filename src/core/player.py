"""
Core media player - orchestrates video and audio playback
Uses PyAV for video decoding and PyQt6 Multimedia for audio
"""

import logging
import av
import threading
import time
import numpy as np
from typing import Optional
from pathlib import Path
from PyQt6.QtCore import QObject, pyqtSignal

from .audio_player import AudioPlayer

logger = logging.getLogger(__name__)


class PlayerSignals(QObject):
    """Signals for thread-safe communication with GUI"""
    frame_ready = pyqtSignal(object)  # Emits frame (numpy array)
    time_update = pyqtSignal(float)   # Emits time position in seconds
    playback_ended = pyqtSignal()     # Emits when playback completes


class MediaPlayer:
    """
    Unified media player for video and audio
    
    Responsibilities:
    - Coordinate video and audio playback
    - Maintain synchronization between streams
    - Provide unified control interface
    - Manage playback state and timing
    """
    
    def __init__(self):
        """Initialize media player components"""
        # Video components
        self._container: Optional[av.container.InputContainer] = None
        self._video_stream = None
        self._current_file: Optional[str] = None
        
        # Audio component
        self._audio_player = AudioPlayer()
        
        # Playback state
        self._is_playing = False
        self._is_paused = True
        self._playback_thread: Optional[threading.Thread] = None
        self._stop_flag = threading.Event()
        
        # Timing and synchronization
        self._current_pts = 0  # Presentation timestamp
        self._video_time_base = 1.0
        self._start_time = 0
        self._pause_time = 0
        
        # Playback properties
        self._volume = 100
        self._playback_speed = 1.0
        self._duration = 0.0
        
        # Thread-safe signals
        self.signals = PlayerSignals()
        
        # Thread safety
        self._lock = threading.Lock()
        
        logger.info("Media player initialized with PyAV + PyQt6 audio")
    
    def initialize(self, video_widget) -> bool:
        """
        Initialize player with video display widget
        
        Args:
            video_widget: Qt widget for video frame display
            
        Returns:
            True if successful
        """
        self._video_widget = video_widget
        logger.info("Player initialized with video widget")
        return True
    
    def load_file(self, filepath: str) -> bool:
        """
        Load a media file for playback
        
        Args:
            filepath: Path to the media file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Stop any current playback
            self.stop()
            
            # Verify file exists
            if not Path(filepath).exists():
                logger.error(f"File not found: {filepath}")
                return False
            
            # Open container with PyAV
            self._container = av.open(filepath)
            
            # Find video stream
            self._video_stream = None
            for stream in self._container.streams.video:
                if stream.codec_context:
                    self._video_stream = stream
                    break
            
            if not self._video_stream:
                logger.error("No video stream found in file")
                return False
            
            # Extract video timing information
            self._video_time_base = float(self._video_stream.time_base)
            
            # Calculate duration
            if self._video_stream.duration:
                self._duration = float(self._video_stream.duration * self._video_time_base)
            elif self._container.duration:
                self._duration = float(self._container.duration) / av.time_base
            else:
                self._duration = 0.0
            
            # Load audio separately using QMediaPlayer
            audio_loaded = self._audio_player.load(filepath)
            if not audio_loaded:
                logger.warning("Audio track not found or failed to load")
            
            # Apply current volume setting
            self._audio_player.set_volume(self._volume)
            
            self._current_file = filepath
            self._current_pts = 0
            
            logger.info(f"Loaded media: {filepath}")
            logger.info(f"Duration: {self._duration:.2f}s, FPS: {self._video_stream.average_rate}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to load file: {e}", exc_info=True)
            return False
    
    def play(self):
        """Start or resume playback"""
        if not self._container:
            logger.warning("No media loaded")
            return
        
        self._is_paused = False
        
        # Start audio playback
        self._audio_player.play()
        
        # Start video playback thread if not already running
        if not self._is_playing:
            self._is_playing = True
            self._stop_flag.clear()
            self._start_time = time.time()
            
            self._playback_thread = threading.Thread(
                target=self._playback_loop,
                daemon=True
            )
            self._playback_thread.start()
            logger.info("Playback started")
        else:
            # Resume from pause
            self._start_time = time.time() - self._pause_time
            logger.info("Playback resumed")
    
    def pause(self):
        """Pause playback"""
        if not self._is_paused:
            self._is_paused = True
            self._pause_time = time.time() - self._start_time
            self._audio_player.pause()
            logger.info("Playback paused")
    
    def toggle_pause(self):
        """Toggle between play and pause states"""
        if self._is_paused:
            self.play()
        else:
            self.pause()
    
    def stop(self):
        """Stop playback and reset to beginning"""
        self._is_playing = False
        self._is_paused = True
        self._stop_flag.set()
        
        # Stop audio
        self._audio_player.stop()
        
        # Wait for playback thread to finish
        if self._playback_thread and self._playback_thread.is_alive():
            self._playback_thread.join(timeout=1.0)
        
        # Reset video position
        if self._container:
            try:
                self._container.seek(0)
                self._current_pts = 0
            except Exception as e:
                logger.error(f"Failed to reset position: {e}")
        
        logger.info("Playback stopped")
    
    def seek(self, seconds: float, relative: bool = False):
        """
        Seek to a specific position
        
        Args:
            seconds: Target position in seconds (or offset if relative)
            relative: If True, seek relative to current position
        """
        if not self._container:
            return
        
        with self._lock:
            try:
                # Calculate target position
                if relative:
                    target_seconds = self.time_pos + seconds
                else:
                    target_seconds = seconds
                
                # Clamp to valid range
                target_seconds = max(0, min(target_seconds, self.duration))
                
                # Convert to stream time base
                target_pts = int(target_seconds / self._video_time_base)
                
                # Seek video container
                self._container.seek(target_pts, stream=self._video_stream)
                self._current_pts = target_pts
                
                # Seek audio
                self._audio_player.seek(int(target_seconds * 1000))
                
                # Update timing for synchronization
                if not self._is_paused:
                    self._start_time = time.time() - target_seconds
                
                logger.debug(f"Seeked to {target_seconds:.2f}s")
                
            except Exception as e:
                logger.error(f"Seek failed: {e}")
    
    def set_speed(self, speed: float):
        """
        Set playback speed for both video and audio
        
        Args:
            speed: Speed multiplier (0.5, 1.0, 1.5, 2.0, etc.)
        """
        self._playback_speed = max(0.1, min(speed, 4.0))
        self._audio_player.set_playback_rate(self._playback_speed)
        logger.info(f"Playback speed set to {self._playback_speed}x")
    
    def load_subtitle(self, subtitle_path: str):
        """
        Load external subtitle file
        
        Args:
            subtitle_path: Path to subtitle file (.srt, .ass, etc.)
        """
        # Subtitle support can be implemented later
        logger.info(f"Subtitle loading: {subtitle_path} (not yet implemented)")
    
    @property
    def volume(self) -> int:
        """Get current volume level (0-100)"""
        return self._volume
    
    @volume.setter
    def volume(self, value: int):
        """Set volume level (0-100)"""
        self._volume = max(0, min(100, value))
        self._audio_player.set_volume(self._volume)
    
    @property
    def is_paused(self) -> bool:
        """Check if playback is paused"""
        return self._is_paused
    
    @property
    def is_playing(self) -> bool:
        """Check if actively playing (not paused)"""
        return self._is_playing and not self._is_paused
    
    @property
    def duration(self) -> float:
        """Get total duration in seconds"""
        return self._duration
    
    @property
    def time_pos(self) -> float:
        """Get current playback position in seconds"""
        if self._is_playing and not self._is_paused:
            return time.time() - self._start_time
        elif self._is_paused:
            return self._pause_time
        return 0.0
    
    @property
    def muted(self) -> bool:
        """Check if audio is muted"""
        return self._audio_player.is_muted
    
    @muted.setter
    def muted(self, value: bool):
        """Set mute state"""
        self._audio_player.set_muted(value)
    
    def toggle_mute(self):
        """Toggle mute state"""
        self._audio_player.toggle_mute()
    
    def shutdown(self):
        """Clean up all resources"""
        self.stop()
        
        # Shutdown audio
        self._audio_player.shutdown()
        
        # Close video container
        if self._container:
            self._container.close()
            self._container = None
        
        logger.info("Player shut down")
    
    def _playback_loop(self):
        """
        Main playback loop for video frames
        Runs in separate thread and syncs with audio
        """
        logger.info("Video playback loop started")
        
        try:
            for packet in self._container.demux(self._video_stream):
                # Check for stop signal
                if self._stop_flag.is_set() or not self._is_playing:
                    break
                
                # Wait while paused
                while self._is_paused and not self._stop_flag.is_set():
                    time.sleep(0.01)
                
                if self._stop_flag.is_set():
                    break
                
                # Decode video frames
                for frame in packet.decode():
                    if self._stop_flag.is_set() or not self._is_playing:
                        break
                    
                    # Convert frame to numpy array (BGR format for Qt compatibility)
                    img = frame.to_ndarray(format='bgr24')
                    
                    # Calculate frame timing
                    frame_pts = float(frame.pts * self._video_time_base) if frame.pts else 0
                    
                    # Synchronize with audio/wall clock
                    current_time = self.time_pos
                    time_diff = frame_pts - current_time
                    
                    # Wait if we're ahead of schedule (with better sync)
                    if time_diff > 0.001:  # Only sync if more than 1ms ahead
                        sleep_time = min(time_diff / self._playback_speed, 0.1)  # Cap at 100ms
                        time.sleep(sleep_time)
                    elif time_diff < -0.5:  # If more than 500ms behind, skip frame
                        continue
                    
                    # Emit frame for display
                    self.signals.frame_ready.emit(img)
                    
                    # Update timing
                    self._current_pts = frame.pts if frame.pts else self._current_pts
                    self.signals.time_update.emit(frame_pts)
            
            # Playback completed
            logger.info("Video playback completed")
            self._is_playing = False
            self.signals.playback_ended.emit()
            
        except Exception as e:
            logger.error(f"Playback error: {e}", exc_info=True)
            self._is_playing = False
        
        logger.info("Video playback loop ended")
