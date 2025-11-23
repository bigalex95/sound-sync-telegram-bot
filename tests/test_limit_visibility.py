import unittest
from unittest.mock import AsyncMock, MagicMock, patch
from aiogram import types
from src.handlers.user_handlers import cmd_my_limit
from src.config import Config
from src.services.usage_tracker import UsageTracker

class TestLimitVisibility(unittest.IsolatedAsyncioTestCase):
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

    async def test_cmd_my_limit(self):
        # Mock message
        message = AsyncMock(spec=types.Message)
        # Configure mock to return a user object with id
        user = MagicMock()
        user.id = 123
        message.from_user = user
        message.answer = AsyncMock()

        # Test initial state (0 used)
        await cmd_my_limit(message)
        
        # Verify response contains correct info
        args, _ = message.answer.call_args
        response_text = args[0]
        self.assertIn("Used: 0", response_text)
        self.assertIn(f"/{Config.MAX_USERS_DAILY_LIMIT}", response_text)

        # Simulate usage
        self.tracker.track_usage(123, 1000)

        # Test after usage
        await cmd_my_limit(message)
        
        args, _ = message.answer.call_args
        response_text = args[0]
        self.assertIn("Used: 1", response_text)

if __name__ == '__main__':
    unittest.main()
