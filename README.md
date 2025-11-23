# SoundSync Bot 🎧

**SoundSync Bot** is a Telegram bot that allows users to download audio from YouTube, SoundCloud, and other platforms, converting them to MP3 with proper metadata and thumbnails.

## Features

- ⬇️ **Download & Convert**: Downloads video/audio and converts to high-quality MP3.
- 🖼️ **Metadata & Thumbnails**: Automatically embeds ID3 tags and album art.
- ⚡ **Asynchronous**: Handles downloads in the background without freezing.
- 🐳 **Docker Ready**: Easy to deploy using Docker.

## Documentation

- [Development Guide](docs/development.md): How to run the bot locally.
- [Deployment Guide](docs/deployment.md): How to push to Docker Hub and deploy on a server.

## Quick Start (Docker)

```bash
# Build
docker build -t sound-sync-telegram-bot .

# Run
docker run --env-file .env bigalex95/sound-sync-telegram-bot
```