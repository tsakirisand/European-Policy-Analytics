"""
Centralized registry for European countries and aggregates.
Handles mapping between Eurostat codes, ISO-2, ISO-3, and country names.
"""

from typing import Dict, Optional, List, TypedDict

class CountryMeta(TypedDict):
    code_iso2: str
    code_iso3: str
    code_eurostat: str
    name: str
    flag: str
    region: str
    is_eu: bool
    is_aggregate: bool
    currency: str

COUNTRIES: Dict[str, CountryMeta] = {
    "AUT": {"code_iso2": "AT", "code_iso3": "AUT", "code_eurostat": "AT", "name": "Austria", "flag": "🇦🇹", "region": "Central Europe", "is_eu": True, "is_aggregate": False, "currency": "EUR"},
    "BEL": {"code_iso2": "BE", "code_iso3": "BEL", "code_eurostat": "BE", "name": "Belgium", "flag": "🇧🇪", "region": "Western Europe", "is_eu": True, "is_aggregate": False, "currency": "EUR"},
    "BGR": {"code_iso2": "BG", "code_iso3": "BGR", "code_eurostat": "BG", "name": "Bulgaria", "flag": "🇧🇬", "region": "Eastern Europe", "is_eu": True, "is_aggregate": False, "currency": "BGN"},
    "HRV": {"code_iso2": "HR", "code_iso3": "HRV", "code_eurostat": "HR", "name": "Croatia", "flag": "🇭🇷", "region": "Southern Europe", "is_eu": True, "is_aggregate": False, "currency": "EUR"},
    "CYP": {"code_iso2": "CY", "code_iso3": "CYP", "code_eurostat": "CY", "name": "Cyprus", "flag": "🇨🇾", "region": "Southern Europe", "is_eu": True, "is_aggregate": False, "currency": "EUR"},
    "CZE": {"code_iso2": "CZ", "code_iso3": "CZE", "code_eurostat": "CZ", "name": "Czechia", "flag": "🇨🇿", "region": "Central Europe", "is_eu": True, "is_aggregate": False, "currency": "CZK"},
    "DNK": {"code_iso2": "DK", "code_iso3": "DNK", "code_eurostat": "DK", "name": "Denmark", "flag": "🇩🇰", "region": "Northern Europe", "is_eu": True, "is_aggregate": False, "currency": "DKK"},
    "EST": {"code_iso2": "EE", "code_iso3": "EST", "code_eurostat": "EE", "name": "Estonia", "flag": "🇪🇪", "region": "Northern Europe", "is_eu": True, "is_aggregate": False, "currency": "EUR"},
    "FIN": {"code_iso2": "FI", "code_iso3": "FIN", "code_eurostat": "FI", "name": "Finland", "flag": "🇫🇮", "region": "Northern Europe", "is_eu": True, "is_aggregate": False, "currency": "EUR"},
    "FRA": {"code_iso2": "FR", "code_iso3": "FRA", "code_eurostat": "FR", "name": "France", "flag": "🇫🇷", "region": "Western Europe", "is_eu": True, "is_aggregate": False, "currency": "EUR"},
    "DEU": {"code_iso2": "DE", "code_iso3": "DEU", "code_eurostat": "DE", "name": "Germany", "flag": "🇩🇪", "region": "Central Europe", "is_eu": True, "is_aggregate": False, "currency": "EUR"},
    "GRC": {"code_iso2": "GR", "code_iso3": "GRC", "code_eurostat": "EL", "name": "Greece", "flag": "🇬🇷", "region": "Southern Europe", "is_eu": True, "is_aggregate": False, "currency": "EUR"},
    "HUN": {"code_iso2": "HU", "code_iso3": "HUN", "code_eurostat": "HU", "name": "Hungary", "flag": "🇭🇺", "region": "Central Europe", "is_eu": True, "is_aggregate": False, "currency": "HUF"},
    "IRL": {"code_iso2": "IE", "code_iso3": "IRL", "code_eurostat": "IE", "name": "Ireland", "flag": "🇮🇪", "region": "Western Europe", "is_eu": True, "is_aggregate": False, "currency": "EUR"},
    "ITA": {"code_iso2": "IT", "code_iso3": "ITA", "code_eurostat": "IT", "name": "Italy", "flag": "🇮🇹", "region": "Southern Europe", "is_eu": True, "is_aggregate": False, "currency": "EUR"},
    "LVA": {"code_iso2": "LV", "code_iso3": "LVA", "code_eurostat": "LV", "name": "Latvia", "flag": "🇱🇻", "region": "Northern Europe", "is_eu": True, "is_aggregate": False, "currency": "EUR"},
    "LTU": {"code_iso2": "LT", "code_iso3": "LTU", "code_eurostat": "LT", "name": "Lithuania", "flag": "🇱🇹", "region": "Northern Europe", "is_eu": True, "is_aggregate": False, "currency": "EUR"},
    "LUX": {"code_iso2": "LU", "code_iso3": "LUX", "code_eurostat": "LU", "name": "Luxembourg", "flag": "🇱🇺", "region": "Western Europe", "is_eu": True, "is_aggregate": False, "currency": "EUR"},
    "MLT": {"code_iso2": "MT", "code_iso3": "MLT", "code_eurostat": "MT", "name": "Malta", "flag": "🇲🇹", "region": "Southern Europe", "is_eu": True, "is_aggregate": False, "currency": "EUR"},
    "NLD": {"code_iso2": "NL", "code_iso3": "NLD", "code_eurostat": "NL", "name": "Netherlands", "flag": "🇳🇱", "region": "Western Europe", "is_eu": True, "is_aggregate": False, "currency": "EUR"},
    "POL": {"code_iso2": "PL", "code_iso3": "POL", "code_eurostat": "PL", "name": "Poland", "flag": "🇵🇱", "region": "Central Europe", "is_eu": True, "is_aggregate": False, "currency": "PLN"},
    "PRT": {"code_iso2": "PT", "code_iso3": "PRT", "code_eurostat": "PT", "name": "Portugal", "flag": "🇵🇹", "region": "Southern Europe", "is_eu": True, "is_aggregate": False, "currency": "EUR"},
    "ROU": {"code_iso2": "RO", "code_iso3": "ROU", "code_eurostat": "RO", "name": "Romania", "flag": "🇷🇴", "region": "Eastern Europe", "is_eu": True, "is_aggregate": False, "currency": "RON"},
    "SVK": {"code_iso2": "SK", "code_iso3": "SVK", "code_eurostat": "SK", "name": "Slovakia", "flag": "🇸🇰", "region": "Central Europe", "is_eu": True, "is_aggregate": False, "currency": "EUR"},
    "SVN": {"code_iso2": "SI", "code_iso3": "SVN", "code_eurostat": "SI", "name": "Slovenia", "flag": "🇸🇮", "region": "Southern Europe", "is_eu": True, "is_aggregate": False, "currency": "EUR"},
    "ESP": {"code_iso2": "ES", "code_iso3": "ESP", "code_eurostat": "ES", "name": "Spain", "flag": "🇪🇸", "region": "Southern Europe", "is_eu": True, "is_aggregate": False, "currency": "EUR"},
    "SWE": {"code_iso2": "SE", "code_iso3": "SWE", "code_eurostat": "SE", "name": "Sweden", "flag": "🇸🇪", "region": "Northern Europe", "is_eu": True, "is_aggregate": False, "currency": "SEK"},
    # Non-EU European Countries
    "GBR": {"code_iso2": "GB", "code_iso3": "GBR", "code_eurostat": "UK", "name": "United Kingdom", "flag": "🇬🇧", "region": "Western Europe", "is_eu": False, "is_aggregate": False, "currency": "GBP"},
    "CHE": {"code_iso2": "CH", "code_iso3": "CHE", "code_eurostat": "CH", "name": "Switzerland", "flag": "🇨🇭", "region": "Central Europe", "is_eu": False, "is_aggregate": False, "currency": "CHF"},
    "NOR": {"code_iso2": "NO", "code_iso3": "NOR", "code_eurostat": "NO", "name": "Norway", "flag": "🇳🇴", "region": "Northern Europe", "is_eu": False, "is_aggregate": False, "currency": "NOK"},
    "ISL": {"code_iso2": "IS", "code_iso3": "ISL", "code_eurostat": "IS", "name": "Iceland", "flag": "🇮🇸", "region": "Northern Europe", "is_eu": False, "is_aggregate": False, "currency": "ISK"},
    # Aggregates
    "EU27": {"code_iso2": "EU", "code_iso3": "EU27", "code_eurostat": "EU27_2020", "name": "European Union (EU-27)", "flag": "🇪🇺", "region": "Aggregate", "is_eu": False, "is_aggregate": True, "currency": "EUR"},
    "EA20": {"code_iso2": "EA", "code_iso3": "EA20", "code_eurostat": "EA20", "name": "Euro Area (EA-20)", "flag": "💶", "region": "Aggregate", "is_eu": False, "is_aggregate": True, "currency": "EUR"},
}

