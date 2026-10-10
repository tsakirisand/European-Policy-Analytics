"""
Unit tests for Country ISO Normalization and Data Normalizer.
"""

import pytest
from src.metadata.countries import normalize_country_code, get_country_name, get_eu27_iso3_list
from src.pipeline.normalizer import DataNormalizer

def test_country_code_normalization():
    assert normalize_country_code("EL") == "GRC"
    assert normalize_country_code("UK") == "GBR"
    assert normalize_country_code("DE") == "DEU"
    assert normalize_country_code("GR") == "GRC"
    assert normalize_country_code("Greece") == "GRC"
    assert normalize_country_code("Germany") == "DEU"
    assert normalize_country_code("INVALID_XYZ") is None

def test_country_names():
    assert get_country_name("GRC") == "Greece"
    assert get_country_name("DEU") == "Germany"

def test_eu27_list():
    eu_list = get_eu27_iso3_list()
    assert len(eu_list) == 27
    assert "GRC" in eu_list
    assert "DEU" in eu_list
    assert "GBR" not in eu_list  # Brexit

def test_normalize_observation():
    record = {
        "country_code": "EL",
        "period": "2023",
        "value": "2.5",
        "unit": "%",
        "dataset_code": "nama_10_gdp"
    }
    norm = DataNormalizer.normalize_observation(record, "GDP_REAL_GROWTH")
    assert norm["country_code"] == "GRC"
    assert norm["period"] == 2023
    assert norm["value"] == 2.5
    assert norm["indicator_id"] == "GDP_REAL_GROWTH"

def test_deduplication():
    records = [
        {"country_code": "DE", "period": 2023, "value": 1.0, "unit": "%", "dataset_code": "nama"},
        {"country_code": "DEU", "period": 2023, "value": 1.5, "unit": "%", "dataset_code": "nama"},  # duplicate
    ]
    dedup = DataNormalizer.normalize_and_deduplicate(records, "GDP_REAL_GROWTH")
    assert len(dedup) == 1
    assert dedup[0]["value"] == 1.5
