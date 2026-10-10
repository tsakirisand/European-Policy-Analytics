"""
Analytical Engine: Country Comparisons & Rankings.
Handles sorting, ranking, aggregate calculations, and multi-country matrix formatting.
"""

import pandas as pd
from typing import List, Dict, Any, Optional
from src.metadata.indicators import INDICATORS
from src.metadata.countries import COUNTRIES, get_country_name, get_country_flag

def rank_countries(
    df_obs: pd.DataFrame,
    indicator_id: str,
    period: int,
    ascending: Optional[bool] = None
) -> pd.DataFrame:
    """
    Ranks countries for a given indicator and reference period.
    """
    meta = INDICATORS.get(indicator_id, {})
    if ascending is None:
        # Default direction from metadata (lower is better vs higher is better)
        better_dir = meta.get("better_direction", "high")
        ascending = True if better_dir == "low" else False

    # Filter for target period and non-aggregate countries
    df_filtered = df_obs[
        (df_obs["indicator_id"] == indicator_id) &
        (df_obs["period"] == period)
    ].copy()

    if df_filtered.empty:
        return pd.DataFrame()

    # Exclude aggregates from national rankings unless requested
    non_agg_codes = [code for code, c in COUNTRIES.items() if not c["is_aggregate"]]
    df_filtered = df_filtered[df_filtered["country_code"].isin(non_agg_codes)]

    # Sort values
    df_sorted = df_filtered.sort_values(by="value", ascending=ascending).reset_index(drop=True)
    df_sorted["rank"] = df_sorted.index + 1
    df_sorted["country_name"] = df_sorted["country_code"].apply(lambda c: get_country_flag(c) + " " + get_country_name(c))
    
    return df_sorted[["rank", "country_code", "country_name", "value", "unit", "period"]]

def calculate_custom_eu_aggregate(
    df_obs: pd.DataFrame,
    indicator_id: str,
    period: int,
    weight_indicator_id: Optional[str] = "POPULATION"
) -> Optional[float]:
    """
    Calculates weighted average EU aggregate if official series is unavailable.
    """
    df_filtered = df_obs[
        (df_obs["indicator_id"] == indicator_id) &
        (df_obs["period"] == period)
    ]
    if df_filtered.empty:
        return None

    eu_countries = [code for code, c in COUNTRIES.items() if c["is_eu"]]
    df_eu = df_filtered[df_filtered["country_code"].isin(eu_countries)]

    if df_eu.empty:
        return None

    if not weight_indicator_id:
        return df_eu["value"].mean()

    # Get weight observations (e.g. population or GDP)
    df_weights = df_obs[
        (df_obs["indicator_id"] == weight_indicator_id) &
        (df_obs["period"] == period) &
        (df_obs["country_code"].isin(eu_countries))
    ]

    if df_weights.empty:
        return df_eu["value"].mean()

    merged = pd.merge(df_eu, df_weights, on="country_code", suffixes=("", "_weight"))
    if merged.empty or merged["value_weight"].sum() == 0:
        return df_eu["value"].mean()

    weighted_val = (merged["value"] * merged["value_weight"]).sum() / merged["value_weight"].sum()
    return float(weighted_val)
