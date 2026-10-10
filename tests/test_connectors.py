"""
Unit tests for API Connectors and Eurostat JSON-stat Multidimensional Indexing.
"""

import pytest
from src.connectors.eurostat import EurostatConnector
from src.connectors.worldbank import WorldBankConnector

def test_eurostat_json_stat_parsing():
    # Mock Eurostat JSON-stat response structure
    mock_data = {
        "id": ["freq", "unit", "sector", "na_item", "geo", "time"],
        "size": [1, 1, 1, 1, 2, 2],
        "dimension": {
            "geo": {"category": {"index": {"DE": 0, "EL": 1}}},
            "time": {"category": {"index": {"2023": 0, "2024": 1}}},
            "unit": {"category": {"label": {"PC_GDP": "Percentage of GDP"}}}
        },
        "value": {
            "0": 62.3,  # DE 2023
            "1": 62.2,  # DE 2024
            "2": 164.3, # EL 2023
            "3": 154.2  # EL 2024
        }
    }

    records = EurostatConnector.parse_json_stat(mock_data, "gov_10dd_edpt1")
    assert len(records) == 4
    
    de_2024 = next(r for r in records if r["country_code"] == "DEU" and r["period"] == 2024)
    el_2024 = next(r for r in records if r["country_code"] == "GRC" and r["period"] == 2024)

    assert de_2024["value"] == 62.2
    assert el_2024["value"] == 154.2

def test_world_bank_parsing():
    wb = WorldBankConnector()
    # Test indicator fetching helper structure
    records = wb.fetch_indicator("NY.GDP.PCAP.CD", 2023, 2024, country_codes=["DEU", "GRC"])
    assert isinstance(records, list)
    if records:
        assert "country_code" in records[0]
        assert "value" in records[0]
        assert "period" in records[0]

def test_world_bank_multi_page_pagination(mocker=None):
    """Verify that WorldBankConnector traverses metadata['pages'] multi-page pagination."""
    from unittest.mock import MagicMock, patch
    wb = WorldBankConnector()

    page1_resp = [
        {"page": 1, "pages": 2, "per_page": 2, "total": 4},
        [
            {"countryiso3code": "DEU", "date": "2023", "value": 54776.76, "indicator": {"value": "GDP per capita"}},
            {"countryiso3code": "FRA", "date": "2023", "value": 44700.14, "indicator": {"value": "GDP per capita"}}
        ]
    ]
    page2_resp = [
        {"page": 2, "pages": 2, "per_page": 2, "total": 4},
        [
            {"countryiso3code": "GRC", "date": "2023", "value": 23343.71, "indicator": {"value": "GDP per capita"}},
            {"countryiso3code": "ESP", "date": "2023", "value": 32670.10, "indicator": {"value": "GDP per capita"}}
        ]
    ]

    with patch.object(wb, "get", side_effect=[page1_resp, page2_resp]):
        records = wb.fetch_indicator("NY.GDP.PCAP.CD", 2023, 2023)
        assert len(records) == 4
        codes = {r["country_code"] for r in records}
        assert codes == {"DEU", "FRA", "GRC", "ESP"}

def test_world_bank_european_country_coverage():
    """Verify that World Bank ingestion retrieves multi-country European coverage beyond AUT and BEL."""
    wb = WorldBankConnector()
    records = wb.fetch_indicator("NY.GDP.PCAP.CD", 2023, 2023, country_codes=["DEU", "FRA", "GRC", "ESP", "ITA"])
    assert len(records) >= 5
    codes = {r["country_code"] for r in records}
    assert {"DEU", "FRA", "GRC", "ESP", "ITA"}.issubset(codes)

