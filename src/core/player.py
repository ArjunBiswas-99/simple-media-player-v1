"""
Unified media player using PyQt6 Multimedia
Handles both video and audio playback through Qt's native framework
"""

import logging
from typing import Optional
from pathlib import Path
from PyQt6.QtCore import QObject, pyqtSignal, QUrl
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget

logger = logging.getLogger(__name__)


class PlayerSignals(QObject):
    """Signals for communication between player and UI"""
    time_update = pyqtSignal(float)   # Current position in seconds
    duration_changed = pyqtSignal(float)  # Total duration in seconds
    playback_ended = pyqtSignal()     # Playback completed
    error_occurred = pyqtSignal(str)  # Error message


class MediaPlayer:
    """
    Unified media player for synchronized audio and video playback
    
    Responsibilities:
    - Load and play media files
    - Control playback state (play, pause, stop, seek)
    - Manage audio output (volume, mute)
    - Provide playback information (position, duration)
    - Emit signals for UI updates
    """
    
    def __init__(self):
        """Initialize media player with Qt Multimedia components"""
        # Core media player
        self._media_player = QMediaPlayer()
        
        # Audio output component
        self._audio_output = QAudioOutput()
        self._media_player.setAudioOutput(self._audio_output)
        
        # Video output widget (set later via initialize())
        self._video_widget: Optional[QVideoWidget] = None
        
        # Playback state
        self._current_file: Optional[str] = None
        self._volume = 100
        self._playback_speed = 1.0
        
        # Communication signals
        self.signals = PlayerSignals()
        
        # Connect internal Qt signals to our custom signals
        self._setup_signal_connections()
        
        logger.info("Media player initialized with PyQt6 Multimedia")
    
    def _setup_signal_connections(self):
        """Configure signal connections for player events"""
        # Position updates (for progress bar)
        self._media_player.positionChanged.connect(
            lambda pos: self.signals.time_update.emit(pos / 1000.0)
        )
        
        # Duration updates (when file loads)
        self._media_player.durationChanged.connect(
            lambda dur: self.signals.duration_changed.emit(dur / 1000.0)
        )
        
        # Playback state changes
        self._media_player.playbackStateChanged.connect(
            self._handle_playback_state_change
        )
        
        # Error handling
        self._media_player.errorOccurred.connect(
            self._handle_error
        )
    
    def _handle_playback_state_change(self, state):
        """
        Handle changes in playback state
        
        Args:
            state: QMediaPlayer.PlaybackState enum value
        """
        if state == QMediaPlayer.PlaybackState.StoppedState:
            # Check if we stopped because we reached the end
            if self._media_player.position() >= self._media_player.duration() - 100:
                logger.info("Playback completed")
                self.signals.playback_ended.emit()
    
    def _handle_error(self, error, error_string):
        """
        Handle playback errors
        
        Args:
            error: QMediaPlayer.Error enum value
            error_string: Human-readable error description
        """
        logger.error(f"Playback error: {error_string}")
        self.signals.error_occurred.emit(error_string)
    
    def initialize(self, video_widget: QVideoWidget) -> bool:
        """
        Initialize player with video display widget
        
        Args:
            video_widget: Qt widget for video rendering
            
        Returns:
            True if successful
        """
        self._video_widget = video_widget
        self._media_player.setVideoOutput(video_widget)
        
        # Set initial volume
        self._audio_output.setVolume(self._volume / 100.0)
        
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
            file_path = Path(filepath)
            if not file_path.exists():
                logger.error(f"File not found: {filepath}")
                return False
            
            # Stop any current playback
            self.stop()
            
            # Convert to QUrl for Qt Multimedia
            url = QUrl.fromLocalFile(str(file_path.absolute()))
            self._media_player.setSource(url)
            
            self._current_file = filepath
            
            logger.info(f"Loaded media: {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load file: {e}", exc_info=True)
            return False
    
    def play(self):
        """Start or resume playback"""
        if not self._current_file:
            logger.warning("No media loaded")
            return
        
        self._media_player.play()
        logger.info("Playback started")
    
    def pause(self):
        """Pause playback"""
        self._media_player.pause()
        logger.info("Playback paused")
    
    def toggle_pause(self):
        """Toggle between play and pause states"""
        if self.is_paused:
            self.play()
        else:
            self.pause()
    
    def stop(self):
        """Stop playback and reset to beginning"""
        self._media_player.stop()
        logger.info("Playback stopped")
    
    def seek(self, seconds: float, relative: bool = False):
        """
        Seek to a specific position in the media
        
        Args:
            seconds: Target position in seconds (or offset if relative)
            relative: If True, seek relative to current position
        """
        if not self._current_file:
            return
        
        try:
            if relative:
                # Seek relative to current position
                current_ms = self._media_player.position()
                target_ms = current_ms + int(seconds * 1000)
            else:
                # Seek to absolute position
                target_ms = int(seconds * 1000)
            
            # Clamp to valid range
            target_ms = max(0, min(target_ms, self._media_player.duration()))
            
            self._media_player.setPosition(target_ms)
            logger.debug(f"Seeked to {target_ms / 1000.0:.2f}s")
            
        except Exception as e:
            logger.error(f"Seek failed: {e}")
    
    def set_speed(self, speed: float):
        """
        Set playback speed for both video and audio
        
        Args:
            speed: Speed multiplier (0.5, 1.0, 1.5, 2.0, etc.)
        """
        self._playback_speed = max(0.1, min(speed, 4.0))
        self._media_player.setPlaybackRate(self._playback_speed)
        logger.info(f"Playback speed set to {self._playback_speed}x")
    
    def load_subtitle(self, subtitle_path: str):
        """
        Load external subtitle file
        
        Args:
            subtitle_path: Path to subtitle file (.srt, .ass, etc.)
        """
        # Subtitle support can be implemented with QMediaPlayer.setSubtitle
        logger.info(f"Subtitle loading: {subtitle_path} (not yet implemented)")
    
    @property
    def volume(self) -> int:
        """Get current volume level (0-100)"""
        return self._volume
    
    @volume.setter
    def volume(self, value: int):
        """
        Set audio volume level
        
        Args:
            value: Volume level (0-100)
        """
        self._volume = max(0, min(100, value))
        # Convert to Qt's 0.0-1.0 range
        self._audio_output.setVolume(self._volume / 100.0)
        logger.debug(f"Volume set to {self._volume}%")
    
    @property
    def is_paused(self) -> bool:
        """Check if playback is paused"""
        return self._media_player.playbackState() == QMediaPlayer.PlaybackState.PausedState
    
    @property
    def is_playing(self) -> bool:
        """Check if actively playing (not paused)"""
        return self._media_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState
    
    @property
    def duration(self) -> float:
        """Get total duration in seconds"""
        return self._media_player.duration() / 1000.0
    
    @property
    def time_pos(self) -> float:
        """Get current playback position in seconds"""
        return self._media_player.position() / 1000.0
    
    @property
    def muted(self) -> bool:
        """Check if audio is muted"""
        return self._audio_output.isMuted()
    
    @muted.setter
    def muted(self, value: bool):
        """
        Set audio mute state
        
        Args:
            value: True to mute, False to unmute
        """
        self._audio_output.setMuted(value)
        logger.debug(f"Muted: {value}")
    
    def toggle_mute(self):
        """Toggle audio mute state"""
        self.muted = not self.muted
    
    def shutdown(self):
        """Clean up resources and stop playback"""
        self.stop()
        self._media_player.setSource(QUrl())
        logger.info("Player shut down")
