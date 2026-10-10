"""
OECD SDMX-JSON Data Connector.
Retrieves productivity, real wages, and social indicators from OECD API.
"""

import logging
from typing import List, Dict, Any, Optional
from src.connectors.base import BaseConnector
from src.metadata.countries import normalize_country_code
import config

logger = logging.getLogger(__name__)

class OECDConnector(BaseConnector):
    def __init__(self):
        super().__init__(base_url=config.OECD_API_BASE)

    def fetch_dataset(
        self,
        dataset_code: str,
        params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Fetches dataset from OECD SDMX-JSON REST service.
        """
        endpoint = f"{dataset_code}/all"
        query_params = {"startTime": "2000"}
        if params:
            query_params.update(params)

        data = self.get(endpoint, params=query_params)
        if not data or "dataSets" not in data:
            logger.warning(f"OECD dataset {dataset_code} returned empty response.")
            return []

        # Parse OECD SDMX-JSON
        try:
            records = []
            dataset = data["dataSets"][0]
            series = dataset.get("series", {})
            structure = data.get("structure", {})
            series_dims = structure.get("dimensions", {}).get("series", [])
            obs_dims = structure.get("dimensions", {}).get("observation", [])

            # Find location of location/country dimension
            location_dim_idx = -1
            for idx, dim in enumerate(series_dims):
                if dim.get("id") in ["LOCATION", "COUNTRY", "COU"]:
                    location_dim_idx = idx
                    break

            time_dim = next((d for d in obs_dims if d.get("id") == "TIME_PERIOD"), None)

            if location_dim_idx == -1 or not time_dim:
                return []

            time_values = [v["id"] for v in time_dim.get("values", [])]

            for s_key_str, s_data in series.items():
                indices = [int(i) for i in s_key_str.split(":")]
                if location_dim_idx < len(indices):
                    country_cat_idx = indices[location_dim_idx]
                    country_raw = series_dims[location_dim_idx]["values"][country_cat_idx]["id"]
                    iso3 = normalize_country_code(country_raw)
                    if not iso3:
                        continue

                    observations = s_data.get("observations", {})
                    for time_idx_str, obs_val_list in observations.items():
                        t_idx = int(time_idx_str)
                        if t_idx < len(time_values):
                            try:
                                period = int(str(time_values[t_idx]).split("-")[0])
                            except (ValueError, TypeError):
                                continue

                            if obs_val_list and obs_val_list[0] is not None:
                                records.append({
                                    "country_code": iso3,
                                    "period": period,
                                    "value": float(obs_val_list[0]),
                                    "unit": "Value",
                                    "dataset_code": dataset_code,
                                    "frequency": "Annual"
                                })
            return records
        except Exception as e:
            logger.error(f"Error parsing OECD dataset {dataset_code}: {e}")
            return []
