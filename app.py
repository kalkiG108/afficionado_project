# ============================================================
# PHASE 3: Streamlit Dashboard
# Afficionado Coffee Roasters - Sales Trend Analysis
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Afficionado Coffee — Sales Analytics",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }
    .main-title {
        font-family: 'DM Serif Display', serif;
        font-size: 2.4rem;
        color: #1a1a1a;
        margin-bottom: 0;
        line-height: 1.1;
    }
    .main-subtitle {
        font-size: 1rem;
        color: #6b6b6b;
        margin-top: 0.3rem;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: #f8f6f1;
        border-left: 4px solid #1D9E75;
        border-radius: 8px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.5rem;
    }
    .metric-label {
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #6b6b6b;
        margin-bottom: 0.2rem;
    }
    .metric-value {
        font-size: 1.6rem;
        font-weight: 600;
        color: #1a1a1a;
    }
    .metric-delta {
        font-size: 0.8rem;
        color: #1D9E75;
        margin-top: 0.1rem;
    }
    .section-header {
        font-family: 'DM Serif Display', serif;
        font-size: 1.3rem;
        color: #1a1a1a;
        border-bottom: 2px solid #e8e3d9;
        padding-bottom: 0.4rem;
        margin-bottom: 1rem;
        margin-top: 1.5rem;
    }
    .insight-box {
        background: #f0faf5;
        border: 1px solid #9FE1CB;
        border-radius: 8px;
        padding: 0.8rem 1.1rem;
        font-size: 0.9rem;
        color: #085041;
        margin-top: 0.5rem;
    }
    div[data-testid="stSidebar"] {
        background: #1a1a1a;
    }
    div[data-testid="stSidebar"] * {
        color: #f0ece3 !important;
    }
    div[data-testid="stSidebar"] .stSelectbox label,
    div[data-testid="stSidebar"] .stMultiSelect label,
    div[data-testid="stSidebar"] .stSlider label,
    div[data-testid="stSidebar"] .stRadio label {
        color: #a89f8c !important;
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: transparent;
        border-bottom: 2px solid #e8e3d9;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border: none;
        font-family: 'DM Sans', sans-serif;
        font-size: 0.9rem;
        color: #6b6b6b;
        padding: 0.5rem 1rem;
    }
    .stTabs [aria-selected="true"] {
        background: transparent;
        color: #1a1a1a !important;
        border-bottom: 2px solid #1D9E75;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():
    df = pd.read_csv("data/coffee_sales_clean.csv")
    DAY_ORDER    = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    BUCKET_ORDER = ["Morning (6–11)", "Afternoon (12–16)", "Evening (17–21)"]
    df["day_of_week"] = pd.Categorical(df["day_of_week"], categories=DAY_ORDER, ordered=True)
    df["time_bucket"] = pd.Categorical(df["time_bucket"], categories=BUCKET_ORDER, ordered=True)
    return df

df_all = load_data()

LOCATIONS    = sorted(df_all["store_location"].unique().tolist())
DAY_ORDER    = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
BUCKET_ORDER = ["Morning (6–11)", "Afternoon (12–16)", "Evening (17–21)"]

STORE_COLORS = {
    "Hell's Kitchen":  "#534AB7",
    "Astoria":         "#1D9E75",
    "Lower Manhattan": "#D85A30"
}

# ============================================================
# SIDEBAR FILTERS
# ============================================================

with st.sidebar:
    st.markdown("## ☕ Filters")
    st.markdown("---")

    selected_stores = st.multiselect(
        "Store Location",
        options=LOCATIONS,
        default=LOCATIONS
    )

    selected_days = st.multiselect(
        "Day of Week",
        options=DAY_ORDER,
        default=DAY_ORDER
    )

    hour_range = st.slider(
        "Hour Range",
        min_value=6, max_value=20,
        value=(6, 20),
        step=1,
        format="%d:00"
    )

    metric_toggle = st.radio(
        "Primary Metric",
        options=["Revenue ($)", "Transaction Count"],
        index=0
    )

    st.markdown("---")
    st.markdown("**Dataset**")
    st.markdown("Afficionado Coffee Roasters · 2025")
    st.markdown(f"**{len(df_all):,}** transactions")

# ============================================================
# APPLY FILTERS
# ============================================================

df = df_all.copy()

if selected_stores:
    df = df[df["store_location"].isin(selected_stores)]
if selected_days:
    df = df[df["day_of_week"].isin(selected_days)]
df = df[(df["hour"] >= hour_range[0]) & (df["hour"] <= hour_range[1])]

metric_col   = "revenue" if metric_toggle == "Revenue ($)" else "transaction_id"
metric_label = "Revenue ($)" if metric_toggle == "Revenue ($)" else "Transaction Count"
metric_agg   = "sum" if metric_toggle == "Revenue ($)" else "count"

# ============================================================
# HEADER + KPI CARDS
# ============================================================

st.markdown('<p class="main-title">Afficionado Coffee Roasters</p>', unsafe_allow_html=True)
st.markdown('<p class="main-subtitle">Sales Trend & Time-Based Performance Analysis · 2025</p>', unsafe_allow_html=True)

if df.empty:
    st.warning("No data matches the selected filters. Please adjust the sidebar.")
    st.stop()

total_revenue   = df["revenue"].sum()
total_txns      = len(df)
avg_txn_value   = df["revenue"].mean()
peak_hour       = df.groupby("hour")["transaction_id"].count().idxmax()
busiest_day     = df.groupby("day_of_week", observed=True)["transaction_id"].count().idxmax()

col1, col2, col3, col4, col5 = st.columns(5)

def metric_card(col, label, value, delta=""):
    col.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-delta">{delta}</div>
    </div>
    """, unsafe_allow_html=True)

metric_card(col1, "Total Revenue",       f"${total_revenue:,.0f}",    "All filtered transactions")
metric_card(col2, "Total Transactions",  f"{total_txns:,}",            "")
metric_card(col3, "Avg Transaction",     f"${avg_txn_value:.2f}",      "Per transaction")
metric_card(col4, "Peak Hour",           f"{peak_hour}:00",            "Highest volume hour")
metric_card(col5, "Busiest Day",         str(busiest_day),             "Most transactions")

st.markdown("---")

# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "📈  Sales Trend",
    "📅  Day of Week",
    "🕐  Hourly Demand",
    "🏪  Location Comparison"
])


# ──────────────────────────────────────────────
# TAB 1: SALES TREND
# ──────────────────────────────────────────────
with tab1:
    st.markdown('<p class="section-header">Weekly Sales Trend</p>', unsafe_allow_html=True)

    weekly = (
        df.groupby("week_number")
        .agg(total_revenue=("revenue","sum"),
             total_transactions=("transaction_id","count"))
        .reset_index()
    )
    weekly["total_revenue"] = weekly["total_revenue"].round(2)

    y_col   = "total_revenue" if metric_toggle == "Revenue ($)" else "total_transactions"
    y_label = metric_label

    fig = make_subplots(specs=[[{"secondary_y": False}]])

    fig.add_trace(go.Scatter(
        x=weekly["week_number"], y=weekly[y_col],
        name=y_label,
        line=dict(color="#1D9E75", width=2.5),
        fill="tozeroy", fillcolor="rgba(29,158,117,0.08)",
        mode="lines", hovertemplate=f"Week %{{x}}<br>{y_label}: %{{y:,.0f}}<extra></extra>"
    ))

    z = np.polyfit(weekly["week_number"], weekly[y_col], 1)
    p = np.poly1d(z)
    fig.add_trace(go.Scatter(
        x=weekly["week_number"], y=np.round(p(weekly["week_number"]), 2),
        name="Trend Line",
        line=dict(color="#D85A30", width=1.5, dash="dash"),
        mode="lines"
    ))

    fig.update_layout(
        xaxis_title="Week Number", yaxis_title=y_label,
        plot_bgcolor="white", paper_bgcolor="white",
        hovermode="x unified", height=380,
        legend=dict(orientation="h", y=1.08, x=1, xanchor="right"),
        margin=dict(t=20, b=40)
    )
    fig.update_yaxes(gridcolor="#f5f0e8")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"""
    <div class="insight-box">
    💡 <b>Insight:</b> Revenue stays consistently between
    ${weekly['total_revenue'].min():,.0f} and ${weekly['total_revenue'].max():,.0f} per week,
    indicating stable, year-round demand. Week {weekly.loc[weekly['total_revenue'].idxmax(),'week_number']}
    recorded the highest revenue (${weekly['total_revenue'].max():,.0f}), likely driven by seasonal factors.
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p class="section-header">Store Revenue Over Time</p>', unsafe_allow_html=True)

    weekly_store = (
        df.groupby(["store_location","week_number"])["revenue"]
        .sum().reset_index()
    )
    weekly_store["revenue"] = weekly_store["revenue"].round(2)

    fig2 = px.line(
        weekly_store, x="week_number", y="revenue", color="store_location",
        labels={"revenue":"Revenue ($)","week_number":"Week Number","store_location":"Store"},
        color_discrete_map=STORE_COLORS
    )
    fig2.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        hovermode="x unified", height=320,
        legend=dict(orientation="h", y=1.08, x=1, xanchor="right"),
        margin=dict(t=10, b=40)
    )
    fig2.update_yaxes(gridcolor="#f5f0e8")
    fig2.update_traces(line_width=2)
    st.plotly_chart(fig2, use_container_width=True)


