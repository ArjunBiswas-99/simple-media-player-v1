"""
Network Stream Handler Module

Handles streaming video URLs from multiple platforms including YouTube, Dailymotion,
Vimeo, and other supported sites. Uses yt-dlp for reliable stream extraction.

Supported Platforms:
    - YouTube (youtube.com, youtu.be)
    - Dailymotion (dailymotion.com)
    - Vimeo (vimeo.com)
    - Twitch (twitch.tv)
    - And 1000+ more sites supported by yt-dlp
"""

import logging
import re
from typing import Optional, Dict, Tuple
from enum import Enum

logger = logging.getLogger(__name__)


class StreamPlatform(Enum):
    """Supported streaming platforms"""
    YOUTUBE = "YouTube"
    DAILYMOTION = "Dailymotion"
    VIMEO = "Vimeo"
    TWITCH = "Twitch"
    DIRECT_LINK = "Direct Link"
    UNKNOWN = "Unknown"


class NetworkStreamHandler:
    """
    Handle streaming video URLs from multiple platforms
    
    This class provides URL validation and stream extraction for various
    video hosting platforms. It uses yt-dlp for reliable extraction while
    maintaining a clean interface for the media player.
    """
    
    # URL patterns for platform detection
    PLATFORM_PATTERNS = {
        StreamPlatform.YOUTUBE: [
            r'(https?://)?(www\.)?(youtube\.com|youtu\.be)/',
            r'(https?://)?(m\.)?youtube\.com/',
        ],
        StreamPlatform.DAILYMOTION: [
            r'(https?://)?(www\.)?dailymotion\.com/',
            r'(https?://)?(www\.)?dai\.ly/',
        ],
        StreamPlatform.VIMEO: [
            r'(https?://)?(www\.)?vimeo\.com/',
        ],
        StreamPlatform.TWITCH: [
            r'(https?://)?(www\.)?twitch\.tv/',
        ],
        StreamPlatform.DIRECT_LINK: [
            r'.*\.(mp4|webm|avi|mkv|mov|flv|m4v)(\?.*)?$',
        ]
    }
    
    def __init__(self):
        """Initialize the network stream handler"""
        self._check_ytdlp_available()
    
    def _check_ytdlp_available(self) -> bool:
        """Check if yt-dlp is available"""
        try:
            import yt_dlp
            logger.info("yt-dlp is available")
            return True
        except ImportError:
            logger.error("yt-dlp is not installed. Install with: pip install yt-dlp")
            return False
    
    def validate_url(self, url: str) -> Tuple[bool, StreamPlatform]:
        """
        Validate if URL is a supported streaming URL
        
        Args:
            url: The URL to validate
            
        Returns:
            Tuple of (is_valid, platform)
        """
        if not url or not url.strip():
            return False, StreamPlatform.UNKNOWN
        
        url = url.strip()
        
        # Check each platform pattern
        for platform, patterns in self.PLATFORM_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, url, re.IGNORECASE):
                    logger.info(f"URL validated as {platform.value}: {url}")
                    return True, platform
        
        # Check if it's a general URL (might be supported by yt-dlp)
        if re.match(r'https?://', url, re.IGNORECASE):
            return True, StreamPlatform.UNKNOWN
        
        return False, StreamPlatform.UNKNOWN
    
    def extract_stream_info(self, url: str, quality: str = 'best') -> Optional[Dict]:
        """
        Extract playable stream information from URL
        
        Uses yt-dlp to extract direct stream URLs and metadata from various
        video hosting platforms.
        
        Args:
            url: The video URL to extract from
            quality: Quality preference ('best', 'worst', or specific like '720p')
            
        Returns:
            Dictionary containing:
                - url: Direct stream URL playable by QMediaPlayer
                - title: Video title
                - platform: Platform name
                - duration: Duration in seconds (if available)
                - thumbnail: Thumbnail URL (if available)
            Returns None if extraction fails
        """
        try:
            import yt_dlp
            
            logger.info(f"Extracting stream from: {url}")
            
            # Configure yt-dlp options
            ydl_opts = {
                'format': 'best',  # Simple: just get the best available format
            }
            
            # Extract video information
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                if not info:
                    logger.error("Failed to extract video information")
                    return None
                
                # Build result dictionary
                result = {
                    'url': info.get('url', ''),
                    'title': info.get('title', 'Unknown Title'),
                    'platform': info.get('extractor_key', 'Unknown'),
                    'duration': info.get('duration', 0),
                    'thumbnail': info.get('thumbnail', ''),
                    'webpage_url': info.get('webpage_url', url),
                }
                
                # Debug logging for stream format
                format_id = info.get('format_id', 'unknown')
                vcodec = info.get('vcodec', 'none')
                acodec = info.get('acodec', 'none')
                has_video = vcodec != 'none'
                has_audio = acodec != 'none'
                
                logger.info(f"Successfully extracted: {result['title']} ({result['platform']})")
                logger.info(f"Format ID: {format_id} | Video: {has_video} ({vcodec}) | Audio: {has_audio} ({acodec})")
                
                if not has_video:
                    logger.warning("⚠️  AUDIO-ONLY stream detected! Video will not play.")
                elif not has_audio:
                    logger.warning("⚠️  VIDEO-ONLY stream detected! Audio will not play.")
                
                return result
                
        except ImportError:
            logger.error("yt-dlp not installed. Cannot extract stream.")
            return None
        except Exception as e:
            logger.error(f"Error extracting stream: {e}")
            return None
    
    
    def get_platform_name(self, platform: StreamPlatform) -> str:
        """Get display name for platform"""
        return platform.value
    
    def is_ytdlp_available(self) -> bool:
        """Check if yt-dlp is available"""
        try:
            import yt_dlp
            return True
        except ImportError:
            return False
