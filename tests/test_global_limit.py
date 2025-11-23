import unittest
from unittest.mock import AsyncMock, MagicMock
from aiogram import types
from src.handlers.user_handlers import cmd_global_limit
from src.config import Config
from src.services.usage_tracker import UsageTracker

class TestGlobalLimit(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tracker = UsageTracker()
        # Reset DB for testing
        import os
        if os.path.exists(Config.DB_PATH):
            os.remove(Config.DB_PATH)
        self.tracker._init_db()

    async def asyncTearDown(self):
        import os
        if os.path.exists(Config.DB_PATH):
            os.remove(Config.DB_PATH)

    async def test_cmd_global_limit(self):
        # Mock message
        message = AsyncMock(spec=types.Message)
        message.answer = AsyncMock()

        # Test initial state (0 bytes)
        await cmd_global_limit(message)
        
        # Verify response contains correct info
        args, _ = message.answer.call_args
        response_text = args[0]
        self.assertIn("Used: 0.00 B", response_text)

        # Simulate usage (e.g., 150 MB)
        # 150 * 1024 * 1024 = 157286400 bytes
        self.tracker.track_usage(123, 157286400)

        # Test after usage
        await cmd_global_limit(message)
        
        args, _ = message.answer.call_args
        response_text = args[0]
        self.assertIn("Used: 150.00 MB", response_text)

if __name__ == '__main__':
    unittest.main()
