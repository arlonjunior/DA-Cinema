# recommender.py

import re
import streamlit as st
import pandas as pd

from utils import load_data
from nls_utils import parse_entity

def find_film_column(df: pd.DataFrame) -> str | None:
    for pref in ("film_name", "film_title"):
        if pref in df.columns:
            return pref
    for col in df.columns:
        if re.search(r"film|movie", col, flags=re.IGNORECASE):
            return col
    for col in df.columns:
        if not pd.api.types.is_numeric_dtype(df[col]):
            return col
    return None

def run_recommender():
    st.subheader("Cast & Content Strategy Recommendations")

    df = load_data()
    df["total_sales"] = pd.to_numeric(df["total_sales"], errors="coerce")
    df["tickets_sold"] = pd.to_numeric(df["tickets_sold"], errors="coerce")

    film_col = find_film_column(df)
    if film_col is None:
        st.error("Unable to locate a film/title column.")
        return

    # --- Explode cast ---
    df_cast = df.copy()
    if "cast_top_5" in df.columns:
        df_cast["cast_top_5"] = (
            df_cast["cast_top_5"]
            .fillna("")
            .astype(str)
            .str.split(",")
        )
        df_cast = df_cast.explode("cast_top_5")
        df_cast["cast_top_5"] = df_cast["cast_top_5"].str.strip()
        df_cast = df_cast[df_cast["cast_top_5"] != ""]
    else:
        df_cast["cast_top_5"] = []

    all_actors = df_cast["cast_top_5"].dropna().unique().tolist()

    # === SECTION 1: Cast Member Revenue Impact ===
    with st.container():
        st.markdown("## Cast Member Revenue Impact (Natural Language Search)")
        nl_actor = st.text_input("Ask about an actor, e.g. 'Revenue impact of Kevin Hart'").strip()
        actor = parse_entity(nl_actor, all_actors)

        if actor:
            actor_df = df_cast[df_cast["cast_top_5"] == actor]
            if actor_df.empty:
                st.warning(f"No records found for actor {actor}.")
            else:
                # Accurate calculations
                total_revenue = actor_df["total_sales"].sum()
                num_screenings = len(actor_df)
                avg_per_screening = total_revenue / num_screenings if num_screenings else 0
                unique_films = actor_df[film_col].nunique()
                all_films = df[film_col].nunique()
                overall_avg = df["total_sales"].mean()
                impact = "Above Average" if avg_per_screening > overall_avg else "Below Average"

                st.write(f"**Actor:** {actor}")
                st.write(f"**Total Revenue from Screenings:** £{total_revenue:,.2f}")
                st.write(f"**Screenings:** {num_screenings}")
                st.write(f"**# Unique Films:** {unique_films} / {all_films}")
                st.write(f"**Avg Revenue per Screening:** £{avg_per_screening:,.2f} ({impact})")
                st.write(f"**Overall Avg per Screening:** £{overall_avg:,.2f}")

                # Detail table of screenings
                film_stats = (
                    actor_df.groupby(["cinema_city", "cinema_name", film_col], as_index=False)["total_sales"]
                    .sum()
                    .sort_values("total_sales", ascending=False)
                )
                film_stats = film_stats.rename(columns={
                    "cinema_city": "City",
                    "cinema_name": "Cinema",
                    film_col: "Film Title",
                    "total_sales": "Total Sales (£)"
                })

                st.markdown(f"### Matched Screenings ({len(film_stats)} rows)")
                st.dataframe(film_stats.style.format({"Total Sales (£)": "£{:,.2f}"}))
        else:
            st.info("No matching actor found. Try another name.")

    # === SECTION 2: Content Strategy by Query ===
    with st.container():
        st.markdown("## Data-Driven Content Suggestions (Natural Language Search)")
        nl_q = st.text_input("e.g. 'Top 10 films in Manchester in the cinema Vue Printworks'").strip().lower()

        nums = re.findall(r"\d+", nl_q)
        top_n = int(nums[0]) if nums else 10

        cities = sorted(df["cinema_city"].dropna().unique().tolist())
        city = parse_entity(nl_q, cities)
        if not city:
            for c in cities:
                if c.lower() in nl_q:
                    city = c
                    break

        df_city = df[df["cinema_city"] == city] if city else df.copy()

        cinemas = sorted(df_city["cinema_name"].dropna().unique().tolist())
        cinema = parse_entity(nl_q, cinemas)
        if not cinema:
            for token in set(re.findall(r"\w+", nl_q)):
                matches = [c for c in cinemas if token.lower() in c.lower()]
                if matches:
                    cinema = matches[0]
                    break

        df_final = df_city[df_city["cinema_name"] == cinema] if cinema else df_city

        if "genre" in nl_q:
            top_genres = (
                df_final.groupby("film_genre")["total_sales"]
                .mean()
                .sort_values(ascending=False)
                .head(top_n)
            )
            title = f"Top {top_n} Genres"
            if city:
                title += f" in {city}"
            if cinema:
                title += f" at {cinema}"
            st.write(f"### {title} by Avg Revenue")
            st.bar_chart(top_genres)

        elif "film" in nl_q or "movie" in nl_q:
            top_films = (
                df_final.groupby(film_col)["tickets_sold"]
                .sum()
                .sort_values(ascending=False)
                .head(top_n)
            )
            title = f"Top {top_n} Films"
            if city:
                title += f" in {city}"
            if cinema:
                title += f" at {cinema}"
            st.write(f"### {title} by Tickets Sold")
            st.bar_chart(top_films)

        else:
            st.info("Mention 'genre' or 'film/movie' and optionally 'top N', city, cinema.")

