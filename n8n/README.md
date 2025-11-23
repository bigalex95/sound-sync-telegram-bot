# ⚡ SoundSync: n8n Workflow

This folder contains the **No-Code** implementation of SoundSync using n8n.

## 🧩 How it Works

Instead of processing the file on our own server, this workflow:

1.  Receives a webhook from Telegram.
2.  Sends the URL to a 3rd Party API (RapidAPI/Cobalt).
3.  Receives the binary file.
4.  Uploads it back to Telegram.

## 🛠 Tools Required

-   **n8n:** Self-hosted or Cloud version.
-   **Telegram Bot Token:** From [@BotFather](https://t.me/botfather).
-   **RapidAPI Key (Optional):** If using a premium downloader API.

## 📥 Import Instructions

1.  **Download the Workflow:**
    -   Locate the `soundsync_workflow.json` file in this folder.
2.  **Import to n8n:**
    -   Open your n8n Editor.
    -   Click "Workflow" (top left) -> "Import from File".
    -   Select `soundsync_workflow.json`.
3.  **Configure Credentials:**
    -   Double click the **Telegram Trigger** node.
    -   Create a new Credential and paste your Bot Token.
    -   Repeat for the **HTTP Request** node if using an API Key.
4.  **Activate:**
    -   Toggle the "Active" switch to ON.

## ⚠️ Limitations

-   File size is limited by the n8n memory and Telegram Bot API (50MB).
-   Dependency on external APIs means if they go down, the bot goes down.
