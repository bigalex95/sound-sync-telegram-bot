import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """
    Configuration class to hold environment variables and constants.
    """
    BOT_TOKEN = os.getenv("BOT_TOKEN")

    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN is not set in the environment variables.")

    # Usage Limits
    MAX_USERS_DAILY_LIMIT = int(os.getenv("MAX_USERS_DAILY_LIMIT", 5))
    # Default to 1 GB (1024 * 1024 * 1024 bytes)
    MAX_GLOBAL_MONTHLY_BYTES = int(os.getenv("MAX_GLOBAL_MONTHLY_BYTES", 1073741824))
    
    # Database
    DB_PATH = os.getenv("DB_PATH", "data/bot_data.db")
    
    # GCP Monitoring (Optional - for accurate network tracking)
    GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
    GCP_INSTANCE_ID = os.getenv("GCP_INSTANCE_ID")
    GCP_ZONE = os.getenv("GCP_ZONE")
