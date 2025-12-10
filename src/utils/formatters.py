"""Utility functions for formatting data."""


def format_time(seconds: float) -> str:
    """
    Format seconds into HH:MM:SS or MM:SS format.
    
    Args:
        seconds: Time in seconds
        
    Returns:
        Formatted time string
    """
    if seconds < 0:
        seconds = 0
        
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes:02d}:{secs:02d}"


def parse_time(time_str: str) -> float:
    """
    Parse a time string (HH:MM:SS or MM:SS) into seconds.
    
    Args:
        time_str: Time string to parse
        
    Returns:
        Time in seconds
    """
    try:
        parts = time_str.split(':')
        if len(parts) == 3:
            hours, minutes, seconds = map(int, parts)
            return hours * 3600 + minutes * 60 + seconds
        elif len(parts) == 2:
            minutes, seconds = map(int, parts)
            return minutes * 60 + seconds
        else:
            return 0.0
    except (ValueError, AttributeError):
        return 0.0
