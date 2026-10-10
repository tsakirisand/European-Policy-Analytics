"""
Unit tests for Data Validator.
"""

import pytest
from src.pipeline.validator import DataValidator

def test_valid_observation():
    record = {"period": 2023, "value": 5.2, "indicator_id": "UNEMP_RATE"}
    is_valid, note = DataValidator.validate_observation(record)
    assert is_valid is True

def test_invalid_period():
    record = {"period": 1850, "value": 5.2, "indicator_id": "UNEMP_RATE"}
    is_valid, note = DataValidator.validate_observation(record)
    assert is_valid is False
    assert "out of expected range" in note

def test_outlier_sanity_check():
    # Unemployment rate of 150% is impossible
    record = {"period": 2023, "value": 150.0, "indicator_id": "UNEMP_RATE"}
    is_valid, note = DataValidator.validate_observation(record)
    assert is_valid is False
    assert "out of plausible bounds" in note

def test_null_value():
    record = {"period": 2023, "value": None, "indicator_id": "UNEMP_RATE"}
    is_valid, note = DataValidator.validate_observation(record)
    assert is_valid is False
