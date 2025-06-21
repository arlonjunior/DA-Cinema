import streamlit as st
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import pandas as pd


def run_forecasting(df):
    st.header("📊 Forecasting Ticket Sales")

    cinema = st.selectbox("Select a Cinema", df['cinema_code'].unique())

    data = df[df['cinema_code'] == cinema].sort_values('date')

    features = ['tickets_sold', 'tickets_out', 'ticket_price', 'capacity', 'occu_perc', 'show_time', 'month', 'quarter',
                'day']
    target = 'total_sales'

    X = data[features]
    y = data[target]

    if len(X) < 20:
        st.warning("⚠️ Not enough records for this cinema to train a model.")
        return

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    model = XGBRegressor()
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    st.write(f"📉 MAE: {mean_absolute_error(y_test, preds):.2f}")

    chart_data = pd.DataFrame({'Actual': y_test.values, 'Predicted': preds}, index=y_test.index)
    st.line_chart(chart_data)