# ──────────────────────────────────────────────
# TAB 2: DAY OF WEEK
# ──────────────────────────────────────────────
with tab2:
    st.markdown('<p class="section-header">Day-of-Week Performance</p>', unsafe_allow_html=True)

    dow = (
        df.groupby("day_of_week", observed=True)
        .agg(total_revenue=("revenue","sum"),
             avg_revenue=("revenue","mean"),
             total_transactions=("transaction_id","count"))
        .reset_index()
    )
    dow["avg_transactions"] = (dow["total_transactions"] / 52).round(1)
    dow["avg_revenue"]      = dow["avg_revenue"].round(2)
    dow["total_revenue"]    = dow["total_revenue"].round(2)

    y_col   = "avg_revenue" if metric_toggle == "Revenue ($)" else "avg_transactions"
    y_label = "Avg Revenue per Txn ($)" if metric_toggle == "Revenue ($)" else "Avg Daily Transactions"

    colors = ["#534AB7" if d not in ["Saturday","Sunday"] else "#D85A30"
              for d in dow["day_of_week"].tolist()]

    col_a, col_b = st.columns(2)

    with col_a:
        fig = go.Figure(go.Bar(
            x=dow["day_of_week"].tolist(), y=dow[y_col],
            marker_color=colors,
            text=dow[y_col].round(2), textposition="outside"
        ))
        fig.update_layout(
            title=y_label, plot_bgcolor="white", paper_bgcolor="white",
            height=360, margin=dict(t=40, b=20),
            xaxis=dict(tickangle=-30)
        )
        fig.update_yaxes(gridcolor="#f5f0e8")
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        weekend_comp = (
            df.groupby("is_weekend")
            .agg(total_revenue=("revenue","sum"),
                 total_txns=("transaction_id","count"),
                 avg_value=("revenue","mean"))
            .reset_index()
        )
        weekend_comp["label"] = weekend_comp["is_weekend"].map({True:"Weekend", False:"Weekday"})

        y_we   = "total_revenue" if metric_toggle == "Revenue ($)" else "total_txns"
        y_we_l = "Total Revenue ($)" if metric_toggle == "Revenue ($)" else "Total Transactions"

        fig2 = go.Figure(go.Bar(
            x=weekend_comp["label"].tolist(),
            y=weekend_comp[y_we].round(2),
            marker_color=["#534AB7","#D85A30"],
            text=weekend_comp[y_we].round(0).astype(int), textposition="outside",
            width=0.4
        ))
        fig2.update_layout(
            title=f"Weekday vs Weekend — {y_we_l}",
            plot_bgcolor="white", paper_bgcolor="white",
            height=360, margin=dict(t=40, b=20)
        )
        fig2.update_yaxes(gridcolor="#f5f0e8")
        st.plotly_chart(fig2, use_container_width=True)

    best_day  = dow.loc[dow["avg_transactions"].idxmax(), "day_of_week"]
    worst_day = dow.loc[dow["avg_transactions"].idxmin(), "day_of_week"]
    st.markdown(f"""
    <div class="insight-box">
    💡 <b>Insight:</b> <b>{best_day}</b> is the busiest day while <b>{worst_day}</b> is the slowest.
    All 3 store locations are in urban NYC neighbourhoods (Hell's Kitchen, Astoria, Lower Manhattan),
    meaning the customer base is predominantly office workers — explaining why weekdays outperform weekends.
    </div>
    """, unsafe_allow_html=True)


