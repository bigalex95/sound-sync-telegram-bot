import unittest
import os
import time
from src.services.usage_tracker import UsageTracker
from src.config import Config

class TestUsageTracker(unittest.TestCase):
    def setUp(self):
        # Use a temporary database for testing
        self.test_db = "test_bot_data.db"
        Config.DB_PATH = self.test_db
        Config.MAX_USERS_DAILY_LIMIT = 2
        Config.MAX_GLOBAL_MONTHLY_BYTES = 1000
        
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
            
        self.tracker = UsageTracker()

    def tearDown(self):
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_user_limit(self):
        user_id = 123
        
        # 1st download
        self.assertTrue(self.tracker.can_user_download(user_id))
        self.tracker.track_usage(user_id, 100)
        self.assertEqual(self.tracker.get_user_usage(user_id), 1)
        
        # 2nd download
        self.assertTrue(self.tracker.can_user_download(user_id))
        self.tracker.track_usage(user_id, 100)
        self.assertEqual(self.tracker.get_user_usage(user_id), 2)
        
        # 3rd download (should fail)
        self.assertFalse(self.tracker.can_user_download(user_id))

    def test_global_limit(self):
        user_id_1 = 123
        user_id_2 = 456
        
        # Total limit is 1000 bytes
        
        # User 1 downloads 600 bytes
        self.assertTrue(self.tracker.can_global_download())
        self.tracker.track_usage(user_id_1, 600)
        
        # User 2 downloads 300 bytes (Total 900)
        self.assertTrue(self.tracker.can_global_download())
        self.tracker.track_usage(user_id_2, 300)
        
        # User 1 tries to download (Total would be > 1000 if we allowed, but check is before download)
        # Current total is 900 < 1000, so it should return True
        self.assertTrue(self.tracker.can_global_download())
        
        # Simulate a download that pushes it over
        self.tracker.track_usage(user_id_1, 200) # Total 1100
        
        # Now it should fail
        self.assertFalse(self.tracker.can_global_download())

if __name__ == '__main__':
    unittest.main()
