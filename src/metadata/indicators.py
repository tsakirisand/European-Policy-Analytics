"""
Catalog of official indicators for European Policy Analytics.
Contains exact metadata, sources, dataset identifiers, units, and calculation methods.
"""

from typing import Dict, TypedDict, List, Optional

class IndicatorMeta(TypedDict):
    id: str
    domain_id: str
    name: str
    short_name: str
    description: str
    unit: str
    unit_symbol: str
    frequency: str  # 'Annual' or 'Monthly' or 'Quarterly'
    source_provider: str  # 'Eurostat', 'ECB', 'World Bank', 'OECD'
    source_dataset_code: str
    source_url: str
    change_type: str  # 'pct' (percentage change) or 'pct_point' (percentage point change)
    better_direction: str  # 'high' (higher is better), 'low' (lower is better), 'neutral'

INDICATORS: Dict[str, IndicatorMeta] = {
    "GDP_REAL_GROWTH": {
        "id": "GDP_REAL_GROWTH",
        "domain_id": "ECON",
        "name": "Real GDP Growth Rate",
        "short_name": "Real GDP Growth",
        "description": "Annual percentage change of real Gross Domestic Product (chain-linked volumes, percentage change on previous period).",
        "unit": "Percentage change",
        "unit_symbol": "%",
        "frequency": "Annual",
        "source_provider": "Eurostat",
        "source_dataset_code": "nama_10_gdp",
        "source_url": "https://ec.europa.eu/eurostat/databrowser/view/nama_10_gdp/default/table",
        "change_type": "pct_point",
        "better_direction": "high"
    },
    "GDP_PC_PPP": {
        "id": "GDP_PC_PPP",
        "domain_id": "PPP",
        "name": "GDP per Capita in Purchasing Power Standards (PPS)",
        "short_name": "GDP per Capita (PPS)",
        "description": "Gross Domestic Product per inhabitant expressed in Purchasing Power Standards (PPS) relative to the EU27 average (EU27=100). Standardized measure of living standards.",
        "unit": "Index (EU27=100)",
        "unit_symbol": "PPS (EU27=100)",
        "frequency": "Annual",
        "source_provider": "Eurostat",
        "source_dataset_code": "nama_10_pc",
        "source_url": "https://ec.europa.eu/eurostat/databrowser/view/nama_10_pc/default/table",
        "change_type": "pct",
        "better_direction": "high"
    },
    "HICP_INFLATION": {
        "id": "HICP_INFLATION",
        "domain_id": "ECON",
        "name": "Harmonised Index of Consumer Prices (HICP) Inflation",
        "short_name": "HICP Inflation",
        "description": "Annual average rate of change in Harmonised Index of Consumer Prices (all-items HICP). Measures consumer price inflation across EU member states.",
        "unit": "Percentage rate",
        "unit_symbol": "%",
        "frequency": "Annual",
        "source_provider": "Eurostat",
        "source_dataset_code": "prc_hicp_aind",
        "source_url": "https://ec.europa.eu/eurostat/databrowser/view/prc_hicp_aind/default/table",
        "change_type": "pct_point",
        "better_direction": "neutral"
    },
    "UNEMP_RATE": {
        "id": "UNEMP_RATE",
        "domain_id": "LABOUR",
        "name": "Total Unemployment Rate",
        "short_name": "Unemployment Rate",
        "description": "Unemployed persons aged 15-74 as a percentage of the total active labor force (EU Labour Force Survey).",
        "unit": "Percentage of labor force",
        "unit_symbol": "%",
        "frequency": "Annual",
        "source_provider": "Eurostat",
        "source_dataset_code": "une_rt_a",
        "source_url": "https://ec.europa.eu/eurostat/databrowser/view/une_rt_a/default/table",
        "change_type": "pct_point",
        "better_direction": "low"
    },
    "YOUTH_UNEMP_RATE": {
        "id": "YOUTH_UNEMP_RATE",
        "domain_id": "LABOUR",
        "name": "Youth Unemployment Rate (Under 25)",
        "short_name": "Youth Unemployment",
        "description": "Unemployed persons under 25 years old as a percentage of the active population aged 15-24.",
        "unit": "Percentage of youth labor force",
        "unit_symbol": "%",
        "frequency": "Annual",
        "source_provider": "Eurostat",
        "source_dataset_code": "une_rt_a",
        "source_url": "https://ec.europa.eu/eurostat/databrowser/view/une_rt_a/default/table",
        "change_type": "pct_point",
        "better_direction": "low"
    },
    "GOV_DEBT_GDP": {
        "id": "GOV_DEBT_GDP",
        "domain_id": "FINANCE_PUB",
        "name": "General Government Gross Debt (% of GDP)",
        "short_name": "Government Debt (% GDP)",
        "description": "Consolidated gross government debt at face value at year-end, expressed as a percentage of Gross Domestic Product.",
        "unit": "Percentage of GDP",
        "unit_symbol": "% of GDP",
        "frequency": "Annual",
        "source_provider": "Eurostat",
        "source_dataset_code": "gov_10dd_edpt1",
        "source_url": "https://ec.europa.eu/eurostat/databrowser/view/gov_10dd_edpt1/default/table",
        "change_type": "pct_point",
        "better_direction": "low"
    },
    "GOV_DEFICIT_GDP": {
        "id": "GOV_DEFICIT_GDP",
        "domain_id": "FINANCE_PUB",
        "name": "General Government Net Lending / Net Borrowing (% of GDP)",
        "short_name": "Fiscal Balance (% GDP)",
        "description": "General government deficit (-) or surplus (+) as a percentage of GDP.",
        "unit": "Percentage of GDP",
        "unit_symbol": "% of GDP",
        "frequency": "Annual",
        "source_provider": "Eurostat",
        "source_dataset_code": "gov_10dd_edpt1",
        "source_url": "https://ec.europa.eu/eurostat/databrowser/view/gov_10dd_edpt1/default/table",
        "change_type": "pct_point",
        "better_direction": "high"
    },
    "POPULATION": {
        "id": "POPULATION",
        "domain_id": "DEMO_SOCIAL",
        "name": "Total Population on 1st January",
        "short_name": "Total Population",
        "description": "Number of persons inhabitating a country on 1 January of the reference year.",
        "unit": "Persons",
        "unit_symbol": "inhabitants",
        "frequency": "Annual",
        "source_provider": "Eurostat",
        "source_dataset_code": "demo_gind",
        "source_url": "https://ec.europa.eu/eurostat/databrowser/view/demo_gind/default/table",
        "change_type": "pct",
        "better_direction": "neutral"
    },
    "RENEWABLE_ENERGY_SHARE": {
        "id": "RENEWABLE_ENERGY_SHARE",
        "domain_id": "ENERGY_ENV",
        "name": "Share of Renewable Energy in Gross Final Energy Consumption",
        "short_name": "Renewable Energy Share",
        "description": "Share of renewable energy sources in total gross energy consumption across heating, cooling, electricity, and transport.",
        "unit": "Percentage of final consumption",
        "unit_symbol": "%",
        "frequency": "Annual",
        "source_provider": "Eurostat",
        "source_dataset_code": "nrg_ind_ren",
        "source_url": "https://ec.europa.eu/eurostat/databrowser/view/nrg_ind_ren/default/table",
        "change_type": "pct_point",
        "better_direction": "high"
    },
    "GHG_EMISSIONS": {
        "id": "GHG_EMISSIONS",
        "domain_id": "ENERGY_ENV",
        "name": "Greenhouse Gas Emissions",
        "short_name": "GHG Emissions",
        "description": "Total emissions of greenhouse gases (including CO2, N2O, CH4, HFCs, PFCs, SF6, NF3) expressed in thousand tonnes of CO2 equivalent.",
        "unit": "Thousand tonnes CO2 equivalent",
        "unit_symbol": "k tonnes CO2eq",
        "frequency": "Annual",
        "source_provider": "Eurostat",
        "source_dataset_code": "env_air_gge",
        "source_url": "https://ec.europa.eu/eurostat/databrowser/view/env_air_gge/default/table",
        "change_type": "pct",
        "better_direction": "low"
    },
    "ECB_POLICY_RATE": {
        "id": "ECB_POLICY_RATE",
        "domain_id": "FINANCE_MON",
        "name": "ECB Main Refinancing Operations Policy Interest Rate",
        "short_name": "ECB Policy Rate",
        "description": "Interest rate set by the European Central Bank Governing Council for key refinancing operations in the Eurozone (time-weighted annual average).",
        "unit": "Percentage per annum",
        "unit_symbol": "% p.a.",
        "frequency": "Annual average (Time-Weighted)",
        "source_provider": "European Central Bank",
        "source_dataset_code": "FM/D.U2.EUR.4F.KR.MRR_RT.LEV",
        "source_url": "https://data.ecb.europa.eu/main-figures/official-interest-rates",
        "change_type": "pct_point",
        "better_direction": "neutral"
    },
    "HOUSEHOLD_LENDING_RATE": {
        "id": "HOUSEHOLD_LENDING_RATE",
        "domain_id": "FINANCE_MON",
        "name": "Bank Interest Rate on Household Loans for House Purchase",
        "short_name": "Mortgage Interest Rate",
        "description": "Average annualized interest rate charged by monetary financial institutions on new loans to households for house purchase.",
        "unit": "Percentage per annum",
        "unit_symbol": "% p.a.",
        "frequency": "Annual average",
        "source_provider": "European Central Bank",
        "source_dataset_code": "MIR/M.DE.B.A2C.A.R.A.2250.EUR.N",
        "source_url": "https://data.ecb.europa.eu/stats/bank-interest-rates",
        "change_type": "pct_point",
        "better_direction": "neutral"
    },
    "AVG_ANNUAL_WAGE": {
        "id": "AVG_ANNUAL_WAGE",
        "domain_id": "LABOUR",
        "name": "Gross Domestic Product per Capita (Current USD)",
        "short_name": "GDP per Capita (USD)",
        "description": "Gross domestic product per capita expressed in current US dollars.",
        "unit": "US Dollars",
        "unit_symbol": "$",
        "frequency": "Annual",
        "source_provider": "World Bank",
        "source_dataset_code": "NY.GDP.PCAP.CD",
        "source_url": "https://api.worldbank.org/v2/indicator/NY.GDP.PCAP.CD",
        "change_type": "pct",
        "better_direction": "high"
    },
    "MINIMUM_MONTHLY_WAGE": {
        "id": "MINIMUM_MONTHLY_WAGE",
        "domain_id": "LABOUR",
        "name": "National Statutory Minimum Monthly Wage",
        "short_name": "Minimum Monthly Wage",
        "description": "National statutory monthly minimum wage expressed in Euros (Eurostat earn_mw_cur). Applies to countries with statutory minimum wages.",
        "unit": "Euros per month",
        "unit_symbol": "€",
        "frequency": "Annual / Bi-annual",
        "source_provider": "Eurostat",
        "source_dataset_code": "earn_mw_cur",
        "source_url": "https://ec.europa.eu/eurostat/databrowser/view/earn_mw_cur/default/table",
        "change_type": "pct",
        "better_direction": "high"
    },
    "AVG_NET_ANNUAL_SALARY": {
        "id": "AVG_NET_ANNUAL_SALARY",
        "domain_id": "LABOUR",
        "name": "Average Net Annual Salary",
        "short_name": "Average Net Salary",
        "description": "Average annual net earnings for a single worker without children earning 100% of average wage (Eurostat earn_nt_net).",
        "unit": "Euros per year",
        "unit_symbol": "€",
        "frequency": "Annual",
        "source_provider": "Eurostat",
        "source_dataset_code": "earn_nt_net",
        "source_url": "https://ec.europa.eu/eurostat/databrowser/view/earn_nt_net/default/table",
        "change_type": "pct",
        "better_direction": "high"
    },
    "POVERTY_RISK_RATE": {
        "id": "POVERTY_RISK_RATE",
        "domain_id": "DEMO_SOCIAL",
        "name": "At-Risk-of-Poverty or Social Exclusion Rate (AROPE)",
        "short_name": "Poverty & Social Exclusion Risk",
        "description": "Share of total population living in households at risk of poverty, severely materially/socially deprived, or living in households with very low work intensity.",
        "unit": "Percentage of population",
        "unit_symbol": "%",
        "frequency": "Annual",
        "source_provider": "Eurostat",
        "source_dataset_code": "ilc_peps01n",
        "source_url": "https://ec.europa.eu/eurostat/databrowser/view/ilc_peps01n/default/table",
        "change_type": "pct_point",
        "better_direction": "low"
    },
    "TRADE_BALANCE_GDP": {
        "id": "TRADE_BALANCE_GDP",
        "domain_id": "TRADE_IND",
        "name": "Trade Balance in Goods (% of GDP)",
        "short_name": "Trade Balance (% GDP)",
        "description": "Net exports of goods and services expressed as a percentage of Gross Domestic Product.",
        "unit": "Percentage of GDP",
        "unit_symbol": "% of GDP",
        "frequency": "Annual",
        "source_provider": "World Bank",
        "source_dataset_code": "NE.RSB.GNFS.ZS",
        "source_url": "https://api.worldbank.org/v2/indicator/NE.RSB.GNFS.ZS",
        "change_type": "pct_point",
        "better_direction": "high"
    },
    "LIFE_EXPECTANCY": {
        "id": "LIFE_EXPECTANCY",
        "domain_id": "DEMO_SOCIAL",
        "name": "Life Expectancy at Birth",
        "short_name": "Life Expectancy",
        "description": "Mean number of years a newborn infant is expected to live under current mortality conditions.",
        "unit": "Years",
        "unit_symbol": "years",
        "frequency": "Annual",
        "source_provider": "World Bank",
        "source_dataset_code": "SP.DYN.LE00.IN",
        "source_url": "https://api.worldbank.org/v2/indicator/SP.DYN.LE00.IN",
        "change_type": "pct",
        "better_direction": "high"
    }
}

def get_indicators_by_domain(domain_id: str) -> List[IndicatorMeta]:
    """Return all indicators belonging to a specific domain."""
    return [ind for ind in INDICATORS.values() if ind["domain_id"] == domain_id]

def get_indicator(indicator_id: str) -> Optional[IndicatorMeta]:
    """Retrieve metadata for a specific indicator by ID."""
    return INDICATORS.get(indicator_id)
