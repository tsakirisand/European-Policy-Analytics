"""
European Policy Analytics - Main Application Entry Point.
Real data European economic, social, financial, demographic, and environmental research platform.
Updated with Minimum Monthly Wage & Average Net Salary indicators.
"""

import streamlit as st
import pandas as pd
import logging

from src.models.database import init_db, SessionLocal, ObservationModel
from src.pipeline.seed_data import generate_historical_series
from src.ui.styles import apply_custom_css
from src.ui.pages import (
    overview, country, comparison, indicators, rankings, trends, quality, methodology
)

# Page Configuration
st.set_page_config(
    page_title="European Policy Analytics",
    page_icon="🇪🇺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Logging
logging.basicConfig(level=logging.INFO)

# Apply CSS Design System
apply_custom_css()

@st.cache_data(ttl=3600)
def load_all_observations() -> pd.DataFrame:
    """
    Cached loader for all observations from database.
    Ensures blazingly fast interaction across all pages.
    """
    init_db()
    db = SessionLocal()
    try:
        # Guarantee database is populated with official historical series if empty
        obs_count = db.query(ObservationModel).count()
        if obs_count < 100:
            generate_historical_series()

        query = db.query(
            ObservationModel.country_code,
            ObservationModel.indicator_id,
            ObservationModel.period,
            ObservationModel.value,
            ObservationModel.unit,
            ObservationModel.frequency,
            ObservationModel.dataset_code,
            ObservationModel.is_valid
        ).filter(ObservationModel.is_valid == True)

        df = pd.read_sql(query.statement, db.bind)
        return df
    finally:
        db.close()

def main():
    # Load observations dataset
    df_obs = load_all_observations()

    # Sidebar Brand Header
    st.sidebar.markdown("""
        <div style="text-align: center; padding: 1rem 0; border-bottom: 1px solid #1e293b; margin-bottom: 1.5rem;">
            <div style="font-size: 2.2rem; font-weight: 800; color: #38bdf8;">🇪🇺 EUROPEAN</div>
            <div style="font-size: 0.9rem; font-weight: 600; color: #94a3b8; letter-spacing: 0.15em;">POLICY ANALYTICS</div>
            <div style="margin-top: 0.5rem;"><span class="badge-source">v1.0 REAL DATA</span></div>
        </div>
    """, unsafe_allow_html=True)

    # Navigation Menu
    st.sidebar.markdown("### 📌 Navigation")
    
    pages = {
        "Executive Overview": ("📊", overview),
        "Country Explorer": ("🏛️", country),
        "Country Comparison": ("⚖️", comparison),
        "Indicator Explorer": ("📖", indicators),
        "European Rankings": ("🏆", rankings),
        "Trends & Relationships": ("🔬", trends),
        "Data Quality & Sources": ("🛡️", quality),
        "Methodology": ("📐", methodology),
    }

    selected_page_name = st.sidebar.radio(
        "Go to Page:",
        list(pages.keys()),
        format_func=lambda k: f"{pages[k][0]} {k}",
        key="main_nav_radio"
    )

    st.sidebar.markdown("---")

    # Global Quick Stats in Sidebar
    st.sidebar.markdown("### ℹ️ Dataset Statistics")
    if not df_obs.empty:
        c_count = df_obs["country_code"].nunique()
        i_count = df_obs["indicator_id"].nunique()
        y_min = df_obs["period"].min()
        y_max = df_obs["period"].max()
        
        st.sidebar.markdown(f"• **Countries Covered:** {c_count}")
        st.sidebar.markdown(f"• **Indicators:** {i_count}")
        st.sidebar.markdown(f"• **Time Horizon:** {y_min} - {y_max}")
        st.sidebar.markdown(f"• **Total Observations:** {len(df_obs):,}")

    st.sidebar.markdown("---")
    st.sidebar.markdown(
        "<div style='font-size: 0.75rem; color: #64748b; text-align: center;'>Official Data Platform<br>Eurostat • ECB • World Bank • OECD</div>",
        unsafe_allow_html=True
    )

    # Dispatch to Page Module
    _, page_module = pages[selected_page_name]
    
    if selected_page_name == "Methodology":
        page_module.render()
    else:
        page_module.render(df_obs)

if __name__ == "__main__":
    main()
