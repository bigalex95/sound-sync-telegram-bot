# 🐍 SoundSync: Python Engine

This branch contains the source code for the **Python** implementation of SoundSync. It uses `aiogram` for the Telegram interface and `yt-dlp` for the heavy lifting.

## 🛠 Tech Stack

- **Python 3.11+**
    
- **aiogram 3.x:** Asynchronous Telegram framework.
    
- **yt-dlp:** The command-line media downloader.
    
- **FFmpeg:** Required for audio conversion.
    

## ⚡ Prerequisites

1. **FFmpeg** must be installed on your system.
    
    - _Mac:_ `brew install ffmpeg`
        
    - _Ubuntu:_ `sudo apt install ffmpeg`
        
    - _Windows:_ [Download Here](https://ffmpeg.org/download.html "null") and add to PATH.
        
2. **Telegram Bot Token:** Get one from [@BotFather](https://t.me/botfather "null").
    

## 📥 Installation

1. **Clone this branch:**
    
    ```
    git clone -b feature/python-engine [https://github.com/bigalex95/soundsync.git](https://github.com/bigalex95/soundsync.git)
    cd soundsync
    ```
    
2. **Set up Virtual Environment:**
    
    ```
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
    
3. **Install Dependencies:**
    
    ```
    pip install -r requirements.txt
    ```
    
4. **Configuration:** Rename `.env.example` to `.env` and add your token:
    
    ```
    BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
    ```
    

## 🚀 Running the Bot

```
python src/main.py
```

## 🐳 Docker Support

Don't want to install FFmpeg manually? Use Docker.

```
docker build -t soundsync .
docker run --env-file .env soundsync
```