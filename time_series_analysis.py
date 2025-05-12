from prophet import Prophet
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def train_prophet_model(data, forecast_periods=30):
    """
    Train a Prophet model for crime forecasting.
    """
    # Initialize and fit the model
    model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=True,
        daily_seasonality=True
    )
    model.fit(data)
    
    # Make future predictions
    future = model.make_future_dataframe(periods=forecast_periods)
    forecast = model.predict(future)
    
    return model, forecast

def analyze_temporal_patterns(df):
    """
    Analyze temporal patterns in crime data.
    """
    # Hourly patterns
    hourly_patterns = df.groupby('Hour').size()
    
    # Daily patterns
    daily_patterns = df.groupby('DayOfWeek').size()
    
    # Monthly patterns
    monthly_patterns = df.groupby('Month').size()
    
    # Yearly trends
    yearly_trends = df.groupby('Year').size()
    
    return {
        'hourly': hourly_patterns,
        'daily': daily_patterns,
        'monthly': monthly_patterns,
        'yearly': yearly_trends
    }

def get_seasonal_decomposition(model, forecast):
    """
    Extract seasonal components from the Prophet model.
    """
    components = model.plot_components(forecast)
    return components

def evaluate_forecast(actual, predicted):
    """
    Evaluate the forecast accuracy using common metrics.
    """
    from sklearn.metrics import mean_absolute_error, mean_squared_error
    
    mae = mean_absolute_error(actual, predicted)
    rmse = np.sqrt(mean_squared_error(actual, predicted))
    
    return {
        'MAE': mae,
        'RMSE': rmse
    } 