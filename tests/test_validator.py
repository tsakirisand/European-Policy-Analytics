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

def test_wage_indicator_rejects_gdp_dataset_and_usd_unit():
    # 1. Rejecting GDP dataset for salary indicator
    bad_source_rec = {
        "period": 2024,
        "value": 45000.0,
        "indicator_id": "AVG_FULL_TIME_ADJUSTED_SALARY",
        "dataset_code": "NY.GDP.PCAP.CD",
        "unit": "Euros per year"
    }
    is_valid, note = DataValidator.validate_observation(bad_source_rec)
    assert is_valid is False
    assert "Source violation" in note
    assert "NY.GDP.PCAP.CD" in note

    # 2. Rejecting US Dollars for salary indicator
    bad_unit_rec = {
        "period": 2024,
        "value": 45000.0,
        "indicator_id": "AVG_FULL_TIME_ADJUSTED_SALARY",
        "dataset_code": "nama_10_fte",
        "unit": "US Dollars"
    }
    is_valid, note = DataValidator.validate_observation(bad_unit_rec)
    assert is_valid is False
    assert "Unit violation" in note

    # 3. Rejecting deprecated AVG_ANNUAL_WAGE
    deprecated_rec = {
        "period": 2024,
        "value": 45000.0,
        "indicator_id": "AVG_ANNUAL_WAGE"
    }
    is_valid, note = DataValidator.validate_observation(deprecated_rec)
    assert is_valid is False
    assert "Deprecated indicator" in note

    # 4. Rejecting salary dataset for GDP_PER_CAPITA
    bad_gdp_rec = {
        "period": 2024,
        "value": 45000.0,
        "indicator_id": "GDP_PER_CAPITA",
        "dataset_code": "nama_10_fte"
    }
    is_valid, note = DataValidator.validate_observation(bad_gdp_rec)
    assert is_valid is False
    assert "Source violation" in note

    # 5. Accepting correct Eurostat nama_10_fte salary record
    good_fte_rec = {
        "period": 2024,
        "value": 53791.0,
        "indicator_id": "AVG_FULL_TIME_ADJUSTED_SALARY",
        "dataset_code": "nama_10_fte",
        "unit": "Euros per year"
    }
    is_valid, note = DataValidator.validate_observation(good_fte_rec)
    assert is_valid is True
    assert note == "Valid observation"

