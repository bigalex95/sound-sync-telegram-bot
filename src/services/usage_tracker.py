import sqlite3
import time
from datetime import datetime, timezone
from src.config import Config

class UsageTracker:
    def __init__(self):
        self.db_path = Config.DB_PATH
        self._init_db()

    def _init_db(self):
        """Initialize the database and create tables if they don't exist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usage_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                file_size_bytes INTEGER NOT NULL,
                timestamp REAL NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    def _get_start_of_day_timestamp(self):
        """Get the timestamp for the start of the current day (UTC)."""
        now = datetime.now(timezone.utc)
        start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        return start_of_day.timestamp()

    def _get_start_of_month_timestamp(self):
        """Get the timestamp for the start of the current month (UTC)."""
        now = datetime.now(timezone.utc)
        start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        return start_of_month.timestamp()

    def can_user_download(self, user_id: int) -> bool:
        """Check if the user has not exceeded their daily limit."""
        start_of_day = self._get_start_of_day_timestamp()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM usage_logs
            WHERE user_id = ? AND timestamp >= ?
        """, (user_id, start_of_day))
        count = cursor.fetchone()[0]
        conn.close()

        return count < Config.MAX_USERS_DAILY_LIMIT

    def can_global_download(self) -> bool:
        """Check if the global monthly limit has not been exceeded."""
        start_of_month = self._get_start_of_month_timestamp()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT SUM(file_size_bytes) FROM usage_logs
            WHERE timestamp >= ?
        """, (start_of_month,))
        result = cursor.fetchone()[0]
        conn.close()

        total_bytes = result if result else 0
        return total_bytes < Config.MAX_GLOBAL_MONTHLY_BYTES

    def track_usage(self, user_id: int, file_size_bytes: int):
        """Record a download usage."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO usage_logs (user_id, file_size_bytes, timestamp)
            VALUES (?, ?, ?)
        """, (user_id, file_size_bytes, time.time()))
        conn.commit()
        conn.close()

    def get_user_usage(self, user_id: int) -> int:
        """Get the number of downloads for the user today."""
        start_of_day = self._get_start_of_day_timestamp()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM usage_logs
            WHERE user_id = ? AND timestamp >= ?
        """, (user_id, start_of_day))
        count = cursor.fetchone()[0]
        conn.close()
        
        return count

    def get_global_usage(self) -> int:
        """Get the total bytes used by the bot this month."""
        start_of_month = self._get_start_of_month_timestamp()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT SUM(file_size_bytes) FROM usage_logs
            WHERE timestamp >= ?
        """, (start_of_month,))
        result = cursor.fetchone()[0]
        conn.close()
        
        return result if result else 0
