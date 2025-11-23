# Deploying to Google Cloud Platform (Always Free Tier)

This guide explains how to deploy the **SoundSync Bot** on a Google Cloud Platform (GCP) **Always Free** tier instance.

## Prerequisites

1.  **Google Account**: You need a Google account.
2.  **Credit/Debit Card**: Required for identity verification (you won't be charged if you stay within free tier limits).

---

## Step 1: Create a GCP Project

1.  Go to the [Google Cloud Console](https://console.cloud.google.com/).
2.  Click on the project dropdown at the top left.
3.  Click **New Project**.
4.  Name it `sound-sync-telegram-bot` (or anything you like) and click **Create**.
5.  Select the newly created project.

## Step 2: Create a VM Instance (Always Free)

To stay within the **Always Free** tier, you must select specific settings:

1.  Navigate to **Compute Engine** > **VM instances**.
2.  Click **Create Instance**.
3.  **Name**: `sound-sync-telegram-bot-vm`
4.  **Region**: Choose one of the following (critical for free tier):
    *   `us-west1` (Oregon)
    *   `us-central1` (Iowa)
    *   `us-east1` (South Carolina)
5.  **Zone**: Any zone in the selected region (e.g., `us-central1-a`).
6.  **Machine Configuration**:
    *   **Series**: `E2`
    *   **Machine type**: `e2-micro` (2 vCPU, 1 GB memory)
7.  **Boot Disk**:
    *   Click **Change**.
    *   **Operating System**: `Ubuntu`
    *   **Version**: `Ubuntu 22.04 LTS` (or latest LTS)
    *   **Boot disk type**: `Standard persistent disk`
    *   **Size (GB)**: `30` (Up to 30GB is free).
    *   Click **Select**.
8.  **Firewall**:
    *   Check `Allow HTTP traffic`.
    *   Check `Allow HTTPS traffic`.
9.  Click **Create**.

## Step 3: Connect to the VM

1.  Wait for the instance to start (green checkmark).
2.  Click the **SSH** button next to your instance in the list.
3.  A new browser window will open with a terminal connected to your server.

## Step 4: Install Docker

Run the following commands in the SSH terminal to install Docker:

```bash
# Update package list
sudo apt-get update

# Install Docker
sudo apt-get install -y docker.io

# Start and enable Docker
sudo systemctl start docker
sudo systemctl enable docker

# Add your user to the docker group (to run without sudo)
sudo usermod -aG docker $USER
```

> [!NOTE]
> You may need to close the SSH window and reconnect for the group change to take effect.

## Step 5: Deploy the Bot

Now, follow the standard deployment steps from the [Deployment Guide](deployment.md#part-2-deploy-on-server):

1.  **Create a directory**:
    ```bash
    mkdir -p ~/sound-sync-telegram-bot
    cd ~/sound-sync-telegram-bot
    ```

2.  **Create .env file**:
    ```bash
    nano .env
    ```
    Paste your `BOT_TOKEN=...` inside. Save with `Ctrl+X`, `Y`, `Enter`.

3.  **Run the Bot**:
    ```bash
    docker run -d \
      --name sound-sync-telegram-bot \
      --env-file .env \
      --restart unless-stopped \
      bigalex95/sound-sync-telegram-bot:latest
    ```

## Step 6: Verify

Check if the bot is running:

```bash
docker ps
docker logs -f sound-sync-telegram-bot
```

## Important Notes on Free Tier

*   **Network Egress**: You get 1GB of network egress from North America to all region destinations (excluding China and Australia) per month. Since this is a Telegram bot, bandwidth usage should be low, but keep an eye on it if you process massive files.
*   **CPU Usage**: `e2-micro` instances are burstable. Sustained high CPU usage might be throttled, but it's usually fine for a bot like this.
