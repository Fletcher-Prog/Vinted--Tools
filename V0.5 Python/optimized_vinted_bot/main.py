"""
Main entry point for the Optimized Vinted Discord Bot
"""

import asyncio
import signal
import sys
import os
from pathlib import Path

# Add the project root to Python path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from utils.logging_setup import setup_logging, log_system_info, configure_external_loggers
from discord_bot.bot import VintedDiscordBot
from config.settings import settings

import logging

class BotRunner:
    """Main bot runner with graceful shutdown handling"""
    
    def __init__(self):
        self.bot = None
        self.running = True
        
    async def start(self):
        """Start the bot with proper initialization"""
        
        # Setup logging
        setup_logging()
        configure_external_loggers()
        
        logger = logging.getLogger(__name__)
        logger.info("Starting Optimized Vinted Discord Bot v2.0")
        
        # Log system information
        log_system_info()
        
        # Validate configuration
        if not self._validate_config():
            logger.error("Configuration validation failed!")
            return False
            
        try:
            # Initialize and start bot
            self.bot = VintedDiscordBot()
            
            # Setup signal handlers for graceful shutdown
            self._setup_signal_handlers()
            
            # Start the bot
            await self.bot.start()
            
        except KeyboardInterrupt:
            logger.info("Received keyboard interrupt")
        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)
        finally:
            await self._cleanup()
            
        return True
        
    def _validate_config(self) -> bool:
        """Validate configuration before starting"""
        logger = logging.getLogger(__name__)
        
        # Check Discord token
        if not settings.discord.token:
            logger.error("Discord bot token is required! Set DISCORD_BOT_TOKEN environment variable.")
            return False
            
        # Check proxy configuration
        if settings.proxy.enabled:
            proxy_file = Path(settings.proxy.proxy_list_file)
            if not proxy_file.exists():
                logger.warning(f"Proxy file not found: {proxy_file}")
                logger.warning("Bot will run without proxy rotation")
                settings.proxy.enabled = False
                
        # Create required directories
        for directory in [settings.LOGS_DIR, settings.DATA_DIR]:
            directory.mkdir(parents=True, exist_ok=True)
            
        logger.info("Configuration validation passed")
        return True
        
    def _setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown"""
        if sys.platform != "win32":
            # Unix-like systems
            loop = asyncio.get_event_loop()
            
            for sig in [signal.SIGTERM, signal.SIGINT]:
                loop.add_signal_handler(
                    sig, lambda: asyncio.create_task(self._shutdown())
                )
        else:
            # Windows
            signal.signal(signal.SIGINT, self._signal_handler)
            signal.signal(signal.SIGTERM, self._signal_handler)
            
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals on Windows"""
        asyncio.create_task(self._shutdown())
        
    async def _shutdown(self):
        """Graceful shutdown"""
        logger = logging.getLogger(__name__)
        logger.info("Initiating graceful shutdown...")
        
        self.running = False
        
        if self.bot:
            await self.bot.stop()
            
    async def _cleanup(self):
        """Cleanup resources"""
        logger = logging.getLogger(__name__)
        logger.info("Cleaning up resources...")
        
        # Additional cleanup if needed
        logger.info("Cleanup complete")

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = [
        'discord.py',
        'aiohttp',
        'sqlite3'  # Built-in, but let's check
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'discord.py':
                import discord
            elif package == 'aiohttp':
                import aiohttp
            elif package == 'sqlite3':
                import sqlite3
            else:
                __import__(package)
        except ImportError:
            missing_packages.append(package)
            
    if missing_packages:
        print(f"❌ Missing required packages: {', '.join(missing_packages)}")
        print("Please install them using: pip install -r requirements.txt")
        return False
        
    return True

def main():
    """Main entry point"""
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required!")
        sys.exit(1)
        
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
        
    # Create and run bot
    runner = BotRunner()
    
    try:
        # Run the bot
        success = asyncio.run(runner.start())
        
        if success:
            print("✅ Bot stopped successfully")
        else:
            print("❌ Bot failed to start")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
