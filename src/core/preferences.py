"""
Simple JSON-based preferences manager
Stores user preferences in settings.json
"""

import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class Preferences:
    """
    Manages application preferences using a JSON file
    
    Settings stored:
    - last_directory: Last opened file directory
    - theme: Current theme ("dark" or "light")
    - volume: Volume level (0-100)
    """
    
    # Default settings
    DEFAULTS = {
        "last_directory": "",
        "theme": "dark",
        "volume": 100
    }
    
    def __init__(self, settings_file: Path = None):
        """
        Initialize preferences manager
        
        Args:
            settings_file: Path to settings.json (defaults to project root)
        """
        if settings_file is None:
            # Store in project root directory
            project_root = Path(__file__).parent.parent.parent
            settings_file = project_root / "settings.json"
        
        self.settings_file = settings_file
        self.settings = self._load_settings()
    
    def _load_settings(self) -> dict:
        """Load settings from JSON file"""
        try:
            if self.settings_file.exists():
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                logger.info(f"Loaded settings from {self.settings_file}")
                # Merge with defaults (in case new settings added)
                return {**self.DEFAULTS, **settings}
            else:
                logger.info("No settings file found, using defaults")
                return self.DEFAULTS.copy()
        except Exception as e:
            logger.error(f"Error loading settings: {e}")
            return self.DEFAULTS.copy()
    
    def _save_settings(self):
        """Save settings to JSON file"""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
            logger.debug(f"Settings saved to {self.settings_file}")
        except Exception as e:
            logger.error(f"Error saving settings: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a setting value"""
        return self.settings.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set a setting value and save"""
        self.settings[key] = value
        self._save_settings()
    
    # Convenience methods for specific settings
    
    def get_last_directory(self) -> str:
        """Get last opened directory"""
        return self.get("last_directory", "")
    
    def set_last_directory(self, directory: str):
        """Set last opened directory"""
        self.set("last_directory", directory)
    
    def get_theme(self) -> str:
        """Get theme ("dark" or "light")"""
        return self.get("theme", "dark")
    
    def set_theme(self, theme: str):
        """Set theme"""
        self.set("theme", theme)
    
    def get_volume(self) -> int:
        """Get volume level (0-100)"""
        return self.get("volume", 100)
    
    def set_volume(self, volume: int):
        """Set volume level"""
        self.set("volume", volume)
