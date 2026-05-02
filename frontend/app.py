import streamlit as st
from add_update import add_update_tab
from analytics_by_category import analytics_by_category_tab
from analytics_by_months import analytics_by_months_tab

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="TrackMySpend",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* ── Hide default header ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%);
    border-right: 1px solid #334155;
}
[data-testid="stSidebar"] * { color: #F1F5F9 !important; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: #1E293B;
    border-radius: 12px;
    padding: 6px;
    border: 1px solid #334155;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    padding: 8px 20px;
    color: #94A3B8 !important;
    font-weight: 500;
    font-size: 14px;
    background: transparent;
    border: none;
    transition: all 0.2s ease;
}
.stTabs [aria-selected="true"] {
    background: #10B981 !important;
    color: #0F172A !important;
    font-weight: 600;
}

/* ── Metric cards ── */
[data-testid="stMetric"] {
    background: #1E293B;
    border: 1px solid #334155;
    border-radius: 16px;
    padding: 20px 24px;
    transition: border-color 0.2s;
}
[data-testid="stMetric"]:hover { border-color: #10B981; }
[data-testid="stMetricLabel"]  { color: #94A3B8 !important; font-size: 13px !important; }
[data-testid="stMetricValue"]  { color: #10B981 !important; font-size: 28px !important; font-weight: 700 !important; }
[data-testid="stMetricDelta"]  { font-size: 13px !important; }

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #10B981, #059669);
    color: #0F172A !important;
    font-weight: 600;
    border: none;
    border-radius: 10px;
    padding: 10px 28px;
    font-size: 14px;
    transition: all 0.2s ease;
    width: 100%;
}
.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 8px 20px rgba(16,185,129,0.35);
}

/* ── Inputs ── */
.stNumberInput input, .stTextInput input, .stSelectbox select,
[data-testid="stDateInput"] input {
    background: #1E293B !important;
    border: 1px solid #334155 !important;
    border-radius: 8px !important;
    color: #F1F5F9 !important;
}
.stNumberInput input:focus, .stTextInput input:focus {
    border-color: #10B981 !important;
    box-shadow: 0 0 0 2px rgba(16,185,129,0.15) !important;
}

/* ── Table ── */
.stTable table {
    border-collapse: separate;
    border-spacing: 0;
    width: 100%;
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid #334155;
}
.stTable thead tr th {
    background: #1E293B !important;
    color: #10B981 !important;
    font-weight: 600;
    font-size: 13px;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    padding: 12px 16px !important;
    border-bottom: 1px solid #334155 !important;
}
.stTable tbody tr td {
    background: #0F172A;
    color: #CBD5E1 !important;
    padding: 12px 16px !important;
    border-bottom: 1px solid #1E293B !important;
    font-family: 'DM Mono', monospace;
    font-size: 13px;
}
.stTable tbody tr:hover td { background: #1E293B; }

/* ── Form container ── */
[data-testid="stForm"] {
    background: #1E293B;
    border: 1px solid #334155;
    border-radius: 16px;
    padding: 24px;
}

/* ── Success / Error ── */
.stSuccess { border-radius: 10px !important; border-left: 4px solid #10B981 !important; }
.stError   { border-radius: 10px !important; border-left: 4px solid #EF4444 !important; }

/* ── Divider ── */
hr { border-color: #334155 !important; }

/* ── Section header helper ── */
.section-header {
    font-size: 22px;
    font-weight: 700;
    color: #F1F5F9;
    margin-bottom: 4px;
}
.section-sub {
    font-size: 13px;
    color: #64748B;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 20px 0 10px'>
        <div style='font-size:48px'>💸</div>
        <div style='font-size:22px; font-weight:700; color:#F1F5F9; letter-spacing:-0.5px'>TrackMySpend</div>
        <div style='font-size:12px; color:#64748B; margin-top:4px'>Personal Finance Dashboard</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown("""
    <div style='padding: 0 8px'>
        <div style='color:#94A3B8; font-size:11px; font-weight:600; letter-spacing:0.1em; text-transform:uppercase; margin-bottom:12px'>Features</div>
        <div style='color:#CBD5E1; font-size:14px; margin-bottom:10px'>📅 &nbsp; Log daily expenses</div>
        <div style='color:#CBD5E1; font-size:14px; margin-bottom:10px'>📊 &nbsp; Category analytics</div>
        <div style='color:#CBD5E1; font-size:14px; margin-bottom:10px'>📆 &nbsp; Monthly trends</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown("""
    <div style='padding: 0 8px'>
        <div style='color:#94A3B8; font-size:11px; font-weight:600; letter-spacing:0.1em; text-transform:uppercase; margin-bottom:12px'>Stack</div>
        <div style='display:flex; flex-wrap:wrap; gap:6px'>
            <span style='background:#1E293B; border:1px solid #334155; color:#10B981; border-radius:6px; padding:3px 10px; font-size:11px; font-weight:600'>FastAPI</span>
            <span style='background:#1E293B; border:1px solid #334155; color:#10B981; border-radius:6px; padding:3px 10px; font-size:11px; font-weight:600'>Streamlit</span>
            <span style='background:#1E293B; border:1px solid #334155; color:#10B981; border-radius:6px; padding:3px 10px; font-size:11px; font-weight:600'>MySQL</span>
            <span style='background:#1E293B; border:1px solid #334155; color:#10B981; border-radius:6px; padding:3px 10px; font-size:11px; font-weight:600'>Pandas</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div style='color:#475569; font-size:11px; text-align:center'>v1.0 · Built by Adarsh Raj</div>", unsafe_allow_html=True)

# ── Main content ───────────────────────────────────────────────────────────────
st.markdown("""
<div style='margin-bottom:24px'>
    <div style='font-size:28px; font-weight:700; color:#F1F5F9; letter-spacing:-0.5px'>
        Good day! 👋
    </div>
    <div style='font-size:14px; color:#64748B; margin-top:4px'>
        Here's an overview of your spending activity.
    </div>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["  📅  Add / Update  ", "  📊  By Category  ", "  📆  By Month  "])

with tab1:
    add_update_tab()
with tab2:
    analytics_by_category_tab()
with tab3:
    analytics_by_months_tab()