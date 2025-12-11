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
                'format': self._get_format_string(quality),
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
                'no_check_certificate': True,
                # Prefer formats that work well with QMediaPlayer
                'format_sort': ['res', 'ext:mp4:m4a'],
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
                
                logger.info(f"Successfully extracted: {result['title']} ({result['platform']})")
                return result
                
        except ImportError:
            logger.error("yt-dlp not installed. Cannot extract stream.")
            return None
        except Exception as e:
            logger.error(f"Error extracting stream: {e}")
            return None
    
    def _get_format_string(self, quality: str) -> str:
        """
        Get yt-dlp format string for quality preference
        
        Args:
            quality: Quality preference string
            
        Returns:
            Format string for yt-dlp
        """
        quality_map = {
            'best': 'best',
            'worst': 'worst',
            '2160p': 'bestvideo[height<=2160]+bestaudio/best[height<=2160]',
            '1440p': 'bestvideo[height<=1440]+bestaudio/best[height<=1440]',
            '1080p': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
            '720p': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
            '480p': 'bestvideo[height<=480]+bestaudio/best[height<=480]',
            '360p': 'bestvideo[height<=360]+bestaudio/best[height<=360]',
        }
        
        return quality_map.get(quality.lower(), 'best')
    
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
