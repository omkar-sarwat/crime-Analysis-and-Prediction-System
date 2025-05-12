import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def create_crime_type_distribution(df):
    """
    Create a bar chart of crime type distribution.
    """
    crime_counts = df['Primary Type'].value_counts().head(10)
    fig = px.bar(
        x=crime_counts.index,
        y=crime_counts.values,
        title='Top 10 Most Common Crime Types',
        labels={'x': 'Crime Type', 'y': 'Count'}
    )
    return fig

def create_temporal_heatmap(df):
    """
    Create a heatmap showing crime patterns by hour and day of week.
    """
    # Create pivot table for heatmap
    heatmap_data = pd.crosstab(df['DayOfWeek'], df['Hour'])
    
    # Reorder days of week
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    heatmap_data = heatmap_data.reindex(days_order)
    
    fig = px.imshow(
        heatmap_data,
        title='Crime Patterns by Hour and Day of Week',
        labels={'x': 'Hour of Day', 'y': 'Day of Week'}
    )
    return fig

def create_monthly_trend(df):
    """
    Create a line chart showing monthly crime trends.
    """
    monthly_data = df.groupby(['Year', 'Month']).size().reset_index(name='count')
    monthly_data['date'] = pd.to_datetime(monthly_data[['Year', 'Month']].assign(day=1))
    
    fig = px.line(
        monthly_data,
        x='date',
        y='count',
        title='Monthly Crime Trends',
        labels={'date': 'Date', 'count': 'Number of Crimes'}
    )
    return fig

def create_forecast_plot(forecast):
    """
    Create a plot showing the forecast results.
    """
    fig = go.Figure()
    
    # Add actual values
    fig.add_trace(go.Scatter(
        x=forecast['ds'],
        y=forecast['yhat'],
        name='Forecast',
        line=dict(color='blue')
    ))
    
    # Add confidence intervals
    fig.add_trace(go.Scatter(
        x=forecast['ds'],
        y=forecast['yhat_upper'],
        fill=None,
        mode='lines',
        line_color='rgba(0,100,80,0.2)',
        name='Upper Bound'
    ))
    
    fig.add_trace(go.Scatter(
        x=forecast['ds'],
        y=forecast['yhat_lower'],
        fill='tonexty',
        mode='lines',
        line_color='rgba(0,100,80,0.2)',
        name='Lower Bound'
    ))
    
    fig.update_layout(
        title='Crime Forecast with Confidence Intervals',
        xaxis_title='Date',
        yaxis_title='Predicted Number of Crimes'
    )
    
    return fig

def create_hotspot_summary(hotspot_patterns):
    """
    Create a summary visualization of hotspot patterns.
    """
    # Convert hotspot patterns to DataFrame
    hotspot_df = pd.DataFrame.from_dict(hotspot_patterns, orient='index')
    
    # Create bar chart of total crimes by hotspot
    fig = px.bar(
        hotspot_df,
        x=hotspot_df.index,
        y='total_crimes',
        title='Total Crimes by Hotspot',
        labels={'x': 'Hotspot', 'y': 'Total Crimes'}
    )
    
    return fig 