"""
Definitions for the 8 Policy Analytics Domains.
"""

from typing import Dict, TypedDict

class DomainMeta(TypedDict):
    id: str
    name: str
    icon: str
    description: str

DOMAINS: Dict[str, DomainMeta] = {
    "ECON": {
        "id": "ECON",
        "name": "Economy",
        "icon": "📈",
        "description": "Macroeconomic performance, GDP growth, production indices, and overall inflation."
    },
    "LABOUR": {
        "id": "LABOUR",
        "name": "Labour & Income",
        "icon": "💼",
        "description": "Employment, total & youth unemployment rates, labor force participation, and wage indicators."
    },
    "PPP": {
        "id": "PPP",
        "name": "Purchasing Power & Living Standards",
        "icon": "🛒",
        "description": "GDP per capita adjusted for PPP, price level indices, household consumption, and living standards."
    },
    "FINANCE_PUB": {
        "id": "FINANCE_PUB",
        "name": "Public Finances",
        "icon": "🏛️",
        "description": "General government debt, fiscal balance (deficit/surplus), government revenues, and public expenditure."
    },
    "FINANCE_MON": {
        "id": "FINANCE_MON",
        "name": "Financial Conditions",
        "icon": "🏦",
        "description": "Central bank policy rates, household/corporate bank lending rates, credit conditions, and monetary statistics."
    },
    "ENERGY_ENV": {
        "id": "ENERGY_ENV",
        "name": "Energy & Environment",
        "icon": "🌱",
        "description": "Electricity and gas prices, renewable energy shares, greenhouse gas emissions, and energy mix."
    },
    "DEMO_SOCIAL": {
        "id": "DEMO_SOCIAL",
        "name": "Demographics & Social Conditions",
        "icon": "👥",
        "description": "Total population, age dependency ratios, life expectancy, fertility, and poverty/social exclusion metrics."
    },
    "TRADE_IND": {
        "id": "TRADE_IND",
        "name": "Trade & Industry",
        "icon": "🚢",
        "description": "International trade balances, exports, imports, industrial production index, and trade openness."
    }
}
