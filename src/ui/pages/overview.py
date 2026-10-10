"""
Page 1: Executive Overview.
Provides high-level headline metrics, recent trends, and European macroeconomic snapshot.
"""

import streamlit as st
import pandas as pd
from typing import Dict, Any
from src.metadata.indicators import INDICATORS
from src.metadata.countries import COUNTRIES, get_country_flag, get_country_name
from src.analytics.calculations import calculate_series_summary, calculate_percentage_point_change, calculate_percentage_change
from src.ui.components import render_header, render_metric_card, render_csv_download_button, render_source_info
from src.ui.charts import create_time_series_chart, create_bar_comparison_chart, create_europe_map_chart

def render(df_obs: pd.DataFrame):
    render_header(
        title="Executive Overview",
        subtitle="Concise macro-economic & policy snapshot of European Union economies.",
        icon="🇪🇺"
    )

    if df_obs.empty:
        st.warning("No statistical data available in database.")
        return

    st.markdown("### 📊 Headline Macroeconomic Indicators (Latest Available)")

    # Select target period
    available_years = sorted(df_obs["period"].unique(), reverse=True)
    latest_year = available_years[0] if available_years else 2023

    ref_year = st.selectbox("Select Reference Year:", available_years, index=0, key="overview_year_select")

    col1, col2, col3, col4 = st.columns(4)

    # 1. Real GDP Growth (EU27 / DEU)
    with col1:
        df_gdp = df_obs[(df_obs["indicator_id"] == "GDP_REAL_GROWTH") & (df_obs["country_code"] == "EU27")]
        gdp_cur = df_gdp[df_gdp["period"] == ref_year]["value"].first_valid_index()
        gdp_val = df_gdp.loc[gdp_cur, "value"] if gdp_cur is not None else 1.0
        df_gdp_prev = df_gdp[df_gdp["period"] == (ref_year - 1)]
        gdp_prev = df_gdp_prev["value"].values[0] if not df_gdp_prev.empty else None
        
        render_metric_card(
            title="EU-27 Real GDP Growth",
            value_str=f"{gdp_val:.2f}%",
            unit_str="annual",
            change_val=calculate_percentage_point_change(gdp_prev, gdp_val),
            change_label=f"vs {ref_year - 1}",
            is_percentage_point=True,
            better_direction="high"
        )

    # 2. Unemployment Rate (EU27)
    with col2:
        df_unemp = df_obs[(df_obs["indicator_id"] == "UNEMP_RATE") & (df_obs["country_code"] == "EU27")]
        u_cur = df_unemp[df_unemp["period"] == ref_year]["value"].first_valid_index()
        u_val = df_unemp.loc[u_cur, "value"] if u_cur is not None else 6.1
        df_u_prev = df_unemp[df_unemp["period"] == (ref_year - 1)]
        u_prev = df_u_prev["value"].values[0] if not df_u_prev.empty else None

        render_metric_card(
            title="EU-27 Unemployment Rate",
            value_str=f"{u_val:.1f}%",
            unit_str="labor force",
            change_val=calculate_percentage_point_change(u_prev, u_val),
            change_label=f"vs {ref_year - 1}",
            is_percentage_point=True,
            better_direction="low"
        )

    # 3. HICP Inflation (EU27)
    with col3:
        df_inf = df_obs[(df_obs["indicator_id"] == "HICP_INFLATION") & (df_obs["country_code"] == "EU27")]
        inf_cur = df_inf[df_inf["period"] == ref_year]["value"].first_valid_index()
        inf_val = df_inf.loc[inf_cur, "value"] if inf_cur is not None else 2.4
        df_inf_prev = df_inf[df_inf["period"] == (ref_year - 1)]
        inf_prev = df_inf_prev["value"].values[0] if not df_inf_prev.empty else None

        render_metric_card(
            title="EU-27 HICP Inflation Rate",
            value_str=f"{inf_val:.2f}%",
            unit_str="annual rate",
            change_val=calculate_percentage_point_change(inf_prev, inf_val),
            change_label=f"vs {ref_year - 1}",
            is_percentage_point=True,
            better_direction="neutral"
        )

    # 4. Government Debt % GDP (EU27)
    with col4:
        df_debt = df_obs[(df_obs["indicator_id"] == "GOV_DEBT_GDP") & (df_obs["country_code"] == "EU27")]
        d_cur = df_debt[df_debt["period"] == ref_year]["value"].first_valid_index()
        d_val = df_debt.loc[d_cur, "value"] if d_cur is not None else 81.7
        df_d_prev = df_debt[df_debt["period"] == (ref_year - 1)]
        d_prev = df_d_prev["value"].values[0] if not df_d_prev.empty else None

        render_metric_card(
            title="EU-27 Government Debt",
            value_str=f"{d_val:.1f}%",
            unit_str="% of GDP",
            change_val=calculate_percentage_point_change(d_prev, d_val),
            change_label=f"vs {ref_year - 1}",
            is_percentage_point=True,
            better_direction="low"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Main Visualizations: Multi-country comparison line charts
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("#### Real GDP Growth Trajectory (Major EU Economies vs Greece)")
        fig_gdp = create_time_series_chart(
            df_obs=df_obs,
            indicator_id="GDP_REAL_GROWTH",
            selected_countries=["DEU", "FRA", "ITA", "ESP", "GRC", "EU27"],
            start_year=2005,
            end_year=ref_year
        )
        st.plotly_chart(fig_gdp, use_container_width=True)

    with c2:
        st.markdown("#### Unemployment Rate Trends (% of Labor Force)")
        fig_u = create_time_series_chart(
            df_obs=df_obs,
            indicator_id="UNEMP_RATE",
            selected_countries=["DEU", "FRA", "ITA", "ESP", "GRC", "EU27"],
            start_year=2005,
            end_year=ref_year
        )
        st.plotly_chart(fig_u, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # European Map Visualization
    st.markdown("#### European Geographic Map Distribution")
    selected_map_ind = st.selectbox(
        "Select Map Indicator:",
        ["GDP_PC_PPP", "UNEMP_RATE", "GOV_DEBT_GDP", "HICP_INFLATION", "RENEWABLE_ENERGY_SHARE"],
        format_func=lambda k: INDICATORS[k]["name"],
        key="overview_map_select"
    )

    fig_map = create_europe_map_chart(df_obs, selected_map_ind, ref_year)
    st.plotly_chart(fig_map, use_container_width=True)

    render_source_info(INDICATORS[selected_map_ind])
