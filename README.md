# Public Health Surveillance & Forecasting Pipeline

[![Python](https://img.shields.io/badge/Python-3.10-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B.svg)](https://share.streamlit.io/)
[![GitHub Actions](https://img.shields.io/badge/Automated-CI%2FCD-2ea44f)](https://github.com/features/actions)

## Project Overview
This repository contains an automated pipeline that fetches, validates, and forecasts daily respiratory infection data for England.

Interactive Dashboard: https://health-surveillance-forecast.streamlit.app/

1. Automatically queries the open UK Health Security Agency (UKHSA) REST API for COVID-19 PCR testing counts.
2. Fits a Prophet time-series model to generate a 30-day forecast with 95% uncertainty intervals.
3. A GitHub Actions cron job runs `pipeline.py` every Monday at 3:00 AM UTC, pushing updated predictions back to the repository.
4. A Streamlit application (`app.py`) reads the automated data and visualizes it using Plotly.

## Repository Structure
`.github/workflows/update_data.yml`: CI/CD automation configuration.
`data/`: Contains the automated historical and forecasted CSV datasets.
`pipeline.py`: The main validation and analysis.
`app.py`: The Streamlit frontend and Plotly visualization script.
`environment.yml`: Conda environment.
`requirements.txt`: pip requirements for Streamlit.
