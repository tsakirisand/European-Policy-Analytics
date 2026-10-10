"""
Data Normalization Module.
Standardizes country codes, reference periods, unit definitions, and deduplicates observations.
"""

from typing import List, Dict, Any
import logging
from src.metadata.countries import normalize_country_code

logger = logging.getLogger(__name__)

class DataNormalizer:

    @staticmethod
    def normalize_observation(record: Dict[str, Any], indicator_id: str) -> Dict[str, Any]:
        """
        Normalizes a single observation record.
        """
        raw_country = record.get("country_code", "")
        iso3 = normalize_country_code(raw_country)
        if not iso3:
            raise ValueError(f"Unknown or unmappable country code: {raw_country}")

        try:
            period = int(record["period"])
        except (KeyError, ValueError, TypeError):
            raise ValueError(f"Invalid period in record: {record.get('period')}")

        try:
            val = float(record["value"])
        except (KeyError, ValueError, TypeError):
            raise ValueError(f"Invalid numerical value: {record.get('value')}")

        unit = str(record.get("unit", "")).strip() or "unit"
        freq = str(record.get("frequency", "Annual")).strip()
        dataset_code = str(record.get("dataset_code", "UNKNOWN")).strip()

        return {
            "country_code": iso3,
            "indicator_id": indicator_id,
            "period": period,
            "value": val,
            "unit": unit,
            "frequency": freq,
            "dataset_code": dataset_code
        }

    @classmethod
    def normalize_and_deduplicate(cls, records: List[Dict[str, Any]], indicator_id: str) -> List[Dict[str, Any]]:
        """
        Normalizes list of observation dicts and deduplicates by (country_code, period),
        keeping the latest reported observation.
        """
        dedup_map: Dict[tuple, Dict[str, Any]] = {}
        error_count = 0

        for r in records:
            try:
                norm = cls.normalize_observation(r, indicator_id)
                key = (norm["country_code"], norm["period"])
                dedup_map[key] = norm  # overwrite with latest
            except ValueError as e:
                error_count += 1
                continue

        if error_count > 0:
            logger.info(f"Normalizer skipped {error_count} records due to validation/format errors.")

        return list(dedup_map.values())
