import requests
import pandas as pd
import os

def fetch_ukhsa_data():
    """
    Fetches surveillance data directly from the official UK Health Security Agency API.
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
    """
    Runs automated assertion checks to ensure data quality before modeling.
    """
    assert not df.empty, "Assertion Failed: Dataframe is empty!"
    assert df['y'].isnull().sum() == 0, "Assertion Failed: Missing values found in target metric!"
    assert df['ds'].is_monotonic_increasing, "Assertion Failed: Dates are not strictly ascending!"
    print("All data quality checks passed.")

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    
    raw_data = fetch_ukhsa_data()
    print(f"Retrieved {len(raw_data)} data points from UKHSA.")
    
    validate_data(raw_data)
    
    output_path = os.path.join("data", "ukhsa_raw_data.csv")
    raw_data.to_csv(output_path, index=False)
    print(f"Data saved successfully to {output_path}")
