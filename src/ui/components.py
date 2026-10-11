"""
Reusable Streamlit UI Components.
Provides metric cards, header bars, source badges, data download buttons, and filters.
"""

import streamlit as st
import pandas as pd
from typing import Optional, Dict, Any, List
from src.metadata.indicators import IndicatorMeta, INDICATORS
from src.metadata.domains import DOMAINS
from src.metadata.countries import get_country_flag, get_country_name

def render_header(title: str, subtitle: str, icon: str = "🇪🇺"):
    """Renders main application header bar."""
    st.markdown(f"""
        <div style="display: flex; align-items: center; justify-content: space-between; padding: 1rem 0; border-bottom: 1px solid #1e293b; margin-bottom: 1.5rem;">
            <div>
                <h1 style="font-size: 2rem; font-weight: 800; color: #f8fafc; margin: 0; display: flex; align-items: center; gap: 0.75rem;">
                    <span>{icon}</span> {title}
                </h1>
                <p style="color: #94a3b8; font-size: 0.95rem; margin: 0.4rem 0 0 0;">{subtitle}</p>
            </div>
            <div>
                <span class="badge-source">OFFICIAL DATA ENGINE</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

def render_metric_card(
    title: str,
    value_str: str,
    unit_str: str,
    change_val: Optional[float] = None,
    change_label: str = "YoY",
    is_percentage_point: bool = False,
    better_direction: str = "high",
    tooltip: Optional[str] = None
):
    """
    Renders styled HTML metric card with percentage or percentage-point change indicators.
    All cards are designed for strict equal height, clean typography, and baseline alignment.
    """
    change_html = ""
    if change_val is not None:
        sign = "+" if change_val > 0 else ""
        unit_suffix = " pp" if is_percentage_point else "%"
        
        # Determine sentiment color based on better_direction
        is_good = (change_val > 0 and better_direction == "high") or (change_val < 0 and better_direction == "low")
        is_bad = (change_val < 0 and better_direction == "high") or (change_val > 0 and better_direction == "low")

        cls = "metric-change-pos" if is_good else ("metric-change-neg" if is_bad else "metric-change-neu")
        change_html = f'<span class="{cls}">{sign}{change_val:.2f}{unit_suffix}</span> <span style="font-size: 0.72rem; color: #64748b;">({change_label})</span>'
    else:
        change_html = '<span style="color: #475569; font-size: 0.75rem;">&nbsp;</span>'

    title_attr = f' title="{tooltip}"' if tooltip else ""
    unit_html = f'<span class="metric-unit">{unit_str}</span>' if unit_str else ''

    st.markdown(f"""
        <div class="metric-card"{title_attr}>
            <div class="metric-title">{title}</div>
            <div class="metric-value-box">
                <div class="metric-value">{value_str} {unit_html}</div>
            </div>
            <div class="metric-sub">{change_html}</div>
        </div>
    """, unsafe_allow_html=True)

def render_csv_download_button(df: pd.DataFrame, filename: str, label: str = "📥 Download CSV"):
    """Renders CSV download button for export functionality."""
    if df.empty:
        return
    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label=label,
        data=csv_data,
        file_name=f"{filename}.csv",
        mime="text/csv"
    )

def render_source_info(meta: IndicatorMeta):
    """Displays official source attribution badge and dataset link."""
    st.markdown(f"""
        <div style="background-color: #0f172a; border: 1px solid #1e293b; border-radius: 8px; padding: 0.75rem 1rem; margin-top: 1rem; font-size: 0.85rem; color: #94a3b8; display: flex; justify-content: space-between; align-items: center;">
            <div>
                <strong>Official Source:</strong> {meta['source_provider']} &nbsp;|&nbsp; 
                <strong>Dataset ID:</strong> <code>{meta['source_dataset_code']}</code> &nbsp;|&nbsp; 
                <strong>Frequency:</strong> {meta['frequency']}
            </div>
            <div>
                <a href="{meta['source_url']}" target="_blank" style="color: #38bdf8; text-decoration: none; font-weight: 600;">Original Data Portal ↗</a>
            </div>
        </div>
    """, unsafe_allow_html=True)