# Lookup maps
EUROSTAT_TO_ISO3: Dict[str, str] = {meta["code_eurostat"]: code for code, meta in COUNTRIES.items()}
ISO2_TO_ISO3: Dict[str, str] = {meta["code_iso2"]: code for code, meta in COUNTRIES.items()}
NAME_TO_ISO3: Dict[str, str] = {meta["name"].lower(): code for code, meta in COUNTRIES.items()}

def normalize_country_code(raw_code: str) -> Optional[str]:
    """
    Normalizes any country input (Eurostat code, ISO-2, ISO-3, or Country Name)
    to standard ISO-3 code. Returns None if unknown.
    """
    if not raw_code:
        return None
    cleaned = str(raw_code).strip()
    upper = cleaned.upper()
    
    if upper in COUNTRIES:
        return upper
    if upper in EUROSTAT_TO_ISO3:
        return EUROSTAT_TO_ISO3[upper]
    if upper in ISO2_TO_ISO3:
        return ISO2_TO_ISO3[upper]
    
    lower = cleaned.lower()
    if lower in NAME_TO_ISO3:
        return NAME_TO_ISO3[lower]
        
    return None

def get_country_name(iso3_code: str) -> str:
    """Returns official country name for ISO3 code."""
    meta = COUNTRIES.get(iso3_code)
    return meta["name"] if meta else iso3_code

def get_country_flag(iso3_code: str) -> str:
    """Returns flag emoji for ISO3 code."""
    meta = COUNTRIES.get(iso3_code)
    return meta["flag"] if meta else "🌐"

def get_eu27_iso3_list() -> List[str]:
    """Returns list of ISO3 codes for all 27 EU member states."""
    return [code for code, meta in COUNTRIES.items() if meta["is_eu"]]

def get_all_country_iso3_list(include_aggregates: bool = False) -> List[str]:
    """Returns list of all available country ISO3 codes."""
    return [code for code, meta in COUNTRIES.items() if include_aggregates or not meta["is_aggregate"]]
