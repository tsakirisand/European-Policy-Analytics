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
    "POPULATION": (10000.0, 1000000000.0) # persons
}

class DataValidator:

    @staticmethod
    def validate_observation(record: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Validates an observation record against rules and sanity bounds.
        Returns (is_valid, validation_note).
        """
        period = record.get("period")
        val = record.get("value")
        ind_id = record.get("indicator_id")

        if period is None or period < 1990 or period > 2030:
            return False, f"Period {period} out of expected range [1990-2030]"

        if val is None or not isinstance(val, (int, float)):
            return False, "Value is null or non-numeric"

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
