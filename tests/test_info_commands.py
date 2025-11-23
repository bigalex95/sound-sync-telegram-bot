import unittest
from unittest.mock import AsyncMock
from aiogram import types
from src.handlers.user_handlers import cmd_help, cmd_about

class TestInfoCommands(unittest.IsolatedAsyncioTestCase):
    async def test_cmd_help(self):
        # Mock message
        message = AsyncMock(spec=types.Message)
        message.answer = AsyncMock()

        await cmd_help(message)
        
        # Verify response contains key info
        args, _ = message.answer.call_args
        response_text = args[0]
        self.assertIn("How to use SoundSync Bot", response_text)
        self.assertIn("/my_limit", response_text)

    async def test_cmd_about(self):
        # Mock message
        message = AsyncMock(spec=types.Message)
        message.answer = AsyncMock()

        await cmd_about(message)
        
        # Verify response contains key info
        args, _ = message.answer.call_args
        response_text = args[0]
        self.assertIn("About SoundSync Bot", response_text)
        self.assertIn("GitHub Repository", response_text)

if __name__ == '__main__':
    unittest.main()