# ──────────────────────────────────────────────
# TAB 3: HOURLY DEMAND
# ──────────────────────────────────────────────
with tab3:
    st.markdown('<p class="section-header">Hourly Demand Analysis</p>', unsafe_allow_html=True)

    hourly = (
        df.groupby("hour")
        .agg(total_transactions=("transaction_id","count"),
             total_revenue=("revenue","sum"))
        .reset_index()
    )
    hourly["total_revenue"] = hourly["total_revenue"].round(2)

    y_col   = "total_revenue" if metric_toggle == "Revenue ($)" else "total_transactions"
    y_label = metric_label
    peak_h  = hourly.loc[hourly[y_col].idxmax(), "hour"]
    peak_v  = hourly[y_col].max()

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(
        x=hourly["hour"], y=hourly["total_transactions"],
        name="Transactions", line=dict(color="#534AB7", width=3),
        fill="tozeroy", fillcolor="rgba(83,74,183,0.07)",
        mode="lines+markers", marker=dict(size=7),
        hovertemplate="Hour %{x}:00<br>Transactions: %{y:,}<extra></extra>"
    ), secondary_y=False)

    fig.add_trace(go.Scatter(
        x=hourly["hour"], y=hourly["total_revenue"],
        name="Revenue ($)", line=dict(color="#1D9E75", width=2.5, dash="dot"),
        mode="lines+markers", marker=dict(size=6),
        hovertemplate="Hour %{x}:00<br>Revenue: $%{y:,.0f}<extra></extra>"
    ), secondary_y=True)

    fig.add_vline(x=10, line_dash="dash", line_color="#D85A30", line_width=1.5,
                  annotation_text="Peak 10:00", annotation_position="top right",
                  annotation_font_color="#D85A30")

    fig.update_layout(
        xaxis=dict(title="Hour of Day", tickmode="linear", tick0=6, dtick=1),
        plot_bgcolor="white", paper_bgcolor="white", height=380,
        hovermode="x unified",
        legend=dict(orientation="h", y=1.08, x=1, xanchor="right"),
        margin=dict(t=20, b=40)
    )
    fig.update_yaxes(title_text="Transaction Count", secondary_y=False, gridcolor="#f5f0e8")
    fig.update_yaxes(title_text="Revenue ($)", secondary_y=True, gridcolor="#f5f0e8")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<p class="section-header">Time Bucket Breakdown</p>', unsafe_allow_html=True)

    bucket = (
        df.groupby("time_bucket", observed=True)
        .agg(total_revenue=("revenue","sum"),
             total_transactions=("transaction_id","count"))
        .reset_index()
    )
    bucket["pct_txns"] = (bucket["total_transactions"] / bucket["total_transactions"].sum() * 100).round(1)
    bucket["pct_rev"]  = (bucket["total_revenue"] / bucket["total_revenue"].sum() * 100).round(1)

    col_a, col_b = st.columns([2, 1])
    with col_a:
        y_col_b = "total_revenue" if metric_toggle == "Revenue ($)" else "total_transactions"
        fig2 = px.bar(
            bucket, x="time_bucket", y=y_col_b,
            color="time_bucket",
            color_discrete_map={
                "Morning (6–11)":    "#534AB7",
                "Afternoon (12–16)": "#1D9E75",
                "Evening (17–21)":   "#D85A30"
            },
            labels={y_col_b: metric_label, "time_bucket": "Time Bucket"},
            text=y_col_b
        )
        fig2.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
        fig2.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            height=320, showlegend=False, margin=dict(t=10, b=20)
        )
        fig2.update_yaxes(gridcolor="#f5f0e8")
        st.plotly_chart(fig2, use_container_width=True)

    with col_b:
        st.markdown("**Share of Total Transactions**")
        for _, row in bucket.iterrows():
            st.markdown(f"""
            <div style="margin-bottom:0.6rem">
                <div style="font-size:0.8rem;color:#6b6b6b">{row['time_bucket']}</div>
                <div style="background:#e8e3d9;border-radius:4px;height:8px;margin:3px 0">
                    <div style="background:#1D9E75;width:{row['pct_txns']}%;height:8px;border-radius:4px"></div>
                </div>
                <div style="font-size:0.85rem;font-weight:600">{row['pct_txns']}%</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-box">
    💡 <b>Insight:</b> The peak at <b>10:00 AM</b> reflects a mid-morning coffee break habit rather than
    a commute rush. Morning (6–11) accounts for over 54% of all transactions.
    Staffing should be heaviest between <b>9 AM and 11 AM</b> across all locations.
    </div>
    """, unsafe_allow_html=True)


