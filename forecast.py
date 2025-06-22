import streamlit as st
import pandas as pd
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from utils import load_data

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

def run_forecast():
    st.subheader("Revenue Forecasting Dashboard")

    df = load_data()

    # Ensure numeric types
    df["total_sales"] = pd.to_numeric(df["total_sales"], errors="coerce")
    df["ticket_price"] = pd.to_numeric(df["ticket_price"], errors="coerce")
    df["capacity"] = pd.to_numeric(df["capacity"], errors="coerce")
    df = df.dropna(subset=["total_sales", "ticket_price", "capacity", "month", "quarter"])

    # Sidebar filters
    st.sidebar.markdown("### Forecast Filters")
    cities = ["All"] + sorted(df["cinema_city"].dropna().unique())
    city = st.sidebar.selectbox("Select City", cities)

    filtered_df = df.copy()
    if city != "All":
        filtered_df = filtered_df[filtered_df["cinema_city"] == city]

    cinemas = ["All"] + sorted(filtered_df["cinema_name"].dropna().unique())
    cinema = st.sidebar.selectbox("Select Cinema", cinemas)

    if cinema != "All":
        filtered_df = filtered_df[filtered_df["cinema_name"] == cinema]

    if filtered_df.empty:
        st.warning("No data available for this selection. Please adjust your filters.")
        return

    # Optional sampling for large datasets
    if len(filtered_df) > 100000:
        filtered_df = filtered_df.sample(n=50000, random_state=42)

    # Define features and target
    features = ["month", "quarter", "ticket_price", "capacity"]
    target = "total_sales"
    X = filtered_df[features]
    y = filtered_df[target]

    if X.empty or y.empty:
        st.warning("Not enough data to train model after filtering.")
        return

    # Split into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    with st.spinner("Training forecasting model..."):
        model = train_model(X_train, y_train)

    # Generate predictions
    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)

    # Display forecast accuracy
    st.success(f"Forecast Complete! Model MAE: £{mae:,.2f}")

    # Plot comparison of actual vs predicted
    st.markdown("### Predicted vs Actual Revenue (Sample)")
    chart_df = pd.DataFrame({
        "Actual": y_test.reset_index(drop=True),
        "Predicted": preds
    })
    st.line_chart(chart_df.head(100))
