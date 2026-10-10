"""
Page 7: Data Quality & Official Sources Portal.
Transparency portal displaying database health, dataset identifiers, data freshness,
validation checks, and live ingestion trigger.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from src.metadata.indicators import INDICATORS
from src.models.database import SessionLocal, IngestionLogModel, ValidationLogModel, ObservationModel
from src.pipeline.ingestion import run_ingestion_pipeline
from src.ui.components import render_header, render_csv_download_button

def render(df_obs: pd.DataFrame):
    render_header(
        title="Data Quality & Official Sources Portal",
        subtitle="Complete transparency into statistical sources, dataset health, validation checks, and API freshness.",
        icon="🛡️"
    )

    db = SessionLocal()
    try:
        total_obs = db.query(ObservationModel).count()
        valid_obs = db.query(ObservationModel).filter(ObservationModel.is_valid == True).count()
        invalid_obs = total_obs - valid_obs

        # Ingestion Logs
        logs = db.query(IngestionLogModel).order_by(IngestionLogModel.timestamp.desc()).limit(20).all()
        val_logs = db.query(ValidationLogModel).order_by(ValidationLogModel.timestamp.desc()).limit(20).all()

        st.markdown("### 📊 Dataset Health Summary")

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("Total Valid Observations", f"{valid_obs:,}")
        with c2:
            st.metric("Integrated Indicators", f"{len(INDICATORS)}")
        with c3:
            st.metric("Validation Flagged", f"{invalid_obs}")
        with c4:
            latest_fetch = db.query(ObservationModel.fetched_at).order_by(ObservationModel.fetched_at.desc()).first()
            fetch_str = latest_fetch[0].strftime("%Y-%m-%d %H:%M") if latest_fetch and latest_fetch[0] else "Pre-packaged"
            st.metric("Data Freshness", fetch_str)

        st.markdown("<br>", unsafe_allow_html=True)

        # Trigger Live Data Refresh Button
        st.markdown("#### 🔄 Live API Ingestion Engine")
        st.markdown("Click below to pull fresh statistical observations directly from official REST APIs (Eurostat, ECB, World Bank, OECD).")

        if st.button("🚀 Fetch Fresh Official Data Now", key="btn_run_ingestion"):
            with st.spinner("Connecting to official APIs (Eurostat, World Bank, ECB)..."):
                results = run_ingestion_pipeline()
                st.success(f"Ingestion completed! Processed {results['total_ingested']} observations.")
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        # Provider Dataset Inventory Table
        st.markdown("#### 📋 Integrated Official Datasets Inventory")
        inventory_data = []
        for ind_id, meta in INDICATORS.items():
            df_ind = df_obs[df_obs["indicator_id"] == ind_id] if not df_obs.empty else pd.DataFrame()
            cnt = len(df_ind)
            cov = df_ind["country_code"].nunique() if not df_ind.empty else 0
            years = sorted(df_ind["period"].unique()) if not df_ind.empty else []
            y_str = f"{years[0]}-{years[-1]}" if years else "N/A"

            inventory_data.append({
                "Indicator ID": ind_id,
                "Name": meta["name"],
                "Provider": meta["source_provider"],
                "Dataset Code": meta["source_dataset_code"],
                "Observations": cnt,
                "Countries": cov,
                "Years Covered": y_str,
                "Source Link": meta["source_url"]
            })

        df_inv = pd.DataFrame(inventory_data)
        st.dataframe(df_inv, use_container_width=True)
        render_csv_download_button(df_inv, "official_datasets_inventory")

        st.markdown("<br>", unsafe_allow_html=True)

        # Recent Ingestion Logs
        st.markdown("#### 📜 Ingestion Audit Logs")
        if logs:
            log_data = [{
                "Provider": l.provider,
                "Dataset": l.dataset_code,
                "Timestamp": l.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "Status": l.status,
                "Records Ingested": l.records_ingested,
                "Error Details": l.error_message or "None"
            } for l in logs]
            st.dataframe(pd.DataFrame(log_data), use_container_width=True)
        else:
            st.info("No ingestion audit logs recorded yet.")

    finally:
        db.close()
