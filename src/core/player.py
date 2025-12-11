"""
Core player module - handles video/audio playback using mpv
"""

import logging
from typing import Optional, Callable
import mpv

logger = logging.getLogger(__name__)


class MediaPlayer:
    """Wrapper around python-mpv for media playback"""
    
    def __init__(self):
        """Initialize the MPV player"""
        self.player: Optional[mpv.MPV] = None
        self._on_end_callback: Optional[Callable] = None
        self._on_time_pos_callback: Optional[Callable] = None
        
    def initialize(self, video_widget):
        """
        Initialize MPV with the video widget
        
        Args:
            video_widget: Qt widget that will display the video
        """
        try:
            # Get the window ID from the Qt widget
            wid = int(video_widget.winId())
            
            # Create MPV instance with configuration
            self.player = mpv.MPV(
                wid=str(wid),
                input_default_bindings=False,  # Disable MPV's default keybindings
                input_vo_keyboard=False,       # We'll handle keyboard ourselves
                keep_open='yes',               # Keep window open at end
                osc=False,                     # Disable on-screen controller
                ytdl=False,                    # Disable youtube-dl integration for MVP
                log_handler=self._log_handler,
                loglevel='info'
            )
            
            # Register event observers
            @self.player.property_observer('time-pos')
            def time_observer(_name, value):
                if value is not None and self._on_time_pos_callback:
                    self._on_time_pos_callback(value)
            
            @self.player.event_callback('end-file')
            def end_file_observer(event):
                if self._on_end_callback:
                    self._on_end_callback()
            
            logger.info("MPV player initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize MPV: {e}")
            return False
    
    def _log_handler(self, loglevel, component, message):
        """Handle MPV log messages"""
        logger.debug(f"[MPV/{component}] {message}")
    
    def load_file(self, filepath: str) -> bool:
        """
        Load a media file
        
        Args:
            filepath: Path to the media file
            
        Returns:
            True if successful, False otherwise
        """
        if not self.player:
            logger.error("Player not initialized")
            return False
        
        try:
            # Use the command method with 'loadfile' to properly load the file
            self.player.command('loadfile', filepath)
            logger.info(f"Loaded file: {filepath}")
            return True
        except Exception as e:
            logger.error(f"Failed to load file: {e}")
            return False
    
    def play(self):
        """Start or resume playback"""
        if self.player:
            self.player.pause = False
    
    def pause(self):
        """Pause playback"""
        if self.player:
            self.player.pause = True
    
    def toggle_pause(self):
        """Toggle play/pause"""
        if self.player:
            self.player.pause = not self.player.pause
    
    def stop(self):
        """Stop playback"""
        if self.player:
            self.player.stop()
    
    def seek(self, seconds: float, relative: bool = False):
        """
        Seek to a position
        
        Args:
            seconds: Target position in seconds (or offset if relative=True)
            relative: If True, seek relative to current position
        """
        if self.player:
            try:
                if relative:
                    self.player.seek(seconds, reference='relative')
                else:
                    self.player.time_pos = seconds
            except Exception as e:
                logger.error(f"Seek failed: {e}")
    
    @property
    def volume(self) -> int:
        """Get current volume (0-100)"""
        if self.player:
            return int(self.player.volume)
        return 100
    
    @volume.setter
    def volume(self, value: int):
        """Set volume (0-100)"""
        if self.player:
            self.player.volume = max(0, min(100, value))
    
    @property
    def is_paused(self) -> bool:
        """Check if playback is paused"""
        if self.player:
            return self.player.pause
        return True
    
    @property
    def is_playing(self) -> bool:
        """Check if media is playing"""
        if self.player:
            return not self.player.pause and self.player.time_pos is not None
        return False
    
    @property
    def duration(self) -> float:
        """Get total duration in seconds"""
        if self.player and self.player.duration:
            return float(self.player.duration)
        return 0.0
    
    @property
    def time_pos(self) -> float:
        """Get current playback position in seconds"""
        if self.player and self.player.time_pos:
            return float(self.player.time_pos)
        return 0.0
    
    @property
    def muted(self) -> bool:
        """Check if audio is muted"""
        if self.player:
            return self.player.mute
        return False
    
    @muted.setter
    def muted(self, value: bool):
        """Mute or unmute audio"""
        if self.player:
            self.player.mute = value
    
    def toggle_mute(self):
        """Toggle mute state"""
        if self.player:
            self.player.mute = not self.player.mute
    
    def toggle_fullscreen(self):
        """Toggle fullscreen mode"""
        if self.player:
            self.player.fullscreen = not self.player.fullscreen
    
    def set_speed(self, speed: float):
        """
        Set playback speed
        
        Args:
            speed: Playback speed multiplier (e.g., 0.5, 1.0, 1.5, 2.0)
        """
        if self.player:
            self.player.speed = speed
    
    def load_subtitle(self, subtitle_path: str):
        """
        Load an external subtitle file
        
        Args:
            subtitle_path: Path to subtitle file (SRT, ASS, etc.)
        """
        if self.player:
            try:
                self.player.sub_add(subtitle_path)
                logger.info(f"Loaded subtitle: {subtitle_path}")
            except Exception as e:
                logger.error(f"Failed to load subtitle: {e}")
    
    def set_time_pos_callback(self, callback: Callable):
        """Set callback for time position updates"""
        self._on_time_pos_callback = callback
    
    def set_end_file_callback(self, callback: Callable):
        """Set callback for end of file"""
        self._on_end_callback = callback
    
    def shutdown(self):
        """Clean up resources"""
        if self.player:
            try:
                self.player.terminate()
            except Exception as e:
                logger.error(f"Error during shutdown: {e}")
            self.player = None
