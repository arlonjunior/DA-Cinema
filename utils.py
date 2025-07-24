import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    df = pd.read_csv("dataset_cinema_sense.csv", encoding="latin1", parse_dates=["date"])
    df.columns = df.columns.str.strip()

    numeric_columns = [
        "total_sales", "tickets_sold", "tickets_out", "ticket_price",
        "ticket_use", "capacity", "occu_perc"
    ]
    for col in numeric_columns:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace("[^0-9.\\-]", "", regex=True)
                .replace("", "0")
                .astype(float)
            )
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    return df

