import streamlit as st
import requests
import pandas as pd

# Clear any lingering state
st.cache_data.clear()

# --- Configuration ---
# Explicitly setting the working Compass telemetry/API gateway
API_BASE_URL = "https://livetrack.atcompass.net:9103"
API_KEY = "F3UM4oyt!oIDDxKRRI644h31"

st.set_page_config(page_title="Live HOS Dispatch Dashboard", layout="wide")
st.title("Live Fleet HOS & Recap Dashboard")

@st.cache_data(ttl=3600)
def fetch_active_drivers():
    url = f"{API_BASE_URL}/HOSDriver/v2.0/GetHOSDriversForClient"
    params = {"HOSClientApiKey": API_KEY, "DriverStatus": 1}
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()

@st.cache_data(ttl=60)
def fetch_hos_data():
    url = f"{API_BASE_URL}/HOSDashboard/v2.0/GetHoursOfServiceByDriverForClient"
    params = {"HOSClientApiKey": API_KEY, "HOSDriverId": -1}
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()

st.subheader("Current Driver Duty Status")

try:
    with st.spinner("Connecting to Apollo REST API..."):
        drivers_data = fetch_active_drivers()
        hos_data = fetch_hos_data()
    
    df_drivers = pd.DataFrame(drivers_data)
    df_hos = pd.DataFrame(hos_data)
    
    if not df_drivers.empty and not df_hos.empty:
        df_merged = pd.merge(df_hos, df_drivers, left_on="DriverId", right_on="Id", how="left")
        st.dataframe(df_merged, use_container_width=True, hide_index=True)
    else:
        st.warning("Connected successfully, but returned empty datasets.")
        
except Exception as e:
    st.error(f"Connection Error: {e}")
