# SoundSync Bot 🎧

**SoundSync Bot** is a Telegram bot that allows users to download audio from YouTube, SoundCloud, and other platforms, converting them to MP3 with proper metadata and thumbnails.

## Features

- ⬇️ **Download & Convert**: Downloads video/audio and converts to high-quality MP3.
- 🖼️ **Metadata & Thumbnails**: Automatically embeds ID3 tags and album art.
- ⚡ **Asynchronous**: Handles downloads in the background without freezing.
- 🐳 **Docker Ready**: Easy to deploy using Docker.

## 🧩 Alternative: n8n Workflow
Prefer a **No-Code** solution? Check out the [n8n implementation](n8n/README.md) in the `n8n/` folder.

## Documentation

- [Development Guide](docs/development.md): How to run the bot locally.
## 🚀 Deployment

### Automated Deployment (GCP + Watchtower)

To enable automatic updates whenever you push to Docker Hub:

1.  **Upload `deploy.sh` and `.env`** to your server.
2.  **Run the deployment script**:
    ```bash
    ./deploy.sh
    ```

This script starts:
- **sound-sync-telegram-bot**: Your telegram bot.
- **Watchtower**: A service that checks for new Docker images every 5 minutes and automatically updates the bot.

Now, whenever you push a new image to Docker Hub (via GitHub Actions), your server will update automatically within a few minutes!
- [Deployment Guide](docs/deployment.md): How to push to Docker Hub and deploy on a server.
- [GCP Free Tier Guide](docs/gcp-free-tier.md): Step-by-step guide for Google Cloud Always Free tier.

## Quick Start (Docker)

```bash
# Build
docker build -t sound-sync-telegram-bot .

# Run
docker run --env-file .env bigalex95/sound-sync-telegram-bot
```