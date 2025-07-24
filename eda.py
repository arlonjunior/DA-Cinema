# eda.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils import load_data

def run_eda():
    # ─── Inject CSS to Prevent KPI Truncation ─────────────────────────────
    st.markdown(
        """
        <style>
          /* Ensure metric values never overflow with "..." */
          [data-testid="stMetricValue"] {
            overflow: visible !important;
            text-overflow: clip !important;
            white-space: nowrap !important;
          }
        </style>
        """,
        unsafe_allow_html=True
    )
    # ─────────────────────────────────────────────────────────────────────

    df = load_data()

    # --- Sidebar filters ---
    st.sidebar.markdown("### Filters")
    city = st.sidebar.selectbox(
        "Select City",
        ["All"] + sorted(df["cinema_city"].dropna().unique())
    )
    if city != "All":
        df = df[df["cinema_city"] == city]

    cinema_options = df["cinema_name"].dropna().unique().tolist()
    cinema = st.sidebar.selectbox(
        "Select Cinema",
        ["All"] + sorted(cinema_options)
    )
    if cinema != "All":
        df = df[df["cinema_name"] == cinema]

    # --- Key Performance Indicators ---
    st.subheader("Key Performance Indicators")
    total_tickets = pd.to_numeric(df["tickets_sold"], errors="coerce").sum()
    total_revenue = pd.to_numeric(df["total_sales"], errors="coerce").sum()
    avg_occupancy = pd.to_numeric(df["occu_perc"], errors="coerce").mean()

    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Tickets Sold",      f"{int(total_tickets):,}")
    kpi2.metric("Total Revenue",     f"£{total_revenue:,.2f}")
    kpi3.metric("Avg Occupancy",     f"{avg_occupancy:.1f}%")

    # --- Ticket Usage Breakdown ---
    tickets_used   = pd.to_numeric(df["ticket_use"], errors="coerce").sum()
    tickets_unused = pd.to_numeric(df["tickets_out"], errors="coerce").sum()

    st.markdown("#### Ticket Usage Breakdown")
    col_chart, col_info = st.columns([1, 1])

    # Small pie chart
    fig, ax = plt.subplots(figsize=(2.5, 2.5))
    ax.pie(
        [tickets_used, tickets_unused],
        colors=["#08306b", "#a6bddb"],
        startangle=90,
        wedgeprops=dict(width=0.6, edgecolor="white")
    )
    ax.axis("equal")
    col_chart.pyplot(fig, use_container_width=True)

    # Metrics + Legend
    col_info.markdown(f"**Tickets Used:** {int(tickets_used):,}")
    col_info.markdown(f"**Tickets Not Used:** {int(tickets_unused):,}")
    col_info.markdown("""
    <div style="display:flex; align-items:center; margin-top:8px;">
      <div style="width:12px; height:12px; background-color:#08306b; margin-right:6px;"></div>Used
    </div>
    <div style="display:flex; align-items:center; margin-top:4px;">
      <div style="width:12px; height:12px; background-color:#a6bddb; margin-right:6px;"></div>Unused
    </div>
    """, unsafe_allow_html=True)

    # --- Sales Over Time ---
    st.markdown("#### Sales Over Time")
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    sales_trend = df.groupby("date")["total_sales"].sum()
    st.line_chart(sales_trend)

