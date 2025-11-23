import asyncio
import os
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Optional
import yt_dlp

class Downloader:
    """
    Service class to handle audio downloading and conversion using yt-dlp.
    """
    
    def __init__(self, download_dir: str = "downloads"):
        self.download_dir = download_dir
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)
            
        # ThreadPoolExecutor to run blocking yt-dlp code without freezing the bot
        self.executor = ThreadPoolExecutor(max_workers=2)

    async def download_audio(self, url: str) -> Dict[str, str]:
        """
        Downloads audio from the given URL, converts to MP3, and adds metadata.
        Returns a dictionary with file paths and metadata.
        """
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{self.download_dir}/%(title)s.%(ext)s',
            'postprocessors': [
                {
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                },
                {
                    'key': 'EmbedThumbnail',
                },
                {
                    'key': 'FFmpegMetadata',
                }
            ],
            'writethumbnail': True,
            'quiet': True,
            'no_warnings': True,
            # 'restrictfilenames': True, # Optional: to avoid weird characters in filenames
        }

        loop = asyncio.get_running_loop()
        
        try:
            # Run the blocking download in a separate thread
            info = await loop.run_in_executor(
                self.executor, 
                lambda: self._download_sync(url, ydl_opts)
            )
            return info
        except Exception as e:
            raise e

    def _download_sync(self, url: str, opts: dict) -> Dict[str, str]:
        """
        Synchronous wrapper for yt-dlp download.
        """
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
            
            # Construct the expected filename
            # Note: yt-dlp might change the extension to mp3 after post-processing
            filename = ydl.prepare_filename(info)
            base, _ = os.path.splitext(filename)
            mp3_filename = f"{base}.mp3"
            
            # Check if thumbnail exists
            thumbnail_path = None
            # yt-dlp saves thumbnail as .jpg or .webp usually
            # We can try to guess or just let the bot handle if it's missing
            # For simplicity, we return the mp3 path and let the handler deal with sending
            
            return {
                "title": info.get("title", "Unknown Title"),
                "file_path": mp3_filename,
                "thumbnail_url": info.get("thumbnail"),
                "duration": info.get("duration")
            }
