import streamlit as st
from utils import load_data
import pandas as pd

def run_performance():
    df = load_data()
    st.subheader("Cinema Performance Leaderboard")

    top_cinemas = (
        df.groupby("cinema_name")["total_sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )
    st.bar_chart(top_cinemas)

    st.markdown("#### Performance by City")
    by_city = df.groupby("cinema_city")["occu_perc"].mean().sort_values()
    st.bar_chart(by_city)
