import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Settings:

    # PostgreSQL
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT")
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

    # API
    BASE_URL = "https://api.jikan.moe/v4"
    REQUEST_TIMEOUT = 30
    REQUEST_DELAY = 1  # Delay in seconds between requests to avoid rate limiting
    MAX_PAGES = 40

    # Directories
    PROJECT_ROOT = Path(__file__).resolve().parent.parent
    RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

    @property
    def DATABASE_URL(self):
        return (
            f"postgresql://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/"
            f"{self.POSTGRES_DB}"
        )

settings = Settings()