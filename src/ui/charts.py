"""
Plotly Chart Builders for European Policy Analytics.
Provides research-grade, interactive time series, bar comparisons, scatter plots, and maps.
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import List, Optional, Dict, Any
from src.metadata.indicators import INDICATORS
from src.metadata.countries import get_country_name, get_country_flag

# Professional Dark Color Palette
COLOR_PALETTE = [
    "#38bdf8", "#818cf8", "#34d399", "#fbbf24", "#f87171",
    "#c084fc", "#f472b6", "#2dd4bf", "#fb923c", "#a3e635"
]

LAYOUT_TEMPLATE = {
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(15, 23, 42, 0.6)",
    "font": {"color": "#cbd5e1", "family": "-apple-system, BlinkMacSystemFont, Segoe UI, Roboto"},
    "xaxis": {"gridcolor": "#1e293b", "zerolinecolor": "#334155"},
    "yaxis": {"gridcolor": "#1e293b", "zerolinecolor": "#334155"},
    "margin": {"l": 40, "r": 40, "t": 50, "b": 40}
}

def create_time_series_chart(
    df_obs: pd.DataFrame,
    indicator_id: str,
    selected_countries: List[str],
    start_year: int = 2000,
    end_year: int = 2025
) -> go.Figure:
    """
    Builds multi-country time series line chart.
    """
    meta = INDICATORS.get(indicator_id, {})
    title_text = f"{meta.get('name', indicator_id)} ({start_year} - {end_year})"

    df_filtered = df_obs[
        (df_obs["indicator_id"] == indicator_id) &
        (df_obs["country_code"].isin(selected_countries)) &
        (df_obs["period"] >= start_year) &
        (df_obs["period"] <= end_year)
    ].copy()

    if df_filtered.empty:
        fig = go.Figure()
        fig.update_layout(**LAYOUT_TEMPLATE, title=title_text + " (No Data Available)")
        return fig

    df_filtered["country_label"] = df_filtered["country_code"].apply(
        lambda c: f"{get_country_flag(c)} {get_country_name(c)}"
    )
    df_filtered = df_filtered.sort_values(by="period")

    fig = px.line(
        df_filtered,
        x="period",
        y="value",
        color="country_label",
        markers=True,
        title=title_text,
        labels={
            "period": "Reference Year",
            "value": f"Unit: {meta.get('unit_symbol', '')}",
            "country_label": "Country / Region"
        },
        color_discrete_sequence=COLOR_PALETTE
    )

    fig.update_layout(**LAYOUT_TEMPLATE)
    fig.update_traces(line=dict(width=2.5), marker=dict(size=6))
    return fig

def create_bar_comparison_chart(
    df_rankings: pd.DataFrame,
    indicator_id: str,
    period: int,
    top_n: Optional[int] = None
) -> go.Figure:
    """
    Builds horizontal bar chart for cross-country comparisons & rankings.
    """
    meta = INDICATORS.get(indicator_id, {})
    title_text = f"{meta.get('name', indicator_id)} by Country ({period})"

    if df_rankings.empty:
        fig = go.Figure()
        fig.update_layout(**LAYOUT_TEMPLATE, title=title_text + " (No Data Available)")
        return fig

    df_plot = df_rankings.copy()
    if top_n:
        df_plot = df_plot.head(top_n)

    # Sort so highest values are at top of horizontal bar chart
    df_plot = df_plot.sort_values(by="value", ascending=True)

    fig = px.bar(
        df_plot,
        x="value",
        y="country_name",
        orientation="h",
        title=title_text,
        text="value",
        labels={"value": f"Unit: {meta.get('unit_symbol', '')}", "country_name": "Country"},
        color="value",
        color_continuous_scale="Blues" if meta.get("better_direction") == "high" else "Reds_r"
    )

    fig.update_layout(**LAYOUT_TEMPLATE, coloraxis_showscale=False)
    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    return fig

def create_scatter_relationship_chart(
    df_aligned: pd.DataFrame,
    indicator_x: str,
    indicator_y: str,
    period: int,
    stats_info: Dict[str, Any]
) -> go.Figure:
    """
    Builds scatter plot with linear trendline for exploring relationships.
    """
    meta_x = INDICATORS.get(indicator_x, {})
    meta_y = INDICATORS.get(indicator_y, {})

    title_text = f"Relationship: {meta_y.get('short_name', indicator_y)} vs {meta_x.get('short_name', indicator_x)} ({period})<br>" \
                 f"<sup>Pearson r = {stats_info.get('r')}, R² = {stats_info.get('r_squared')}, p = {stats_info.get('p_value')}</sup>"

    if df_aligned.empty:
        fig = go.Figure()
        fig.update_layout(**LAYOUT_TEMPLATE, title=title_text + " (No Data Available)")
        return fig

    fig = px.scatter(
        df_aligned,
        x="x_value",
        y="y_value",
        text="country_label",
        trendline="ols",
        title=title_text,
        labels={
            "x_value": f"{meta_x.get('name', indicator_x)} ({meta_x.get('unit_symbol', '')})",
            "y_value": f"{meta_y.get('name', indicator_y)} ({meta_y.get('unit_symbol', '')})"
        },
        color_discrete_sequence=["#38bdf8"]
    )

    fig.update_layout(**LAYOUT_TEMPLATE)
    fig.update_traces(textposition='top center', marker=dict(size=10, opacity=0.85))
    return fig

def create_europe_map_chart(
    df_obs: pd.DataFrame,
    indicator_id: str,
    period: int
) -> go.Figure:
    """
    Builds interactive Choropleth Map for European countries using real ISO-3 locations.
    """
    meta = INDICATORS.get(indicator_id, {})
    title_text = f"European Map: {meta.get('name', indicator_id)} ({period})"

    df_filtered = df_obs[
        (df_obs["indicator_id"] == indicator_id) &
        (df_obs["period"] == period)
    ].copy()

    if df_filtered.empty:
        fig = go.Figure()
        fig.update_layout(**LAYOUT_TEMPLATE, title=title_text + " (No Data Available)")
        return fig

    fig = px.choropleth(
        df_filtered,
        locations="country_code",
        locationmode="ISO-3",
        color="value",
        hover_name="country_code",
        title=title_text,
        labels={"value": meta.get("unit_symbol", "Value")},
        color_continuous_scale="Viridis",
        scope="europe"
    )

    fig.update_layout(
        **LAYOUT_TEMPLATE,
        geo=dict(
            scope="europe",
            showframe=False,
            showcoastlines=True,
            coastlinecolor="#334155",
            bgcolor="rgba(0,0,0,0)",
            landcolor="#1e293b"
        )
    )
    return fig

def create_radar_chart(
    country_name: str,
    categories: List[str],
    country_scores: List[float],
    benchmark_name: str = "EU-27 Benchmark",
    benchmark_scores: Optional[List[float]] = None
) -> go.Figure:
    """
    Builds multidimensional radar (spider) chart comparing country vs benchmark.
    Scores normalized on a 0-100 scale.
    """
    fig = go.Figure()

    # Close polygon by repeating first value
    cats_loop = categories + [categories[0]]
    country_loop = country_scores + [country_scores[0]]

    fig.add_trace(go.Scatterpolar(
        r=country_loop,
        theta=cats_loop,
        fill='toself',
        fillcolor='rgba(56, 189, 248, 0.3)',
        line=dict(color='#38bdf8', width=2.5),
        name=country_name
    ))

    if benchmark_scores:
        bench_loop = benchmark_scores + [benchmark_scores[0]]
        fig.add_trace(go.Scatterpolar(
            r=bench_loop,
            theta=cats_loop,
            fill='toself',
            fillcolor='rgba(251, 191, 36, 0.15)',
            line=dict(color='#fbbf24', width=2, dash='dot'),
            name=benchmark_name
        ))

    fig.update_layout(
        **LAYOUT_TEMPLATE,
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor="#1e293b",
                linecolor="#334155",
                tickfont=dict(size=10, color="#94a3b8")
            ),
            angularaxis=dict(
                gridcolor="#1e293b",
                linecolor="#334155",
                tickfont=dict(size=12, color="#f8fafc")
            ),
            bgcolor="rgba(15, 23, 42, 0.6)"
        ),
        showlegend=True,
        title=f"Policy Performance Profile: {country_name} vs {benchmark_name}"
    )
    return fig

