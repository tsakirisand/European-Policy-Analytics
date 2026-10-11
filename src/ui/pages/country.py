"""
Page 2: European Country Explorer.
In-depth profile for any selected European country across all 8 analytical domains,
featuring radar benchmark profiles, European ranking scorecards, salary dynamics (Kaitz index),
and multi-indicator historical dossier exports.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any, List

from src.metadata.countries import COUNTRIES, get_country_flag, get_country_name, get_all_country_iso3_list
from src.metadata.domains import DOMAINS
from src.metadata.indicators import INDICATORS, get_indicators_by_domain
from src.analytics.calculations import (
    calculate_series_summary, calculate_percentage_point_change, calculate_percentage_change, calculate_cagr
)
from src.analytics.comparisons import rank_countries
from src.analytics.synthesis import generate_country_synthesis
from src.ui.components import render_header, render_metric_card, render_csv_download_button, render_source_info
from src.ui.charts import create_time_series_chart, create_radar_chart, LAYOUT_TEMPLATE, COLOR_PALETTE

def render(df_obs: pd.DataFrame):
    render_header(
        title="European Country Explorer",
        subtitle="Comprehensive economic, fiscal, labour, wage, and environmental dossier per country.",
        icon="🏛️"
    )

    if df_obs.empty:
        st.warning("No data available.")
        return

    # Country & Benchmark Selection Controls
    all_countries = get_all_country_iso3_list(include_aggregates=False)
    all_targets = ["EU27", "EA20"] + [c for c in all_countries if c not in ["EU27", "EA20"]]

    default_idx = all_countries.index("CZE") if "CZE" in all_countries else (all_countries.index("GRC") if "GRC" in all_countries else 0)

    start_year = int(df_obs["period"].min())
    end_year = int(df_obs["period"].max())

    c_sel1, c_sel2 = st.columns([1, 1])
    with c_sel1:
        selected_iso3 = st.selectbox(
            "Select European Country:",
            all_countries,
            index=default_idx,
            format_func=lambda code: f"{get_country_flag(code)} {get_country_name(code)} ({code})",
            key="country_explorer_select"
        )
    with c_sel2:
        benchmark_target = st.selectbox(
            "Comparison Benchmark:",
            all_targets,
            index=0,
            format_func=lambda code: f"{get_country_flag(code)} {get_country_name(code)} ({code})",
            key="country_explorer_benchmark"
        )
    meta = COUNTRIES.get(selected_iso3, {})
    bench_meta = COUNTRIES.get(benchmark_target, {})

    # Filter observations for selected country
    df_country = df_obs[df_obs["country_code"] == selected_iso3]
    df_country_horizon = df_country[(df_country["period"] >= start_year) & (df_country["period"] <= end_year)]

    # Country Header Banner
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); border: 1px solid #334155; border-radius: 12px; padding: 1.25rem; margin-bottom: 1.25rem;">
            <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 1rem;">
                <div style="display: flex; align-items: center; gap: 1rem;">
                    <span style="font-size: 3.2rem;">{meta.get('flag')}</span>
                    <div>
                        <h2 style="margin: 0; color: #f8fafc; font-size: 1.8rem; font-weight: 800;">{meta.get('name')}</h2>
                        <span style="color: #94a3b8; font-size: 0.9rem;">
                            Region: <strong>{meta.get('region')}</strong> &nbsp;|&nbsp; 
                            National Currency: <strong>{meta.get('currency')}</strong> &nbsp;|&nbsp; 
                            ISO-3: <code>{selected_iso3}</code>
                        </span>
                    </div>
                </div>
                <div style="display: flex; gap: 0.5rem; align-items: center;">
                    <span class="badge-domain">{'🇪🇺 EU Member State' if meta.get('is_eu') else '🌍 Non-EU European Economy'}</span>
                    <span class="badge-source">Benchmark: {bench_meta.get('name', benchmark_target)}</span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 1. Executive Country Snapshot (KPI Ribbon)
    kpi_indicators = [
        ("POPULATION", "Population", "inhabitants"),
        ("GDP_REAL_GROWTH", "Real GDP Growth", "%"),
        ("UNEMP_RATE", "Unemployment Rate", "%"),
        ("MINIMUM_MONTHLY_WAGE", "Minimum Wage", "€/mo"),
        ("AVG_NET_ANNUAL_SALARY", "Avg Net Salary", "€/yr"),
        ("GOV_DEBT_GDP", "Gov Debt", "% GDP")
    ]

    kpi_cols = st.columns(len(kpi_indicators))
    for idx, (ind_key, kpi_label, kpi_unit) in enumerate(kpi_indicators):
        with kpi_cols[idx]:
            df_k = df_country[df_country["indicator_id"] == ind_key].sort_values("period")
            if not df_k.empty:
                last_row = df_k.iloc[-1]
                v = last_row["value"]
                p = int(last_row["period"])
                prev_v = df_k.iloc[-2]["value"] if len(df_k) > 1 else None
                
                ind_meta = INDICATORS.get(ind_key, {})
                is_pp = ind_meta.get("change_type") == "pct_point"
                chg = calculate_percentage_point_change(prev_v, v) if is_pp else calculate_percentage_change(prev_v, v)

                val_format = f"{v:,.0f}" if v >= 1000 else f"{v:,.2f}"
                render_metric_card(
                    title=kpi_label,
                    value_str=val_format,
                    unit_str=kpi_unit,
                    change_val=chg,
                    change_label=f"vs {p-1}",
                    is_percentage_point=is_pp,
                    better_direction=ind_meta.get("better_direction", "high")
                )
            else:
                st.info(f"N/A ({kpi_label})")

    st.markdown("<br>", unsafe_allow_html=True)

    # 2. Eight Policy Domain Deep-Dive Tabs + Strategic Synthesis Tab
    domain_keys = list(DOMAINS.keys())
    tab_titles = ["🧠 What the Data Show & Strategic Analysis"] + [f"{DOMAINS[d]['icon']} {DOMAINS[d]['name']}" for d in domain_keys]
    tabs = st.tabs(tab_titles)

    # TAB 0: WHAT THE DATA SHOW & STRATEGIC SYNTHESIS
    with tabs[0]:
        synthesis = generate_country_synthesis(df_obs, selected_iso3, benchmark_target, start_year, end_year)

        st.markdown(f"### 🧠 What the Data Show: Comprehensive Analysis & Strategic Results")
        st.markdown(f"**Empirical diagnosis for {meta.get('name')} benchmarked against {bench_meta.get('name', benchmark_target)} over {start_year}–{end_year}.**")
        st.markdown("<br>", unsafe_allow_html=True)

        # Executive Verdict Card
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); border-left: 5px solid #38bdf8; border-radius: 8px; padding: 1.25rem; margin-bottom: 1.5rem;">
                <div style="font-size: 1.1rem; color: #f8fafc; font-weight: 600; margin-bottom: 0.5rem;">🎯 Executive Synthesis & Macro Verdict</div>
                <div style="color: #cbd5e1; font-size: 0.95rem; line-height: 1.6;">
                    {synthesis['executive_verdict']}
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Strategic Macroeconomic Performance & Radar Benchmark
        with st.expander(f"📊 Macroeconomic Performance Profile & European Standings ({meta.get('name')} vs {bench_meta.get('name')})", expanded=False):
            col_radar, col_rankings = st.columns([1.2, 1])

            with col_radar:
                st.markdown(f"##### 🕸️ Multidimensional Policy Radar (0-100 Benchmark)")
                
                def get_latest_val(c_code, i_id):
                    sub = df_obs[(df_obs["country_code"] == c_code) & (df_obs["indicator_id"] == i_id)].sort_values("period")
                    return sub.iloc[-1]["value"] if not sub.empty else None

                categories = ["Living Standards", "Labour Health", "Earnings Level", "Fiscal Health", "Green Transition"]

                c_gdp = get_latest_val(selected_iso3, "GDP_PC_PPP") or 80.0
                c_u = get_latest_val(selected_iso3, "UNEMP_RATE") or 6.0
                c_sal = get_latest_val(selected_iso3, "AVG_NET_ANNUAL_SALARY") or 20000.0
                c_debt = get_latest_val(selected_iso3, "GOV_DEBT_GDP") or 60.0
                c_ren = get_latest_val(selected_iso3, "RENEWABLE_ENERGY_SHARE") or 20.0

                b_gdp = get_latest_val(benchmark_target, "GDP_PC_PPP") or 100.0
                b_u = get_latest_val(benchmark_target, "UNEMP_RATE") or 6.0
                b_sal = get_latest_val(benchmark_target, "AVG_NET_ANNUAL_SALARY") or 28200.0
                b_debt = get_latest_val(benchmark_target, "GOV_DEBT_GDP") or 81.0
                b_ren = get_latest_val(benchmark_target, "RENEWABLE_ENERGY_SHARE") or 23.0

                c_scores = [
                    min(100.0, max(10.0, (c_gdp / 160.0) * 100.0)),
                    min(100.0, max(10.0, ((20.0 - c_u) / 18.0) * 100.0)),
                    min(100.0, max(10.0, (c_sal / 55000.0) * 100.0)),
                    min(100.0, max(10.0, ((160.0 - c_debt) / 140.0) * 100.0)),
                    min(100.0, max(10.0, (c_ren / 65.0) * 100.0))
                ]

                b_scores = [
                    min(100.0, max(10.0, (b_gdp / 160.0) * 100.0)),
                    min(100.0, max(10.0, ((20.0 - b_u) / 18.0) * 100.0)),
                    min(100.0, max(10.0, (b_sal / 55000.0) * 100.0)),
                    min(100.0, max(10.0, ((160.0 - b_debt) / 140.0) * 100.0)),
                    min(100.0, max(10.0, (b_ren / 65.0) * 100.0))
                ]

                fig_radar = create_radar_chart(
                    country_name=meta.get("name", selected_iso3),
                    categories=categories,
                    country_scores=[round(s, 1) for s in c_scores],
                    benchmark_name=bench_meta.get("name", benchmark_target),
                    benchmark_scores=[round(s, 1) for s in b_scores]
                )
                st.plotly_chart(fig_radar, use_container_width=True)

            with col_rankings:
                st.markdown(f"##### 🏆 European Standing & Rank Positions (2024)")
                st.markdown(f"*Where {meta.get('name')} places across 31 European nations:*")

                rank_trackers = [
                    ("GDP_PC_PPP", "Living Standards (PPS)", False),
                    ("GDP_REAL_GROWTH", "Real GDP Growth Rate", False),
                    ("UNEMP_RATE", "Low Unemployment Rate", True),
                    ("AVG_NET_ANNUAL_SALARY", "Average Net Salary", False),
                    ("MINIMUM_MONTHLY_WAGE", "Minimum Monthly Wage", False),
                    ("RENEWABLE_ENERGY_SHARE", "Renewable Energy Share", False),
                    ("GOV_DEBT_GDP", "Low Government Debt (% GDP)", True),
                    ("LIFE_EXPECTANCY", "Life Expectancy at Birth", False)
                ]

                for ind_id, label_rank, asc_flag in rank_trackers:
                    df_rk = rank_countries(df_obs, ind_id, period=2024, ascending=asc_flag)
                    if not df_rk.empty:
                        match_rk = df_rk[df_rk["country_code"] == selected_iso3]
                        if not match_rk.empty:
                            rk_val = int(match_rk.iloc[0]["rank"])
                            rk_val_num = match_rk.iloc[0]["value"]
                            ind_m = INDICATORS.get(ind_id, {})
                            badge_color = "#34d399" if rk_val <= 10 else ("#38bdf8" if rk_val <= 20 else "#fbbf24")
                            st.markdown(f"""
                                <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.35rem 0.6rem; margin-bottom: 0.35rem; background: #0f172a; border-radius: 6px; border: 1px solid #1e293b;">
                                    <span style="font-size: 0.85rem; color: #cbd5e1;">{label_rank}</span>
                                    <div>
                                        <span style="font-size: 0.85rem; color: #94a3b8; margin-right: 0.5rem;">{rk_val_num:,.1f} {ind_m.get('unit_symbol','')}</span>
                                        <span style="font-weight: 700; color: {badge_color}; font-size: 0.85rem; background: #1e293b; padding: 0.15rem 0.45rem; border-radius: 4px;">#{rk_val} of {len(df_rk)}</span>
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)

        # What the Data Show (4 Core Pillars)
        st.markdown("#### 🔍 What the Data Explicitly Demonstrate")
        st.markdown("*Empirical findings derived from verified official Eurostat, ECB, World Bank, and OECD datasets:*")
        
        c_f1, c_f2 = st.columns(2)
        for f_idx, item in enumerate(synthesis["findings"]):
            target_col = c_f1 if f_idx % 2 == 0 else c_f2
            with target_col:
                st.markdown(f"""
                    <div style="background: #0f172a; border: 1px solid #1e293b; border-radius: 8px; padding: 1rem; margin-bottom: 1rem;">
                        <div style="font-weight: 700; color: #38bdf8; font-size: 0.95rem; margin-bottom: 0.4rem;">{item['pillar']}</div>
                        <div style="font-size: 0.88rem; color: #cbd5e1; line-height: 1.5;">{item['observation']}</div>
                    </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Strengths vs Vulnerabilities Scorecard
        st.markdown("#### ⚖️ Structural Competitive Edges vs. Policy Vulnerabilities")
        col_str, col_vuln = st.columns(2)

        with col_str:
            st.markdown("""
                <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                    <span style="font-size: 1.2rem;">🟢</span>
                    <strong style="color: #34d399; font-size: 1rem;">Empirical Strengths & Outperformance</strong>
                </div>
            """, unsafe_allow_html=True)
            if synthesis["strengths"]:
                for s in synthesis["strengths"]:
                    st.markdown(f"""
                        <div style="background: rgba(52, 211, 153, 0.08); border: 1px solid rgba(52, 211, 153, 0.25); border-radius: 6px; padding: 0.75rem; margin-bottom: 0.5rem; font-size: 0.88rem; color: #f0fdf4;">
                            {s}
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No standout comparative strengths identified in the current period.")

        with col_vuln:
            st.markdown("""
                <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                    <span style="font-size: 1.2rem;">🔴</span>
                    <strong style="color: #f87171; font-size: 1rem;">Structural Vulnerabilities & Policy Risks</strong>
                </div>
            """, unsafe_allow_html=True)
            if synthesis["vulnerabilities"]:
                for v in synthesis["vulnerabilities"]:
                    st.markdown(f"""
                        <div style="background: rgba(248, 113, 113, 0.08); border: 1px solid rgba(248, 113, 113, 0.25); border-radius: 6px; padding: 0.75rem; margin-bottom: 0.5rem; font-size: 0.88rem; color: #fef2f2;">
                            {v}
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No critical structural vulnerabilities detected in the current period.")

        st.markdown("<br>", unsafe_allow_html=True)

        # What We Gather from Them (Strategic Deductions)
        st.markdown("#### 💡 What We Gather From Them: Strategic Conclusions & Takeaways")
        st.markdown("*Translating empirical trends into actionable policy insights:*")

        for takeaway in synthesis["takeaways"]:
            st.markdown(f"""
                <div style="background: #0f172a; border-left: 4px solid #fbbf24; border-radius: 6px; padding: 0.85rem 1rem; margin-bottom: 0.6rem; font-size: 0.9rem; color: #f8fafc;">
                    {takeaway}
                </div>
            """, unsafe_allow_html=True)

        # Downloadable Strategic Brief
        briefing_md = f"""# Strategic Policy Assessment: {meta.get('name')} ({selected_iso3})
**Reference Horizon:** {start_year} - {end_year}
**Benchmark Target:** {bench_meta.get('name', benchmark_target)}

## Executive Verdict
{synthesis['executive_verdict']}

## Empirical Findings
""" + "\n".join([f"### {f['pillar']}\n{f['observation']}\n" for f in synthesis['findings']]) + f"""
## Comparative Strengths
""" + "\n".join([f"- {s}" for s in synthesis['strengths']]) + f"""

## Structural Vulnerabilities
""" + "\n".join([f"- {v}" for v in synthesis['vulnerabilities']]) + f"""

## Strategic Takeaways
""" + "\n".join([f"- {t}" for t in synthesis['takeaways']])

        st.download_button(
            label="📄 Download Complete Strategic Analysis Brief (Markdown)",
            data=briefing_md.encode('utf-8'),
            file_name=f"{selected_iso3}_strategic_analysis_{start_year}_{end_year}.md",
            mime="text/markdown"
        )

    # Granular Policy Domain Tabs (Index 1 to 8)
    for idx, d_key in enumerate(domain_keys):
        with tabs[idx + 1]:
            d_meta = DOMAINS[d_key]
            st.markdown(f"#### {d_meta['icon']} {d_meta['name']} Analytical Profile")
            st.markdown(f"*{d_meta['description']}*")
            st.markdown("<br>", unsafe_allow_html=True)

            domain_indicators = get_indicators_by_domain(d_key)
            if not domain_indicators:
                st.info("No indicators assigned to this domain.")
                continue

            # Render key indicator cards for domain in rows of up to 4
            num_cols = min(len(domain_indicators), 4)
            for chunk_start in range(0, len(domain_indicators), num_cols):
                chunk = domain_indicators[chunk_start:chunk_start + num_cols]
                grid_cols = st.columns(len(chunk))
                for ind_idx, ind in enumerate(chunk):
                    with grid_cols[ind_idx]:
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

            # Special Salary Dynamics Deep Dive in Labour & Income domain
            if d_key == "LABOUR":
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("##### 💼 Wage Floor & Salary Structure Dynamics")
                
                mw_rows = df_country[df_country["indicator_id"] == "MINIMUM_MONTHLY_WAGE"].sort_values("period")
                net_rows = df_country[df_country["indicator_id"] == "AVG_NET_ANNUAL_SALARY"].sort_values("period")

                if not mw_rows.empty and not net_rows.empty:
                    latest_mw = mw_rows.iloc[-1]["value"]
                    latest_net_annual = net_rows.iloc[-1]["value"]
                    latest_net_monthly = latest_net_annual / 12.0
                    kaitz_ratio = (latest_mw / latest_net_monthly) * 100.0

                    s_col1, s_col2, s_col3 = st.columns(3)
                    with s_col1:
                        st.metric(
                            label="Kaitz Index (Min Wage / Avg Monthly Net)",
                            value=f"{kaitz_ratio:.1f} %",
                            help="National statutory minimum monthly wage as a proportion of estimated average net monthly earnings."
                        )
                    with s_col2:
                        st.metric(
                            label="Estimated Monthly Net Take-Home Salary",
                            value=f"€{latest_net_monthly:,.2f}",
                            help="Average net annual salary divided by 12 months."
                        )
                    with s_col3:
                        c_sal_2000 = net_rows.iloc[0]["value"]
                        tot_growth = ((latest_net_annual - c_sal_2000) / c_sal_2000) * 100.0
                        st.metric(
                            label=f"Total Net Salary Growth ({int(net_rows.iloc[0]['period'])}-{int(net_rows.iloc[-1]['period'])})",
                            value=f"+{tot_growth:.1f} %",
                            help="Cumulative net salary growth since reference start period."
                        )

            st.markdown("<br>", unsafe_allow_html=True)

            # Interactive Trend Comparison Engine (Country vs Benchmark)
            c_chart_sel, c_chart_mode = st.columns([3, 1])
            with c_chart_sel:
                ind_to_plot = st.selectbox(
                    f"Select Indicator to Chart ({d_meta['name']}):",
                    [i["id"] for i in domain_indicators],
                    format_func=lambda k: INDICATORS[k]["name"],
                    key=f"country_tab_chart_select_{d_key}"
                )
            with c_chart_mode:
                view_mode = st.radio(
                    "Chart View Mode:",
                    ["Actual Values", "Indexed Trajectory (Base=100)"],
                    key=f"country_chart_mode_{d_key}"
                )

            # Chart Creation
            if view_mode == "Actual Values":
                fig_trend = create_time_series_chart(
                    df_obs=df_obs,
                    indicator_id=ind_to_plot,
                    selected_countries=[selected_iso3, benchmark_target],
                    start_year=start_year,
                    end_year=end_year
                )
            else:
                # Indexed growth trajectory (Base Year = 100)
                sub_df = df_obs[
                    (df_obs["indicator_id"] == ind_to_plot) &
                    (df_obs["country_code"].isin([selected_iso3, benchmark_target])) &
                    (df_obs["period"] >= start_year) &
                    (df_obs["period"] <= end_year)
                ].copy()

                if not sub_df.empty:
                    # Normalize each country to 100 at start_year
                    indexed_records = []
                    for c_code, c_group in sub_df.groupby("country_code"):
                        c_group = c_group.sort_values("period")
                        base_val = c_group.iloc[0]["value"]
                        if base_val != 0:
                            c_group["indexed_value"] = (c_group["value"] / base_val) * 100.0
                        else:
                            c_group["indexed_value"] = 100.0
                        indexed_records.append(c_group)
                    
                    df_indexed = pd.concat(indexed_records)
                    df_indexed["country_label"] = df_indexed["country_code"].apply(
                        lambda c: f"{get_country_flag(c)} {get_country_name(c)}"
                    )

                    ind_meta_p = INDICATORS.get(ind_to_plot, {})
                    fig_trend = px.line(
                        df_indexed,
                        x="period",
                        y="indexed_value",
                        color="country_label",
                        markers=True,
                        title=f"{ind_meta_p.get('name', ind_to_plot)} — Cumulative Growth Index ({start_year}=100)",
                        labels={"period": "Year", "indexed_value": f"Index ({start_year}=100)", "country_label": "Country / Benchmark"},
                        color_discrete_sequence=COLOR_PALETTE
                    )
                    fig_trend.update_layout(**LAYOUT_TEMPLATE)
                    fig_trend.update_traces(line=dict(width=2.5), marker=dict(size=6))
                else:
                    fig_trend = go.Figure()
                    fig_trend.update_layout(**LAYOUT_TEMPLATE, title="No data available for index trajectory")

            st.plotly_chart(fig_trend, use_container_width=True)

            # Domain Historical Records Table & Download
            df_dom_obs = df_country_horizon[df_country_horizon["indicator_id"].isin([i["id"] for i in domain_indicators])].copy()
            if not df_dom_obs.empty:
                st.markdown("##### Detailed Historical Records")
                pivoted = df_dom_obs.pivot(index="period", columns="indicator_id", values="value").sort_index(ascending=False)
                # Rename columns to short names for readability
                pivoted.columns = [INDICATORS[col]["short_name"] if col in INDICATORS else col for col in pivoted.columns]
                st.dataframe(pivoted, use_container_width=True)
                render_csv_download_button(df_dom_obs, f"{selected_iso3}_{d_key}_{start_year}_{end_year}_data")

    st.markdown("<br>", unsafe_allow_html=True)

    # 4. Complete Country Statistical Dossier (All 18 Indicators Export)
    with st.expander(f"📁 Download Complete National Statistical Dossier ({meta.get('name')} — All 18 Indicators)", expanded=False):
        st.markdown(f"Access complete official time series observations for **{meta.get('name')}** across all 18 European Policy indicators from **{start_year} to {end_year}**.")
        
        full_pivoted = df_country_horizon.pivot(index="period", columns="indicator_id", values="value").sort_index(ascending=False)
        full_pivoted.columns = [INDICATORS[col]["name"] if col in INDICATORS else col for col in full_pivoted.columns]
        st.dataframe(full_pivoted, use_container_width=True, height=400)
        
        render_csv_download_button(
            df_country_horizon,
            filename=f"dossier_{selected_iso3}_all_indicators_{start_year}_{end_year}",
            label=f"📥 Download Full {meta.get('name')} Statistical Dossier (CSV)"
        )

