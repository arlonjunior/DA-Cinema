import streamlit as st
import pandas as pd
from utils import load_data


def run_eda():
    df = load_data()

    # Sidebar filters
    st.sidebar.markdown("### Filters")
    city = st.sidebar.selectbox("Select City", ["All"] + sorted(df["cinema_city"].dropna().unique().tolist()))

    if city != "All":
        df = df[df["cinema_city"] == city]

    cinema_options = df["cinema_name"].dropna().unique().tolist()
    cinema = st.sidebar.selectbox("Select Cinema", ["All"] + sorted(cinema_options))

    if cinema != "All":
        df = df[df["cinema_name"] == cinema]

    # KPI Metrics
    st.subheader("Key Performance Indicators")
    col1, col2, col3 = st.columns(3)
    total_tickets = pd.to_numeric(df["tickets_sold"], errors="coerce").sum()
    total_revenue = pd.to_numeric(df["total_sales"], errors="coerce").sum()
    avg_occupancy = pd.to_numeric(df["occu_perc"], errors="coerce").mean()

    col1.metric("Tickets Sold", f"{int(total_tickets):,}")
    col2.metric("Total Revenue", f"£{total_revenue:,.2f}")
    col3.metric("Avg Occupancy", f"{avg_occupancy:.1f}%")

    # Sales Over Time
    st.markdown("#### Sales Over Time")
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    sales_trend = df.groupby("date")["total_sales"].sum()
    st.line_chart(sales_trend)
