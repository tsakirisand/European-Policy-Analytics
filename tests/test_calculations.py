"""
Unit tests for Analytical Calculations Engine.
"""

import pytest
import math
import pandas as pd
from src.analytics.calculations import (
    calculate_percentage_change, calculate_percentage_point_change, calculate_cagr, calculate_series_summary
)

def test_percentage_change():
    # Regular positive growth
    assert calculate_percentage_change(100.0, 110.0) == 10.0
    # Contraction
    assert calculate_percentage_change(100.0, 90.0) == -10.0
    # Zero starting value -> None (prevent div by zero)
    assert calculate_percentage_change(0.0, 50.0) is None
    # None values
    assert calculate_percentage_change(None, 10.0) is None

def test_percentage_point_change():
    # Unemployment moves from 10% to 12%
    assert calculate_percentage_point_change(10.0, 12.0) == 2.0
    # Debt moves from 160% to 150%
    assert calculate_percentage_point_change(160.0, 150.0) == -10.0
    assert calculate_percentage_point_change(None, 5.0) is None

def test_cagr():
    # 100 to 121 over 2 years -> 10% annual
    cagr = calculate_cagr(100.0, 121.0, 2)
    assert pytest.approx(cagr, 0.01) == 10.0

    # Negative starting value -> None
    assert calculate_cagr(-50.0, 100.0, 5) is None
    # Zero periods -> None
    assert calculate_cagr(100.0, 150.0, 0) is None

def test_series_summary():
    df = pd.DataFrame({"value": [10.0, 12.0, 15.0]})
    summary = calculate_series_summary(df)
    assert summary["latest"] == 15.0
    assert summary["min"] == 10.0
    assert summary["max"] == 15.0
    assert summary["mean"] == 12.333333333333334
    assert summary["yoy_pp_change"] == 3.0
