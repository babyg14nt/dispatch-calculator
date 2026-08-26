import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, time

# --- Page Configuration ---
st.set_page_config(
    page_title="Shipping Universe LLC | Command Center",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Futuristic Minimal Theme Styling ---
st.markdown("""
    <style>
    .stApp {
        background-color: #0b0f19;
        color: #f3f4f6;
        font-family: 'Inter', sans-serif;
    }
    h1, h2, h3 {
        color: #38bdf8;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    .metric-card {
        background: rgba(17, 24, 39, 0.7);
        border: 1px solid rgba(56, 189, 248, 0.2);
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        backdrop-filter: blur(4px);
    }
    .stNumberInput input, .stTimeInput input, .stTextInput input {
        background-color: #1f2937 !important;
        color: #ffffff !important;
        border: 1px solid #374151 !important;
        border-radius: 8px !important;
    }
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
st.markdown("### SHIPPING UNIVERSE LLC")
st.markdown("<p style='color: #9ca3af; margin-top: -15px;'>HOS Compliance, Profitability & HOS-Strict ETA Command Center</p>", unsafe_allow_html=True)
st.markdown("---")

# --- Tab Layout for Clean Organization ---
tab1, tab2 = st.tabs(["⚡ HOS & Compliance HUD", "💰 Load Profitability & HOS ETA Analyzer"])

with tab1:
    st.markdown("#### Real-Time Driver Parameters")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        driver_name = st.text_input("Driver Name", "Unit-01 Operator", key="t1_name")
    with c2:
        driving_hours_left = st.number_input("Driving Hours Left (11h max)", min_value=0.0, max_value=11.0, value=8.5, step=0.25, key="t1_drive")
    with c3:
        shift_hours_left = st.number_input("Shift Window Left (14h max)", min_value=0.0, max_value=14.0, value=11.0, step=0.25, key="t1_shift")
    with c4:
        cycle_hours_left = st.number_input("70-Hour Cycle Available", min_value=0.0, max_value=70.0, value=45.25, step=0.25, key="t1_cycle")

    max_legal_drive = min(driving_hours_left, shift_hours_left, cycle_hours_left)

    if max_legal_drive > 4.0:
        status_color, status_text = "#10b981", "OPTIMAL STATUS"
    elif max_legal_drive > 1.5:
        status_color, status_text = "#f59e0b", "RESTRICTED WINDOW"
    else:
        status_color, status_text = "#ef4444", "CRITICAL BREAK REQUIRED"

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### Operational HUD")
    h1, h2, h3, h4 = st.columns(4)
    with h1:
        st.markdown(f"<div class='metric-card'><p style='color: #9ca3af; font-size: 14px;'>MAX LEGAL RUNWAY</p><h2 style='color: {status_color};'>{max_legal_drive:.2f} hrs</h2></div>", unsafe_allow_html=True)
    with h2:
        st.markdown(f"<div class='metric-card'><p style='color: #9ca3af; font-size: 14px;'>SYSTEM STATUS</p><h4 style='color: {status_color};'>{status_text}</h4></div>", unsafe_allow_html=True)
    with h3:
        st.markdown(f"<div class='metric-card'><p style='color: #9ca3af; font-size: 14px;'>CYCLE CAPACITY</p><h2 style='color: #38bdf8;'>{cycle_hours_left:.2f} hrs</h2></div>", unsafe_allow_html=True)
    with h4:
        st.markdown(f"<div class='metric-card'><p style='color: #9ca3af; font-size: 14px;'>ACTIVE OPERATOR</p><h4 style='color: #f3f4f6;'>{driver_name}</h4></div>", unsafe_allow_html=True)

with tab2:
    st.markdown("#### Spot Market Financials & Route Parameters")
    p1, p2, p3 = st.columns(3)
    with p1:
        gross_pay = st.number_input("Gross Load Pay ($)", min_value=0.0, value=2400.0, step=50.0)
        loaded_miles = st.number_input("Loaded Miles", min_value=0.0, value=1200.0, step=10.0)
    with p2:
        deadhead_miles = st.number_input("Deadhead Miles", min_value=0.0, value=100.0, step=10.0)
        fuel_cost_per_gallon = st.number_input("Diesel Price ($/gal)", min_value=0.0, value=3.85, step=0.05)
    with p3:
        truck_mpg = st.number_input("Fleet MPG", min_value=1.0, value=6.5, step=0.1)
        average_speed = st.number_input("Estimated Avg Speed (MPH)", min_value=10.0, value=55.0, step=1.0)

    st.markdown("---")
    st.markdown("#### Driver HOS Baseline for Dispatch ETA")
    
    # Mirroring current driver constraints into the ETA engine
    e1, e2, e3 = st.columns(3)
    with e1:
        current_drive_left = st.number_input("Current Drive Hours Left", min_value=0.0, max_value=11.0, value=float(driving_hours_left), step=0.25)
    with e2:
        current_shift_left = st.number_input("Current Shift Window Left", min_value=0.0, max_value=14.0, value=float(shift_hours_left), step=0.25)
    with e3:
        current_cycle_left = st.number_input("Current Cycle Hours Left", min_value=0.0, max_value=70.0, value=float(cycle_hours_left), step=0.25)

    st.markdown("---")
    st.markdown("#### Dispatch Timing & Expenses")
    t1, t2 = st.columns(2)
    with t1:
        pickup_date = st.date_input("Scheduled Pickup Date", datetime.now())
        pickup_time = st.time_input("Scheduled Pickup Time", time(8, 0))
    with t2:
        fixed_expenses = st.number_input("Other Expenses (Tolls, Lumper, etc. $)", min_value=0.0, value=150.0, step=10.0)

    # --- Financial Calculations ---
    total_miles = loaded_miles + deadhead_miles
    total_gallons = total_miles / truck_mpg if truck_mpg > 0 else 0
    total_fuel_cost = total_gallons * fuel_cost_per_gallon
    total_cost = total_fuel_cost + fixed_expenses
    net_profit = gross_pay - total_cost
    rpm = gross_pay / total_miles if total_miles > 0 else 0

    # --- Strict HOS-Based ETA Engine ---
    total_trip_hours_needed = total_miles / average_speed if average_speed > 0 else 0
    current_dt = datetime.combine(pickup_date, pickup_time)
    
    # Tracking operational clocks
    remaining_drive_to_complete = total_trip_hours_needed
    active_drive_left_in_shift = min(current_drive_left, current_shift_left, current_cycle_left)
    
    # Simulation loop accounting for mandatory 10-hour breaks
    while remaining_drive_to_complete > 0:
        if active_drive_left_in_shift >= remaining_drive_to_complete:
            # Can finish the trip within current legal limits without breaking
            current_dt += timedelta(hours=remaining_drive_to_complete)
            remaining_drive_to_complete = 0
        else:
            # Drive as much as legally possible until hitting the HOS ceiling
            current_dt += timedelta(hours=active_drive_left_in_shift)
            remaining_drive_to_complete -= active_drive_left_in_shift
            
            # Mandatory 10-hour sleeper berth/off-duty rest break required by FMCSA regulations
            current_dt += timedelta(hours=10)
            
            # Reset legal limits for the next fresh shift (11 hours max driving / 14 hour shift)
            active_drive_left_in_shift = 11.0

    estimated_dropoff_dt = current_dt

    # Profitability Color Codes
    if rpm >= 2.20:
        prof_color = "#10b981"
        prof_rating = "HIGHLY PROFITABLE"
    elif rpm >= 1.75:
        prof_color = "#38bdf8"
        prof_rating = "STANDARD MARGIN"
    else:
        prof_color = "#ef4444"
        prof_rating = "LOW MARGIN / SUB-OPTIMAL"

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### 📊 Profitability & HOS-Strict ETA Dashboard")
    
    r1, r2, r3, r4 = st.columns(4)
    with r1:
        st.markdown(f"<div class='metric-card'><p style='color: #9ca3af; font-size: 14px;'>NET PROFIT</p><h2 style='color: {prof_color};'>${net_profit:,.2f}</h2></div>", unsafe_allow_html=True)
    with r2:
        st.markdown(f"<div class='metric-card'><p style='color: #9ca3af; font-size: 14px;'>RATE PER MILE (RPM)</p><h2 style='color: {prof_color};'>${rpm:.2f}</h2></div>", unsafe_allow_html=True)
    with r3:
        st.markdown(f"<div class='metric-card'><p style='color: #9ca3af; font-size: 14px;'>HOS-STRICT DROP-OFF ETA</p><h4 style='color: #38bdf8; margin-top: 10px;'>{estimated_dropoff_dt.strftime('%b %d, %Y - %H:%M')}</h4></div>", unsafe_allow_html=True)
    with r4:
        st.markdown(f"<div class='metric-card'><p style='color: #9ca3af; font-size: 14px;'>LOAD RATING</p><h4 style='color: {prof_color}; margin-top: 10px;'>{prof_rating}</h4></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Commit Load Profile to Dispatch Log"):
        log_data = pd.DataFrame([{
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Company": "Shipping Universe LLC",
            "Gross Pay": f"${gross_pay:,.2f}",
            "Total Miles": total_miles,
            "RPM": f"${rpm:.2f}",
            "Net Profit": f"${net_profit:,.2f}",
            "HOS-Strict Drop-Off": estimated_dropoff_dt.strftime('%Y-%m-%d %H:%M')
        }])
        st.success("Load profile successfully processed and logged.")
        st.dataframe(log_data, use_container_width=True, hide_index=True)
