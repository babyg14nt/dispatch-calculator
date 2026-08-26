import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# --- Configuration ---
API_BASE_URL = "https://livetrack.atcompass.net:9103" # Try this first
API_KEY = "F3UM4oyt!oIDDxKRRI644h31"

st.set_page_config(page_title="Live HOS Dispatch Dashboard", layout="wide")
st.title("Live Fleet HOS & Recap Dashboard")

# --- Data Fetching Functions ---
# Caching the roster for 1 hour to save API calls, as active drivers change infrequently.
@st.cache_data(ttl=3600)
def fetch_active_drivers():
    url = f"{API_BASE_URL}/HOSDriver/v2.0/GetHOSDriversForClient"
    params = {
        "HOSClientApiKey": API_KEY,
        "DriverStatus": 1 # 1 = Active Drivers Only
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching driver roster: {e}")
        return None

# Caching live HOS data for 60 seconds.
@st.cache_data(ttl=60) 
def fetch_hos_data():
    url = f"{API_BASE_URL}/HOSDashboard/v2.0/GetHoursOfServiceByDriverForClient"
    params = {
        "HOSClientApiKey": API_KEY,
        "HOSDriverId": -1 # -1 = All Drivers
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching live HOS data: {e}")
        return None

# --- Main Application Logic ---
st.subheader("Current Driver Duty Status")

with st.spinner("Fetching data from Apollo REST API..."):
    drivers_data = fetch_active_drivers()
    hos_data = fetch_hos_data()

if drivers_data and hos_data:
    # Convert API responses into Pandas DataFrames for easy manipulation
    df_drivers = pd.DataFrame(drivers_data)
    df_hos = pd.DataFrame(hos_data)
    
    if not df_drivers.empty and not df_hos.empty:
        # Map the relevant IDs to join the data (Adjust column names based on exact API JSON response)
        # Assuming 'Id' in drivers matches 'DriverId' in HOS data based on standard patterns.
        df_merged = pd.merge(
            df_hos, 
            df_drivers, 
            left_on="DriverId", 
            right_on="Id", 
            how="left"
        )
        
        # Select and rename columns to make the dashboard readable
        # Note: You may need to tweak these exact string names depending on the raw JSON keys
        display_columns = {
            "DriverName": "Driver Name",
            "CurrentDutyStatus": "Duty Status",
            "DrivingLeft": "Driving Time Left",
            "ShiftLeft": "Shift Time Left",
            "CycleLeft": "Cycle Time Left (Recap)",
            "NextBreak": "Next Break Required"
        }
        
        # Filter only the columns that actually exist in the merged dataframe to avoid KeyError
        available_cols = {k: v for k, v in display_columns.items() if k in df_merged.columns}
        
        df_display = df_merged[list(available_cols.keys())].rename(columns=available_cols)
        
        # Display as an interactive dataframe
        st.dataframe(df_display, use_container_width=True, hide_index=True)
        
        # Adding a refresh button to clear the 60-second cache instantly if needed
        if st.button("Force Live Refresh"):
            fetch_hos_data.clear()
            st.rerun()
    else:
        st.warning("Data was retrieved successfully, but no driver records were found.")
else:
    st.info("Check your API key or base URL configuration.")
