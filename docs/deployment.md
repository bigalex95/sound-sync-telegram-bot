# Deployment Guide

This guide covers how to deploy the **SoundSync Bot** using Docker Hub and a Linux server.

## Prerequisites

1.  **Docker Hub Account**: [Sign up here](https://hub.docker.com/).
2.  **Linux Server**: A VPS (e.g., DigitalOcean, AWS, Hetzner) with SSH access.
3.  **Docker Installed**: Both on your local machine and the server.

---

## Part 1: Push to Docker Hub

### 1. Login to Docker Hub
Run this command on your local machine and enter your credentials:
```bash
docker login
```

### 2. Build and Tag the Image
```bash
# Build the image
docker build -t sound-sync-telegram-bot .

# Tag it for Docker Hub
docker tag sound-sync-telegram-bot bigalex95/sound-sync-telegram-bot:latest
```

### 3. Push the Image
```bash
docker push bigalex95/sound-sync-telegram-bot:latest
```

> [!TIP]
> **Do I need to create the repo on Docker Hub first?**
> No! If the repository doesn't exist, Docker Hub will automatically create it as a **Public** repository when you push. If you want it to be **Private**, you should create it on the Docker Hub website first.

---

## Part 2: Deploy on Server

### 1. Connect to your Server
```bash
ssh user@your-server-ip
```

### 2. Install Docker (if not installed)
```bash
# Update package index
sudo apt-get update

# Install Docker
sudo apt-get install -y docker.io

# Start and enable Docker service
sudo systemctl start docker
sudo systemctl enable docker
```

### 3. Prepare Environment
Create a directory for the bot and your `.env` file.
```bash
mkdir -p ~/sound-sync-telegram-bot
cd ~/sound-sync-telegram-bot
nano .env
```
Paste your `BOT_TOKEN` into the `.env` file:
```env
BOT_TOKEN=your_actual_bot_token_here
```
Press `Ctrl+X`, then `Y`, then `Enter` to save.

### 4. Pull and Run
```bash
# Pull the image
sudo docker pull bigalex95/sound-sync-telegram-bot:latest

# Run the container in detached mode (background)
# --restart unless-stopped ensures it restarts if the server reboots or the bot crashes
sudo docker run -d \
  --name sound-sync-telegram-bot \
  --env-file .env \
  --restart unless-stopped \
  bigalex95/sound-sync-telegram-bot:latest
```

### 5. Verify
Check if the bot is running:
```bash
sudo docker ps
```
View logs:
```bash
sudo docker logs -f sound-sync-telegram-bot
```

## Updating the Bot
To update the bot with new code:
1.  **Local**: Rebuild and push (`docker build ...`, `docker push ...`).
2.  **Server**:
    ```bash
    sudo docker pull bigalex95/sound-sync-telegram-bot:latest
    sudo docker stop sound-sync-telegram-bot
    sudo docker rm sound-sync-telegram-bot
    # Run the run command again (see Step 4)
    ```

## Troubleshooting

### "requested access to the resource is denied"
This usually means you are not logged in correctly or don't have permission.
1.  Run `docker logout`.
2.  Run `docker login` and enter your username and password/token again.
3.  Ensure you are pushing to `your-username/repo-name`.

