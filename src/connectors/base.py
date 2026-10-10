"""
Base HTTP API Connector with error handling, rate limiting, and retries.
"""

import time
import logging
import requests
from typing import Optional, Dict, Any
import config

logger = logging.getLogger(__name__)

class BaseConnector:
    """Base API Connector providing resilient HTTP methods."""

    def __init__(self, base_url: str, timeout: int = config.DEFAULT_TIMEOUT):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "European-Policy-Analytics/1.0 (Research Platform)"
        })

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> Optional[Any]:
        """
        Executes an HTTP GET request with retries and exponential backoff.
        """
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}" if endpoint else self.base_url
        
        for attempt in range(1, config.MAX_RETRIES + 1):
            try:
                response = self.session.get(url, params=params, headers=headers, timeout=self.timeout)
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 404:
                    logger.warning(f"Resource not found (404) at {url}")
                    return None
                else:
                    logger.warning(f"API Attempt {attempt} failed with status {response.status_code}: {response.text[:200]}")
            except requests.RequestException as e:
                logger.warning(f"API Attempt {attempt} connection error: {e}")

            if attempt < config.MAX_RETRIES:
                sleep_time = config.BACKOFF_FACTOR * (2 ** (attempt - 1))
                time.sleep(sleep_time)

        logger.error(f"Failed to retrieve data from {url} after {config.MAX_RETRIES} attempts.")
        return None
