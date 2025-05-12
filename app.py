import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import sys
import os

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_processing import load_data, prepare_time_series_data, get_crime_stats, prepare_clustering_data
from hotspot_detection import perform_clustering, create_heatmap, analyze_hotspot_patterns
from time_series_analysis import train_prophet_model, analyze_temporal_patterns, get_seasonal_decomposition
from visualization import (
    create_crime_type_distribution,
    create_temporal_heatmap,
    create_monthly_trend,
    create_forecast_plot,
    create_hotspot_summary
)

def main():
    st.set_page_config(page_title="Chicago Crime Analysis", layout="wide")
    st.title("Chicago Crime Analysis and Prediction System")
    
    local_data_path = "data/chicago_crime_data.csv"
    df = None
    error = None
    with st.spinner("Loading data..."):
        try:
            if os.path.exists(local_data_path):
                st.info(f"Using local data file: {local_data_path}")
                df = load_data(local_data_path)
                df.columns = df.columns.str.strip()  # Strip column names
            else:
                uploaded_file = st.file_uploader("Upload Chicago Crime Dataset (CSV)", type=['csv'])
                if uploaded_file is not None:
                    df = load_data(uploaded_file)
                    df.columns = df.columns.str.strip()
                else:
                    st.warning("Please upload a CSV file or place it in the data directory as 'chicago_crime_data.csv'.")
                    st.stop()
        except Exception as e:
            error = str(e)
    if error:
        st.error(f"Error loading data: {error}")
        st.stop()
    if df is None or df.empty:
        st.error("No data loaded or data is empty.")
        st.stop()
    # Debug output
    st.success(f"Loaded {len(df)} rows.")
    st.write("Sample data:", df.head())
    # Filter to most recent year for faster processing
    if 'Year' in df.columns:
        max_year = df['Year'].max()
        df = df[df['Year'] == max_year]
        st.info(f"Filtered to most recent year: {max_year} ({len(df)} rows)")
    if df.empty:
        st.error("DataFrame is empty after filtering. Please check your CSV and date format.")
        st.stop()
    # Sidebar
    st.sidebar.title("Analysis Options")
    analysis_type = st.sidebar.selectbox(
        "Select Analysis Type",
        ["Overview", "Hotspot Analysis", "Temporal Analysis", "Forecasting"]
    )
    if analysis_type == "Overview":
        st.header("Crime Overview")
        stats = get_crime_stats(df)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Crimes", stats['total_crimes'])
        with col2:
            st.metric("Unique Crime Types", stats['unique_crime_types'])
        with col3:
            st.metric("Most Common Crime", stats['most_common_crime'])
        st.plotly_chart(create_crime_type_distribution(df))
        st.plotly_chart(create_temporal_heatmap(df))
    elif analysis_type == "Hotspot Analysis":
        st.header("Crime Hotspot Analysis")
        clustering_data = prepare_clustering_data(df)
        n_clusters = st.slider("Number of Hotspots", 5, 20, 10)
        clusters, cluster_centers = perform_clustering(clustering_data, n_clusters)
        m = create_heatmap(df, cluster_centers)
        folium_static(m)
        hotspot_patterns = analyze_hotspot_patterns(df, clusters)
        st.plotly_chart(create_hotspot_summary(hotspot_patterns))
    elif analysis_type == "Temporal Analysis":
        st.header("Temporal Crime Patterns")
        st.plotly_chart(create_monthly_trend(df))
        patterns = analyze_temporal_patterns(df)
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Hourly Distribution")
            st.bar_chart(patterns['hourly'])
        with col2:
            st.subheader("Daily Distribution")
            st.bar_chart(patterns['daily'])
    else:  # Forecasting
        st.header("Crime Forecasting")
        ts_data = prepare_time_series_data(df)
        forecast_periods = st.slider("Forecast Period (Days)", 7, 90, 30)
        with st.spinner("Training forecasting model and predicting..."):
            try:
                model, forecast = train_prophet_model(ts_data, forecast_periods)
                st.plotly_chart(create_forecast_plot(forecast))
                st.subheader("Seasonal Components")
                components = get_seasonal_decomposition(model, forecast)
                st.pyplot(components)
            except Exception as e:
                st.error(f"Forecasting error: {e}")

if __name__ == "__main__":
    main() 