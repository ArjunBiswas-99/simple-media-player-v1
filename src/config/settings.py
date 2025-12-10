"""Application settings for Simple Media Player."""

from typing import List

# Supported media file formats
SUPPORTED_VIDEO_FORMATS: List[str] = [
    "*.mp4",
    "*.mkv",
    "*.avi",
    "*.mov",
    "*.wmv",
    "*.flv",
    "*.webm",
    "*.m4v",
]

SUPPORTED_AUDIO_FORMATS: List[str] = [
    "*.mp3",
    "*.wav",
    "*.flac",
    "*.m4a",
    "*.aac",
    "*.ogg",
    "*.wma",
]

# Combine all supported formats
ALL_SUPPORTED_FORMATS: List[str] = SUPPORTED_VIDEO_FORMATS + SUPPORTED_AUDIO_FORMATS

# File dialog filter string
FILE_FILTER: str = (
    "Media Files ("
    + " ".join(ALL_SUPPORTED_FORMATS)
    + ");;"
    + "Video Files ("
    + " ".join(SUPPORTED_VIDEO_FORMATS)
    + ");;"
    + "Audio Files ("
    + " ".join(SUPPORTED_AUDIO_FORMATS)
    + ");;"
    + "All Files (*.*)"
)

# Window settings
DEFAULT_WINDOW_WIDTH: int = 960
DEFAULT_WINDOW_HEIGHT: int = 600
MINIMUM_WINDOW_WIDTH: int = 640
MINIMUM_WINDOW_HEIGHT: int = 400

# Player settings
DEFAULT_VOLUME: int = 50  # 0-100
SEEK_STEP_SECONDS: int = 5
VOLUME_STEP: int = 5
