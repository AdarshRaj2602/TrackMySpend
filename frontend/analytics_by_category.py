import streamlit as st
from datetime import datetime
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

API_URL = "http://localhost:8000"

CATEGORY_ICONS = {
    "Rent": "🏠",
    "Food": "🍔",
    "Shopping": "🛍️",
    "Entertainment": "🎬",
    "Other": "📦"
}

COLORS = ["#10B981", "#3B82F6", "#F59E0B", "#EF4444", "#8B5CF6"]

def analytics_by_category_tab():
    st.markdown("""
    <div class='section-header'>Spending by Category</div>
    <div class='section-sub'>Pick a date range to break down your expenses by category.</div>
    """, unsafe_allow_html=True)

    # ── Date range picker ──────────────────────────────────────────────────────
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        start_date = st.date_input("📅 Start Date", datetime(2024, 8, 1))
    with col2:
        end_date = st.date_input("📅 End Date", datetime(2024, 8, 31))
    with col3:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        fetch = st.button("📊  Analyse")

    if not fetch:
        st.markdown("""
        <div style='text-align:center; padding:60px 0; color:#334155'>
            <div style='font-size:48px'>📊</div>
            <div style='font-size:16px; margin-top:12px; color:#475569'>Select a date range and click Analyse</div>
        </div>
        """, unsafe_allow_html=True)
        return

    # ── API call ───────────────────────────────────────────────────────────────
    payload = {
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date":   end_date.strftime("%Y-%m-%d")
    }
    response = requests.post(f"{API_URL}/analytics/", json=payload)

    if response.status_code != 200:
        st.error("❌ Failed to fetch analytics. Make sure the backend is running.")
        return

    data = response.json()

    if not data:
        st.info("ℹ️ No expenses found for the selected date range.")
        return

    # ── Build dataframe ────────────────────────────────────────────────────────
    rows = []
    for cat, vals in data.items():
        rows.append({
            "Category": cat,
            "Icon":     CATEGORY_ICONS.get(cat, "💰"),
            "Total":    vals["total"],
            "Percent":  vals["percentage"]
        })
    df = pd.DataFrame(rows).sort_values("Percent", ascending=False).reset_index(drop=True)

    grand_total = df["Total"].sum()
    top_cat     = df.iloc[0]["Category"]
    num_cats    = len(df)

    # ── Metric strip ───────────────────────────────────────────────────────────
    m1, m2, m3 = st.columns(3)
    m1.metric("💰 Total Spent",    f"₹{grand_total:,.2f}")
    m2.metric("🏆 Top Category",   f"{CATEGORY_ICONS.get(top_cat,'')} {top_cat}")
    m3.metric("🗂️ Categories",     str(num_cats))

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

    # ── Charts side by side ────────────────────────────────────────────────────
    chart_col, pie_col = st.columns([1.6, 1])

    with chart_col:
        st.markdown("<div style='color:#94A3B8; font-size:13px; font-weight:600; margin-bottom:8px'>SPENDING BREAKDOWN</div>", unsafe_allow_html=True)
        fig_bar = px.bar(
            df,
            x="Category", y="Percent",
            text=df["Percent"].map(lambda x: f"{x:.1f}%"),
            color="Category",
            color_discrete_sequence=COLORS,
        )
        fig_bar.update_traces(
            textposition="outside",
            textfont=dict(color="#F1F5F9", size=12),
            marker_line_width=0,
            width=0.5,
        )
        fig_bar.update_layout(
            plot_bgcolor  ="rgba(0,0,0,0)",
            paper_bgcolor ="rgba(0,0,0,0)",
            font_color    ="#94A3B8",
            showlegend    =False,
            margin        =dict(t=10, b=0, l=0, r=0),
            xaxis=dict(gridcolor="#1E293B", tickfont=dict(size=12, color="#CBD5E1")),
            yaxis=dict(gridcolor="#1E293B", ticksuffix="%", tickfont=dict(size=11)),
            height=320,
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with pie_col:
        st.markdown("<div style='color:#94A3B8; font-size:13px; font-weight:600; margin-bottom:8px'>SHARE</div>", unsafe_allow_html=True)
        fig_pie = go.Figure(go.Pie(
            labels=df["Category"],
            values=df["Total"],
            hole=0.55,
            marker=dict(colors=COLORS, line=dict(color="#0F172A", width=2)),
            textinfo="percent",
            textfont=dict(size=11, color="#F1F5F9"),
        ))
        fig_pie.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#94A3B8",
            showlegend=True,
            legend=dict(font=dict(color="#CBD5E1", size=11), bgcolor="rgba(0,0,0,0)"),
            margin=dict(t=0, b=0, l=0, r=0),
            height=320,
        )
        fig_pie.add_annotation(
            text=f"₹{grand_total:,.0f}",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=14, color="#10B981", family="DM Sans"),
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # ── Detail table ───────────────────────────────────────────────────────────
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    st.markdown("<div style='color:#94A3B8; font-size:13px; font-weight:600; margin-bottom:8px'>DETAIL TABLE</div>", unsafe_allow_html=True)

    display_df = df.copy()
    display_df["Category"] = display_df.apply(lambda r: f"{r['Icon']}  {r['Category']}", axis=1)
    display_df["Total"]    = display_df["Total"].map("₹{:,.2f}".format)
    display_df["Percent"]  = display_df["Percent"].map("{:.2f}%".format)
    display_df = display_df[["Category", "Total", "Percent"]]
    display_df.columns = ["Category", "Amount Spent", "% of Total"]

    st.table(display_df)