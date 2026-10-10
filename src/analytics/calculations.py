"""
Analytical Engine: Statistical and Mathematical Calculations.
Handles YoY change, percentage vs percentage-point change, CAGR, summary metrics,
and safe mathematical operations.
"""

import math
import numpy as np
import pandas as pd
from typing import Optional, Dict, Any, List, Tuple

def calculate_percentage_change(v_start: float, v_end: float) -> Optional[float]:
    """
    Calculates percentage change: ((v_end - v_start) / |v_start|) * 100.
    Handles zero denominators safely.
    """
    if v_start is None or v_end is None:
        return None
    if math.isclose(v_start, 0.0, abs_tol=1e-9):
        return None  # Prevent division by zero
    return ((v_end - v_start) / abs(v_start)) * 100.0

def calculate_percentage_point_change(v_start: float, v_end: float) -> Optional[float]:
    """
    Calculates percentage-point change: v_end - v_start.
    Used for rate indicators (% of GDP, % unemployment, % inflation).
    """
    if v_start is None or v_end is None:
        return None
    return v_end - v_start

def calculate_cagr(v_start: float, v_end: float, num_periods: int) -> Optional[float]:
    """
    Calculates Compound Annual Growth Rate (CAGR): ((v_end / v_start) ^ (1/n) - 1) * 100.
    Requires positive v_start and v_end, and num_periods > 0.
    """
    if v_start is None or v_end is None or num_periods <= 0:
        return None
    if v_start <= 0 or v_end <= 0:
        return None  # CAGR invalid for negative/zero values
    return (((v_end / v_start) ** (1.0 / num_periods)) - 1.0) * 100.0

def calculate_series_summary(df_series: pd.DataFrame, value_col: str = "value") -> Dict[str, Any]:
    """
    Computes standard summary statistics for a numerical time series.
    """
    if df_series.empty or value_col not in df_series.columns:
        return {
            "latest": None,
            "min": None,
            "max": None,
            "mean": None,
            "std": None,
            "yoy_change": None,
            "change_type": "pct"
        }

    valid_vals = df_series[value_col].dropna().sort_values()
    if valid_vals.empty:
        return {"latest": None, "min": None, "max": None, "mean": None}

    latest_val = valid_vals.iloc[-1]
    prev_val = valid_vals.iloc[-2] if len(valid_vals) > 1 else None

    return {
        "latest": latest_val,
        "min": valid_vals.min(),
        "max": valid_vals.max(),
        "mean": valid_vals.mean(),
        "std": valid_vals.std() if len(valid_vals) > 1 else 0.0,
        "prev_val": prev_val,
        "yoy_pct_change": calculate_percentage_change(prev_val, latest_val) if prev_val is not None else None,
        "yoy_pp_change": calculate_percentage_point_change(prev_val, latest_val) if prev_val is not None else None,
    }
