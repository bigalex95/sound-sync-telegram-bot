import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from src.config import Config
from src.handlers import user_handlers

# Configure logging
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

async def main():
    """
    Main entry point for the bot.
    """
    bot = Bot(token=Config.BOT_TOKEN)
    dp = Dispatcher()

    # Include routers
    dp.include_router(user_handlers.router)

    try:
        logging.info("Starting bot polling...")
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Error occurred: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot stopped by user.")