# ──────────────────────────────────────────────
# TAB 4: LOCATION COMPARISON
# ──────────────────────────────────────────────
with tab4:
    st.markdown('<p class="section-header">Cross-Location Comparison</p>', unsafe_allow_html=True)

    col_a, col_b, col_c = st.columns(3)
    for col, loc in zip([col_a, col_b, col_c], LOCATIONS):
        loc_df = df[df["store_location"] == loc]
        col.markdown(f"""
        <div class="metric-card" style="border-left-color:{STORE_COLORS.get(loc,'#1D9E75')}">
            <div class="metric-label">{loc}</div>
            <div class="metric-value">${loc_df['revenue'].sum():,.0f}</div>
            <div class="metric-delta">{len(loc_df):,} transactions · avg ${loc_df['revenue'].mean():.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<p class="section-header">Hourly Heatmap by Store</p>', unsafe_allow_html=True)

    heatmap_data = (
        df.groupby(["store_location","hour"])["transaction_id"]
        .count().reset_index(name="transactions")
    )
    pivot = heatmap_data.pivot(index="store_location", columns="hour", values="transactions").fillna(0)

    fig = go.Figure(go.Heatmap(
        z=pivot.values,
        x=[f"{h}:00" for h in pivot.columns],
        y=pivot.index.tolist(),
        colorscale=[[0,"#f8f6f1"],[0.5,"#9FE1CB"],[1,"#085041"]],
        text=pivot.values.astype(int),
        texttemplate="%{text}",
        hovertemplate="Store: %{y}<br>Hour: %{x}<br>Transactions: %{z}<extra></extra>",
        colorbar=dict(title="Txns")
    ))
    fig.update_layout(
        xaxis_title="Hour of Day", yaxis_title="",
        plot_bgcolor="white", paper_bgcolor="white",
        height=260, margin=dict(t=10, b=40)
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<p class="section-header">Time Bucket Distribution by Store</p>', unsafe_allow_html=True)

    bucket_store = (
        df.groupby(["store_location","time_bucket"], observed=True)["transaction_id"]
        .count().reset_index(name="transactions")
    )
    y_col_bs = "transactions"

    fig2 = px.bar(
        bucket_store, x="store_location", y=y_col_bs,
        color="time_bucket", barmode="group",
        labels={"transactions":"Transaction Count","store_location":"Store","time_bucket":"Time Bucket"},
        color_discrete_map={
            "Morning (6–11)":    "#534AB7",
            "Afternoon (12–16)": "#1D9E75",
            "Evening (17–21)":   "#D85A30"
        },
        category_orders={"time_bucket": BUCKET_ORDER}
    )
    fig2.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        height=360, margin=dict(t=10, b=20),
        legend=dict(orientation="h", y=1.08, x=1, xanchor="right")
    )
    fig2.update_yaxes(gridcolor="#f5f0e8")
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("""
    <div class="insight-box">
    💡 <b>Insight:</b> All three stores show near-identical temporal demand patterns — peak at 10 AM,
    morning-dominant traffic. Lower Manhattan customers spend slightly more per transaction ($4.81 avg)
    suggesting a higher-income or office-professional clientele in that area.
    </div>
    """, unsafe_allow_html=True)