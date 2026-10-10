"""
Page 4: Indicator Explorer & Catalog.
Searchable directory of official statistical indicators with dataset identifiers and metadata.
"""

import streamlit as st
import pandas as pd
from src.metadata.indicators import INDICATORS, get_indicator
from src.metadata.domains import DOMAINS
from src.metadata.countries import get_country_flag, get_country_name
from src.ui.components import render_header, render_csv_download_button, render_source_info
from src.ui.charts import create_time_series_chart

def render(df_obs: pd.DataFrame):
    render_header(
        title="Indicator Explorer & Catalog",
        subtitle="Searchable directory of integrated official statistical indicators and source metadata.",
        icon="📖"
    )

    # Search & Filter Controls
    col_search, col_domain = st.columns([2, 1])

    with col_search:
        search_query = st.text_input("🔍 Search Indicators by Keyword:", "", placeholder="e.g. GDP, unemployment, inflation, debt...")

    with col_domain:
        domain_options = ["ALL"] + list(DOMAINS.keys())
        selected_domain = st.selectbox(
            "Filter by Domain:",
            domain_options,
            format_func=lambda d: "All Domains" if d == "ALL" else f"{DOMAINS[d]['icon']} {DOMAINS[d]['name']}"
        )

    # Filter indicators
    filtered_indicators = []
    for ind_id, meta in INDICATORS.items():
        if selected_domain != "ALL" and meta["domain_id"] != selected_domain:
            continue
        if search_query:
            q = search_query.lower()
            match = q in meta["name"].lower() or q in meta["short_name"].lower() or q in meta["description"].lower() or q in meta["source_dataset_code"].lower()
            if not match:
                continue
        filtered_indicators.append(meta)

    st.markdown(f"**Found {len(filtered_indicators)} matching indicators**")
    st.markdown("<br>", unsafe_allow_html=True)

    if not filtered_indicators:
        st.info("No indicators match your search criteria.")
        return

    # Indicator Catalog Display
    for meta in filtered_indicators:
        with st.expander(f"{DOMAINS[meta['domain_id']]['icon']} {meta['name']} ({meta['source_provider']})", expanded=False):
            st.markdown(f"**Description:** {meta['description']}")
            
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.markdown(f"**Domain:** {DOMAINS[meta['domain_id']]['name']}")
                st.markdown(f"**Unit:** `{meta['unit']}` ({meta['unit_symbol']})")
            with c2:
                st.markdown(f"**Source Provider:** {meta['source_provider']}")
                st.markdown(f"**Dataset Code:** `[{meta['source_dataset_code']}]`({meta['source_url']})")
            with c3:
                st.markdown(f"**Frequency:** {meta['frequency']}")
                st.markdown(f"**Calculation Type:** {'Percentage Point' if meta['change_type'] == 'pct_point' else 'Percentage Change'}")
            with c4:
                # Country coverage count from df_obs
                if not df_obs.empty:
                    df_ind_obs = df_obs[df_obs["indicator_id"] == meta["id"]]
                    countries_count = df_ind_obs["country_code"].nunique()
                    years = sorted(df_ind_obs["period"].unique())
                    year_str = f"{years[0]} - {years[-1]}" if years else "N/A"
                    st.markdown(f"**Country Coverage:** {countries_count} countries")
                    st.markdown(f"**Available Years:** {year_str}")

            render_source_info(meta)

            # Interactive chart preview within expander
            st.markdown("##### Quick Chart Preview (EU-27 & Top Economies)")
            fig_prev = create_time_series_chart(
                df_obs=df_obs,
                indicator_id=meta["id"],
                selected_countries=["DEU", "FRA", "ITA", "ESP", "GRC", "EU27"],
                start_year=2000,
                end_year=2025
            )
            st.plotly_chart(fig_prev, use_container_width=True)
