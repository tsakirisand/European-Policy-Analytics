"""
Eurostat API Data Connector.
Retrieves official statistical datasets from Eurostat API dissemination REST service.
Handles multi-dimensional JSON-stat structures with exact dimension stride indexing.
"""

import logging
from typing import List, Dict, Any, Optional
from src.connectors.base import BaseConnector
from src.metadata.countries import normalize_country_code
import config

logger = logging.getLogger(__name__)

class EurostatConnector(BaseConnector):
    def __init__(self):
        super().__init__(base_url=config.EUROSTAT_API_BASE)

    def fetch_dataset(
        self,
        dataset_code: str,
        params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Fetches dataset from Eurostat API and decodes JSON-stat dimensions.
        """
        query_params = {"lang": "en"}
        if params:
            query_params.update(params)

        data = self.get(dataset_code, params=query_params)
        if not data or "dimension" not in data or "value" not in data:
            logger.warning(f"Eurostat dataset {dataset_code} returned empty or invalid response.")
            return []

        return self.parse_json_stat(data, dataset_code)

    @staticmethod
    def parse_json_stat(data: Dict[str, Any], dataset_code: str) -> List[Dict[str, Any]]:
        """
        Parses Eurostat JSON-stat structure with exact stride multipliers.
        """
        dimensions = data.get("dimension", {})
        ids = data.get("id", [])
        sizes = data.get("size", [])
        values = data.get("value", {})

        if "geo" not in dimensions or "time" not in dimensions:
            logger.warning(f"Dataset {dataset_code} missing 'geo' or 'time' dimensions.")
            return []

        geo_pos = ids.index("geo")
        time_pos = ids.index("time")

        geo_categories = dimensions["geo"].get("category", {}).get("index", {})
        time_categories = dimensions["time"].get("category", {}).get("index", {})

        # Unit label if present
        unit_label = "value"
        if "unit" in dimensions:
            unit_cat = dimensions["unit"].get("category", {}).get("label", {})
            if unit_cat:
                unit_label = list(unit_cat.values())[0]

        # Calculate stride multipliers
        strides = [1] * len(sizes)
        for i in range(len(sizes) - 2, -1, -1):
            strides[i] = strides[i + 1] * sizes[i + 1]

        # Compute offset for non-geo, non-time single-category dimensions
        base_offset = 0
        for idx, d_id in enumerate(ids):
            if d_id not in ["geo", "time"]:
                # Default to index 0 of that dimension
                base_offset += 0 * strides[idx]

        records = []
        for geo_code, geo_idx in geo_categories.items():
            iso3 = normalize_country_code(geo_code)
            if not iso3:
                continue

            for time_str, time_idx in time_categories.items():
                try:
                    period = int(str(time_str).split("-")[0])
                except (ValueError, TypeError):
                    continue

                flat_idx = base_offset + geo_idx * strides[geo_pos] + time_idx * strides[time_pos]

                val_key = str(flat_idx)
                if val_key in values:
                    val = values[val_key]
                    if val is not None and isinstance(val, (int, float)):
                        records.append({
                            "country_code": iso3,
                            "period": period,
                            "value": float(val),
                            "unit": unit_label,
                            "dataset_code": dataset_code,
                            "frequency": "Annual" if len(str(time_str)) == 4 else "Other"
                        })

        return records
