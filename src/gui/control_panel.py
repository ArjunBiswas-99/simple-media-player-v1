"""Control panel widget for Simple Media Player."""

from typing import Optional
from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QPushButton, 
    QSlider, QLabel, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon


class ControlPanel(QWidget):
    """
    Control panel with playback controls, progress bar, and volume.
    
    Signals:
        play_clicked: User clicked play button
        pause_clicked: User clicked pause button
        stop_clicked: User clicked stop button
        seek_requested: User seeked to position (position in seconds)
        volume_changed: User changed volume (volume 0-100)
    """
    
    play_clicked = pyqtSignal()
    pause_clicked = pyqtSignal()
    stop_clicked = pyqtSignal()
    seek_requested = pyqtSignal(float)  # position in seconds
    volume_changed = pyqtSignal(int)  # volume 0-100
    
    def __init__(self, parent: Optional[QWidget] = None):
        """Initialize the control panel."""
        super().__init__(parent)
        
        self._seeking = False
        self._duration = 0.0
        
        self._setup_ui()
        self._connect_signals()
        
    def _setup_ui(self) -> None:
        """Set up the user interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 10)
        layout.setSpacing(5)
        
        # Progress bar and time display
        progress_layout = QHBoxLayout()
        progress_layout.setSpacing(10)
        
        self._time_label = QLabel("00:00")
        self._time_label.setMinimumWidth(50)
        progress_layout.addWidget(self._time_label)
        
        self._progress_slider = QSlider(Qt.Orientation.Horizontal)
        self._progress_slider.setMinimum(0)
        self._progress_slider.setMaximum(1000)
        self._progress_slider.setValue(0)
        self._progress_slider.setEnabled(False)
        progress_layout.addWidget(self._progress_slider, stretch=1)
        
        self._duration_label = QLabel("00:00")
        self._duration_label.setMinimumWidth(50)
        self._duration_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        progress_layout.addWidget(self._duration_label)
        
        layout.addLayout(progress_layout)
        
        # Control buttons and volume
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(10)
        
        # Playback buttons
        self._play_button = QPushButton("▶ Play")
        self._play_button.setMinimumWidth(80)
        self._play_button.setEnabled(False)
        controls_layout.addWidget(self._play_button)
        
        self._pause_button = QPushButton("⏸ Pause")
        self._pause_button.setMinimumWidth(80)
        self._pause_button.setEnabled(False)
        controls_layout.addWidget(self._pause_button)
        
        self._stop_button = QPushButton("⏹ Stop")
        self._stop_button.setMinimumWidth(80)
        self._stop_button.setEnabled(False)
        controls_layout.addWidget(self._stop_button)
        
        controls_layout.addStretch()
        
        # Volume control
        volume_label = QLabel("Volume:")
        controls_layout.addWidget(volume_label)
        
        self._volume_slider = QSlider(Qt.Orientation.Horizontal)
        self._volume_slider.setMinimum(0)
        self._volume_slider.setMaximum(100)
        self._volume_slider.setValue(50)
        self._volume_slider.setMaximumWidth(150)
        controls_layout.addWidget(self._volume_slider)
        
        self._volume_label = QLabel("50%")
        self._volume_label.setMinimumWidth(40)
        controls_layout.addWidget(self._volume_label)
        
        layout.addLayout(controls_layout)
        
    def _connect_signals(self) -> None:
        """Connect internal signals."""
        self._play_button.clicked.connect(self.play_clicked.emit)
        self._pause_button.clicked.connect(self.pause_clicked.emit)
        self._stop_button.clicked.connect(self.stop_clicked.emit)
        
        self._progress_slider.sliderPressed.connect(self._on_slider_pressed)
        self._progress_slider.sliderReleased.connect(self._on_slider_released)
        self._progress_slider.valueChanged.connect(self._on_slider_value_changed)
        
        self._volume_slider.valueChanged.connect(self._on_volume_changed)
        
    def _on_slider_pressed(self) -> None:
        """Handle progress slider press."""
        self._seeking = True
        
    def _on_slider_released(self) -> None:
        """Handle progress slider release."""
        self._seeking = False
        if self._duration > 0:
            position = (self._progress_slider.value() / 1000.0) * self._duration
            self.seek_requested.emit(position)
            
    def _on_slider_value_changed(self, value: int) -> None:
        """Handle progress slider value change."""
        if self._seeking and self._duration > 0:
            position = (value / 1000.0) * self._duration
            from utils.formatters import format_time
            self._time_label.setText(format_time(position))
            
    def _on_volume_changed(self, value: int) -> None:
        """Handle volume slider change."""
        self._volume_label.setText(f"{value}%")
        self.volume_changed.emit(value)
        
    def set_media_loaded(self, loaded: bool) -> None:
        """
        Enable/disable controls based on media loaded state.
        
        Args:
            loaded: True if media is loaded, False otherwise
        """
        self._play_button.setEnabled(loaded)
        self._pause_button.setEnabled(loaded)
        self._stop_button.setEnabled(loaded)
        self._progress_slider.setEnabled(loaded)
        
    def set_playing_state(self, is_playing: bool, is_paused: bool) -> None:
        """
        Update button states based on playback state.
        
        Args:
            is_playing: True if media is playing
            is_paused: True if media is paused
        """
        if is_playing and not is_paused:
            self._play_button.setEnabled(False)
            self._pause_button.setEnabled(True)
        elif is_paused:
            self._play_button.setEnabled(True)
            self._pause_button.setEnabled(False)
        else:
            self._play_button.setEnabled(True)
            self._pause_button.setEnabled(False)
            
    def update_position(self, position: float, duration: float) -> None:
        """
        Update the progress bar and time displays.
        
        Args:
            position: Current position in seconds
            duration: Total duration in seconds
        """
        from utils.formatters import format_time
        
        self._duration = duration
        
        if not self._seeking:
            self._time_label.setText(format_time(position))
            
            if duration > 0:
                progress = int((position / duration) * 1000)
                self._progress_slider.setValue(progress)
            else:
                self._progress_slider.setValue(0)
                
        self._duration_label.setText(format_time(duration))
        
    def set_volume(self, volume: int) -> None:
        """
        Set the volume slider position.
        
        Args:
            volume: Volume level (0-100)
        """
        self._volume_slider.setValue(volume)
        self._volume_label.setText(f"{volume}%")
        
    def get_volume(self) -> int:
        """
        Get the current volume slider value.
        
        Returns:
            Volume level (0-100)
        """
        return self._volume_slider.value()
