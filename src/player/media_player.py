"""Media player wrapper using python-mpv."""

from typing import Optional, Callable
from pathlib import Path
import mpv
from PyQt6.QtCore import QObject, pyqtSignal


class MediaPlayer(QObject):
    """
    Wrapper around python-mpv for media playback.
    
    Signals:
        position_changed: Emitted when playback position changes (current_time, duration)
        state_changed: Emitted when playback state changes (is_playing, is_paused)
        file_loaded: Emitted when a file is successfully loaded
        error_occurred: Emitted when an error occurs (error_message)
    """
    
    position_changed = pyqtSignal(float, float)  # current_time, duration
    state_changed = pyqtSignal(bool, bool)  # is_playing, is_paused
    file_loaded = pyqtSignal(str)  # file_path
    error_occurred = pyqtSignal(str)  # error_message
    
    def __init__(self, parent: Optional[QObject] = None):
        """Initialize the media player."""
        super().__init__(parent)
        
        self._mpv: Optional[mpv.MPV] = None
        self._current_file: Optional[str] = None
        self._is_playing: bool = False
        self._is_paused: bool = False
        
    def initialize(self, wid: int) -> None:
        """
        Initialize MPV player with window ID.
        
        Args:
            wid: Window ID for embedding video
        """
        try:
            self._mpv = mpv.MPV(
                wid=str(wid),
                keep_open=True,
                idle=True,
                osc=False,  # Disable on-screen controller
                input_default_bindings=False,  # Disable default key bindings
                input_vo_keyboard=False,  # Disable keyboard input
            )
            
            # Set up property observers
            self._mpv.observe_property('time-pos', self._on_time_position_changed)
            self._mpv.observe_property('duration', self._on_duration_changed)
            self._mpv.observe_property('pause', self._on_pause_changed)
            
        except Exception as e:
            self.error_occurred.emit(f"Failed to initialize player: {str(e)}")
            
    def load_file(self, file_path: str) -> bool:
        """
        Load a media file.
        
        Args:
            file_path: Path to the media file
            
        Returns:
            True if file loaded successfully, False otherwise
        """
        if not self._mpv:
            self.error_occurred.emit("Player not initialized")
            return False
            
        try:
            path = Path(file_path)
            if not path.exists():
                self.error_occurred.emit(f"File not found: {file_path}")
                return False
                
            self._mpv.play(str(path))
            self._current_file = file_path
            self._is_playing = True
            self._is_paused = False
            
            self.file_loaded.emit(file_path)
            self.state_changed.emit(self._is_playing, self._is_paused)
            return True
            
        except Exception as e:
            self.error_occurred.emit(f"Failed to load file: {str(e)}")
            return False
            
    def play(self) -> None:
        """Start or resume playback."""
        if self._mpv and self._current_file:
            try:
                self._mpv.pause = False
                self._is_playing = True
                self._is_paused = False
                self.state_changed.emit(self._is_playing, self._is_paused)
            except Exception as e:
                self.error_occurred.emit(f"Failed to play: {str(e)}")
                
    def pause(self) -> None:
        """Pause playback."""
        if self._mpv and self._current_file:
            try:
                self._mpv.pause = True
                self._is_playing = True
                self._is_paused = True
                self.state_changed.emit(self._is_playing, self._is_paused)
            except Exception as e:
                self.error_occurred.emit(f"Failed to pause: {str(e)}")
                
    def stop(self) -> None:
        """Stop playback."""
        if self._mpv:
            try:
                self._mpv.stop()
                self._is_playing = False
                self._is_paused = False
                self.state_changed.emit(self._is_playing, self._is_paused)
            except Exception as e:
                self.error_occurred.emit(f"Failed to stop: {str(e)}")
                
    def seek(self, position: float) -> None:
        """
        Seek to a specific position.
        
        Args:
            position: Position in seconds
        """
        if self._mpv and self._current_file:
            try:
                self._mpv.seek(position, reference='absolute')
            except Exception as e:
                self.error_occurred.emit(f"Failed to seek: {str(e)}")
                
    def set_volume(self, volume: int) -> None:
        """
        Set the volume level.
        
        Args:
            volume: Volume level (0-100)
        """
        if self._mpv:
            try:
                self._mpv.volume = max(0, min(100, volume))
            except Exception as e:
                self.error_occurred.emit(f"Failed to set volume: {str(e)}")
                
    def get_volume(self) -> int:
        """
        Get the current volume level.
        
        Returns:
            Current volume (0-100)
        """
        if self._mpv:
            try:
                return int(self._mpv.volume)
            except Exception:
                pass
        return 50
        
    def get_duration(self) -> float:
        """
        Get the duration of the current media.
        
        Returns:
            Duration in seconds, or 0 if not available
        """
        if self._mpv and self._current_file:
            try:
                duration = self._mpv.duration
                return duration if duration is not None else 0.0
            except Exception:
                pass
        return 0.0
        
    def get_position(self) -> float:
        """
        Get the current playback position.
        
        Returns:
            Position in seconds, or 0 if not available
        """
        if self._mpv and self._current_file:
            try:
                pos = self._mpv.time_pos
                return pos if pos is not None else 0.0
            except Exception:
                pass
        return 0.0
        
    def is_playing(self) -> bool:
        """Check if media is currently playing."""
        return self._is_playing and not self._is_paused
        
    def is_paused(self) -> bool:
        """Check if media is paused."""
        return self._is_paused
        
    def has_media(self) -> bool:
        """Check if a media file is loaded."""
        return self._current_file is not None
        
    def _on_time_position_changed(self, name: str, value: Optional[float]) -> None:
        """Handle time position changes."""
        if value is not None:
            duration = self.get_duration()
            self.position_changed.emit(value, duration)
            
    def _on_duration_changed(self, name: str, value: Optional[float]) -> None:
        """Handle duration changes."""
        if value is not None:
            position = self.get_position()
            self.position_changed.emit(position, value)
            
    def _on_pause_changed(self, name: str, value: Optional[bool]) -> None:
        """Handle pause state changes."""
        if value is not None:
            self._is_paused = value
            if self._current_file:
                self._is_playing = True
            self.state_changed.emit(self._is_playing, self._is_paused)
            
    def cleanup(self) -> None:
        """Clean up resources."""
        if self._mpv:
            try:
                self._mpv.terminate()
            except Exception:
                pass
            self._mpv = None
        self._current_file = None
        self._is_playing = False
        self._is_paused = False
