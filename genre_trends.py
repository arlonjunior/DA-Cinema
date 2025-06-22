import streamlit as st
from utils import load_data
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def run_trends():
    st.subheader("Genre Performance Insights")

    df = load_data()
    df["total_sales"] = pd.to_numeric(df["total_sales"], errors="coerce")
    df["tickets_sold"] = pd.to_numeric(df["tickets_sold"], errors="coerce")
    df = df.dropna(subset=["film_genre", "total_sales", "tickets_sold"])

    # ======================= SECTION 1 =======================
    with st.container():
        st.markdown("## Average Revenue per Genre")

        genre_sales = (
            df.groupby("film_genre")["total_sales"]
            .mean()
            .sort_values(ascending=True)
        )

        top_n = st.slider("Show Top N Genres", min_value=5, max_value=20, value=10, key="top_n_genres")
        genre_sales = genre_sales.tail(top_n)

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x=genre_sales.values, y=genre_sales.index, ax=ax, palette="Blues_r")
        ax.set_xlabel("Average Revenue per Screening (£)")
        ax.set_ylabel("Genre")
        ax.set_title(f"Top {top_n} Genres by Average Revenue")
        ax.tick_params(axis="x", labelrotation=45)
        st.pyplot(fig)

    # ======================= SECTION 2 =======================
    with st.container():
        st.markdown("## Top Genres by City")

        cities = ["All"] + sorted(df["cinema_city"].dropna().unique())
        selected_city = st.selectbox("Select City", cities, key="city_filter_pivot")

        city_df = df.copy()
        if selected_city != "All":
            city_df = city_df[city_df["cinema_city"] == selected_city]

        pivot = (
            city_df.pivot_table(
                index="cinema_city",
                columns="film_genre",
                values="tickets_sold",
                aggfunc="sum"
            )
            .fillna(0)
            .astype(int)
        )

        if pivot.empty:
            st.warning("No data available for this city.")
        else:
            st.markdown(
                "This table shows how many tickets were sold for each genre, grouped by city. "
                "The **yellow highlight** shows the most popular genre in each city."
            )

            styled = pivot.style \
                .format("{:,}") \
                .highlight_max(axis=1, props="background-color: #08306b;")

            st.dataframe(styled)
