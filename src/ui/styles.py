"""
Custom CSS styles and design system for European Policy Analytics.
Provides a modern, dark-themed, research-grade user experience.
"""

import streamlit as st

def apply_custom_css():
    st.markdown("""
        <style>
        /* Main background & typography */
        .stApp {
            background-color: #0b0f19;
            color: #e2e8f0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #111827;
            border-right: 1px solid #1f2937;
        }

        /* Force Streamlit column containers to stretch to 100% height for equal card alignment */
        div[data-testid="stHorizontalBlock"] {
            align-items: stretch !important;
        }

        div[data-testid="column"] {
            display: flex !important;
            flex-direction: column !important;
            height: 100% !important;
        }

        div[data-testid="column"] > div {
            display: flex !important;
            flex-direction: column !important;
            flex: 1 1 auto !important;
            height: 100% !important;
        }

        div[data-testid="column"] [data-testid="stVerticalBlock"],
        div[data-testid="column"] [data-testid="stElementContainer"],
        div[data-testid="column"] [data-testid="stMarkdown"],
        div[data-testid="column"] [data-testid="stMarkdownContainer"] {
            display: flex !important;
            flex-direction: column !important;
            flex: 1 1 auto !important;
            height: 100% !important;
        }

        /* Metric Cards - Strict Equal Height & Flex Alignment */
        .metric-card {
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            border: 1px solid #334155;
            border-radius: 12px;
            padding: 0.9rem 0.85rem;
            margin-bottom: 0.5rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 2px 4px -1px rgba(0, 0, 0, 0.2);
            transition: transform 0.2s ease, border-color 0.2s ease;
            display: flex !important;
            flex-direction: column !important;
            justify-content: space-between !important;
            height: 100% !important;
            min-height: 152px !important;
            box-sizing: border-box !important;
        }
        .metric-card:hover {
            border-color: #38bdf8;
            transform: translateY(-2px);
        }
        .metric-title {
            color: #94a3b8;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            min-height: 2.2rem;
            line-height: 1.25;
            margin-bottom: 0.3rem;
            display: flex;
            align-items: flex-start;
            overflow: hidden;
        }
        .metric-value-box {
            display: flex;
            align-items: baseline;
            margin: 0.25rem 0;
            min-height: 2rem;
        }
        .metric-value {
            color: #f8fafc;
            font-size: clamp(1.15rem, 1.35vw, 1.38rem);
            font-weight: 700;
            line-height: 1.15;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            display: flex;
            align-items: baseline;
            gap: 0.25rem;
            flex-wrap: nowrap;
        }
        .metric-unit {
            font-size: 0.75rem;
            font-weight: 500;
            color: #94a3b8;
            white-space: nowrap;
        }
        .metric-sub {
            color: #64748b;
            font-size: 0.74rem;
            margin-top: 0.3rem;
            min-height: 1.2rem;
            display: flex;
            align-items: center;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .metric-change-pos {
            color: #34d399;
            font-weight: 600;
        }
        .metric-change-neg {
            color: #f87171;
            font-weight: 600;
        }
        .metric-change-neu {
            color: #94a3b8;
            font-weight: 500;
        }

        /* Badge Pills */
        .badge-source {
            display: inline-block;
            background-color: #1e293b;
            color: #38bdf8;
            border: 1px solid #0284c7;
            padding: 0.2rem 0.6rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
        }
        .badge-domain {
            display: inline-block;
            background-color: #312e81;
            color: #a5b4fc;
            padding: 0.2rem 0.6rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
        }

        /* Alert Callouts */
        .callout-info {
            background-color: #0f172a;
            border-left: 4px solid #38bdf8;
            padding: 1rem;
            border-radius: 0 8px 8px 0;
            margin-bottom: 1rem;
        }
        .callout-warning {
            background-color: #1c1917;
            border-left: 4px solid #fbbf24;
            padding: 1rem;
            border-radius: 0 8px 8px 0;
            margin-bottom: 1rem;
        }

        /* Section Header */
        .section-header {
            font-size: 1.4rem;
            font-weight: 700;
            color: #f8fafc;
            border-bottom: 2px solid #1e293b;
            padding-bottom: 0.5rem;
            margin-top: 1.5rem;
            margin-bottom: 1rem;
        }

        /* Data table container styling */
        div[data-testid="stDataFrame"] {
            border: 1px solid #1e293b;
            border-radius: 8px;
        }
        </style>
    """, unsafe_allow_html=True)
