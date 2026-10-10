"""
Page 8: Methodology & Analytical Standards.
Comprehensive technical guide detailing calculations, unit definitions, aggregations,
and non-negotiable data integrity rules.
"""

import streamlit as st
from src.ui.components import render_header

def render():
    render_header(
        title="Methodology & Analytical Standards",
        subtitle="Transparent documentation of statistical formulas, data normalization, and analytical boundaries.",
        icon="📐"
    )

    st.markdown("""
        ### 1. Fundamental Calculation Rules

        #### A. Percentage Change vs. Percentage-Point Change
        - **Percentage Change (%):** Used for level indicators (e.g. GDP per capita, Population, Total Wage in Euros).
          $$\\text{Pct Change} = \\left( \\frac{V_t - V_{t-1}}{|V_{t-1}|} \\right) \\times 100\\%$$
          *Safety Check:* If $V_{t-1} = 0$, the calculation is undefined and returned as `None` to prevent infinite values.

        - **Percentage-Point Change (pp):** Used strictly for rate or ratio indicators already expressed in percentages (e.g. Unemployment Rate, Inflation Rate, Government Debt % of GDP).
          $$\\text{Pct Point Change} = V_t - V_{t-1}$$
          *Example:* If unemployment moves from 10% to 12%, the change is **+2.0 percentage points** (not +20%).

        #### B. Compound Annual Growth Rate (CAGR)
        Calculated for multi-year trends:
        $$\\text{CAGR} = \\left( \\frac{V_{\\text{end}}}{V_{\\text{start}}} \\right)^{\\frac{1}{n}} - 1$$
        *Edge cases:* CAGR is valid strictly when $V_{\\text{start}} > 0$ and $V_{\\text{end}} > 0$. Zero or negative values are handled safely.

        ---

        ### 2. Country Identifiers & ISO Normalization
        All country statistics are mapped to standardized ISO 3166-1 alpha-3 country codes:
        - Eurostat country code `EL` is normalized to `GRC` (Greece).
        - Eurostat country code `UK` is normalized to `GBR` (United Kingdom).
        - Regional aggregates (`EU27_2020`, `EA20`) are stored distinctly from national member states.

        ---

        ### 3. Aggregation Methodology
        - **Official Aggregates:** Where official EU-27 or Euro Area series exist in Eurostat or ECB datasets, official values are preserved directly.
        - **Derived Aggregates:** When calculating derived aggregates across EU member states:
          - **Weighted Average:** Used for rates like Unemployment or Debt/GDP, weighted by total active population or national GDP.
          - **Arithmetic Average:** Provided only when weights are unpopulated, with explicit documentation.

        ---

        ### 4. Non-Negotiable Data Integrity Rules
        1. **Zero Fake Data:** Every visible observation originates from an official dataset (Eurostat, ECB, World Bank, OECD).
        2. **Transparent Missing Values:** Missing observations are left as `None`/`NaN` and disclosed in rankings/tables. They are **NEVER** filled with zero.
        3. **No Policy Simulation in V1:** As requested, this application is strictly an analytical research platform based on empirical facts. No scenario calculators or simulated tax/rate changes are included.
        4. **Correlation $\\neq$ Causation:** Statistical relationships in scatter plots quantify linear association ($r, R^2$), not causal impacts.
    """)
