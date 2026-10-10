# 🇪🇺 European Policy Analytics

A professional, real-data European economic, social, financial, demographic, and environmental policy research platform.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.14-blue.svg)
![Framework](https://img.shields.io/badge/framework-Streamlit%20%7C%20Plotly-green.svg)
![Data Integrity](https://img.shields.io/badge/data_integrity-100%25_Official-brightgreen.svg)

---

## 🌟 Executive Summary

**European Policy Analytics** collects, processes, normalizes, validates, analyzes, and visualizes official economic, social, fiscal, demographic, and environmental statistics across 31 European countries (all 27 EU member states plus United Kingdom, Switzerland, Norway, and Iceland) and EU-wide aggregates.

Built as an analytical research product, the platform prioritizes **data quality**, **mathematical rigor**, **provenance transparency**, and **professional visual aesthetics**.

> [!IMPORTANT]
> **Data Integrity Guarantee:** This platform uses **100% factual official statistics** from official API connectors (Eurostat, ECB, World Bank, OECD). It contains zero fabricated values and zero simulated policy calculators in V1.

---

## 🏛️ Analytical Policy Domains (8 Domains)

1. **Economy (ECON):** Real GDP growth, GDP per capita, HICP consumer price inflation, industrial output.
2. **Labour & Income (LABOUR):** Total unemployment rate, youth unemployment rate, GDP per capita (USD).
3. **Purchasing Power & Living Standards (PPP):** GDP per capita in Purchasing Power Standards (PPS, EU27=100).
4. **Public Finances (FINANCE_PUB):** General government gross debt (% GDP), fiscal deficit/surplus balance (% GDP).
5. **Financial Conditions (FINANCE_MON):** ECB main refinancing policy interest rate, bank mortgage lending rates.
6. **Energy & Environment (ENERGY_ENV):** Share of renewable energy in gross final energy consumption (%), greenhouse gas emissions.
7. **Demographics & Social Conditions (DEMO_SOCIAL):** Total population, at-risk-of-poverty or social exclusion rate (AROPE), life expectancy.
8. **Trade & Industry (TRADE_IND):** International trade balance in goods (% GDP), net exports.

---

## 💻 Application Pages (8 Pages)

The platform features a clean navigation system with 8 dedicated analytical pages:

1. **📊 Executive Overview:** Concise macro-economic dashboard displaying headline European metrics, multi-country trend lines, and interactive European geographic maps.
2. **🏛️ European Country Explorer:** Comprehensive profile for any selected European country across all 8 policy domains with historical trend breakdowns vs. EU-27 averages.
3. **⚖️ Country Comparison:** Side-by-side comparative engine allowing users to select custom country groups, time horizons, and indicators with snapshot bar charts and CSV data exports.
4. **📖 Indicator Explorer & Catalog:** Searchable inventory of integrated indicators detailing dataset codes, provider sources, units, frequencies, and direct links to official data portals.
5. **🏆 European Rankings:** Ranks European economies by indicator performance for any chosen year, respecting directionality (e.g. low unemployment is top performance) and disclosing missing observations.
6. **🔬 Trends & Indicator Relationships:** Cross-indicator scatter plot engine with OLS linear trendlines, Pearson correlation coefficients ($r$), $R^2$, $p$-values, and correlation vs. causation disclaimers.
7. **🛡️ Data Quality & Official Sources Portal:** Complete data provenance dashboard showing database health, validation logs, data freshness, and an interactive **Live API Ingestion Engine** trigger.
8. **📐 Methodology & Analytical Standards:** Transparent guide documenting percentage vs. percentage-point change formulas, CAGR calculations, ISO country normalization, and derived EU aggregate rules.

---

## 🛰️ Integrated Official Data Sources & Datasets

| Source Provider | Official Dataset Identifier | Indicator Description | Frequency |
| :--- | :--- | :--- | :--- |
| **Eurostat** | `nama_10_gdp` | Real GDP Growth & Components | Annual |
| **Eurostat** | `nama_10_pc` | GDP per Capita in PPS (EU27=100) | Annual |
| **Eurostat** | `prc_hicp_aind` | HICP Harmonised Consumer Inflation | Annual |
| **Eurostat** | `une_rt_a` | Total & Youth Unemployment Rate | Annual |
| **Eurostat** | `gov_10dd_edpt1` | Government Debt & Deficit (% GDP) | Annual |
| **Eurostat** | `nrg_ind_ren` | Renewable Energy Share (%) | Annual |
| **Eurostat** | `env_air_gge` | Greenhouse Gas Emissions (k tonnes) | Annual |
| **Eurostat** | `ilc_peps01n` | At-risk-of-poverty or social exclusion | Annual |
| **Eurostat** | `demo_gind` | Total Population on 1st January | Annual |
| **European Central Bank (ECB)** | `FM/D.U2.EUR.4F.KR.MRR_RT.LEV` | ECB Main Refinancing Policy Interest Rate | Annual avg (Time-Weighted) |
| **European Central Bank (ECB)** | `MIR/M.DE.B.A2C.A.R.A.2250.EUR.N` | Bank Mortgage Lending Interest Rates | Annual avg |
| **World Bank API v2** | `NY.GDP.PCAP.CD` | Gross Domestic Product per Capita (Current USD) | Annual |
| **World Bank API v2** | `NE.RSB.GNFS.ZS` | Trade Balance in Goods & Services (% GDP) | Annual |
| **World Bank API v2** | `SP.DYN.LE00.IN` | Life Expectancy at Birth (years) | Annual |

---

## 📐 Mathematical Calculations & Integrity

### Percentage Change vs. Percentage-Point Change
- **Percentage Change ($\%$):** Used for level indicators ($V_t$):
  $$\text{Pct Change} = \left( \frac{V_t - V_{t-1}}{|V_{t-1}|} \right) \times 100\%$$
  *Zero Denominators:* Evaluated safely to prevent division-by-zero or infinite artifacts.

- **Percentage-Point Change ($\text{pp}$):** Used for rate indicators already expressed as percentages (unemployment rate, inflation rate, debt % GDP):
  $$\text{Pct Point Change} = V_t - V_{t-1}$$

### Compound Annual Growth Rate (CAGR)
$$\text{CAGR} = \left( \frac{V_{\text{end}}}{V_{\text{start}}} \right)^{\frac{1}{n}} - 1$$

---

## 🛠️ Project Architecture

```
European-Policy-Analytics/
├── app.py                      # Main Streamlit application entry point
├── config.py                   # Centralized paths, DB, API settings & timeouts
├── requirements.txt            # Python dependencies
├── pytest.ini                  # Pytest configuration
├── data/
│   └── policy_analytics.db     # SQLite database storing normalized observations & logs
├── src/
│   ├── models/                 # SQLAlchemy ORM models & Pydantic schemas
│   │   ├── database.py
│   │   └── schema.py
│   ├── metadata/               # Countries (31 countries + EU27/EA20), domains, indicators catalog
│   │   ├── countries.py
│   │   ├── domains.py
│   │   └── indicators.py
│   ├── connectors/             # Resilient HTTP API connectors (retries, backoff, rate-limiting)
│   │   ├── base.py
│   │   ├── eurostat.py
│   │   ├── ecb.py
│   │   ├── worldbank.py
│   │   └── oecd.py
│   ├── pipeline/               # Data ingestion, normalizer, validator & database seeder
│   │   ├── normalizer.py
│   │   ├── validator.py
│   │   ├── ingestion.py
│   │   └── seed_data.py
│   ├── analytics/              # Mathematical calculations, rankings, correlations
│   │   ├── calculations.py
│   │   ├── comparisons.py
│   │   └── relationships.py
│   └── ui/                     # Research-grade UI styling, Plotly charts & pages
│       ├── styles.py
│       ├── components.py
│       ├── charts.py
│       └── pages/
│           ├── overview.py
│           ├── country.py
│           ├── comparison.py
│           ├── indicators.py
│           ├── rankings.py
│           ├── trends.py
│           ├── quality.py
│           └── methodology.py
└── tests/                      # Automated unit test suite (15 passing tests)
    ├── test_calculations.py
    ├── test_normalizer.py
    ├── test_validator.py
    └── test_pipeline.py
```

---

## 🚀 Quickstart Guide

### 1. Requirements
- Python 3.10+
- `pip`

### 2. Installation
```bash
# Clone or navigate to the project directory
cd European-Policy-Analytics

# Install required dependencies
python3 -m pip install -r requirements.txt
```

### 3. Run Automated Test Suite
```bash
python3 -m pytest
```

### 4. Launch Application
```bash
python3 -m streamlit run app.py
```

Open your browser at `http://localhost:8501` to explore the European Policy Analytics platform.

---

## 🧪 Testing Summary

The test suite verifies:
- **ISO 3166-1 Code Normalization:** Eurostat `EL` $\rightarrow$ `GRC`, `UK` $\rightarrow$ `GBR`, `DE` $\rightarrow$ `DEU`.
- **Deduplication Logic:** Handling duplicate dataset observations by keeping latest reported value.
- **Mathematical Accuracy:** Percentage change vs. percentage-point change, CAGR calculations, zero-denominator safety.
- **Data Quality Validation:** Plausible bounds checks for unemployment ($[0\%, 60\%]$), government debt ($[0\%, 300\%]$), and outlier detection.
- **Database Operations:** Table creation, metadata seeding, observation upserts, and ingestion logging.

---

## 🚫 Out of Scope (Version 1.0)
As specified in requirements, policy simulation, hypothetical scenario modeling, predictive policy impact calculators, and simulated tax/rate changes are **explicitly out of scope** for V1 to ensure strict factual reliability.

---

## 📄 License & Attribution
Designed for policy research and economic analysis using official open statistical data from **Eurostat**, **European Central Bank**, **World Bank**, and **OECD**.
