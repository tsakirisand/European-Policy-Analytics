"""
Analytical Engine: Indicators Relationships & Correlation.
Aligns multi-indicator time series across countries and computes Pearson statistical correlation.
"""

import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, Any, Tuple, Optional
from src.metadata.indicators import INDICATORS
from src.metadata.countries import get_country_flag, get_country_name, COUNTRIES

def align_indicators_data(
    df_obs: pd.DataFrame,
    indicator_x: str,
    indicator_y: str,
    period: int,
    exclude_aggregates: bool = True
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Aligns observations of two indicators for a target reference period.
    Computes Pearson correlation coefficient (r), p-value, and R-squared.
    """
    df_x = df_obs[(df_obs["indicator_id"] == indicator_x) & (df_obs["period"] == period)][["country_code", "value"]].rename(columns={"value": "x_value"})
    df_y = df_obs[(df_obs["indicator_id"] == indicator_y) & (df_obs["period"] == period)][["country_code", "value"]].rename(columns={"value": "y_value"})

    if exclude_aggregates:
        non_agg = [c for c, meta in COUNTRIES.items() if not meta["is_aggregate"]]
        df_x = df_x[df_x["country_code"].isin(non_agg)]
        df_y = df_y[df_y["country_code"].isin(non_agg)]

    merged = pd.merge(df_x, df_y, on="country_code").dropna()

    if len(merged) < 3:
        return merged, {"r": 0.0, "p_value": 1.0, "r_squared": 0.0, "count": len(merged)}

    merged["country_label"] = merged["country_code"].apply(lambda c: f"{get_country_flag(c)} {c}")
    merged["country_name"] = merged["country_code"].apply(get_country_name)

    r, p_val = stats.pearsonr(merged["x_value"], merged["y_value"])

    meta_x = INDICATORS.get(indicator_x, {})
    meta_y = INDICATORS.get(indicator_y, {})

    stats_summary = {
        "r": round(float(r), 4),
        "p_value": round(float(p_val), 5),
        "r_squared": round(float(r ** 2), 4),
        "count": len(merged),
        "indicator_x_name": meta_x.get("name", indicator_x),
        "indicator_y_name": meta_y.get("name", indicator_y),
        "indicator_x_unit": meta_x.get("unit_symbol", ""),
        "indicator_y_unit": meta_y.get("unit_symbol", "")
    }

    return merged, stats_summary
