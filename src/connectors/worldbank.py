"""
World Bank API Data Connector.
Retrieves macroeconomic and social statistics from World Bank Open Data API v2.
"""

import logging
from typing import List, Dict, Any, Optional
from src.connectors.base import BaseConnector
from src.metadata.countries import normalize_country_code, COUNTRIES
import config

logger = logging.getLogger(__name__)

class WorldBankConnector(BaseConnector):
    def __init__(self):
        super().__init__(base_url=config.WORLD_BANK_API_BASE)

    def fetch_indicator(
        self,
        indicator_code: str,
        start_year: int = 2000,
        end_year: int = 2025,
        country_codes: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Fetches indicator observations from World Bank API v2 with robust multi-page pagination.
        If country_codes is provided, queries those specific ISO3 codes.
        Otherwise, queries country/all with pagination across all pages.
        """
        if country_codes:
            valid_codes = [code for code in country_codes if code and not COUNTRIES.get(code, {}).get("is_aggregate", False)]
            geo_param = ";".join(valid_codes) if valid_codes else "all"
        else:
            geo_param = "all"

        endpoint = f"country/{geo_param}/indicator/{indicator_code}"
        
        page = 1
        total_pages = 1
        all_observations = []
        per_page = 1000

        while page <= total_pages:
            params = {
                "date": f"{start_year}:{end_year}",
                "format": "json",
                "per_page": per_page,
                "page": page
            }
            try:
                data = self.get(endpoint, params=params)
                if not data or not isinstance(data, list) or len(data) < 2:
                    logger.warning(f"World Bank indicator {indicator_code} page {page} returned empty response.")
                    break

                meta = data[0]
                if isinstance(meta, dict) and "pages" in meta:
                    total_pages = meta.get("pages", 1)

                obs_page = data[1]
                if obs_page and isinstance(obs_page, list):
                    all_observations.extend(obs_page)

                page += 1
            except Exception as e:
                logger.error(f"Error fetching World Bank page {page} for {indicator_code}: {e}")
                break

        records = []
        for obs in all_observations:
            if not isinstance(obs, dict):
                continue

            val = obs.get("value")
            if val is None or not isinstance(val, (int, float)):
                continue

            country_iso3 = obs.get("countryiso3code")
            if not country_iso3:
                country_iso3 = normalize_country_code(obs.get("country", {}).get("id"))

            normalized_iso3 = normalize_country_code(country_iso3)
            if not normalized_iso3:
                continue

            try:
                period = int(obs.get("date"))
            except (ValueError, TypeError):
                continue

            records.append({
                "country_code": normalized_iso3,
                "period": period,
                "value": float(val),
                "unit": obs.get("indicator", {}).get("value", indicator_code),
                "dataset_code": indicator_code,
                "frequency": "Annual"
            })

        return records

