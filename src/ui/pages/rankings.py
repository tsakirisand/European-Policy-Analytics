"""
Page 5: European Country Rankings.
Ranks European economies by indicator performance for any chosen reference period.
"""

import streamlit as st
import pandas as pd
from src.metadata.indicators import INDICATORS
from src.metadata.countries import COUNTRIES
from src.analytics.comparisons import rank_countries
from src.ui.components import render_header, render_csv_download_button, render_source_info
from src.ui.charts import create_bar_comparison_chart

def render(df_obs: pd.DataFrame):
    render_header(
        title="European Rankings",
        subtitle="Rank European countries by official economic, social, fiscal, and energy performance.",
        icon="🏆"
    )

    if df_obs.empty:
        st.warning("No data available.")
        return

    indicator_ids = list(INDICATORS.keys())
    available_years = sorted(df_obs["period"].unique(), reverse=True)

    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        selected_indicator = st.selectbox(
            "Select Indicator to Rank:",
            indicator_ids,
            index=0,
            format_func=lambda k: f"{INDICATORS[k]['name']} ({INDICATORS[k]['unit_symbol']})",
            key="rankings_indicator_select"
        )

    with col2:
        selected_year = st.selectbox(
            "Reference Year:",
            available_years,
            index=0,
            key="rankings_year_select"
        )

    meta = INDICATORS[selected_indicator]
    default_asc = True if meta["better_direction"] == "low" else False

    with col3:
        sort_order = st.radio(
            "Sort Order:",
            ["Descending (High to Low)", "Ascending (Low to High)"],
            index=1 if default_asc else 0,
            key="rankings_sort_radio"
        )
        ascending = True if "Ascending" in sort_order else False

    # Execute Ranking Calculation
    df_rankings = rank_countries(
        df_obs=df_obs,
        indicator_id=selected_indicator,
        period=selected_year,
        ascending=ascending
    )

    if df_rankings.empty:
        st.info(f"No valid observations available for {meta['name']} in year {selected_year}.")
        return

    # Disclosure on missing countries
    non_agg_count = len([c for c, m in COUNTRIES.items() if not m["is_aggregate"]])
    covered_count = len(df_rankings)
    missing_count = non_agg_count - covered_count

    st.markdown(f"**Ranked {covered_count} countries for reference year {selected_year}** " + (f"*(Missing observations for {missing_count} countries)*" if missing_count > 0 else ""))
    st.markdown("<br>", unsafe_allow_html=True)

    # Visualization
    c_chart, c_table = st.columns([1, 1])

    with c_chart:
        st.markdown(f"#### Top Ranked Countries: {meta['name']}")
        fig_rank = create_bar_comparison_chart(df_rankings, selected_indicator, selected_year, top_n=15)
        st.plotly_chart(fig_rank, use_container_width=True)

    with c_table:
        st.markdown("#### Complete Rankings Table")
        df_table = df_rankings[["rank", "country_name", "value", "unit"]].copy()
        df_table.columns = ["Rank", "Country", f"Value ({meta['unit_symbol']})", "Unit"]
        st.dataframe(df_table, use_container_width=True, height=500)
        render_csv_download_button(df_table, f"rankings_{selected_indicator}_{selected_year}")

    render_source_info(meta)
