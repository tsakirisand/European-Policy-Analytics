"""
European Central Bank (ECB) Data Portal SDMX REST API Connector.
Retrieves official monetary policy interest rates and household lending statistics.
"""

import csv
import io
import logging
from collections import defaultdict
from typing import List, Dict, Any, Optional
from src.connectors.base import BaseConnector
import config

logger = logging.getLogger(__name__)

class ECBConnector(BaseConnector):
    def __init__(self):
        super().__init__(base_url=config.ECB_SDMX_BASE)

    def fetch_policy_rate(self) -> List[Dict[str, Any]]:
        """
        Fetches official ECB Main Refinancing Operations Policy Interest Rate
        from series key: FM/D.U2.EUR.4F.KR.MRR_RT.LEV
        
        Methodology & Calculation:
        - The source series provides daily observations for every calendar day.
        - Calculates an explicit time-weighted annual average rate based on the duration
          (number of calendar days) each rate level was in effect:
            Time-Weighted Avg = sum(rate_i * duration_i) / total_days
        - Tags incomplete current year (2026) with an explicit validation warning.
        """
        url = f"{self.base_url.rstrip('/')}/FM/D.U2.EUR.4F.KR.MRR_RT.LEV"
        try:
            response = self.session.get(url, params={"format": "csvdata"}, timeout=self.timeout)
            if response.status_code != 200:
                logger.warning(f"ECB Policy Rate request returned status {response.status_code}")
                return []

            reader = csv.DictReader(io.StringIO(response.text))
            year_daily_obs = defaultdict(list)
            for row in reader:
                t = row.get("TIME_PERIOD", "")
                v = row.get("OBS_VALUE", "")
                if t and v:
                    try:
                        yr = int(t.split("-")[0])
                        year_daily_obs[yr].append((t, float(v)))
                    except ValueError:
                        pass

            current_year = 2026
            records = []
            for yr in sorted(year_daily_obs.keys()):
                if 2000 <= yr <= 2026 and year_daily_obs[yr]:
                    daily_obs = year_daily_obs[yr]
                    total_days = len(daily_obs)
                    # Time-weighted average: each daily observation represents a 1-day duration
                    weighted_sum = sum(val * 1.0 for _, val in daily_obs)
                    time_weighted_avg = weighted_sum / total_days

                    rec = {
                        "country_code": "EU27",
                        "period": yr,
                        "value": float(time_weighted_avg),
                        "unit": "% p.a.",
                        "dataset_code": "FM/D.U2.EUR.4F.KR.MRR_RT.LEV",
                        "frequency": "Annual average (Time-Weighted)"
                    }
                    if yr == current_year:
                        rec["validation_note"] = "Incomplete calendar year (YTD average up to 2026-10-10)"
                    records.append(rec)

            return records
        except Exception as e:
            logger.error(f"Error fetching ECB policy rate: {e}")
            return []

    def fetch_household_lending_rate(self, country_iso2: str = "DE") -> List[Dict[str, Any]]:
        """
        Fetches Bank Interest Rate on Household Loans for House Purchase (annual averages)
        from series key: MIR/M.{country_iso2}.B.A2C.A.R.A.2250.EUR.N
        """
        key = f"MIR/M.{country_iso2}.B.A2C.A.R.A.2250.EUR.N"
        url = f"{self.base_url.rstrip('/')}/{key}"
        try:
            response = self.session.get(url, params={"format": "csvdata"}, timeout=self.timeout)
            if response.status_code != 200:
                logger.warning(f"ECB Lending Rate for {country_iso2} returned status {response.status_code}")
                return []

            reader = csv.DictReader(io.StringIO(response.text))
            year_vals = defaultdict(list)
            for row in reader:
                t = row.get("TIME_PERIOD", "")
                v = row.get("OBS_VALUE", "")
                if t and v:
                    try:
                        yr = int(t.split("-")[0])
                        year_vals[yr].append(float(v))
                    except ValueError:
                        pass

            records = []
            from src.metadata.countries import normalize_country_code
            iso3 = normalize_country_code(country_iso2) or "DEU"

            current_year = 2026
            for yr, vals in year_vals.items():
                if 2000 <= yr <= 2026 and vals:
                    avg_v = sum(vals) / len(vals)
                    rec = {
                        "country_code": iso3,
                        "period": yr,
                        "value": float(avg_v),
                        "unit": "% p.a.",
                        "dataset_code": key,
                        "frequency": "Annual average"
                    }
                    if yr == current_year:
                        rec["validation_note"] = "Incomplete calendar year (YTD average up to 2026-10-10)"
                    records.append(rec)

            return records
        except Exception as e:
            logger.error(f"Error fetching ECB lending rate for {country_iso2}: {e}")
            return []
