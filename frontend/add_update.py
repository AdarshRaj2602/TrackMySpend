import streamlit as st
from datetime import datetime
import requests

API_URL = "http://localhost:8000"

CATEGORIES = ["Rent", "Food", "Shopping", "Entertainment", "Other"]

CATEGORY_ICONS = {
    "Rent": "🏠",
    "Food": "🍔",
    "Shopping": "🛍️",
    "Entertainment": "🎬",
    "Other": "📦"
}

def add_update_tab():
    st.markdown("""
    <div class='section-header'>Add / Update Expenses</div>
    <div class='section-sub'>Log up to 5 expenses for any date. Existing entries are pre-filled.</div>
    """, unsafe_allow_html=True)

    # ── Date picker ────────────────────────────────────────────────────────────
    col_date, col_spacer = st.columns([1, 2])
    with col_date:
        selected_date = st.date_input(
            "📅 Select Date",
            datetime(2024, 8, 1),
        )

    # ── Fetch existing expenses ────────────────────────────────────────────────
    response = requests.get(f"{API_URL}/expenses/{selected_date}")
    if response.status_code == 200:
        existing_expenses = response.json()
    else:
        st.error("⚠️ Could not connect to the server. Make sure the backend is running.")
        existing_expenses = []

    # ── Quick summary strip ────────────────────────────────────────────────────
    if existing_expenses:
        total = sum(e["amount"] for e in existing_expenses)
        top_cat = max(
            set(e["category"] for e in existing_expenses),
            key=lambda c: sum(e["amount"] for e in existing_expenses if e["category"] == c)
        )
        m1, m2, m3 = st.columns(3)
        m1.metric("💰 Day Total", f"₹{total:,.2f}")
        m2.metric("📝 Entries", str(len(existing_expenses)))
        m3.metric("🏆 Top Category", f"{CATEGORY_ICONS.get(top_cat,'')} {top_cat}")

        st.markdown("<div style='margin: 8px 0 16px'></div>", unsafe_allow_html=True)

    # ── Expense form ───────────────────────────────────────────────────────────
    with st.form(key="expenses_form"):

        # Header row
        h1, h2, h3 = st.columns([1.2, 1.2, 2])
        with h1:
            st.markdown("<div style='color:#64748B; font-size:12px; font-weight:600; text-transform:uppercase; letter-spacing:0.08em'>Amount (₹)</div>", unsafe_allow_html=True)
        with h2:
            st.markdown("<div style='color:#64748B; font-size:12px; font-weight:600; text-transform:uppercase; letter-spacing:0.08em'>Category</div>", unsafe_allow_html=True)
        with h3:
            st.markdown("<div style='color:#64748B; font-size:12px; font-weight:600; text-transform:uppercase; letter-spacing:0.08em'>Notes</div>", unsafe_allow_html=True)

        expenses = []
        date_key = str(selected_date)

        for i in range(5):
            amount   = existing_expenses[i]["amount"]   if i < len(existing_expenses) else 0.0
            category = existing_expenses[i]["category"] if i < len(existing_expenses) else "Shopping"
            notes    = existing_expenses[i]["notes"]    if i < len(existing_expenses) else ""

            c1, c2, c3 = st.columns([1.2, 1.2, 2])
            with c1:
                amount_input = st.number_input(
                    label="Amount", min_value=0.0, step=10.0, value=float(amount),
                    key=f"amount_{date_key}_{i}", label_visibility="collapsed"
                )
            with c2:
                cat_options = [f"{CATEGORY_ICONS[c]}  {c}" for c in CATEGORIES]
                default_idx = CATEGORIES.index(category) if category in CATEGORIES else 0
                category_input_raw = st.selectbox(
                    label="Category", options=cat_options, index=default_idx,
                    key=f"category_{date_key}_{i}", label_visibility="collapsed"
                )
                category_input = category_input_raw.split("  ")[-1]
            with c3:
                notes_input = st.text_input(
                    label="Notes", value=notes, placeholder="What did you spend on?",
                    key=f"notes_{date_key}_{i}", label_visibility="collapsed"
                )

            expenses.append({
                "amount": amount_input,
                "category": category_input,
                "notes": notes_input,
            })

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        submit_button = st.form_submit_button("💾  Save Expenses")

        if submit_button:
            filtered = [e for e in expenses if e["amount"] > 0]
            if not filtered:
                st.warning("⚠️ Please enter at least one expense amount before saving.")
            else:
                save_response = requests.post(f"{API_URL}/expenses/{selected_date}", json=filtered)
                if save_response.status_code == 200:
                    st.success(f"✅ {len(filtered)} expense(s) saved for {selected_date}!")
                else:
                    st.error("❌ Failed to save expenses. Please check the backend server.")