import streamlit as st
import pandas as pd
from datetime import datetime, time

# --- Page Configuration ---
st.set_page_config(
    page_title="Shipping Universe LLC | HOS Calculator",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Futuristic Minimal Theme Styling ---
st.markdown("""
    <style>
    /* Main Background & Font */
    .stApp {
        background-color: #0b0f19;
        color: #f3f4f6;
        font-family: 'Inter', sans-serif;
    }
    
    /* Neon Header Accents */
    h1, h2, h3 {
        color: #38bdf8;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    
    /* Minimal Glassmorphism Cards */
    .metric-card {
        background: rgba(17, 24, 39, 0.7);
        border: 1px solid rgba(56, 189, 248, 0.2);
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        backdrop-filter: blur(4px);
    }
    
    /* Custom Inputs */
    .stNumberInput input, .stTimeInput input {
        background-color: #1f2937 !important;
        color: #ffffff !important;
        border: 1px solid #374151 !important;
        border-radius: 8px !important;
    }
    
    /* Futuristic Button */
    .stButton button {
        background: linear-gradient(135deg, #0ea5e9 0%, #2563eb 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.6rem 1.2rem;
        box-shadow: 0 0 15px rgba(14, 165, 233, 0.4);
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        box-shadow: 0 0 25px rgba(14, 165, 233, 0.8);
        transform: translateY(-1px);
    }
    </style>
""", unsafe_allow_html=True)

# --- Header Section ---
col_logo, col_title = st.columns([0.1, 0.9])
with col_title:
    st.markdown("### SHIPPING UNIVERSE LLC")
    st.markdown("<p style='color: #9ca3af; margin-top: -15px;'>Next-Gen Fleet HOS & Recap Operations Command</p>", unsafe_allow_html=True)

st.markdown("---")

# --- Interactive Input Panel ---
st.markdown("#### ⚡ Real-Time Driver Parameters")
input_col1, input_col2, input_col3, input_col4 = st.columns(4)

with input_col1:
    driver_name = st.text_input("Driver Name", "Unit-01 Operator")
with input_col2:
    driving_hours_left = st.number_input("Driving Hours Left (11h max)", min_value=0.0, max_value=11.0, value=8.5, step=0.25)
with input_col3:
    shift_hours_left = st.number_input("Shift Window Left (14h max)", min_value=0.0, max_value=14.0, value=11.0, step=0.25)
with input_col4:
    cycle_hours_left = st.number_input("70-Hour Cycle Available", min_value=0.0, max_value=70.0, value=45.25, step=0.25)

st.markdown("<br>", unsafe_allow_html=True)

# --- Calculations ---
# Determine the binding constraint (the minimum time available before a mandatory stop)
max_legal_drive = min(driving_hours_left, shift_hours_left, cycle_hours_left)

# Status Assessment Color Codes
if max_legal_drive > 4.0:
    status_color = "#10b981" # Green
    status_text = "OPTIMAL STATUS"
elif max_legal_drive > 1.5:
    status_color = "#f59e0b" # Amber
    status_text = "RESTRICTED WINDOW"
else:
    status_color = "#ef4444" # Red
    status_text = "CRITICAL BREAK REQUIRED"

# --- HUD Dashboard Display ---
st.markdown("#### 📊 Operational HUD")
hud1, hud2, hud3, hud4 = st.columns(4)

with hud1:
    st.markdown(f"""
        <div class="metric-card">
            <p style='color: #9ca3af; font-size: 14px; margin-bottom: 0;'>MAX LEGAL RUNWAY</p>
            <h2 style='color: {status_color}; margin-top: 5px;'>{max_legal_drive:.2f} hrs</h2>
        </div>
    """, unsafe_allow_html=True)

with hud2:
    st.markdown(f"""
        <div class="metric-card">
            <p style='color: #9ca3af; font-size: 14px; margin-bottom: 0;'>SYSTEM STATUS</p>
            <h4 style='color: {status_color}; margin-top: 10px;'>{status_text}</h4>
        </div>
    """, unsafe_allow_html=True)

with hud3:
    st.markdown(f"""
        <div class="metric-card">
            <p style='color: #9ca3af; font-size: 14px; margin-bottom: 0;'>CYCLE CAPACITY</p>
            <h2 style='color: #38bdf8; margin-top: 5px;'>{cycle_hours_left:.2f} hrs</h2>
        </div>
    """, unsafe_allow_html=True)

with hud4:
    st.markdown(f"""
        <div class="metric-card">
            <p style='color: #9ca3af; font-size: 14px; margin-bottom: 0;'>ACTIVE OPERATOR</p>
            <h4 style='color: #f3f4f6; margin-top: 10px;'>{driver_name}</h4>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# --- Action & Logging Simulator ---
if st.button("Generate Operator Status Snapshot"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    snapshot_data = pd.DataFrame([{
        "Timestamp": timestamp,
        "Company": "Shipping Universe LLC",
        "Operator": driver_name,
        "Driving Hours Left": driving_hours_left,
        "Shift Window Left": shift_hours_left,
        "Cycle Left": cycle_hours_left,
        "Effective Limit": max_legal_drive,
        "Status": status_text
    }])
    
    st.success("Snapshot compiled successfully into dispatch buffer.")
    st.dataframe(snapshot_data, use_container_width=True, hide_index=True)
