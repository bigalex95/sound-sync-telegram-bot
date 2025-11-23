#!/bin/bash

# Stop existing containers
echo "Stopping existing containers..."
docker stop sound-sync-telegram-bot watchtower || true
docker rm sound-sync-telegram-bot watchtower || true

# Pull the latest version
echo "Pulling latest image..."
docker pull bigalex95/sound-sync-telegram-bot:latest

# Run the Bot
echo "Starting SoundSync Bot..."
docker run -d \
  --name sound-sync-telegram-bot \
  --restart unless-stopped \
  -v $(pwd)/data:/app/data \
  --env-file .env \
  bigalex95/sound-sync-telegram-bot:latest

# Run Watchtower
echo "Starting Watchtower..."
docker run -d \
  --name watchtower \
  -v /var/run/docker.sock:/var/run/docker.sock \
  containrrr/watchtower \
  --interval 300 \
  --cleanup \
  sound-sync-telegram-bot

echo "Deployment complete! Watchtower is monitoring for updates every 5 minutes."
