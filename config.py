import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# Database
DB_PATH = DATA_DIR / "policy_analytics.db"
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", f"sqlite:///{DB_PATH}")

# API Settings & Timeouts
DEFAULT_TIMEOUT = 15  # seconds
MAX_RETRIES = 3
BACKOFF_FACTOR = 1.0

# Data Freshness / Caching (seconds)
CACHE_TTL_DEFAULT = 86400  # 24 hours

# Official Source Base URLs
EUROSTAT_API_BASE = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data"
WORLD_BANK_API_BASE = "https://api.worldbank.org/v2"
ECB_SDMX_BASE = "https://data-api.ecb.europa.eu/service/data"
OECD_API_BASE = "https://stats.oecd.org/SDMX-JSON/data"

# Application Details
APP_NAME = "European Policy Analytics"
APP_VERSION = "1.0.0"
DEFAULT_REFERENCE_YEAR = 2023
