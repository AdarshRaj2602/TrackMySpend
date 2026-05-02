import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

API_URL = "http://localhost:8000"

MONTH_ORDER = [
    "January","February","March","April","May","June",
    "July","August","September","October","November","December"
]

def analytics_by_months_tab():
    st.markdown("""
    <div class='section-header'>Monthly Spending Trends</div>
    <div class='section-sub'>A month-over-month view of all your recorded expenses.</div>
    """, unsafe_allow_html=True)

    # ── Fetch data ─────────────────────────────────────────────────────────────
    response = requests.get(f"{API_URL}/expenses/")
    if response.status_code != 200:
        st.error("❌ Failed to fetch monthly data. Make sure the backend is running.")
        return

    raw = response.json()
    if not raw:
        st.info("ℹ️ No expense data found yet.")
        return

    # ── Build & sort dataframe ─────────────────────────────────────────────────
    df = pd.DataFrame({
        "Month": [r["month_name"] for r in raw],
        "Total": [r["total"]      for r in raw],
    })
    df["MonthOrder"] = df["Month"].apply(
        lambda m: MONTH_ORDER.index(m) if m in MONTH_ORDER else 99
    )
    df = df.sort_values("MonthOrder").reset_index(drop=True)

    grand_total = df["Total"].sum()
    peak_month  = df.loc[df["Total"].idxmax(), "Month"]
    avg_monthly = grand_total / len(df)

    # ── Metric strip ───────────────────────────────────────────────────────────
    m1, m2, m3 = st.columns(3)
    m1.metric("💰 All-Time Total",  f"₹{grand_total:,.2f}")
    m2.metric("📈 Peak Month",      peak_month)
    m3.metric("📊 Monthly Average", f"₹{avg_monthly:,.2f}")

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

    # ── Area + bar chart ───────────────────────────────────────────────────────
    st.markdown("<div style='color:#94A3B8; font-size:13px; font-weight:600; margin-bottom:8px'>SPENDING OVER TIME</div>", unsafe_allow_html=True)

    fig = go.Figure()

    # Filled area
    fig.add_trace(go.Scatter(
        x=df["Month"], y=df["Total"],
        mode="lines",
        line=dict(color="#10B981", width=3),
        fill="tozeroy",
        fillcolor="rgba(16,185,129,0.08)",
        hovertemplate="<b>%{x}</b><br>₹%{y:,.2f}<extra></extra>",
    ))

    # Dot markers
    fig.add_trace(go.Scatter(
        x=df["Month"], y=df["Total"],
        mode="markers",
        marker=dict(color="#10B981", size=10, line=dict(color="#0F172A", width=2)),
        hoverinfo="skip",
    ))

    # Average line
    fig.add_hline(
        y=avg_monthly,
        line_dash="dot",
        line_color="#F59E0B",
        line_width=1.5,
        annotation_text=f"Avg ₹{avg_monthly:,.0f}",
        annotation_font_color="#F59E0B",
        annotation_font_size=11,
    )

    fig.update_layout(
        plot_bgcolor ="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color   ="#94A3B8",
        showlegend   =False,
        margin       =dict(t=10, b=0, l=0, r=0),
        height       =340,
        xaxis=dict(gridcolor="#1E293B", tickfont=dict(size=12, color="#CBD5E1")),
        yaxis=dict(gridcolor="#1E293B", tickprefix="₹", tickfont=dict(size=11)),
        hovermode="x unified",
    )

    st.plotly_chart(fig, use_container_width=True)

    # ── Monthly table ──────────────────────────────────────────────────────────
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    st.markdown("<div style='color:#94A3B8; font-size:13px; font-weight:600; margin-bottom:8px'>MONTHLY BREAKDOWN</div>", unsafe_allow_html=True)

    display_df = df[["Month", "Total"]].copy()
    display_df["% of Year"] = (display_df["Total"] / grand_total * 100).map("{:.1f}%".format)
    display_df["Total"]     = display_df["Total"].map("₹{:,.2f}".format)
    display_df.columns      = ["Month", "Amount Spent", "% of Year"]

    st.table(display_df)