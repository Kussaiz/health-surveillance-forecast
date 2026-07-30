import requests
import pandas as pd
from prophet import Prophet
import os
import warnings

warnings.filterwarnings('ignore')

def fetch_ukhsa_data():
    """
    Fetches respiratory surveillance data directly from the official UKHSA API.
    """
    print("Connecting to UKHSA API...")
    url = (
        "https://api.ukhsa-dashboard.data.gov.uk/"
        "themes/infectious_disease/sub_themes/respiratory/topics/COVID-19/"
        "geography_types/Nation/geographies/England/"
        "metrics/COVID-19_testing_PCRcountByDay?page_size=365"
    )
    
    response = requests.get(url)
    if response.status_code != 200:
        raise ConnectionError(f"Failed to fetch data from UKHSA API. HTTP Status: {response.status_code}")
        
    data = response.json()
    results = data.get("results", [])
    
    df = pd.DataFrame(results)
    df = df[['date', 'metric_value']].copy()
    df.rename(columns={'date': 'ds', 'metric_value': 'y'}, inplace=True)
    df['ds'] = pd.to_datetime(df['ds'])
    df = df.sort_values('ds').reset_index(drop=True)
    
    return df

def validate_data(df):
    assert not df.empty, "Assertion Failed: Dataframe is empty"
    assert df['y'].isnull().sum() == 0, "Assertion Failed: Missing values found in target metric"
    assert df['ds'].is_monotonic_increasing, "Assertion Failed: Dates are not strictly ascending"
    print("All data quality checks passed.")

def run_forecast(df, forecast_days=30):
    """
    Fits a Prophet time-series model with a 95% confidence interval.
    """
    print(f"Fitting Prophet model for a {forecast_days}-day forecast horizon...")
    
    model = Prophet(
        interval_width=0.95,
        weekly_seasonality=True,
        daily_seasonality=False,
        yearly_seasonality=True
    )
    
    model.fit(df)
    
    future = model.make_future_dataframe(periods=forecast_days)
    forecast = model.predict(future)
    
    forecast_filtered = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].copy()
    
    output_df = pd.merge(forecast_filtered, df[['ds', 'y']], on='ds', how='left')
    
    return output_df

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    
    raw_data = fetch_ukhsa_data()
    print(f"Retrieved {len(raw_data)}")
    
    validate_data(raw_data)
    
    raw_data.to_csv("data/ukhsa_raw_data.csv", index=False)
    
    forecast_df = run_forecast(raw_data, forecast_days=30)
    output_path = os.path.join("data", "forecast_results.csv")
    forecast_df.to_csv(output_path, index=False)
    
    print(f"Forecast dataset saved to {output_path}")
