import streamlit as st
import requests
import pandas as pd

API_URL = "http://localhost:8000"

def analytics_by_months_tab():
    response = requests.get(f"{API_URL}/expenses/")
    if response.status_code == 200:
        existing_expenses = response.json()
    else:
        st.error("Failed to retrieve expenses")
        existing_expenses = []

    data = {
        "Months": [month["month_name"] for month in existing_expenses],
        "Total": [month["total"] for month in existing_expenses]
    }

    df = pd.DataFrame(data)
    st.title("Expanse Breakdown By Months")
    st.bar_chart(data=df.set_index("Months")['Total'], use_container_width=True)
    df["Total"] = df["Total"].map("{:.2f}".format)

    st.table(df)