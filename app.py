import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="UKHSA Respiratory Surveillance", layout="wide")
st.title("Public Health Surveillance and Forecasting Dashboard")
st.markdown("Automated 30-day case forecasting using Meta Prophet and live UKHSA API data.")

@st.cache_data
def load_data():
    df = pd.read_csv("data/forecast_results.csv")
    df['ds'] = pd.to_datetime(df['ds'])
    return df

df = load_data()

historical = df.dropna(subset=['y'])
forecast = df[df['ds'] > historical['ds'].max()]

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=historical['ds'], y=historical['y'], 
    mode='lines+markers', name='Actual Cases', line=dict(color='black')
))

fig.add_trace(go.Scatter(
    x=forecast['ds'], y=forecast['yhat'], 
    mode='lines', name='Forecasted Trend', line=dict(color='red', dash='dash')
))

fig.add_trace(go.Scatter(
    x=forecast['ds'].tolist() + forecast['ds'].tolist()[::-1],
    y=forecast['yhat_upper'].tolist() + forecast['yhat_lower'].tolist()[::-1],
    fill='toself', fillcolor='rgba(255, 0, 0, 0.2)', line=dict(color='rgba(255,255,255,0)'),
    name='95% Confidence Interval', showlegend=True
))

fig.update_layout(
    title="Daily COVID-19 PCR Testing Counts (England)",
    xaxis_title="Date", yaxis_title="Number of Cases",
    hovermode="x unified", template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

st.header("Briefing")

start_forecast = forecast.iloc[0]['yhat']
end_forecast = forecast.iloc[-1]['yhat']
percent_change = ((end_forecast - start_forecast) / start_forecast) * 100

st.subheader("Automated Trend Analysis")
if percent_change > 5:
    st.error(f"The model forecasts a {percent_change:.1f}% increase in cases over the next 30 days.")
elif percent_change < -5:
    st.success(f"The model forecasts a {abs(percent_change):.1f}% decrease in cases over the next 30 days.")
else:
    st.info(f"The model forecasts relatively stable case counts (changing by {percent_change:.1f}%) over the next 30 days.")

st.markdown("---")
st.markdown("This dashboard updates automatically every Monday at 3:00 AM UTC.")
