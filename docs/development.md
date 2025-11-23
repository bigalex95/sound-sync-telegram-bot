# Development Guide

## Local Setup

### Prerequisites
- Python 3.11+
- FFmpeg installed (`sudo apt install ffmpeg` on Ubuntu)

### Installation

1.  **Clone the repository** (if you haven't already).
2.  **Create a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configuration**:
    - Copy `.env.example` to `.env`.
    - Set your `BOT_TOKEN`.

### Running Locally
```bash
python main.py
```

## Project Structure

- `src/handlers`: Contains bot command and message handlers.
- `src/services`: Core logic (Downloader, Cleaner).
- `src/utils`: Helper functions.
- `main.py`: Entry point.
