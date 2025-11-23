import os
from aiogram import Router, F, types
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile
from src.services.downloader import Downloader
from src.services.cleaner import Cleaner
from src.services.usage_tracker import UsageTracker
from src.config import Config
from src.utils.helpers import is_valid_url, is_spotify_url

router = Router()
downloader = Downloader()
usage_tracker = UsageTracker()

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    """
    Handler for /start command.
    """
    await message.answer(
        "👋 Hello! I'm SoundSync Bot.\n\n"
        "Send me a link from YouTube, SoundCloud, etc., and I'll send you the MP3.\n"
        f"Daily Limit: {Config.MAX_USERS_DAILY_LIMIT} songs."
    )

@router.message(F.text == "/my_limit")
async def cmd_my_limit(message: types.Message):
    """
    Handler for /my_limit command.
    """
    user_id = message.from_user.id
    usage_count = usage_tracker.get_user_usage(user_id)
    remaining = Config.MAX_USERS_DAILY_LIMIT - usage_count
    
    await message.answer(
        f"📊 **Daily Limit Status**\n"
        f"Used: {usage_count}/{Config.MAX_USERS_DAILY_LIMIT}\n"
        f"Remaining: {max(0, remaining)}"
    )

@router.message(F.text)
async def handle_url(message: types.Message):
    """
    Handler for text messages (URLs).
    """
    user_id = message.from_user.id
    url = message.text.strip()

    if not is_valid_url(url):
        await message.answer("❌ That doesn't look like a valid URL.")
        return

    if is_spotify_url(url):
        await message.answer(
            "🎵 Spotify links are not fully supported in this MVP.\n"
            "Please use YouTube or SoundCloud links for now."
        )
        return

    # Check Global Limit
    if not usage_tracker.can_global_download():
        await message.answer(
            "⚠️ Service temporarily unavailable.\n"
            "The bot has reached its monthly traffic limit. Please try again next month."
        )
        return

    # Check User Limit
    if not usage_tracker.can_user_download(user_id):
        usage_count = usage_tracker.get_user_usage(user_id)
        await message.answer(
            f"⚠️ You have reached your daily limit ({usage_count}/{Config.MAX_USERS_DAILY_LIMIT}).\n"
            "Please come back tomorrow!"
        )
        return

    # Send initial status
    status_msg = await message.answer("⬇️ Downloading...")

    try:
        # Download and convert
        info = await downloader.download_audio(url)
        file_path = info.get("file_path")
        title = info.get("title")
        duration = info.get("duration")
        thumbnail_url = info.get("thumbnail_url")

        if not file_path or not os.path.exists(file_path):
            await status_msg.edit_text("❌ Failed to process the file.")
            return

        # Update status
        await status_msg.edit_text("⬆️ Uploading...")

        # Track Usage
        file_size = os.path.getsize(file_path)
        usage_tracker.track_usage(user_id, file_size)
        
        # Get updated usage for caption
        usage_count = usage_tracker.get_user_usage(user_id)

        # Send audio
        audio_file = FSInputFile(file_path)
        await message.answer_audio(
            audio=audio_file,
            caption=f"🎧 {title}\n\n📊 Daily Limit: {usage_count}/{Config.MAX_USERS_DAILY_LIMIT}",
            duration=duration,
            thumbnail=FSInputFile(thumbnail_url) if thumbnail_url and os.path.exists(thumbnail_url) else None
        )

        # Cleanup
        await status_msg.delete()
        Cleaner.remove_file(file_path)
        
        # Try to clean up thumbnail if it was downloaded locally (yt-dlp behavior varies)
        # We can implement a more robust cleanup in the Cleaner service if needed

    except Exception as e:
        await status_msg.edit_text(f"❌ An error occurred: {str(e)}")
