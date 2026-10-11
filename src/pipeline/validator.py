"""
Data Quality Validator.
Applies sanity rules and numerical bounds validation to statistical observations.
"""

from typing import Dict, Any, List, Tuple
import logging
from src.metadata.indicators import get_indicator

logger = logging.getLogger(__name__)

# Sanity range rules per indicator ID
INDICATOR_SANITY_BOUNDS = {
    "UNEMP_RATE": (0.0, 60.0),            # % range
    "YOUTH_UNEMP_RATE": (0.0, 90.0),      # % range
    "HICP_INFLATION": (-20.0, 100.0),     # % range
    "GOV_DEBT_GDP": (0.0, 300.0),         # % of GDP
    "GOV_DEFICIT_GDP": (-50.0, 30.0),     # % of GDP
    "RENEWABLE_ENERGY_SHARE": (0.0, 100.0), # % range
    "POVERTY_RISK_RATE": (0.0, 100.0),    # % range
    "GDP_REAL_GROWTH": (-30.0, 40.0),     # % change
    "LIFE_EXPECTANCY": (40.0, 100.0),     # years
    "POPULATION": (10000.0, 1000000000.0), # persons
    "AVG_FULL_TIME_ADJUSTED_SALARY": (1000.0, 250000.0), # annual salary in EUR
    "MINIMUM_MONTHLY_WAGE": (50.0, 10000.0),             # monthly minimum wage in EUR
    "AVG_NET_ANNUAL_SALARY": (1000.0, 200000.0),         # annual net salary in EUR
    "GDP_PER_CAPITA": (500.0, 300000.0)                  # USD per capita
}

class DataValidator:

    @staticmethod
    def validate_observation(record: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Validates an observation record against rules and sanity bounds.
        Enforces strict separation between salary indicators and GDP per capita.
        Returns (is_valid, validation_note).
        """
        period = record.get("period")
        val = record.get("value")
        ind_id = record.get("indicator_id")
        dataset_code = record.get("dataset_code", "")
        unit = str(record.get("unit", "")).strip()

        if period is None or period < 1990 or period > 2030:
            return False, f"Period {period} out of expected range [1990-2030]"

        if val is None or not isinstance(val, (int, float)):
            return False, "Value is null or non-numeric"

        # Explicit prevention of deprecated or misattributed wage indicators
        if ind_id == "AVG_ANNUAL_WAGE":
            return False, "Deprecated indicator AVG_ANNUAL_WAGE is forbidden; use AVG_FULL_TIME_ADJUSTED_SALARY"

        # Enforce that AVG_FULL_TIME_ADJUSTED_SALARY cannot accidentally use NY.GDP.PCAP.CD
        if ind_id == "AVG_FULL_TIME_ADJUSTED_SALARY":
            if dataset_code == "NY.GDP.PCAP.CD":
                return False, "Source violation: AVG_FULL_TIME_ADJUSTED_SALARY cannot use World Bank NY.GDP.PCAP.CD (GDP per capita)"
            if unit in ["US Dollars", "$", "USD"]:
                return False, "Unit violation: AVG_FULL_TIME_ADJUSTED_SALARY must be in Euros, not US Dollars"
            if dataset_code and dataset_code not in ["nama_10_fte", "UNKNOWN"]:
                return False, f"Source violation: AVG_FULL_TIME_ADJUSTED_SALARY must use Eurostat nama_10_fte, got {dataset_code}"

        # Enforce that GDP_PER_CAPITA cannot use salary datasets
        if ind_id == "GDP_PER_CAPITA":
            if dataset_code in ["nama_10_fte", "earn_mw_cur", "earn_nt_net"]:
                return False, f"Source violation: GDP_PER_CAPITA cannot use wage dataset {dataset_code}"

        # Check domain-specific sanity bounds
        if ind_id in INDICATOR_SANITY_BOUNDS:
            min_b, max_b = INDICATOR_SANITY_BOUNDS[ind_id]
            if val < min_b or val > max_b:
                return False, f"Value {val} out of plausible bounds [{min_b}, {max_b}] for {ind_id}"

        return True, "Valid observation"

    @classmethod
    def filter_and_mark_validations(cls, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Processes list of normalized records, setting 'is_valid' and 'validation_note'.
        """
        validated_records = []
        for r in records:
            is_valid, note = cls.validate_observation(r)
            r["is_valid"] = is_valid
            r["validation_note"] = note
            validated_records.append(r)
        return validated_records
