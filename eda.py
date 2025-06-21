import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt


def run_eda(df):
    st.header("📈 Exploratory Data Analysis")

    if st.checkbox("Show Raw Dataset"):
        st.dataframe(df.head())

    st.subheader("🎞️ Top 10 Cinemas by Total Sales")
    top_cinemas = df.groupby('cinema_code')['total_sales'].sum().nlargest(10)
    fig1 = sns.barplot(x=top_cinemas.values, y=top_cinemas.index)
    st.pyplot(fig1.figure)

    st.subheader("📅 Occupancy Trend Over Time")
    fig2 = sns.lineplot(data=df, x="date", y="occu_perc")
    st.pyplot(fig2.figure)
