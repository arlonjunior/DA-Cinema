import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    # Read with appropriate encoding
    df = pd.read_csv("dataset_cinema_sense.csv", encoding="latin1", parse_dates=["date"])

    # Strip whitespace from column names
    df.columns = df.columns.str.strip()

    # Standardize numeric columns
    numeric_columns = [
        "total_sales", "tickets_sold", "tickets_out", "ticket_price",
        "ticket_use", "capacity", "occu_perc"
    ]
    for col in numeric_columns:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace("[^0-9.\-]", "", regex=True)
                .replace("", "0")  # Replace blanks with zero
                .astype(float)
            )

    # Ensure date column is valid datetime
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    return df