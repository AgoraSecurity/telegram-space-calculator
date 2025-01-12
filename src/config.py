import os

from dotenv import load_dotenv

# Ensure we load environment variables before accessing them
load_dotenv()


class Config:
    API_ID = int(os.getenv("TELEGRAM_API_ID", "0"))  # Convert to int
    API_HASH = os.getenv("TELEGRAM_API_HASH", "")
    SESSION_NAME = "media_analyzer"
    GROUPS_FILE = os.path.join("data", "groups.json")  # Use os.path for compatibility
