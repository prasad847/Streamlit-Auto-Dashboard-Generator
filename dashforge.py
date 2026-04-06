# ============================================================
# DashForge — Intelligent Dashboard Generator
# ============================================================
# streamlit run dashforge.py
# pip install streamlit pandas plotly openpyxl numpy
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json
import io
from datetime import datetime

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DashForge — Dashboard Generator",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────
# DESIGN SYSTEM — Light, editorial, warm cream + coral accents
# Inspired by modern SaaS aesthetics: lots of white space,
# strong typography, subtle warm tones, crisp cards
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

:root {
  --cream:     #faf8f4;
  --cream2:    #f3f0ea;
  --cream3:    #ede9e0;
  --white:     #ffffff;
  --coral:     #e8633a;
  --coral-lt:  #fbeee8;
  --coral-mid: #f5a58a;
  --teal:      #2a7b6f;
  --teal-lt:   #e6f4f1;
  --navy:      #1a2332;
  --text:      #1a2332;
  --muted:     #6b7280;
  --muted2:    #9ca3af;
  --border:    #e8e3d8;
  --border2:   #d4cfc4;
  --shadow:    0 1px 3px rgba(26,35,50,0.06), 0 4px 16px rgba(26,35,50,0.04);
  --shadow-lg: 0 4px 24px rgba(26,35,50,0.10);
  --r:         12px;
  --r-sm:      8px;
  --font:      'DM Sans', sans-serif;
  --serif:     'Instrument Serif', serif;
  --mono:      'DM Mono', monospace;
}

/* ── RESET ── */
* { box-sizing: border-box; }

.stApp {
  background: var(--cream) !important;
  font-family: var(--font) !important;
  color: var(--text) !important;
}

/* ── HIDE STREAMLIT CHROME ── */
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] { display: none !important; }

.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--cream2); }
::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 4px; }

/* ── SIDEBAR ── */
section[data-testid="stSidebar"] {
  background: var(--white) !important;
  border-right: 1px solid var(--border) !important;
  padding-top: 0 !important;
}
section[data-testid="stSidebar"] > div {
  padding-top: 0 !important;
}
[data-testid="stSidebarContent"] {
  padding: 0 !important;
}

/* ── BUTTONS ── */
.stButton > button {
  background: var(--coral) !important;
  color: #fff !important;
  border: none !important;
  border-radius: var(--r-sm) !important;
  font-family: var(--font) !important;
  font-weight: 600 !important;
  font-size: 14px !important;
  padding: 10px 22px !important;
  transition: all 0.18s !important;
  box-shadow: 0 1px 3px rgba(232,99,58,0.25) !important;
}
.stButton > button:hover {
  background: #d4522a !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 4px 12px rgba(232,99,58,0.3) !important;
}

/* ── FILE UPLOADER ── */
.stFileUploader > div {
  background: var(--white) !important;
  border: 2px dashed var(--border2) !important;
  border-radius: var(--r) !important;
  transition: border-color 0.2s !important;
}
.stFileUploader > div:hover {
  border-color: var(--coral-mid) !important;
}

/* ── INPUTS ── */
.stTextInput > div > div > input,
.stSelectbox > div > div,
.stMultiSelect > div > div {
  background: var(--white) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--r-sm) !important;
  color: var(--text) !important;
  font-family: var(--font) !important;
  font-size: 14px !important;
}
.stTextInput > div > div > input:focus {
  border-color: var(--coral) !important;
  box-shadow: 0 0 0 3px rgba(232,99,58,0.1) !important;
}

/* ── RADIO ── */
.stRadio > div {
  gap: 8px;
}
.stRadio label {
  background: var(--white) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--r-sm) !important;
  padding: 10px 18px !important;
  cursor: pointer !important;
  transition: all 0.15s !important;
  font-size: 14px !important;
  font-weight: 500 !important;
}
.stRadio label:hover { border-color: var(--coral-mid) !important; }

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
  background: var(--cream2) !important;
  border-radius: var(--r-sm) !important;
  padding: 4px !important;
  gap: 2px !important;
  border: 1px solid var(--border) !important;
}
.stTabs [data-baseweb="tab"] {
  background: transparent !important;
  color: var(--muted) !important;
  border-radius: 6px !important;
  font-family: var(--font) !important;
  font-size: 13px !important;
  font-weight: 500 !important;
}
.stTabs [aria-selected="true"] {
  background: var(--white) !important;
  color: var(--coral) !important;
  box-shadow: var(--shadow) !important;
}

/* ── METRICS ── */
[data-testid="metric-container"] {
  background: var(--white) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--r) !important;
  padding: 20px !important;
  box-shadow: var(--shadow) !important;
}
[data-testid="metric-container"] label {
  color: var(--muted) !important;
  font-family: var(--font) !important;
  font-size: 11px !important;
  font-weight: 600 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.5px !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
  color: var(--text) !important;
  font-family: var(--font) !important;
  font-weight: 700 !important;
  font-size: 26px !important;
}

/* ── SUCCESS / INFO / WARNING ── */
.stSuccess {
  background: var(--teal-lt) !important;
  border-left: 3px solid var(--teal) !important;
  border-radius: var(--r-sm) !important;
  color: var(--teal) !important;
}
.stInfo {
  background: #eff6ff !important;
  border-left: 3px solid #3b82f6 !important;
  border-radius: var(--r-sm) !important;
}
.stWarning {
  background: #fefce8 !important;
  border-left: 3px solid #eab308 !important;
  border-radius: var(--r-sm) !important;
}

