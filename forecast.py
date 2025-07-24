# forecast.py

import streamlit as st
import pandas as pd
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from utils import load_data

from pandas.tseries.offsets import MonthEnd

@st.cache_resource
def train_model(X, y):
    model = XGBRegressor(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X, y)
    return model

def create_future_df(start_date, months, avg_price, avg_capacity):
    future_dates = pd.date_range(start=start_date, periods=months, freq='M') + MonthEnd(0)
    future_df = pd.DataFrame({
        "month": future_dates.month,
        "quarter": future_dates.quarter,
        "ticket_price": avg_price,
        "capacity": avg_capacity
    }, index=future_dates)
    return future_df

def run_forecast():
    st.subheader("Revenue Forecasting Dashboard")
    df = load_data()

    df["total_sales"] = pd.to_numeric(df["total_sales"], errors="coerce")
    df["ticket_price"] = pd.to_numeric(df["ticket_price"], errors="coerce")
    df["capacity"] = pd.to_numeric(df["capacity"], errors="coerce")
    df = df.dropna(subset=["total_sales", "ticket_price", "capacity", "month", "quarter"])

    st.sidebar.markdown("### Forecast Filters")
    cities = ["All"] + sorted(df["cinema_city"].dropna().unique())
    city = st.sidebar.selectbox("Select City", cities)

    filtered = df[df["cinema_city"] == city] if city != "All" else df.copy()
    cinemas = ["All"] + sorted(filtered["cinema_name"].dropna().unique())
    cinema = st.sidebar.selectbox("Select Cinema", cinemas)

    filtered = filtered[filtered["cinema_name"] == cinema] if cinema != "All" else filtered
    if filtered.empty:
        st.warning("No data available for this selection.")
        return

    if len(filtered) > 100000:
        filtered = filtered.sample(n=50000, random_state=42)

    features = ["month", "quarter", "ticket_price", "capacity"]
    X = filtered[features]
    y = filtered["total_sales"]

    if X.empty or y.empty:
        st.warning("Not enough data to train model after filtering.")
        return

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    with st.spinner("Training forecasting model..."):
        model = train_model(X_train, y_train)

    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    st.success(f"Forecast Complete! Model MAE: £{mae:,.2f}")

    st.markdown("### Predicted vs Actual Revenue")
    chart_df = pd.DataFrame({
        "Actual": y_test.reset_index(drop=True),
        "Predicted": preds
    })
    st.line_chart(chart_df.head(100))

    # === NEW SECTION: Future Revenue Forecast ===
    st.markdown("### Forecast Future Revenue")

    future_start = st.date_input("Select forecast start date", pd.to_datetime("2025-08-01"))
    horizon = st.slider("Months to forecast", 1, 12, 6)

    avg_price = X_train["ticket_price"].mean()
    avg_capacity = X_train["capacity"].mean()

    future_df = create_future_df(future_start, horizon, avg_price, avg_capacity)

    future_preds = model.predict(future_df[features])

    forecast_df = pd.DataFrame({
        "Date": future_df.index,
        "Predicted Revenue (£)": future_preds
    })
    forecast_df.set_index("Date", inplace=True)

    st.line_chart(forecast_df)

