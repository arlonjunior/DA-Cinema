import streamlit as st
from data_utils import load_and_preprocess_data
from eda import run_eda
from forecast import run_forecasting
from nl_query_engine import run_nlq

st.set_page_config(page_title="CinemaSense", layout="wide")
st.title("🍿 CinemaSense Dashboard")

menu = st.sidebar.selectbox("Navigate", ["Welcome", "EDA", "Forecasting", "Ask a Question (NLQ)"])

df = load_and_preprocess_data()

if menu == "Welcome":
    st.markdown("""
    ### 🎥 Welcome to CinemaSense
    A Natural Language-powered dashboard for analyzing and predicting cinema performance.
    Use the left menu to explore different modules!
    """)

elif menu == "EDA":
    run_eda(df)

elif menu == "Forecasting":
    run_forecasting(df)

elif menu == "Ask a Question (NLQ)":
    run_nlq(df)