/* ── DATAFRAME ── */
[data-testid="stDataFrame"] {
  border: 1px solid var(--border) !important;
  border-radius: var(--r) !important;
  overflow: hidden !important;
}

h1,h2,h3 {
  font-family: var(--font) !important;
  color: var(--text) !important;
}

/* ── SIDEBAR SELECT ── */
section[data-testid="stSidebar"] .stSelectbox > div > div {
  background: var(--cream) !important;
}
section[data-testid="stSidebar"] .stMultiSelect > div > div {
  background: var(--cream) !important;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# PLOTLY THEME — warm light palette
# ─────────────────────────────────────────────────────────────
CHART_COLORS = [
    "#e8633a", "#2a7b6f", "#f59e0b", "#6366f1",
    "#ec4899", "#10b981", "#f97316", "#8b5cf6",
    "#0ea5e9", "#84cc16"
]

def chart_layout(title=""):
    return dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#ffffff",
        font=dict(family="DM Sans, sans-serif", color="#1a2332", size=12),
        title=dict(text=title, font=dict(size=14, color="#1a2332", family="DM Sans"), x=0, pad=dict(l=4)),
        margin=dict(l=16, r=16, t=40 if title else 20, b=16),
        xaxis=dict(gridcolor="#f0ede6", gridwidth=1, linecolor="#e8e3d8",
                   tickfont=dict(size=11, color="#6b7280")),
        yaxis=dict(gridcolor="#f0ede6", gridwidth=1, linecolor="#e8e3d8",
                   tickfont=dict(size=11, color="#6b7280")),
        showlegend=True,
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
        colorway=CHART_COLORS,
    )


# ─────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────
def init_state():
    defaults = dict(
        raw_df=None,
        filename="",
        auto_config=None,       # auto-generated dashboard config
        custom_config=None,     # user-customized config
        active_config=None,     # whichever is being shown
        flow_step="upload",     # upload → auto_shown → customize → final
        custom_step=0,          # sub-step within customization
        custom_wip=dict(        # work-in-progress custom config
            title="My Dashboard",
            kpis=[],
            charts=[],
            filters=[],
        ),
    )
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()


# ─────────────────────────────────────────────────────────────
# COLUMN CLASSIFIER
# ─────────────────────────────────────────────────────────────
def classify_columns(df):
    numeric   = df.select_dtypes(include="number").columns.tolist()
    cat_raw   = df.select_dtypes(include=["object", "category"]).columns.tolist()
    dt_raw    = df.select_dtypes(include=["datetime64"]).columns.tolist()

    # Try to coerce object cols with 'date'/'time' in name to datetime
    for col in cat_raw[:]:
        if any(k in col.lower() for k in ["date","time","year","month","day","period"]):
            try:
                df[col] = pd.to_datetime(df[col], errors="coerce")
                if df[col].notna().sum() > 0.5 * len(df):
                    dt_raw.append(col)
                    cat_raw.remove(col)
            except Exception:
                pass

    # Categorical: only cols with sensible cardinality
    categorical = [c for c in cat_raw if 2 <= df[c].nunique() <= 50]
    datetime_cols = dt_raw

    return numeric, categorical, datetime_cols


# ─────────────────────────────────────────────────────────────
# SMART COLUMN SCORER — picks best numeric columns
# ─────────────────────────────────────────────────────────────
def score_numeric_cols(df, numeric_cols):
    scored = []
    for col in numeric_cols:
        series = df[col].dropna()
        if len(series) == 0:
            continue
        completeness = df[col].notna().sum() / len(df)
        if completeness < 0.70:
            continue
        # Coefficient of variation — higher = more interesting
        mean = series.mean()
        cv   = (series.std() / mean) if mean != 0 else 0
        score = completeness * 0.4 + min(abs(cv), 3) * 0.6
        scored.append((col, score, completeness, cv))
    scored.sort(key=lambda x: -x[1])
    return [s[0] for s in scored]


