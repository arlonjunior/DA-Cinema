import streamlit as st
import pandas as pd


def parse_nl_query(query, df):
    q = query.lower()

    if "highest sales" in q:
        return df.groupby("cinema_code")["total_sales"].sum().sort_values(ascending=False).head(5).reset_index()

    elif "average occupancy" in q:
        return df.groupby("cinema_code")["occu_perc"].mean().sort_values(ascending=False).head(5).reset_index()

    elif "top ticket prices" in q:
        return df.nlargest(10, "ticket_price")[["cinema_code", "film_code", "ticket_price"]]

    elif "busiest day" in q:
        return df.groupby("day")["tickets_sold"].sum().sort_values(ascending=False).head(1).reset_index()

    else:
        return "⚠️ Query not recognized. Try asking about 'highest sales', 'average occupancy', or 'busiest day'."


def run_nlq(df):
    st.header("🧠 Natural Language Query Engine")

    query = st.text_input("Ask something like 'Which cinemas had the highest sales?'")

    if query:
        result = parse_nl_query(query, df)
        if isinstance(result, pd.DataFrame):
            st.dataframe(result)
        else:
            st.warning(result)
