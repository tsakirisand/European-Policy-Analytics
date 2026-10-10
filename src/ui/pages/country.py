"""
Page 2: European Country Explorer.
In-depth profile for any selected European country across all 8 analytical domains.
"""

import streamlit as st
import pandas as pd
from typing import Dict, Any
from src.metadata.countries import COUNTRIES, get_country_flag, get_country_name, get_all_country_iso3_list
from src.metadata.domains import DOMAINS
from src.metadata.indicators import INDICATORS, get_indicators_by_domain
from src.analytics.calculations import calculate_series_summary, calculate_percentage_point_change, calculate_percentage_change
from src.ui.components import render_header, render_metric_card, render_csv_download_button, render_source_info
from src.ui.charts import create_time_series_chart

def render(df_obs: pd.DataFrame):
    render_header(
        title="European Country Explorer",
        subtitle="Detailed economic, fiscal, labour, and environmental profile per country.",
        icon="🏛️"
    )

    if df_obs.empty:
        st.warning("No data available.")
        return

    # Country Selector
    all_countries = get_all_country_iso3_list(include_aggregates=False)
    
    # Set default to GRC (Greece) or DEU (Germany)
    default_idx = all_countries.index("GRC") if "GRC" in all_countries else 0

    col_sel, col_empty = st.columns([1, 2])
    with col_sel:
        selected_iso3 = st.selectbox(
            "Select European Country:",
            all_countries,
            index=default_idx,
            format_func=lambda code: f"{get_country_flag(code)} {get_country_name(code)} ({code})",
            key="country_explorer_select"
        )

    meta = COUNTRIES.get(selected_iso3, {})

    # Country Info Banner
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); border: 1px solid #334155; border-radius: 12px; padding: 1.25rem; margin-bottom: 1.5rem;">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div style="display: flex; align-items: center; gap: 1rem;">
                    <span style="font-size: 3rem;">{meta.get('flag')}</span>
                    <div>
                        <h2 style="margin: 0; color: #f8fafc; font-size: 1.8rem;">{meta.get('name')}</h2>
                        <span style="color: #94a3b8; font-size: 0.9rem;">Region: {meta.get('region')} | Currency: {meta.get('currency')} | ISO-3: {selected_iso3}</span>
                    </div>
                </div>
                <div>
                    <span class="badge-domain">{'EU Member State' if meta.get('is_eu') else 'Non-EU European Country'}</span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Filter observations for selected country
    df_country = df_obs[df_obs["country_code"] == selected_iso3]

    # Domain Tabs
    domain_keys = list(DOMAINS.keys())
    tabs = st.tabs([f"{DOMAINS[d]['icon']} {DOMAINS[d]['name']}" for d in domain_keys])

    for idx, d_key in enumerate(domain_keys):
        with tabs[idx]:
            d_meta = DOMAINS[d_key]
            st.markdown(f"#### {d_meta['icon']} {d_meta['name']} Domain Overview")
            st.markdown(f"*{d_meta['description']}*")
            st.markdown("<br>", unsafe_allow_html=True)

            domain_indicators = get_indicators_by_domain(d_key)
            if not domain_indicators:
                st.info("No indicators assigned to this domain.")
                continue

            # Render key indicator cards for domain
            grid_cols = st.columns(min(len(domain_indicators), 3))
            
            for ind_idx, ind in enumerate(domain_indicators[:3]):
                with grid_cols[ind_idx % 3]:
                    df_ind = df_country[df_country["indicator_id"] == ind["id"]].sort_values(by="period")
                    if not df_ind.empty:
                        latest_row = df_ind.iloc[-1]
                        val = latest_row["value"]
                        period = int(latest_row["period"])

                        prev_val = df_ind.iloc[-2]["value"] if len(df_ind) > 1 else None
                        
                        is_pp = ind["change_type"] == "pct_point"
                        change = calculate_percentage_point_change(prev_val, val) if is_pp else calculate_percentage_change(prev_val, val)

                        render_metric_card(
                            title=ind["short_name"],
                            value_str=f"{val:,.2f}" if val < 1000 else f"{val:,.0f}",
                            unit_str=ind["unit_symbol"],
                            change_val=change,
                            change_label=f"vs {period - 1}",
                            is_percentage_point=is_pp,
                            better_direction=ind["better_direction"]
                        )
                    else:
                        st.info(f"No observations available for {ind['short_name']}")

            st.markdown("<br>", unsafe_allow_html=True)

            # Historical Trend Line Chart vs EU27 Average
            ind_to_plot = st.selectbox(
                f"Select Indicator to Chart ({d_meta['name']}):",
                [i["id"] for i in domain_indicators],
                format_func=lambda k: INDICATORS[k]["name"],
                key=f"country_tab_chart_select_{d_key}"
            )

            fig_trend = create_time_series_chart(
                df_obs=df_obs,
                indicator_id=ind_to_plot,
                selected_countries=[selected_iso3, "EU27"],
                start_year=2000,
                end_year=2025
            )
            st.plotly_chart(fig_trend, use_container_width=True)

            # Domain Data Table & Download
            df_dom_obs = df_country[df_country["indicator_id"].isin([i["id"] for i in domain_indicators])].copy()
            if not df_dom_obs.empty:
                st.markdown("##### Detailed Historical Records")
                pivoted = df_dom_obs.pivot(index="period", columns="indicator_id", values="value").sort_index(ascending=False)
                st.dataframe(pivoted, use_container_width=True)
                render_csv_download_button(df_dom_obs, f"{selected_iso3}_{d_key}_data")
