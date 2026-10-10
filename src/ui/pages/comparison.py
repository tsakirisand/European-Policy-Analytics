"""
Page 3: Country Comparison Engine.
Side-by-side comparative analysis across multiple European countries and policy indicators.
"""

import streamlit as st
import pandas as pd
from typing import List
from src.metadata.countries import get_all_country_iso3_list, get_country_name, get_country_flag
from src.metadata.indicators import INDICATORS
from src.analytics.calculations import calculate_percentage_change, calculate_percentage_point_change
from src.ui.components import render_header, render_csv_download_button, render_source_info
from src.ui.charts import create_time_series_chart, create_bar_comparison_chart

def render(df_obs: pd.DataFrame):
    render_header(
        title="Country Comparison",
        subtitle="Side-by-side statistical comparison of selected European economies.",
        icon="⚖️"
    )

    if df_obs.empty:
        st.warning("No data available.")
        return

    all_countries = get_all_country_iso3_list(include_aggregates=True)
    indicator_ids = list(INDICATORS.keys())

    # Control Bar
    col1, col2, col3 = st.columns([2, 2, 1])

    with col1:
        selected_countries = st.multiselect(
            "Select Countries & Aggregates:",
            all_countries,
            default=["GRC", "DEU", "FRA", "ESP", "ITA", "EU27"],
            format_func=lambda c: f"{get_country_flag(c)} {get_country_name(c)} ({c})",
            key="comp_country_select"
        )

    with col2:
        selected_indicator = st.selectbox(
            "Select Indicator:",
            indicator_ids,
            index=0,
            format_func=lambda k: f"{INDICATORS[k]['name']} ({INDICATORS[k]['unit_symbol']})",
            key="comp_indicator_select"
        )

    with col3:
        available_years = sorted(df_obs["period"].unique())
        min_y, max_y = available_years[0], available_years[-1]
        start_year, end_year = st.slider(
            "Time Horizon:",
            min_value=min_y,
            max_value=max_y,
            value=(2005, max_y),
            key="comp_year_slider"
        )

    if not selected_countries:
        st.info("Please select at least one country to compare.")
        return

    meta = INDICATORS[selected_indicator]

    # Time-Series Comparison Chart
    st.markdown(f"### 📈 Time-Series Comparison: {meta['name']}")
    fig_ts = create_time_series_chart(
        df_obs=df_obs,
        indicator_id=selected_indicator,
        selected_countries=selected_countries,
        start_year=start_year,
        end_year=end_year
    )
    st.plotly_chart(fig_ts, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Snapshot Bar Chart for Reference Year
    col_bar, col_table = st.columns([1, 1])

    with col_bar:
        ref_year = st.selectbox(
            "Select Snapshot Year:",
            sorted(range(start_year, end_year + 1), reverse=True),
            index=0,
            key="comp_snapshot_year"
        )
        
        df_filtered = df_obs[
            (df_obs["indicator_id"] == selected_indicator) &
            (df_obs["country_code"].isin(selected_countries)) &
            (df_obs["period"] == ref_year)
        ].copy()

        df_filtered["country_name"] = df_filtered["country_code"].apply(
            lambda c: f"{get_country_flag(c)} {get_country_name(c)}"
        )
        df_filtered = df_filtered.sort_values(by="value", ascending=True)

        st.markdown(f"#### Snapshot Bar Chart ({ref_year})")
        fig_bar = create_bar_comparison_chart(df_filtered, selected_indicator, ref_year)
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_table:
        st.markdown(f"#### Comparison Data Matrix ({ref_year})")
        if not df_filtered.empty:
            df_display = df_filtered[["country_code", "country_name", "value", "unit"]].copy()
            df_display.columns = ["Code", "Country", f"Value ({meta['unit_symbol']})", "Unit"]
            st.dataframe(df_display, use_container_width=True)
            render_csv_download_button(df_display, f"comparison_{selected_indicator}_{ref_year}")

    render_source_info(meta)
