"""
Configuration settings for the Vinted Discord Bot
"""

import os
from dataclasses import dataclass
from typing import List, Optional
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent.parent
CONFIG_DIR = BASE_DIR / "config"
LOGS_DIR = BASE_DIR / "logs"
DATA_DIR = BASE_DIR / "data"

# Create directories if they don't exist
LOGS_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)

@dataclass
class ProxySettings:
    """Proxy configuration settings"""
    enabled: bool = True
    rotation_enabled: bool = True
    max_retries: int = 3
    timeout: int = 10
    health_check_interval: int = 300  # 5 minutes
    proxy_list_file: str = "proxy_list.txt"
    
@dataclass
class VintedAPISettings:
    """Vinted API configuration"""
    base_url: str = "https://www.vinted.com"
    catalog_endpoint: str = "/api/v2/catalog/items"
    item_endpoint: str = "/api/v2/items"
    rate_limit_delay: float = 1.0  # seconds between requests
    max_retries: int = 5
    timeout: int = 30
    
@dataclass
class DiscordSettings:
    """Discord bot configuration"""
    token: str = os.getenv("DISCORD_BOT_TOKEN", "")
    command_prefix: str = "!"
    max_embeds_per_message: int = 10
    
@dataclass
class DatabaseSettings:
    """Database configuration for tracking published items"""
    file_path: str = str(DATA_DIR / "published_items.db")
    max_stored_items: int = 10000
    cleanup_interval: int = 86400  # 24 hours in seconds
    
@dataclass
class LoggingSettings:
    """Logging configuration"""
    level: str = "INFO"
    file_path: str = str(LOGS_DIR / "vinted_bot.log")
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    backup_count: int = 5
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
@dataclass
class MonitoringSettings:
    """Monitoring and health check settings"""
    enabled: bool = True
    health_check_interval: int = 60  # seconds
    metrics_retention_days: int = 7
    alert_threshold_error_rate: float = 0.1  # 10% error rate
    
class Settings:
    """Main settings class"""
    
    def __init__(self):
        self.proxy = ProxySettings()
        self.vinted_api = VintedAPISettings()
        self.discord = DiscordSettings()
        self.database = DatabaseSettings()
        self.logging = LoggingSettings()
        self.monitoring = MonitoringSettings()
        
        # Load environment-specific settings
        self._load_environment_settings()
        
    def _load_environment_settings(self):
        """Load settings from environment variables"""
        
        # Discord settings
        if os.getenv("DISCORD_BOT_TOKEN"):
            self.discord.token = os.getenv("DISCORD_BOT_TOKEN")
            
        # Proxy settings
        if os.getenv("PROXY_ENABLED"):
            self.proxy.enabled = os.getenv("PROXY_ENABLED").lower() == "true"
            
        if os.getenv("PROXY_ROTATION_ENABLED"):
            self.proxy.rotation_enabled = os.getenv("PROXY_ROTATION_ENABLED").lower() == "true"
            
        # API settings
        if os.getenv("VINTED_RATE_LIMIT_DELAY"):
            try:
                self.vinted_api.rate_limit_delay = float(os.getenv("VINTED_RATE_LIMIT_DELAY"))
            except ValueError:
                pass
                
        # Logging level
        if os.getenv("LOG_LEVEL"):
            self.logging.level = os.getenv("LOG_LEVEL").upper()

# Global settings instance
settings = Settings()
