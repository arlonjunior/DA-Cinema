import streamlit as st
from eda import run_eda
from forecast import run_forecast
from recommender import run_recommender
from cinema_performance import run_performance
from genre_trends import run_trends


def local_css():
    st.markdown("""
        <style>
            html, body, [class*="css"]  {
                font-family: 'Segoe UI', sans-serif;
            }
            h1, h2, h3 {
                color: #08306b;
            }
            .stButton>button {
                background-color: #08306b;
                color: white;
                font-weight: bold;
                border-radius: 5px;
                padding: 0.6rem 1.2rem;
            }
        </style>
    """, unsafe_allow_html=True)


local_css()

st.set_page_config(page_title="Cinema Intelligence Dashboard", layout="wide")
st.title("Cinema Intelligence Platform")

with st.sidebar:
    st.image("cinesense_analysis_navy_2_vector.png", width=400)
    st.markdown("### Welcome to CinemaSense Insights")

menu = st.sidebar.selectbox("", [
    "Executive Summary",
    "Cinema & City Performance",
    "Genre & Film Trends",
    "Revenue Forecasting",
    "Strategic Recommendations"
])

if menu == "Executive Summary":
    run_eda()

elif menu == "Cinema & City Performance":
    run_performance()

elif menu == "Genre & Film Trends":
    run_trends()

elif menu == "Revenue Forecasting":
    run_forecast()

elif menu == "Strategic Recommendations":
    run_recommender()