# ─────────────────────────────────────────────────────────────
# AUTO DASHBOARD CONFIG GENERATOR
# ─────────────────────────────────────────────────────────────
def auto_generate_config(df, filename=""):
    numeric, categorical, datetime_cols = classify_columns(df)
    top_numeric = score_numeric_cols(df, numeric)

    config = {
        "title":   filename.replace(".csv","").replace(".xlsx","").replace("_"," ").replace("-"," ").title() or "Auto Dashboard",
        "kpis":    [],
        "charts":  [],
        "filters": [],
    }

    # ── KPIs ──
    config["kpis"].append({"label": "Total Records", "value": len(df), "format": "int"})

    for col in top_numeric[:2]:
        series = df[col].dropna()
        total  = series.sum()
        avg    = series.mean()
        config["kpis"].append({
            "label":  f"Total {col[:22]}",
            "col":    col,
            "agg":    "sum",
            "format": "number",
        })
        config["kpis"].append({
            "label":  f"Avg {col[:24]}",
            "col":    col,
            "agg":    "mean",
            "format": "number",
        })
    config["kpis"] = config["kpis"][:4]  # max 4

    # ── CHARTS ──
    # (1) Bar chart — best categorical × best numeric
    if categorical and top_numeric:
        best_cat = next((c for c in categorical if df[c].nunique() < 15), None)
        if best_cat:
            config["charts"].append({
                "type":  "bar",
                "title": f"{top_numeric[0]} by {best_cat}",
                "x":     best_cat,
                "y":     top_numeric[0],
                "agg":   "sum",
            })

    # (2) Line chart — datetime × top numeric
    if datetime_cols and top_numeric:
        config["charts"].append({
            "type":  "line",
            "title": f"{top_numeric[0]} over time",
            "x":     datetime_cols[0],
            "y":     top_numeric[0],
            "agg":   "sum",
        })

    # (3) Histogram — top numeric
    if top_numeric:
        config["charts"].append({
            "type":  "histogram",
            "title": f"Distribution of {top_numeric[0]}",
            "x":     top_numeric[0],
        })

    # (4) Pie — only if small cardinality categorical
    if categorical:
        pie_col = next((c for c in categorical if df[c].nunique() <= 6), None)
        if pie_col and top_numeric:
            config["charts"].append({
                "type":  "pie",
                "title": f"{top_numeric[0]} share by {pie_col}",
                "names": pie_col,
                "values": top_numeric[0],
                "agg":   "sum",
            })

    # (5) Second bar if we have another numeric
    if len(top_numeric) > 1 and categorical:
        best_cat = next((c for c in categorical if df[c].nunique() < 15), None)
        if best_cat and len(config["charts"]) < 5:
            config["charts"].append({
                "type":  "bar",
                "title": f"{top_numeric[1]} by {best_cat}",
                "x":     best_cat,
                "y":     top_numeric[1],
                "agg":   "mean",
            })

    config["charts"] = config["charts"][:5]

    # ── FILTERS ──
    for col in categorical:
        if 2 <= df[col].nunique() <= 20:
            config["filters"].append(col)
        if len(config["filters"]) >= 4:
            break

    return config


# ─────────────────────────────────────────────────────────────
# APPLY FILTERS
# ─────────────────────────────────────────────────────────────
def apply_filters(df, config, filter_selections):
    dff = df.copy()
    for col, val in filter_selections.items():
        if val and "All" not in val:
            dff = dff[dff[col].isin(val)]
    return dff


# ─────────────────────────────────────────────────────────────
# KPI VALUE COMPUTER
# ─────────────────────────────────────────────────────────────
def compute_kpi(df, kpi):
    if "value" in kpi:
        return kpi["value"]
    col = kpi.get("col")
    agg = kpi.get("agg","sum")
    if not col or col not in df.columns:
        return "—"
    series = df[col].dropna()
    if agg == "sum":   return series.sum()
    if agg == "mean":  return series.mean()
    if agg == "count": return series.count()
    if agg == "max":   return series.max()
    if agg == "min":   return series.min()
    return "—"

def fmt_kpi(val, fmt="number"):
    if val == "—": return "—"
    try:
        v = float(val)
        if fmt == "int": return f"{int(v):,}"
        if v >= 1_000_000: return f"{v/1_000_000:.2f}M"
        if v >= 1_000:     return f"{v/1_000:.1f}K"
        return f"{v:,.2f}"
    except Exception:
        return str(val)


# ─────────────────────────────────────────────────────────────
# CHART RENDERER
# ─────────────────────────────────────────────────────────────
def render_chart(dff, chart):
    ctype = chart.get("type","bar")
    title = chart.get("title","")

    try:
        if ctype == "bar":
            x, y = chart["x"], chart["y"]
            agg   = chart.get("agg","sum")
            if x not in dff.columns or y not in dff.columns:
                st.caption(f"⚠ Column not found: {x} or {y}"); return
            grouped = dff.groupby(x)[y].agg(agg).reset_index().sort_values(y, ascending=False).head(20)
            fig = px.bar(grouped, x=x, y=y, color=x, color_discrete_sequence=CHART_COLORS,
                         title=title)
            fig.update_layout(**chart_layout(title))
            fig.update_traces(marker_line_width=0)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        elif ctype == "line":
            x, y = chart["x"], chart["y"]
            agg   = chart.get("agg","sum")
            if x not in dff.columns or y not in dff.columns:
                st.caption(f"⚠ Column not found: {x} or {y}"); return
            dff2 = dff.copy()
            try:
                dff2[x] = pd.to_datetime(dff2[x], errors="coerce")
                dff2 = dff2.dropna(subset=[x]).sort_values(x)
                grouped = dff2.groupby(dff2[x].dt.to_period("M").astype(str))[y].agg(agg).reset_index()
            except Exception:
                grouped = dff2[[x, y]].dropna().head(50)
            fig = px.line(grouped, x=x, y=y, title=title,
                          color_discrete_sequence=[CHART_COLORS[0]])
            fig.update_layout(**chart_layout(title))
            fig.update_traces(line_width=2.5, fill="tozeroy",
                              fillcolor="rgba(232,99,58,0.07)")
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        elif ctype == "histogram":
            x = chart["x"]
            if x not in dff.columns:
                st.caption(f"⚠ Column not found: {x}"); return
            fig = px.histogram(dff, x=x, title=title,
                               color_discrete_sequence=[CHART_COLORS[0]])
            fig.update_layout(**chart_layout(title))
            fig.update_traces(marker_line_width=0, marker_line_color="white")
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        elif ctype == "pie":
            names  = chart.get("names")
            values = chart.get("values")
            agg    = chart.get("agg","sum")
            if not names or not values:
                st.caption("⚠ Pie chart config missing names/values"); return
            if names not in dff.columns or values not in dff.columns:
                st.caption(f"⚠ Column not found: {names} or {values}"); return
            grouped = dff.groupby(names)[values].agg(agg).reset_index().head(8)
            fig = px.pie(grouped, names=names, values=values, title=title,
                         color_discrete_sequence=CHART_COLORS, hole=0.45)
            fig.update_layout(**chart_layout(title))
            fig.update_traces(textfont_size=12,
                              marker_line_width=2, marker_line_color="white")
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        elif ctype == "scatter":
            x, y = chart["x"], chart["y"]
            color = chart.get("color")
            if x not in dff.columns or y not in dff.columns:
                st.caption(f"⚠ Column not found: {x} or {y}"); return
            fig = px.scatter(dff.sample(min(2000,len(dff))), x=x, y=y,
                             color=color if color and color in dff.columns else None,
                             title=title, color_discrete_sequence=CHART_COLORS,
                             opacity=0.65)
            fig.update_layout(**chart_layout(title))
            fig.update_traces(marker_size=6)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    except Exception as e:
        st.caption(f"⚠ Chart error: {e}")


