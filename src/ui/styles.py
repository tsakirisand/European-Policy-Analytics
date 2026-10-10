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

        /* Metric Cards */
        .metric-card {
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            border: 1px solid #334155;
            border-radius: 12px;
            padding: 1.25rem;
            margin-bottom: 1rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 2px 4px -1px rgba(0, 0, 0, 0.2);
            transition: transform 0.2s ease, border-color 0.2s ease;
        }
        .metric-card:hover {
            border-color: #38bdf8;
            transform: translateY(-2px);
        }
        .metric-title {
            color: #94a3b8;
            font-size: 0.85rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.4rem;
        }
        .metric-value {
            color: #f8fafc;
            font-size: 1.8rem;
            font-weight: 700;
            line-height: 1.2;
        }
        .metric-sub {
            color: #64748b;
            font-size: 0.8rem;
            margin-top: 0.3rem;
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
