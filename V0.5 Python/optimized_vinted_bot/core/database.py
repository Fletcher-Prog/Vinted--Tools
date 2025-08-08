"""
Database management for tracking published items and bot state
"""

import sqlite3
import asyncio
import logging
import time
import json
from typing import List, Dict, Optional, Set, Any
from pathlib import Path
from datetime import datetime, timedelta
from dataclasses import asdict

try:
    from .vinted_api import VintedItem
    from ..config.settings import settings
except ImportError:
    # Fallback for direct execution
    import sys
    from pathlib import Path
    PROJECT_ROOT = Path(__file__).parent.parent
    sys.path.insert(0, str(PROJECT_ROOT))
    from core.vinted_api import VintedItem
    from config.settings import settings

class DatabaseManager:
    """SQLite database manager for the bot"""
    
    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or settings.database.file_path
        self.logger = logging.getLogger(__name__)
        
        # Ensure database directory exists
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize database
        self._init_database()
        
    def _init_database(self):
        """Initialize database tables"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Table for published items
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS published_items (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        item_id INTEGER NOT NULL,
                        channel_id INTEGER NOT NULL,
                        search_url TEXT NOT NULL,
                        title TEXT,
                        price TEXT,
                        brand TEXT,
                        size TEXT,
                        user_login TEXT,
                        item_url TEXT,
                        photo_url TEXT,
                        published_at REAL NOT NULL,
                        item_data TEXT,
                        UNIQUE(item_id, channel_id)
                    )
                """)
                
                # Table for search configurations
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS search_configs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        channel_id INTEGER UNIQUE NOT NULL,
                        search_url TEXT NOT NULL,
                        is_active BOOLEAN DEFAULT 1,
                        created_at REAL NOT NULL,
                        last_check REAL,
                        items_found_count INTEGER DEFAULT 0,
                        errors_count INTEGER DEFAULT 0
                    )
                """)
                
                # Table for bot statistics
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS bot_stats (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp REAL NOT NULL,
                        total_requests INTEGER DEFAULT 0,
                        successful_requests INTEGER DEFAULT 0,
                        failed_requests INTEGER DEFAULT 0,
                        items_published INTEGER DEFAULT 0,
                        active_channels INTEGER DEFAULT 0,
                        proxy_stats TEXT
                    )
                """)
                
                # Table for error logs
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS error_logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp REAL NOT NULL,
                        error_type TEXT NOT NULL,
                        error_message TEXT NOT NULL,
                        context TEXT,
                        channel_id INTEGER,
                        search_url TEXT
                    )
                """)
                
                # Create indexes for better performance
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_published_items_item_id ON published_items(item_id)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_published_items_channel_id ON published_items(channel_id)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_published_items_published_at ON published_items(published_at)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_search_configs_channel_id ON search_configs(channel_id)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_bot_stats_timestamp ON bot_stats(timestamp)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_error_logs_timestamp ON error_logs(timestamp)")
                
                conn.commit()
                self.logger.info("Database initialized successfully")
                
        except sqlite3.Error as e:
            self.logger.error(f"Database initialization error: {e}")
            raise
            
    def add_search_config(self, channel_id: int, search_url: str) -> bool:
        """Add or update search configuration for a channel"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT OR REPLACE INTO search_configs 
                    (channel_id, search_url, is_active, created_at, last_check)
                    VALUES (?, ?, 1, ?, NULL)
                """, (channel_id, search_url, time.time()))
                
                conn.commit()
                self.logger.info(f"Added search config for channel {channel_id}")
                return True
                
        except sqlite3.Error as e:
            self.logger.error(f"Error adding search config: {e}")
            return False
            
    def remove_search_config(self, channel_id: int) -> bool:
        """Remove search configuration for a channel"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("DELETE FROM search_configs WHERE channel_id = ?", (channel_id,))
                
                if cursor.rowcount > 0:
                    conn.commit()
                    self.logger.info(f"Removed search config for channel {channel_id}")
                    return True
                else:
                    self.logger.warning(f"No search config found for channel {channel_id}")
                    return False
                    
        except sqlite3.Error as e:
            self.logger.error(f"Error removing search config: {e}")
            return False
            
    def get_search_config(self, channel_id: int) -> Optional[Dict[str, Any]]:
        """Get search configuration for a channel"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT channel_id, search_url, is_active, created_at, 
                           last_check, items_found_count, errors_count
                    FROM search_configs 
                    WHERE channel_id = ?
                """, (channel_id,))
                
                row = cursor.fetchone()
                if row:
                    return {
                        "channel_id": row[0],
                        "search_url": row[1],
                        "is_active": bool(row[2]),
                        "created_at": row[3],
                        "last_check": row[4],
                        "items_found_count": row[5],
                        "errors_count": row[6]
                    }
                    
        except sqlite3.Error as e:
            self.logger.error(f"Error getting search config: {e}")
            
        return None
        
    def get_all_search_configs(self) -> List[Dict[str, Any]]:
        """Get all active search configurations"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT channel_id, search_url, is_active, created_at,
                           last_check, items_found_count, errors_count
                    FROM search_configs 
                    WHERE is_active = 1
                    ORDER BY created_at
                """)
                
                configs = []
                for row in cursor.fetchall():
                    configs.append({
                        "channel_id": row[0],
                        "search_url": row[1],
                        "is_active": bool(row[2]),
                        "created_at": row[3],
                        "last_check": row[4],
                        "items_found_count": row[5],
                        "errors_count": row[6]
                    })
                    
                return configs
                
        except sqlite3.Error as e:
            self.logger.error(f"Error getting search configs: {e}")
            return []
            
    def is_item_published(self, item_id: int, channel_id: int) -> bool:
        """Check if an item has already been published to a channel"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT 1 FROM published_items 
                    WHERE item_id = ? AND channel_id = ?
                """, (item_id, channel_id))
                
                return cursor.fetchone() is not None
                
        except sqlite3.Error as e:
            self.logger.error(f"Error checking if item is published: {e}")
            return False  # Assume not published to avoid duplicates
            
    def mark_item_published(self, item: VintedItem, channel_id: int, search_url: str) -> bool:
        """Mark an item as published to a channel"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Convert item to JSON for storage
                item_data = json.dumps(item.to_dict())
                
                cursor.execute("""
                    INSERT OR IGNORE INTO published_items
                    (item_id, channel_id, search_url, title, price, brand, size,
                     user_login, item_url, photo_url, published_at, item_data)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    item.id, channel_id, search_url, item.title, item.price,
                    item.brand, item.size, item.user_login, item.url,
                    item.photo_url, time.time(), item_data
                ))
                
                conn.commit()
                
                if cursor.rowcount > 0:
                    self.logger.debug(f"Marked item {item.id} as published to channel {channel_id}")
                    return True
                else:
                    self.logger.debug(f"Item {item.id} already published to channel {channel_id}")
                    return False
                    
        except sqlite3.Error as e:
            self.logger.error(f"Error marking item as published: {e}")
            return False
            
    def get_published_items_for_channel(self, channel_id: int, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recently published items for a channel"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT item_id, title, price, brand, size, user_login,
                           item_url, photo_url, published_at
                    FROM published_items 
                    WHERE channel_id = ?
                    ORDER BY published_at DESC
                    LIMIT ?
                """, (channel_id, limit))
                
                items = []
                for row in cursor.fetchall():
                    items.append({
                        "item_id": row[0],
                        "title": row[1],
                        "price": row[2],
                        "brand": row[3],
                        "size": row[4],
                        "user_login": row[5],
                        "item_url": row[6],
                        "photo_url": row[7],
                        "published_at": row[8]
                    })
                    
                return items
                
        except sqlite3.Error as e:
            self.logger.error(f"Error getting published items: {e}")
            return []
            
    def update_search_config_stats(self, channel_id: int, items_found: int = 0, error_occurred: bool = False):
        """Update statistics for a search configuration"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                if error_occurred:
                    cursor.execute("""
                        UPDATE search_configs 
                        SET last_check = ?, errors_count = errors_count + 1
                        WHERE channel_id = ?
                    """, (time.time(), channel_id))
                else:
                    cursor.execute("""
                        UPDATE search_configs 
                        SET last_check = ?, items_found_count = items_found_count + ?
                        WHERE channel_id = ?
                    """, (time.time(), items_found, channel_id))
                    
                conn.commit()
                
        except sqlite3.Error as e:
            self.logger.error(f"Error updating search config stats: {e}")
            
    def save_bot_stats(self, stats: Dict[str, Any]):
        """Save bot statistics"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                proxy_stats = json.dumps(stats.get("proxy_stats", {}))
                
                cursor.execute("""
                    INSERT INTO bot_stats
                    (timestamp, total_requests, successful_requests, failed_requests,
                     items_published, active_channels, proxy_stats)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    time.time(),
                    stats.get("total_requests", 0),
                    stats.get("successful_requests", 0),
                    stats.get("failed_requests", 0),
                    stats.get("items_published", 0),
                    stats.get("active_channels", 0),
                    proxy_stats
                ))
                
                conn.commit()
                
        except sqlite3.Error as e:
            self.logger.error(f"Error saving bot stats: {e}")
            
    def log_error(self, error_type: str, error_message: str, context: str = "", 
                  channel_id: Optional[int] = None, search_url: Optional[str] = None):
        """Log an error to the database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO error_logs
                    (timestamp, error_type, error_message, context, channel_id, search_url)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (time.time(), error_type, error_message, context, channel_id, search_url))
                
                conn.commit()
                
        except sqlite3.Error as e:
            self.logger.error(f"Error logging error to database: {e}")
            
    def cleanup_old_data(self, days_to_keep: int = 30):
        """Clean up old data from the database"""
        try:
            cutoff_time = time.time() - (days_to_keep * 24 * 60 * 60)
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Clean old published items
                cursor.execute("DELETE FROM published_items WHERE published_at < ?", (cutoff_time,))
                published_deleted = cursor.rowcount
                
                # Clean old bot stats
                cursor.execute("DELETE FROM bot_stats WHERE timestamp < ?", (cutoff_time,))
                stats_deleted = cursor.rowcount
                
                # Clean old error logs
                cursor.execute("DELETE FROM error_logs WHERE timestamp < ?", (cutoff_time,))
                errors_deleted = cursor.rowcount
                
                conn.commit()
                
                self.logger.info(f"Cleanup: Deleted {published_deleted} published items, "
                               f"{stats_deleted} stat records, {errors_deleted} error logs")
                
        except sqlite3.Error as e:
            self.logger.error(f"Error during cleanup: {e}")
            
    def get_database_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                stats = {}
                
                # Count records in each table
                tables = ["published_items", "search_configs", "bot_stats", "error_logs"]
                for table in tables:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    stats[f"{table}_count"] = cursor.fetchone()[0]
                    
                # Get database file size
                db_file = Path(self.db_path)
                if db_file.exists():
                    stats["database_size_mb"] = db_file.stat().st_size / (1024 * 1024)
                else:
                    stats["database_size_mb"] = 0
                    
                # Get recent activity
                cursor.execute("""
                    SELECT COUNT(*) FROM published_items 
                    WHERE published_at > ?
                """, (time.time() - 24 * 60 * 60,))  # Last 24 hours
                stats["items_published_24h"] = cursor.fetchone()[0]
                
                cursor.execute("""
                    SELECT COUNT(*) FROM error_logs 
                    WHERE timestamp > ?
                """, (time.time() - 24 * 60 * 60,))  # Last 24 hours
                stats["errors_24h"] = cursor.fetchone()[0]
                
                return stats
                
        except sqlite3.Error as e:
            self.logger.error(f"Error getting database stats: {e}")
            return {"error": str(e)}
            
    async def start_cleanup_task(self):
        """Start background cleanup task"""
        self.logger.info("Starting database cleanup task")
        
        while True:
            try:
                # Run cleanup every 24 hours
                await asyncio.sleep(24 * 60 * 60)
                self.cleanup_old_data()
                
            except Exception as e:
                self.logger.error(f"Error in cleanup task: {e}")
                await asyncio.sleep(60 * 60)  # Wait 1 hour before retry