# ─────────────────────────────────────────────────────────────
# DASHBOARD RENDERER (full page)
# ─────────────────────────────────────────────────────────────
def render_dashboard(df, config, filter_selections=None):
    if filter_selections is None:
        filter_selections = {}

    dff = apply_filters(df, config, filter_selections)

    # ── Dashboard title ──
    st.markdown(f"""
    <div style="padding: 28px 0 20px 0; border-bottom: 1px solid #e8e3d8; margin-bottom: 28px;">
      <div style="font-size:11px;font-weight:700;letter-spacing:2px;text-transform:uppercase;
           color:#e8633a;margin-bottom:6px;font-family:'DM Sans',sans-serif;">Dashboard</div>
      <div style="font-family:'Instrument Serif',serif;font-size:32px;color:#1a2332;
           line-height:1.1;font-style:italic;">{config.get('title','Dashboard')}</div>
      <div style="font-size:12px;color:#9ca3af;margin-top:5px;">
        {len(dff):,} records
        {f"<span style='margin:0 6px;'>·</span> Filtered from {len(df):,}" if len(dff) < len(df) else ""}
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── KPI cards ──
    kpis = config.get("kpis", [])
    if kpis:
        kpi_cols = st.columns(len(kpis))
        kpi_accent = ["#e8633a","#2a7b6f","#6366f1","#f59e0b"]
        for i, kpi in enumerate(kpis):
            val = compute_kpi(dff, kpi)
            disp = fmt_kpi(val, kpi.get("format","number"))
            acc = kpi_accent[i % len(kpi_accent)]
            with kpi_cols[i]:
                st.markdown(f"""
                <div style="background:#fff;border:1px solid #e8e3d8;border-radius:12px;
                     padding:20px 22px;box-shadow:0 1px 4px rgba(26,35,50,0.06);
                     border-top:3px solid {acc};">
                  <div style="font-size:10px;font-weight:700;letter-spacing:1px;text-transform:uppercase;
                       color:#9ca3af;margin-bottom:10px;">{kpi.get('label','Metric')}</div>
                  <div style="font-size:28px;font-weight:700;color:#1a2332;
                       letter-spacing:-1px;line-height:1;">{disp}</div>
                  <div style="font-size:11px;color:#9ca3af;margin-top:5px;">
                    {kpi.get('agg','').title() if kpi.get('agg') else 'Count'}
                  </div>
                </div>
                """, unsafe_allow_html=True)

    # ── Charts grid ──
    charts = config.get("charts", [])
    if not charts:
        st.markdown("""
        <div style="text-align:center;padding:60px;color:#9ca3af;">
          No charts configured yet.
        </div>
        """, unsafe_allow_html=True)
        return

    # Responsive 2-col grid
    for i in range(0, len(charts), 2):
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"""
            <div style="background:#fff;border:1px solid #e8e3d8;border-radius:12px;
                 padding:20px;box-shadow:0 1px 4px rgba(26,35,50,0.06);margin-bottom:16px;">
            """, unsafe_allow_html=True)
            render_chart(dff, charts[i])
            st.markdown("</div>", unsafe_allow_html=True)
        if i + 1 < len(charts):
            with c2:
                st.markdown(f"""
                <div style="background:#fff;border:1px solid #e8e3d8;border-radius:12px;
                     padding:20px;box-shadow:0 1px 4px rgba(26,35,50,0.06);margin-bottom:16px;">
                """, unsafe_allow_html=True)
                render_chart(dff, charts[i+1])
                st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# SIDEBAR — LOGO + FILTERS
# ─────────────────────────────────────────────────────────────
def render_sidebar(df, config):
    with st.sidebar:
        # Logo
        st.markdown("""
        <div style="padding:24px 20px 20px;border-bottom:1px solid #e8e3d8;">
          <div style="font-family:'Instrument Serif',serif;font-size:22px;
               color:#1a2332;font-style:italic;margin-bottom:2px;">
            ⬡ DashForge
          </div>
          <div style="font-size:11px;color:#9ca3af;letter-spacing:0.3px;">Dashboard Generator</div>
        </div>
        """, unsafe_allow_html=True)

        filter_selections = {}

        filters = config.get("filters", [])
        if filters and df is not None:
            st.markdown("""
            <div style="padding:16px 20px 8px;font-size:10px;font-weight:700;
                 letter-spacing:2px;text-transform:uppercase;color:#9ca3af;">Filters</div>
            """, unsafe_allow_html=True)
            with st.container():
                for col in filters:
                    if col in df.columns:
                        options = ["All"] + sorted(df[col].dropna().unique().astype(str).tolist())
                        sel = st.multiselect(col, options, default=["All"], key=f"filter_{col}")
                        filter_selections[col] = sel
        else:
            st.markdown("""
            <div style="padding:20px;color:#9ca3af;font-size:13px;">
              No filters available yet. Upload a dataset to get started.
            </div>
            """, unsafe_allow_html=True)

        # Dataset info at bottom
        if df is not None:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f"""
            <div style="padding:14px 20px;background:#faf8f4;border-radius:10px;
                 margin:0 4px;border:1px solid #e8e3d8;">
              <div style="font-size:10px;font-weight:700;text-transform:uppercase;
                   letter-spacing:1px;color:#9ca3af;margin-bottom:8px;">Dataset</div>
              <div style="font-size:12px;color:#6b7280;line-height:1.8;">
                <div>📄 {st.session_state.filename}</div>
                <div>⬢ {df.shape[0]:,} rows</div>
                <div>◫ {df.shape[1]} columns</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

        return filter_selections


# ─────────────────────────────────────────────────────────────
# CUSTOMIZATION WIZARD — step-by-step guided flow
# ─────────────────────────────────────────────────────────────
def render_customization_wizard(df):
    numeric, categorical, datetime_cols = classify_columns(df)
    top_numeric = score_numeric_cols(df, numeric)
    wip = st.session_state.custom_wip
    step = st.session_state.custom_step

    # Step header
    steps = ["Dashboard Name", "KPI Builder", "Chart Builder", "Filters", "Preview & Save"]
    step_labels = [f"{'✓' if i < step else str(i+1)}. {s}" for i, s in enumerate(steps)]

    st.markdown(f"""
    <div style="background:#fff;border:1px solid #e8e3d8;border-radius:12px;
         padding:20px 24px;margin-bottom:24px;box-shadow:0 1px 4px rgba(26,35,50,0.06);">
      <div style="font-size:11px;font-weight:700;letter-spacing:2px;text-transform:uppercase;
           color:#9ca3af;margin-bottom:12px;">Customization Wizard</div>
      <div style="display:flex;gap:8px;flex-wrap:wrap;">
    """, unsafe_allow_html=True)

    step_colors = []
    for i, label in enumerate(steps):
        if i < step:
            col = "#2a7b6f"; bg = "#e6f4f1"; txt = "✓ " + label
        elif i == step:
            col = "#e8633a"; bg = "#fbeee8"; txt = f"● {label}"
        else:
            col = "#9ca3af"; bg = "#f9f7f2"; txt = f"{i+1}. {label}"
        st.markdown(f"""
        <span style="padding:5px 14px;border-radius:100px;font-size:12px;font-weight:600;
             background:{bg};color:{col};border:1px solid {col}30;">
          {txt}
        </span>
        """, unsafe_allow_html=True)

    st.markdown("</div></div>", unsafe_allow_html=True)

    # ── STEP 0: Dashboard Name ──
    if step == 0:
        st.markdown("### What should we call this dashboard?")
        title = st.text_input("Dashboard title", value=wip.get("title","My Dashboard"), placeholder="e.g. Sales Overview Q4 2025")
        c1, c2 = st.columns([1,4])
        with c1:
            if st.button("Next →", key="step0_next"):
                if title.strip():
                    st.session_state.custom_wip["title"] = title.strip()
                    st.session_state.custom_step = 1
                    st.rerun()
                else:
                    st.warning("Please enter a dashboard name.")

    # ── STEP 1: KPI Builder ──
    elif step == 1:
        st.markdown("### Which metrics matter most to you?")
        st.caption("Select up to 4 KPIs. Each KPI = one number displayed prominently at the top.")

        kpis = wip.get("kpis", [])

        # Show existing KPIs
        if kpis:
            st.markdown("**Added KPIs:**")
            for i, kpi in enumerate(kpis):
                col_txt = kpi.get("col", "Count")
                agg_txt = kpi.get("agg", "")
                c1, c2 = st.columns([5,1])
                with c1:
                    st.markdown(f"""
                    <div style="background:#faf8f4;border:1px solid #e8e3d8;border-radius:8px;
                         padding:10px 16px;font-size:13px;color:#1a2332;">
                      📊 <b>{kpi.get('label','KPI')}</b>
                      <span style="color:#9ca3af;font-size:11px;margin-left:8px;">{agg_txt} of {col_txt}</span>
                    </div>
                    """, unsafe_allow_html=True)
                with c2:
                    if st.button("✕", key=f"del_kpi_{i}"):
                        kpis.pop(i)
                        st.session_state.custom_wip["kpis"] = kpis
                        st.rerun()

        if len(kpis) < 4:
            st.markdown("<br>**Add a KPI:**", unsafe_allow_html=True)
            k1, k2, k3, k4 = st.columns([3,2,2,1])
            with k1:
                kpi_col = st.selectbox("Column", ["Total Records"] + top_numeric, key="kpi_col_sel")
            with k2:
                agg_opts = ["count"] if kpi_col == "Total Records" else ["sum","mean","count","max","min"]
                kpi_agg = st.selectbox("Aggregation", agg_opts, key="kpi_agg_sel")
            with k3:
                auto_label = "Total Records" if kpi_col == "Total Records" else f"{kpi_agg.title()} {kpi_col[:20]}"
                kpi_label = st.text_input("Label", value=auto_label, key="kpi_label_sel")
            with k4:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("＋ Add", key="add_kpi"):
                    new_kpi = {"label": kpi_label}
                    if kpi_col == "Total Records":
                        new_kpi["value"] = len(df)
                        new_kpi["format"] = "int"
                    else:
                        new_kpi["col"]    = kpi_col
                        new_kpi["agg"]    = kpi_agg
                        new_kpi["format"] = "number"
                    kpis.append(new_kpi)
                    st.session_state.custom_wip["kpis"] = kpis
                    st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1,1,4])
        with c1:
            if st.button("← Back", key="step1_back"):
                st.session_state.custom_step = 0; st.rerun()
        with c2:
            if st.button("Next →", key="step1_next"):
                if not kpis:
                    # Auto-add total records if nothing added
                    st.session_state.custom_wip["kpis"] = [{"label":"Total Records","value":len(df),"format":"int"}]
                st.session_state.custom_step = 2; st.rerun()

    # ── STEP 2: Chart Builder ──
    elif step == 2:
        st.markdown("### Which charts do you want?")
        st.caption("Add up to 5 charts. Mix and match types based on your data.")

        charts = wip.get("charts", [])

        # Existing charts
        if charts:
            st.markdown("**Added charts:**")
            for i, chart in enumerate(charts):
                c1, c2 = st.columns([5,1])
                with c1:
                    ctype = chart.get("type","bar").title()
                    ctitle = chart.get("title","Chart")
                    icon = {"Bar":"📊","Line":"📈","Histogram":"📉","Pie":"🥧","Scatter":"✦"}.get(ctype,"📊")
                    st.markdown(f"""
                    <div style="background:#faf8f4;border:1px solid #e8e3d8;border-radius:8px;
                         padding:10px 16px;font-size:13px;color:#1a2332;">
                      {icon} <b>{ctitle}</b>
                      <span style="color:#9ca3af;font-size:11px;margin-left:8px;">{ctype}</span>
                    </div>
                    """, unsafe_allow_html=True)
                with c2:
                    if st.button("✕", key=f"del_chart_{i}"):
                        charts.pop(i)
                        st.session_state.custom_wip["charts"] = charts
                        st.rerun()

        if len(charts) < 5:
            st.markdown("<br>**Add a chart:**", unsafe_allow_html=True)
            chart_type = st.radio("Chart type", ["Bar","Line","Histogram","Pie","Scatter"],
                                  horizontal=True, key="chart_type_sel")

            all_cols = numeric + categorical
            ch1, ch2, ch3, ch4 = st.columns([2,2,2,2])

            new_chart = {"type": chart_type.lower()}

            if chart_type == "Bar":
                with ch1: cx = st.selectbox("X (Category)", categorical or all_cols, key="bar_x_sel")
                with ch2: cy = st.selectbox("Y (Numeric)", top_numeric or all_cols, key="bar_y_sel")
                with ch3: ca = st.selectbox("Aggregation", ["sum","mean","count","max","min"], key="bar_a_sel")
                new_chart.update({"x":cx,"y":cy,"agg":ca,"title":f"{cy} by {cx}"})

            elif chart_type == "Line":
                dt_opts = datetime_cols if datetime_cols else all_cols
                with ch1: cx = st.selectbox("X (Date/Time)", dt_opts, key="line_x_sel")
                with ch2: cy = st.selectbox("Y (Numeric)", top_numeric or all_cols, key="line_y_sel")
                with ch3: ca = st.selectbox("Aggregation", ["sum","mean"], key="line_a_sel")
                new_chart.update({"x":cx,"y":cy,"agg":ca,"title":f"{cy} over time"})

            elif chart_type == "Histogram":
                with ch1: cx = st.selectbox("Column", top_numeric or all_cols, key="hist_x_sel")
                new_chart.update({"x":cx,"title":f"Distribution of {cx}"})

            elif chart_type == "Pie":
                with ch1: cn = st.selectbox("Category", categorical or all_cols, key="pie_n_sel")
                with ch2: cv = st.selectbox("Value", top_numeric or all_cols, key="pie_v_sel")
                with ch3: ca = st.selectbox("Aggregation", ["sum","mean","count"], key="pie_a_sel")
                new_chart.update({"names":cn,"values":cv,"agg":ca,"title":f"{cv} by {cn}"})

            elif chart_type == "Scatter":
                with ch1: cx = st.selectbox("X", top_numeric or all_cols, key="sc_x_sel")
                with ch2: cy = st.selectbox("Y", top_numeric[1:] or all_cols, key="sc_y_sel")
                c_opts = ["None"] + categorical
                with ch3: cc = st.selectbox("Color by", c_opts, key="sc_c_sel")
                new_chart.update({"x":cx,"y":cy,"color":cc if cc!="None" else None,"title":f"{cx} vs {cy}"})

            with ch4:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("＋ Add", key="add_chart"):
                    charts.append(new_chart)
                    st.session_state.custom_wip["charts"] = charts
                    st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1,1,4])
        with c1:
            if st.button("← Back", key="step2_back"):
                st.session_state.custom_step = 1; st.rerun()
        with c2:
            if st.button("Next →", key="step2_next"):
                st.session_state.custom_step = 3; st.rerun()

    # ── STEP 3: Filters ──
    elif step == 3:
        st.markdown("### Which filters should users have?")
        st.caption("Select columns for sidebar filters. Best used with categorical columns.")

        all_filter_opts = [c for c in categorical if 2 <= df[c].nunique() <= 20]
        current_filters = wip.get("filters", [])

        if not all_filter_opts:
            st.info("No suitable filter columns found (need categorical columns with 2–20 unique values).")
            selected = []
        else:
            selected = st.multiselect(
                "Select filter columns",
                all_filter_opts,
                default=[c for c in current_filters if c in all_filter_opts],
                key="filter_sel"
            )
            for col in selected:
                st.markdown(f"""
                <div style="display:inline-flex;align-items:center;gap:6px;
                     background:#fbeee8;border:1px solid #f5a58a;border-radius:6px;
                     padding:4px 12px;font-size:12px;color:#e8633a;font-weight:600;margin:3px;">
                  🔽 {col} &nbsp;·&nbsp; {df[col].nunique()} values
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1,1,4])
        with c1:
            if st.button("← Back", key="step3_back"):
                st.session_state.custom_step = 2; st.rerun()
        with c2:
            if st.button("Preview →", key="step3_next"):
                st.session_state.custom_wip["filters"] = selected
                st.session_state.custom_step = 4; st.rerun()

    # ── STEP 4: Preview & Save ──
    elif step == 4:
        st.markdown("### Your custom dashboard is ready!")

        config_summary = {
            "title":   wip.get("title"),
            "kpis":    len(wip.get("kpis",[])),
            "charts":  len(wip.get("charts",[])),
            "filters": len(wip.get("filters",[])),
        }

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"""
            <div style="background:#e6f4f1;border:1px solid #a7d5cf;border-radius:10px;padding:16px 20px;">
              <div style="font-size:20px;font-weight:700;color:#2a7b6f;">{config_summary['kpis']}</div>
              <div style="font-size:12px;color:#2a7b6f;font-weight:600;">KPI Cards</div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div style="background:#fbeee8;border:1px solid #f5a58a;border-radius:10px;padding:16px 20px;">
              <div style="font-size:20px;font-weight:700;color:#e8633a;">{config_summary['charts']}</div>
              <div style="font-size:12px;color:#e8633a;font-weight:600;">Charts</div>
            </div>
            """, unsafe_allow_html=True)
        with c3:
            st.markdown(f"""
            <div style="background:#f0f0fe;border:1px solid #c4c4f8;border-radius:10px;padding:16px 20px;">
              <div style="font-size:20px;font-weight:700;color:#6366f1;">{config_summary['filters']}</div>
              <div style="font-size:12px;color:#6366f1;font-weight:600;">Filters</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        c1, c2, c3 = st.columns([1,1,4])
        with c1:
            if st.button("← Edit", key="step4_back"):
                st.session_state.custom_step = 3; st.rerun()
        with c2:
            if st.button("✅ Apply Dashboard", key="step4_apply"):
                st.session_state.custom_config  = dict(st.session_state.custom_wip)
                st.session_state.active_config  = st.session_state.custom_config
                st.session_state.flow_step      = "final"
                st.rerun()


# ─────────────────────────────────────────────────────────────
# EXPORT HELPERS
# ─────────────────────────────────────────────────────────────
def export_config_json(config):
    return json.dumps(config, indent=2, default=str)


# ─────────────────────────────────────────────────────────────
# MAIN APP
# ─────────────────────────────────────────────────────────────
def main():
    df      = st.session_state.raw_df
    config  = st.session_state.active_config
    step    = st.session_state.flow_step

    # Always render sidebar (filters only visible after upload)
    filter_selections = render_sidebar(df, config or {})

    # ─── MAIN CONTENT AREA ───
    main_area = st.container()

    with main_area:

        # ════════════════════════════════
        # STEP: UPLOAD
        # ════════════════════════════════
        if step == "upload":
            # Full-screen upload landing
            st.markdown("""
            <div style="padding: 60px 5% 0;">
              <div style="max-width:640px; margin:0 auto; text-align:center;">
                <div style="font-size:11px;font-weight:700;letter-spacing:3px;text-transform:uppercase;
                     color:#e8633a;margin-bottom:20px;">Dashboard Generator</div>
                <div style="font-family:'Instrument Serif',serif;font-size:48px;color:#1a2332;
                     line-height:1.1;margin-bottom:16px;font-style:italic;">
                  Instant dashboards,<br>
                  <span style="color:#e8633a;">from any dataset</span>
                </div>
                <p style="font-size:17px;color:#6b7280;line-height:1.7;margin-bottom:40px;font-family:'DM Sans',sans-serif;">
                  Upload a CSV or Excel file and DashForge intelligently generates
                  KPI cards, charts, and filters — automatically.
                </p>
              </div>
            </div>
            """, unsafe_allow_html=True)

            # How it works
            st.markdown("""
            <div style="display:flex;gap:20px;max-width:720px;margin:0 auto 48px;padding:0 5%;">
            """, unsafe_allow_html=True)
            steps_info = [
                ("01","Upload","Drop in your CSV or Excel file"),
                ("02","Auto-Generate","Smart dashboard created instantly"),
                ("03","Customise","Fine-tune KPIs, charts & filters"),
            ]
            cols = st.columns(3)
            for i, (num, title, desc) in enumerate(steps_info):
                with cols[i]:
                    st.markdown(f"""
                    <div style="text-align:center;padding:24px 16px;background:#fff;
                         border:1px solid #e8e3d8;border-radius:12px;
                         box-shadow:0 1px 4px rgba(26,35,50,0.05);">
                      <div style="width:36px;height:36px;background:#fbeee8;border-radius:50%;
                           display:flex;align-items:center;justify-content:center;
                           margin:0 auto 12px;font-size:13px;font-weight:700;color:#e8633a;">{num}</div>
                      <div style="font-weight:700;color:#1a2332;font-size:14px;margin-bottom:6px;">{title}</div>
                      <div style="font-size:12px;color:#9ca3af;line-height:1.5;">{desc}</div>
                    </div>
                    """, unsafe_allow_html=True)

            # Upload widget
            st.markdown("<div style='max-width:520px;margin:0 auto;padding:0 5%;'>", unsafe_allow_html=True)
            uploaded = st.file_uploader(
                "Drop your file here",
                type=["csv","xlsx","xls"],
                label_visibility="collapsed",
                help="Supports CSV and Excel files"
            )
            st.markdown("</div>", unsafe_allow_html=True)

            if uploaded:
                with st.spinner("Analysing dataset and generating dashboard…"):
                    try:
                        if uploaded.name.lower().endswith(".csv"):
                            df = pd.read_csv(uploaded)
                        else:
                            df = pd.read_excel(uploaded, engine="openpyxl")

                        if df.empty:
                            st.error("The uploaded file is empty.")
                            return

                        # Store
                        st.session_state.raw_df    = df
                        st.session_state.filename  = uploaded.name
                        config = auto_generate_config(df, uploaded.name)
                        st.session_state.auto_config   = config
                        st.session_state.active_config = config
                        st.session_state.flow_step     = "auto_shown"
                        # Pre-fill custom wizard with auto config
                        st.session_state.custom_wip = {
                            "title":   config["title"],
                            "kpis":    list(config["kpis"]),
                            "charts":  list(config["charts"]),
                            "filters": list(config["filters"]),
                        }
                        st.session_state.custom_step = 0
                        st.rerun()

                    except Exception as e:
                        st.error(f"Could not read file: {e}")

        # ════════════════════════════════
        # STEP: AUTO DASHBOARD SHOWN
        # ════════════════════════════════
        elif step == "auto_shown":
            # Render the auto dashboard
            st.markdown("<div style='padding: 24px 4% 0;'>", unsafe_allow_html=True)
            render_dashboard(df, config, filter_selections)
            st.markdown("</div>", unsafe_allow_html=True)

            # Satisfaction prompt
            st.markdown("""
            <div style="background:#fff;border:1px solid #e8e3d8;border-radius:14px;
                 padding:28px 32px;margin:8px 4%;box-shadow:0 2px 8px rgba(26,35,50,0.07);">
              <div style="font-family:'Instrument Serif',serif;font-size:22px;color:#1a2332;
                   margin-bottom:8px;font-style:italic;">
                How does this look?
              </div>
              <div style="font-size:14px;color:#6b7280;margin-bottom:20px;line-height:1.6;">
                DashForge generated this dashboard automatically from your data.
                You can use it as-is, or customise KPIs, charts, and filters to match exactly what you need.
              </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<div style='padding:0 4%;margin-top:16px;'>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns([1,1,4])
            with col1:
                if st.button("✅  Use this dashboard"):
                    st.session_state.flow_step = "final"
                    st.rerun()
            with col2:
                if st.button("⚙️  Customise dashboard"):
                    st.session_state.flow_step = "customize"
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        # ════════════════════════════════
        # STEP: CUSTOMISE
        # ════════════════════════════════
        elif step == "customize":
            st.markdown("<div style='padding: 24px 4% 0;'>", unsafe_allow_html=True)

            # Back to auto
            if st.button("← Back to auto dashboard"):
                st.session_state.flow_step = "auto_shown"
                st.rerun()

            st.markdown("<br>", unsafe_allow_html=True)
            render_customization_wizard(df)
            st.markdown("</div>", unsafe_allow_html=True)

        # ════════════════════════════════
        # STEP: FINAL DASHBOARD
        # ════════════════════════════════
        elif step == "final":
            st.markdown("<div style='padding: 24px 4% 0;'>", unsafe_allow_html=True)

            # Action bar
            action_c1, action_c2, action_c3, action_spacer = st.columns([1,1,1,4])
            with action_c1:
                if st.button("⚙️ Customise"):
                    st.session_state.flow_step = "customize"
                    st.rerun()
            with action_c2:
                # Export config as JSON
                config_json = export_config_json(st.session_state.active_config)
                st.download_button(
                    "⬇️ Export Config",
                    data=config_json,
                    file_name="dashboard_config.json",
                    mime="application/json",
                    key="export_json"
                )
            with action_c3:
                # Export filtered data as CSV
                if df is not None:
                    filt_df = apply_filters(df, config, filter_selections)
                    csv_buf = io.StringIO()
                    filt_df.to_csv(csv_buf, index=False)
                    st.download_button(
                        "⬇️ Export Data",
                        data=csv_buf.getvalue(),
                        file_name="dashboard_data.csv",
                        mime="text/csv",
                        key="export_csv"
                    )

            st.markdown("<br>", unsafe_allow_html=True)

            # Render the active dashboard
            render_dashboard(df, st.session_state.active_config, filter_selections)

            # Start over
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("↩  New Dataset"):
                for key in ["raw_df","filename","auto_config","custom_config","active_config","custom_wip","custom_step"]:
                    if key in ["custom_wip"]:
                        st.session_state[key] = {"title":"My Dashboard","kpis":[],"charts":[],"filters":[]}
                    elif key == "custom_step":
                        st.session_state[key] = 0
                    else:
                        st.session_state[key] = None
                st.session_state.filename  = ""
                st.session_state.flow_step = "upload"
                st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# RUN
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()
