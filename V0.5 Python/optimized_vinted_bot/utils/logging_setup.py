"""
Advanced logging setup for the Vinted bot
"""

import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Optional

try:
    from ..config.settings import settings
except ImportError:
    # Fallback for direct execution
    import sys
    from pathlib import Path
    PROJECT_ROOT = Path(__file__).parent.parent
    sys.path.insert(0, str(PROJECT_ROOT))
    from config.settings import settings

class ColoredFormatter(logging.Formatter):
    """Colored formatter for console output"""
    
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
        'RESET': '\033[0m'        # Reset
    }
    
    def format(self, record):
        # Add color to levelname
        if hasattr(record, 'levelname'):
            color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
            record.levelname = f"{color}{record.levelname}{self.COLORS['RESET']}"
            
        return super().format(record)

def setup_logging(
    level: Optional[str] = None,
    log_file: Optional[str] = None,
    console_output: bool = True,
    colored_output: bool = True
):
    """
    Setup comprehensive logging for the application
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file
        console_output: Whether to output to console
        colored_output: Whether to use colored output in console
    """
    
    # Use settings if not provided
    level = level or settings.logging.level
    log_file = log_file or settings.logging.file_path
    
    # Convert string level to logging constant
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    
    # Remove existing handlers
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
        
    # Set root level
    root_logger.setLevel(numeric_level)
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        fmt=settings.logging.format,
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    console_formatter = ColoredFormatter(
        fmt='%(asctime)s - %(name)-20s - %(levelname)-8s - %(message)s',
        datefmt='%H:%M:%S'
    ) if colored_output else logging.Formatter(
        fmt='%(asctime)s - %(name)-20s - %(levelname)-8s - %(message)s',
        datefmt='%H:%M:%S'
    )
    
    # Console handler
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(numeric_level)
        console_handler.setFormatter(console_formatter)
        root_logger.addHandler(console_handler)
        
    # File handler with rotation
    if log_file:
        # Ensure log directory exists
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.handlers.RotatingFileHandler(
            filename=log_file,
            maxBytes=settings.logging.max_file_size,
            backupCount=settings.logging.backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(numeric_level)
        file_handler.setFormatter(detailed_formatter)
        root_logger.addHandler(file_handler)
        
    # Create specific loggers for different components
    _setup_component_loggers(numeric_level)
    
    # Log the setup
    logger = logging.getLogger(__name__)
    logger.info(f"Logging setup complete - Level: {level}, File: {log_file}")
    
def _setup_component_loggers(level: int):
    """Setup loggers for specific components"""
    
    # Component loggers with specific configurations
    components = [
        'optimized_vinted_bot.core.proxy_manager',
        'optimized_vinted_bot.core.vinted_api',
        'optimized_vinted_bot.core.database',
        'optimized_vinted_bot.discord_bot.bot',
        'aiohttp.access',
        'discord',
        'urllib3.connectionpool',
    ]
    
    for component in components:
        logger = logging.getLogger(component)
        logger.setLevel(level)
        
        # Set specific levels for noisy libraries
        if component in ['aiohttp.access', 'urllib3.connectionpool']:
            logger.setLevel(logging.WARNING)
        elif component == 'discord':
            logger.setLevel(logging.INFO)
            
class ContextFilter(logging.Filter):
    """Add context information to log records"""
    
    def filter(self, record):
        # Add custom fields to the record
        record.bot_version = "2.0.0"
        return True

def get_logger(name: str, context: Optional[dict] = None) -> logging.Logger:
    """
    Get a logger with optional context
    
    Args:
        name: Logger name
        context: Additional context to include in logs
        
    Returns:
        Configured logger
    """
    logger = logging.getLogger(name)
    
    if context:
        # Add context filter
        context_filter = ContextFilter()
        for key, value in context.items():
            setattr(context_filter, key, value)
        logger.addFilter(context_filter)
        
    return logger

def log_system_info():
    """Log system information at startup"""
    import platform
    import sys
    import psutil
    
    logger = logging.getLogger(__name__)
    
    logger.info("="*50)
    logger.info("SYSTEM INFORMATION")
    logger.info("="*50)
    logger.info(f"Python Version: {sys.version}")
    logger.info(f"Platform: {platform.platform()}")
    logger.info(f"Architecture: {platform.machine()}")
    logger.info(f"Processor: {platform.processor()}")
    
    # Memory info
    memory = psutil.virtual_memory()
    logger.info(f"Total Memory: {memory.total / (1024**3):.1f} GB")
    logger.info(f"Available Memory: {memory.available / (1024**3):.1f} GB")
    
    # Disk info
    disk = psutil.disk_usage('/')
    logger.info(f"Disk Space: {disk.free / (1024**3):.1f} GB free of {disk.total / (1024**3):.1f} GB")
    
    logger.info("="*50)

class LoggingMixin:
    """Mixin class to add logging capabilities to any class"""
    
    @property
    def logger(self):
        """Get logger for this class"""
        if not hasattr(self, '_logger'):
            self._logger = logging.getLogger(f"{self.__class__.__module__}.{self.__class__.__name__}")
        return self._logger
        
    def log_method_call(self, method_name: str, **kwargs):
        """Log a method call with parameters"""
        params = ", ".join(f"{k}={v}" for k, v in kwargs.items())
        self.logger.debug(f"Calling {method_name}({params})")
        
    def log_performance(self, operation: str, duration: float):
        """Log performance metrics"""
        self.logger.info(f"Performance: {operation} completed in {duration:.3f}s")

# Specific logger configurations for external libraries
def configure_external_loggers():
    """Configure logging for external libraries"""
    
    # Reduce verbosity of HTTP libraries
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("aiohttp").setLevel(logging.WARNING)
    logging.getLogger("aiohttp.access").setLevel(logging.WARNING)
    
    # Discord.py logging
    discord_logger = logging.getLogger("discord")
    discord_logger.setLevel(logging.INFO)
    
    # SQLite logging
    logging.getLogger("sqlite3").setLevel(logging.WARNING)
    
def setup_error_tracking():
    """Setup error tracking and alerting"""
    
    class ErrorTracker(logging.Handler):
        """Custom handler to track errors"""
        
        def __init__(self):
            super().__init__()
            self.error_count = 0
            self.last_errors = []
            self.max_stored_errors = 10
            
        def emit(self, record):
            if record.levelno >= logging.ERROR:
                self.error_count += 1
                error_info = {
                    'timestamp': record.created,
                    'level': record.levelname,
                    'message': record.getMessage(),
                    'module': record.module,
                    'funcName': record.funcName,
                    'lineno': record.lineno
                }
                
                self.last_errors.append(error_info)
                if len(self.last_errors) > self.max_stored_errors:
                    self.last_errors.pop(0)
                    
        def get_error_summary(self):
            """Get summary of recent errors"""
            return {
                'total_errors': self.error_count,
                'recent_errors': self.last_errors
            }
    
    # Add error tracker to root logger
    error_tracker = ErrorTracker()
    logging.getLogger().addHandler(error_tracker)
    
    return error_tracker

# Exception logging decorator
def log_exceptions(logger=None):
    """Decorator to log exceptions in functions"""
    def decorator(func):
        import functools
        
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            log = logger or logging.getLogger(func.__module__)
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                log.error(f"Exception in {func.__name__}: {e}", exc_info=True)
                raise
                
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            log = logger or logging.getLogger(func.__module__)
            try:
                return func(*args, **kwargs)
            except Exception as e:
                log.error(f"Exception in {func.__name__}: {e}", exc_info=True)
                raise
                
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    return decorator

# Import asyncio for the decorator
import asyncio
