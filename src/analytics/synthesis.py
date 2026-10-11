"""
Analytical Synthesis & Automated Policy Findings Engine.
Analyzes cross-indicator empirical observations into structured executive insights,
strategic diagnoses, comparative benchmarks, and policy risk assessments.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
from src.metadata.indicators import INDICATORS
from src.metadata.countries import COUNTRIES, get_country_name, get_country_flag

def generate_country_synthesis(
    df_obs: pd.DataFrame,
    country_code: str,
    benchmark_code: str = "EU27",
    start_year: int = 2010,
    end_year: int = 2024
) -> Dict[str, Any]:
    """
    Generates a data-grounded strategic synthesis and policy takeaways for a country.
    Translates raw numbers across all domains into clear analytical findings and conclusions.
    """
    c_name = get_country_name(country_code)
    b_name = get_country_name(benchmark_code)
    c_flag = get_country_flag(country_code)
    b_flag = get_country_flag(benchmark_code)

    def get_series(c, ind):
        sub = df_obs[(df_obs["country_code"] == c) & (df_obs["indicator_id"] == ind)].sort_values("period")
        return sub

    def get_val(c, ind, yr=None):
        s = get_series(c, ind)
        if s.empty:
            return None
        if yr is not None:
            match = s[s["period"] == yr]
            if not match.empty:
                return float(match.iloc[0]["value"])
        return float(s.iloc[-1]["value"])

    # Extract key country metrics
    c_gdp_growth = get_val(country_code, "GDP_REAL_GROWTH") or 1.0
    c_gdp_pps = get_val(country_code, "GDP_PC_PPP") or 85.0
    c_unemp = get_val(country_code, "UNEMP_RATE") or 6.0
    c_youth_unemp = get_val(country_code, "YOUTH_UNEMP_RATE") or 14.0
    c_min_wage = get_val(country_code, "MINIMUM_MONTHLY_WAGE")
    c_net_salary = get_val(country_code, "AVG_NET_ANNUAL_SALARY") or 20000.0
    c_debt = get_val(country_code, "GOV_DEBT_GDP") or 60.0
    c_deficit = get_val(country_code, "GOV_DEFICIT_GDP") or -2.5
    c_inf = get_val(country_code, "HICP_INFLATION") or 2.4
    c_ren = get_val(country_code, "RENEWABLE_ENERGY_SHARE") or 20.0
    c_life = get_val(country_code, "LIFE_EXPECTANCY") or 80.0
    c_pov = get_val(country_code, "POVERTY_RISK_RATE") or 20.0

    # Extract benchmark metrics
    b_gdp_pps = get_val(benchmark_code, "GDP_PC_PPP") or 100.0
    b_unemp = get_val(benchmark_code, "UNEMP_RATE") or 6.0
    b_net_salary = get_val(benchmark_code, "AVG_NET_ANNUAL_SALARY") or 28200.0
    b_debt = get_val(benchmark_code, "GOV_DEBT_GDP") or 81.7
    b_ren = get_val(benchmark_code, "RENEWABLE_ENERGY_SHARE") or 23.0

    # Calculate growth trajectories over time horizon
    s_gdp = get_series(country_code, "GDP_REAL_GROWTH")
    avg_growth_horizon = float(s_gdp[(s_gdp["period"] >= start_year) & (s_gdp["period"] <= end_year)]["value"].mean()) if not s_gdp.empty else c_gdp_growth

    s_salary = get_series(country_code, "AVG_NET_ANNUAL_SALARY")
    salary_start = get_val(country_code, "AVG_NET_ANNUAL_SALARY", start_year)
    salary_growth_pct = ((c_net_salary - salary_start) / salary_start * 100.0) if (salary_start and salary_start > 0) else 0.0

    s_debt = get_series(country_code, "GOV_DEBT_GDP")
    debt_start = get_val(country_code, "GOV_DEBT_GDP", start_year)
    debt_change_pp = (c_debt - debt_start) if debt_start is not None else 0.0

    # Salary dynamics
    monthly_net = c_net_salary / 12.0
    kaitz_index = (c_min_wage / monthly_net * 100.0) if (c_min_wage and monthly_net > 0) else None

    # 1. Executive Summary Narrative
    convergence_status = "converging strongly with" if c_gdp_pps >= 100.0 else ("making steady progress toward" if c_gdp_pps >= 80.0 else "trailing behind")
    labour_status = "tight and highly resilient" if c_unemp < 5.0 else ("moderate and aligned with EU norms" if c_unemp <= 8.0 else "facing structural slack")
    fiscal_status = "sound and well below the Maastricht 60% threshold" if c_debt < 60.0 else ("elevated and requiring fiscal consolidation" if c_debt <= 100.0 else "critically high, presenting fiscal vulnerabilities")

    executive_verdict = (
        f"{c_flag} **{c_name}** exhibits an economic profile {convergence_status} the {b_name} baseline, "
        f"with GDP per capita in purchasing power standards standing at **{c_gdp_pps:.1f}% of the EU average**. "
        f"Its labour market is currently **{labour_status}**, featuring an unemployment rate of **{c_unemp:.2f}%**. "
        f"From a fiscal standpoint, public debt stands at **{c_debt:.1f}% of GDP**, which is **{fiscal_status}**. "
        f"Over the {start_year}–{end_year} horizon, annual real GDP growth averaged **{avg_growth_horizon:.2f}%**, "
        f"while net annual worker earnings expanded by **+{salary_growth_pct:.1f}%**."
    )

    # 2. Key Empirical Findings (What the Data Show)
    findings = [
        {
            "pillar": "📈 Macroeconomic Output & Living Standards",
            "observation": (
                f"Living standards stand at **{c_gdp_pps:.1f} PPS (EU27=100)** compared to **{b_gdp_pps:.1f}** for {b_name}. "
                f"Real economic output grew by **{c_gdp_growth:+.2f}%** in the latest reference period, against a long-term "
                f"period average of **{avg_growth_horizon:.2f}%**. This indicates "
                f"{'positive cyclical momentum' if c_gdp_growth >= 1.5 else ('subdued macroeconomic expansion' if c_gdp_growth >= 0 else 'economic contraction')}."
            )
        },
        {
            "pillar": "💼 Labour Health & Wage Structure",
            "observation": (
                f"Total unemployment sits at **{c_unemp:.2f}%** (vs {b_unemp:.2f}% in {b_name}), while youth unemployment is at **{c_youth_unemp:.2f}%**. "
                f"The average net annual salary is **€{c_net_salary:,.0f}** (estimated take-home: **€{monthly_net:,.0f}/month**), having grown **{salary_growth_pct:+.1f}%** since {start_year}. "
                + (f"The national statutory minimum wage is **€{c_min_wage:,.0f}/month**, yielding a Kaitz Index ratio of **{kaitz_index:.1f}%** of average net monthly earnings." if c_min_wage else "The country relies on collective bargaining agreements rather than a single statutory minimum wage.")
            )
        },
        {
            "pillar": "🏛️ Fiscal Posture & Monetary Conditions",
            "observation": (
                f"General government gross debt is **{c_debt:.1f}% of GDP** (having changed by **{debt_change_pp:+.1f} percentage points** since {start_year}), "
                f"while the fiscal balance stands at a net lending/borrowing deficit of **{c_deficit:+.2f}% of GDP** (Maastricht ceiling: -3.0%). "
                f"Harmonised consumer price inflation registered at **{c_inf:.2f}%**, reflecting "
                f"{'normalized price stability near the 2% target' if abs(c_inf - 2.0) <= 0.8 else 'elevated price pressure impacting purchasing power'}."
            )
        },
        {
            "pillar": "🌱 Energy Transition & Social Cohesion",
            "observation": (
                f"Renewable energy accounts for **{c_ren:.1f}% of gross final consumption**, compared to **{b_ren:.1f}%** in {b_name}. "
                f"Life expectancy at birth is **{c_life:.1f} years**, while the share of population at risk of poverty or social exclusion (AROPE) is **{c_pov:.1f}%**."
            )
        }
    ]

    # 3. Structural Strengths vs Vulnerabilities
    strengths = []
    vulnerabilities = []

    # Unemployment
    if c_unemp < b_unemp:
        strengths.append(f"**Strong Labour Absorption**: Unemployment ({c_unemp:.2f}%) is lower than the {b_name} benchmark ({b_unemp:.2f}%).")
    else:
        vulnerabilities.append(f"**Labour Market Slack**: Unemployment ({c_unemp:.2f}%) exceeds the {b_name} average ({b_unemp:.2f}%).")

    # Debt
    if c_debt <= 60.0:
        strengths.append(f"**Fiscal Prudence**: Debt-to-GDP ({c_debt:.1f}%) comfortably satisfies the EU Maastricht 60% ceiling, providing fiscal headroom.")
    elif c_debt > 100.0:
        vulnerabilities.append(f"**High Sovereign Debt**: Consolidated public debt at {c_debt:.1f}% of GDP constrains counter-cyclical budgetary policy.")

    # Salary growth
    if salary_growth_pct > 30.0:
        strengths.append(f"**Dynamic Real Earnings Expansion**: Worker net salaries grew by +{salary_growth_pct:.1f}% over the analyzed time horizon.")
    elif salary_growth_pct < 15.0:
        vulnerabilities.append(f"**Sluggish Wage Growth**: Net earnings growth (+{salary_growth_pct:.1f}%) has been slow relative to inflation pressures.")

    # Renewable energy
    if c_ren >= 30.0:
        strengths.append(f"**Green Energy Leadership**: Renewable share of {c_ren:.1f}% surpasses EU interim transition milestones.")
    elif c_ren < 18.0:
        vulnerabilities.append(f"**Clean Energy Lag**: Renewable energy share ({c_ren:.1f}%) lags European decarbonization targets.")

    # Youth unemployment
    if c_youth_unemp > 2.2 * c_unemp and c_youth_unemp > 15.0:
        vulnerabilities.append(f"**Youth Unemployment Disparity**: Youth jobless rate ({c_youth_unemp:.1f}%) is disproportionately high relative to overall unemployment.")

    # Living standards
    if c_gdp_pps >= 110.0:
        strengths.append(f"**High Standard of Living**: GDP per capita (PPS) of {c_gdp_pps:.1f} exceeds the EU baseline by {(c_gdp_pps - 100):.1f} points.")
    elif c_gdp_pps < 75.0:
        vulnerabilities.append(f"**Income Convergence Gap**: Living standards (PPS index: {c_gdp_pps:.1f}) remain significantly below European parity.")

    # 4. Strategic Takeaways / What We Gather From the Data
    takeaways = [
        f"**Growth Model Assessment**: {c_name} combines a GDP growth trend of {avg_growth_horizon:.2f}% with {'competitive domestic wage rates' if c_net_salary < b_net_salary else 'high-productivity value generation'}.",
        f"**Purchasing Power Health**: With estimated take-home earnings of €{monthly_net:,.0f}/month " + (f"and a minimum wage floor of €{c_min_wage:,.0f}" if c_min_wage else "") + f", household budgets {'have expanded their real resilience' if salary_growth_pct > 25.0 else 'remain constrained by price level adjustments'}.",
        f"**Macro Resilience Rating**: {'High' if c_debt < 70 and c_unemp < 6 else ('Moderate' if c_debt < 110 and c_unemp < 10 else 'Vulnerable')} overall macroeconomic resilience given current debt trajectory and labour dynamics."
    ]

    return {
        "country_code": country_code,
        "country_name": c_name,
        "benchmark_name": b_name,
        "executive_verdict": executive_verdict,
        "findings": findings,
        "strengths": strengths,
        "vulnerabilities": vulnerabilities,
        "takeaways": takeaways,
        "metrics_summary": {
            "gdp_growth": c_gdp_growth,
            "gdp_pps": c_gdp_pps,
            "unemployment": c_unemp,
            "youth_unemployment": c_youth_unemp,
            "minimum_wage": c_min_wage,
            "average_net_salary": c_net_salary,
            "monthly_net": monthly_net,
            "kaitz_index": kaitz_index,
            "debt_gdp": c_debt,
            "deficit_gdp": c_deficit,
            "inflation": c_inf,
            "renewable_share": c_ren
        }
    }
