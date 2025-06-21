import pandas as pd


def load_and_preprocess_data(file_path="dataset_.csv"):
    df = pd.read_csv(file_path)

    # Convert date column to datetime
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['quarter'] = df['date'].dt.quarter
    df['year'] = df['date'].dt.year

    # Fill missing values
    df['occu_perc'].fillna(df['occu_perc'].median(), inplace=True)
    df['capacity'].fillna(df['capacity'].median(), inplace=True)

    return df
