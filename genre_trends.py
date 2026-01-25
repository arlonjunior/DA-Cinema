import re
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import Normalize
import seaborn as sns   # ← added for palette

from utils import load_data
from nls_utils import parse_entity

def run_trends():
    st.subheader("Genre Performance Insights")
    df = load_data()

    df["tickets_sold"] = pd.to_numeric(df["tickets_sold"], errors="coerce")
    df["total_sales"] = pd.to_numeric(df["total_sales"], errors="coerce")
    df = df.dropna(subset=["film_genre", "tickets_sold", "total_sales", "cinema_city"])

    # SECTION 1: Average Revenue per Genre
    with st.container():
        st.markdown("## Average Revenue per Genre")
        genre_sales = (
            df.groupby("film_genre")["total_sales"]
              .mean()
              .sort_values()
        )
        top_n = st.slider("Show Top N Genres", 5, 20, 10)
        genre_sales = genre_sales.tail(top_n)

        norm = Normalize(vmin=genre_sales.min(), vmax=genre_sales.max())
        colors = plt.cm.Blues(norm(genre_sales.values))

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.barh(
            genre_sales.index,
            genre_sales.values,
            color=colors
        )
        ax.set_xlabel("Average Revenue per Screening (£)")
        ax.set_ylabel("Genre")
        ax.set_title(f"Top {top_n} Genres by Average Revenue", fontsize=14, pad=15)
        st.pyplot(fig)

    # SECTION 2: Donut Chart for Top Genres by City
    with st.container():
        st.markdown("## Top Genres by City (Natural Language Search)")
        st.write("Type “Top 3 genres in London” or pick a city manually.")

        nl_query = st.text_input(
            "Enter query",
            placeholder="e.g. Top 7 genres in Manchester"
        ).strip().lower()
        cities = sorted(df["cinema_city"].unique())
        city_manual = st.selectbox("Or select a city:", ["All"] + cities)

        # Extract city via substring or fuzzy match
        city_nls = None
        if nl_query:
            for c in cities:
                if c.lower() in nl_query:
                    city_nls = c
                    break
            if city_nls is None:
                city_nls = parse_entity(nl_query, cities)
        city = city_nls or city_manual

        # Extract Top-N number
        nums = re.findall(r"\d+", nl_query)
        top_n_city = int(nums[0]) if nums else 10

        df_city = df[df["cinema_city"] == city] if city != "All" else df.copy()
        genre_counts = (
            df_city.groupby("film_genre")["tickets_sold"]
                   .sum()
                   .sort_values(ascending=False)
                   .head(top_n_city)
        )

        if genre_counts.empty:
            st.warning(f"No data for **{city}**")
            return

        labels = genre_counts.index.tolist()
        sizes  = genre_counts.values

        # Use a distinct Set3 palette
        colors_city = sns.color_palette("Set3", n_colors=len(sizes))

        fig, ax = plt.subplots(figsize=(8, 8))
        wedges, _ = ax.pie(
            sizes,
            labels=None,
            startangle=90,
            colors=colors_city,
            wedgeprops=dict(width=0.3, edgecolor='white')
        )

        # Annotate percentages
        for i, w in enumerate(wedges):
            ang = (w.theta2 - w.theta1) / 2. + w.theta1
            x = 0.85 * np.cos(np.deg2rad(ang))
            y = 0.85 * np.sin(np.deg2rad(ang))
            pct = f"{sizes[i]/sizes.sum()*100:.1f}%"
            ax.text(x, y, pct, ha="center", va="center", fontsize=10, color="#333")

        ax.legend(
            wedges,
            labels,
            title="Genres",
            loc="center left",
            bbox_to_anchor=(1, 0.5),
            fontsize=9
        )
        ax.set_title(f"Top {top_n_city} Genres in {city}", y=1.08, fontsize=14)
        ax.axis("equal")
        st.pyplot(fig)

