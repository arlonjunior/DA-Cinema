import streamlit as st
import pandas as pd
from utils import load_data

def run_recommender():
    st.subheader("Cast & Content Strategy Recommendations")

    df = load_data()
    df["total_sales"] = pd.to_numeric(df["total_sales"], errors="coerce")
    df["tickets_sold"] = pd.to_numeric(df["tickets_sold"], errors="coerce")
    df["cast_top_5"] = df["cast_top_5"].astype(str)

    # ========= SECTION 1: Cast Revenue Impact =========
    with st.container():
        st.markdown("## Cast Member Revenue Impact")

        actor_query = st.text_input("Enter actor's name (partial or full):", key="actor_search").strip().lower()

        # Explode cast names
        df_cast = df.copy()
        df_cast["cast_top_5"] = df_cast["cast_top_5"].str.split(",")
        df_cast = df_cast.explode("cast_top_5")
        df_cast["cast_top_5"] = df_cast["cast_top_5"].str.strip()
        all_actors = df_cast["cast_top_5"].dropna().unique()

        # Match actor query to available names
        matched_actors = [actor for actor in all_actors if actor_query in actor.lower()] if actor_query else []

        selected_actor = None
        if matched_actors:
            selected_actor = st.selectbox("Select actor name", sorted(matched_actors))

        if selected_actor:
            actor_df = df_cast[df_cast["cast_top_5"] == selected_actor]

            if actor_df.empty:
                st.warning("No films found with that actor.")
            else:
                avg_actor_revenue = actor_df["total_sales"].mean()
                avg_overall_revenue = df["total_sales"].mean()
                impact = "Above Average" if avg_actor_revenue > avg_overall_revenue else "Below Average"
                film_column = "film_title" if "film_title" in actor_df.columns else actor_df.columns[0]
                unique_films = actor_df[film_column].nunique()

                st.markdown(f"**Actor:** `{selected_actor}`")
                st.markdown(f"**Films Participated In:** {unique_films} out of {df[film_column].nunique()} total films")
                st.markdown(f"**Average Revenue for Their Films:** £{avg_actor_revenue:,.2f} ({impact})")
                st.markdown(f"**Overall Average Revenue:** £{avg_overall_revenue:,.2f}")

                st.dataframe(
                    actor_df[[film_column, "cast_top_5", "total_sales"]]
                    .drop_duplicates()
                    .sort_values("total_sales", ascending=False)
                    .rename(columns={film_column: "Film Title", "cast_top_5": "Cast", "total_sales": "Total Sales (£)"})
                    .reset_index(drop=True)
                    .style.format({"Total Sales (£)": "£{:,.2f}"})
                )

    # ========= SECTION 2: Data-Driven Content Suggestions =========
    with st.container():
        st.markdown("## Data-Driven Content Recommendations")

        # Top Films by Tickets Sold
        if "film_title" in df.columns:
            top_films = (
                df.groupby("film_title")["tickets_sold"]
                .sum()
                .sort_values(ascending=False)
                .head(10)
            )
            with st.expander("Top Ticket-Selling Films"):
                st.bar_chart(top_films)

        # Most Profitable Genres
        if "film_genre" in df.columns:
            top_genres = (
                df.groupby("film_genre")["total_sales"]
                .mean()
                .sort_values(ascending=False)
                .head(10)
            )
            with st.expander("Most Profitable Genres (Avg Revenue)"):
                st.bar_chart(top_genres)

        # Top Cast Members by Avg Revenue
        with st.expander("Cast Members with Highest Avg Revenue"):
            cast_df = df.copy()
            cast_df["cast_top_5"] = cast_df["cast_top_5"].str.split(",")
            exploded = cast_df.explode("cast_top_5")
            exploded["cast_top_5"] = exploded["cast_top_5"].str.strip()

            top_cast = (
                exploded.groupby("cast_top_5")["total_sales"]
                .mean()
                .sort_values(ascending=False)
                .head(10)
                .rename("Avg Revenue (£)")
                .reset_index()
            )

            st.dataframe(
                top_cast.style.format({"Avg Revenue (£)": "£{:,.2f}"})
            )
