import pandas as pd
import numpy as np
from datetime import datetime
import streamlit as st

def load_data(file_path):
    """
    Load the Chicago Crime dataset and perform initial cleaning.
    """
    st.write("Reading CSV (last 100,000 rows, optimized columns)...")
    # Define columns to load and dtypes
    cols = ['Date', 'Primary Type', 'Description', 'Latitude', 'Longitude', 'Year']
    dtypes = {
        'Primary Type': 'category',
        'Description': 'category',
        'Year': 'int16',
        'Latitude': 'float32',
        'Longitude': 'float32'
    }
    # Get total number of rows
    with open(file_path) as f:
        total_rows = sum(1 for _ in f) - 1  # minus header
    skip_rows = max(1, total_rows - 50000)
    df = pd.read_csv(
        file_path,
        skiprows=range(1, skip_rows+1),
        usecols=cols,
        dtype=dtypes,
        parse_dates=['Date'],
        date_format='%m/%d/%Y %I:%M:%S %p'
    )
    st.write(f"CSV loaded: {len(df)} rows")
    st.write("Extracting temporal features...")
    df['Hour'] = df['Date'].dt.hour
    df['DayOfWeek'] = df['Date'].dt.day_name()
    df['Month'] = df['Date'].dt.month
    st.write("Dropping missing coordinates...")
    df = df.dropna(subset=['Latitude', 'Longitude'])
    st.write("Filtering invalid coordinates...")
    df = df[
        (df['Latitude'] >= 41.6) & (df['Latitude'] <= 42.0) &
        (df['Longitude'] >= -87.9) & (df['Longitude'] <= -87.5)
    ]
    st.write(f"Data after filtering: {len(df)} rows")
    return df

def prepare_time_series_data(df, frequency='D'):
    """
    Prepare data for time series analysis.
    """
    # Group by date and count crimes
    daily_crimes = df.groupby(df['Date'].dt.date).size().reset_index()
    daily_crimes.columns = ['ds', 'y']
    daily_crimes['ds'] = pd.to_datetime(daily_crimes['ds'])
    
    return daily_crimes

def get_crime_stats(df):
    """
    Calculate basic crime statistics.
    """
    stats = {
        'total_crimes': len(df),
        'unique_crime_types': df['Primary Type'].nunique(),
        'most_common_crime': df['Primary Type'].mode()[0],
        'crime_by_hour': df.groupby('Hour').size().to_dict(),
        'crime_by_day': df.groupby('DayOfWeek').size().to_dict(),
        'crime_by_month': df.groupby('Month').size().to_dict()
    }
    
    return stats

def prepare_clustering_data(df):
    """
    Prepare data for K-Means clustering.
    """
    # Select relevant columns for clustering
    clustering_data = df[['Latitude', 'Longitude']].copy()
    
    return clustering_data 