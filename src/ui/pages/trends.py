"""
Page 6: Trends & Indicator Relationships.
Investigates statistical correlations and cross-country patterns between policy indicators.
"""

import streamlit as st
import pandas as pd
from src.metadata.indicators import INDICATORS
from src.analytics.relationships import align_indicators_data
from src.ui.components import render_header, render_csv_download_button, render_source_info
from src.ui.charts import create_scatter_relationship_chart

def render(df_obs: pd.DataFrame):
    render_header(
        title="Trends & Indicator Relationships",
        subtitle="Explore cross-country statistical patterns, correlation, and multi-indicator relationships.",
        icon="🔬"
    )

    if df_obs.empty:
        st.warning("No data available.")
        return

    indicator_ids = list(INDICATORS.keys())
    available_years = sorted(df_obs["period"].unique(), reverse=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        ind_x = st.selectbox(
            "Select X-Axis Indicator:",
            indicator_ids,
            index=indicator_ids.index("GDP_PC_PPP") if "GDP_PC_PPP" in indicator_ids else 0,
            format_func=lambda k: f"X: {INDICATORS[k]['name']}",
            key="trends_ind_x"
        )

    with col2:
        ind_y = st.selectbox(
            "Select Y-Axis Indicator:",
            indicator_ids,
            index=indicator_ids.index("UNEMP_RATE") if "UNEMP_RATE" in indicator_ids else 1,
            format_func=lambda k: f"Y: {INDICATORS[k]['name']}",
            key="trends_ind_y"
        )

    with col3:
        selected_year = st.selectbox(
            "Reference Year:",
            available_years,
            index=0,
            key="trends_year_select"
        )

    meta_x = INDICATORS[ind_x]
    meta_y = INDICATORS[ind_y]

    # Align Data & Calculate Pearson Correlation
    df_aligned, stats_summary = align_indicators_data(
        df_obs=df_obs,
        indicator_x=ind_x,
        indicator_y=ind_y,
        period=selected_year,
        exclude_aggregates=True
    )

    # Statistical Summary Callout Cards
    st.markdown("#### Statistical Summary & Correlation Metrics")
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Pearson Correlation (r)", f"{stats_summary.get('r'):.4f}")
    with c2:
        st.metric("Coefficient of Determination (R²)", f"{stats_summary.get('r_squared'):.4f}")
    with c3:
        st.metric("Statistical p-value", f"{stats_summary.get('p_value'):.5f}")
    with c4:
        st.metric("Matched Countries", f"{stats_summary.get('count')}")

    # Warning Box
    st.markdown("""
        <div class="callout-warning">
            ⚠️ <strong>Methodological Disclaimer:</strong> Correlation measures linear association between two statistical series. 
            <strong>Correlation does NOT prove or establish causation.</strong> Statistical relationships may be influenced by unobserved confounders or structural economic factors.
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Interactive Scatter Plot
    fig_scatter = create_scatter_relationship_chart(
        df_aligned=df_aligned,
        indicator_x=ind_x,
        indicator_y=ind_y,
        period=selected_year,
        stats_info=stats_summary
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

    # Export & Data Table
    if not df_aligned.empty:
        st.markdown("##### Aligned Observations Table")
        df_table = df_aligned[["country_code", "country_name", "x_value", "y_value"]].copy()
        df_table.columns = ["Code", "Country", f"{meta_x['name']} ({meta_x['unit_symbol']})", f"{meta_y['name']} ({meta_y['unit_symbol']})"]
        st.dataframe(df_table, use_container_width=True)
        render_csv_download_button(df_table, f"relationship_{ind_x}_vs_{ind_y}_{selected_year}")
