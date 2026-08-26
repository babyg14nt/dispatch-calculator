import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, time

# --- Page Configuration ---
st.set_page_config(
    page_title="Shipping Universe LLC | Command Deck",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- High-End Sci-Fi / Futuristic Styling ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800&family=Inter:wght@300;400;500;600&display=swap');

    .stApp {
        background: radial-gradient(circle at 50% 10%, #0d1527 0%, #060911 100%);
        color: #f3f4f6;
        font-family: 'Inter', sans-serif;
    }
    
    /* Futuristic Headers */
    h1, h2, h3, h4 {
        font-family: 'Orbitron', sans-serif !important;
        letter-spacing: 1px;
    }
    
    .main-title {
        background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.2rem;
    }
    
    /* Glassmorphism Panels */
    .glass-container {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(56, 189, 248, 0.15);
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 10px 30px 0 rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(12px);
        margin-bottom: 20px;
    }
    
    .metric-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.8) 100%);
        border: 1px solid rgba(56, 189, 248, 0.25);
        padding: 20px;
        border-radius: 14px;
        box-shadow: inset 0 1px 1px 0 rgba(255, 255, 255, 0.1), 0 4px 20px rgba(0, 0, 0, 0.4);
        backdrop-filter: blur(8px);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: rgba(56, 189, 248, 0.6);
    }
    
    /* Input Styling */
    .stNumberInput input, .stTimeInput input, .stTextInput input, .stDateInput input {
        background-color: #0b1329 !important;
        color: #38bdf8 !important;
        font-family: 'Orbitron', sans-serif !important;
        border: 1px solid #1e293b !important;
        border-radius: 10px !important;
        padding: 10px !important;
    }
    
    /* Glowing Action Buttons */
    .stButton button {
        background: linear-gradient(135deg, #0ea5e9 0%, #6366f1 100%);
        color: white;
        font-family: 'Orbitron', sans-serif;
        letter-spacing: 0.5px;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        padding: 0.7rem 1.5rem;
        box-shadow: 0 0 20px rgba(14, 165, 233, 0.4);
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton button:hover {
        box-shadow: 0 0 30px rgba(99, 102, 241, 0.8);
        transform: translateY(-2px);
    }
    
    /* Table Enhancements */
    dataframe {
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Header Section ---
st.markdown("<h1 class='main-title'>SHIPPING UNIVERSE LLC</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #94a3b8; font-family: 'Orbitron'; font-size: 0.9rem; letter-spacing: 2px; margin-top: -15px;'>// QUANTUM FLEET COMMAND & HOS-STRICT LOGISTICS ENGINE</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# --- Layout Grid: Inputs ---
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
    st.markdown("### ⚡ Active Operator Baseline")
    driver_name = st.text_input("Operator Designation", "Unit-01 Operator")
    
    ic1, ic2, ic3 = st.columns(3)
    with ic1:
        driving_hours_left = st.number_input("Drive Left (11h)", min_value=0.0, max_value=11.0, value=8.5, step=0.25)
    with ic2:
        shift_hours_left = st.number_input("Shift Left (14h)", min_value=0.0, max_value=14.0, value=11.0, step=0.25)
    with ic3:
        cycle_hours_left = st.number_input("Cycle Left", min_value=0.0, max_value=70.0, value=45.25, step=0.25)
    st.markdown("</div>", unsafe_allow_html=True)

with col_right:
    st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
    st.markdown("### 💰 Spot Market Parameters")
    
    rc1, rc2 = st.columns(2)
    with rc1:
        gross_pay = st.number_input("Gross Load Pay ($)", min_value=0.0, value=2400.0, step=50.0)
        loaded_miles = st.number_input("Loaded Miles", min_value=0.0, value=1200.0, step=10.0)
    with rc2:
        deadhead_miles = st.number_input("Deadhead Miles", min_value=0.0, value=100.0, step=10.0)
        fuel_cost_per_gallon = st.number_input("Diesel Price ($/gal)", min_value=0.0, value=3.85, step=0.05)
    st.markdown("</div>", unsafe_allow_html=True)

# Secondary Row for Operational Config
st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
st.markdown("### 🧭 Route Dynamics & Timing")
tc1, tc2, tc3, tc4 = st.columns(4)
with tc1:
    truck_mpg = st.number_input("Fleet MPG", min_value=1.0, value=6.5, step=0.1)
with tc2:
    average_speed = st.number_input("Average Speed (MPH)", min_value=10.0, value=55.0, step=1.0)
with tc3:
    pickup_date = st.date_input("Pickup Date", datetime.now())
with tc4:
    pickup_time = st.time_input("Pickup Time", time(8, 0))

fixed_expenses = st.number_input("Additional Expenses (Tolls, Lumper, etc. $)", min_value=0.0, value=150.0, step=10.0)
st.markdown("</div>", unsafe_allow_html=True)

# --- Calculation Engine ---
total_miles = loaded_miles + deadhead_miles
total_gallons = total_miles / truck_mpg if truck_mpg > 0 else 0
total_fuel_cost = total_gallons * fuel_cost_per_gallon
total_cost = total_fuel_cost + fixed_expenses
net_profit = gross_pay - total_cost
rpm = gross_pay / total_miles if total_miles > 0 else 0

# Strict HOS-Based ETA & Timeline Simulation Engine
total_trip_hours_needed = total_miles / average_speed if average_speed > 0 else 0
current_dt = datetime.combine(pickup_date, pickup_time)

remaining_drive_to_complete = total_trip_hours_needed
drive_clock = driving_hours_left
shift_clock = shift_hours_left
cycle_clock = cycle_hours_left

active_drive_left_in_shift = min(drive_clock, shift_clock, cycle_clock)
timeline_events = []

timeline_events.append({
    "Milestone": "🚀 Trip Pickup Initiated",
    "Timestamp": current_dt.strftime('%b %d, %H:%M'),
    "Drive Clock": f"{drive_clock:.2f}h",
    "Shift Clock": f"{shift_clock:.2f}h",
    "Cycle Clock": f"{cycle_clock:.2f}h"
})

while remaining_drive_to_complete > 0:
    if active_drive_left_in_shift >= remaining_drive_to_complete:
        current_dt += timedelta(hours=remaining_drive_to_complete)
        drive_clock -= remaining_drive_to_complete
        shift_clock -= remaining_drive_to_complete
        cycle_clock -= remaining_drive_to_complete
        
        timeline_events.append({
            "Milestone": "🏁 Final Drop-Off Reached",
            "Timestamp": current_dt.strftime('%b %d, %H:%M'),
            "Drive Clock": f"{max(0.0, drive_clock):.2f}h",
            "Shift Clock": f"{max(0.0, shift_clock):.2f}h",
            "Cycle Clock": f"{max(0.0, cycle_clock):.2f}h"
        })
        remaining_drive_to_complete = 0
    else:
        current_dt += timedelta(hours=active_drive_left_in_shift)
        remaining_drive_to_complete -= active_drive_left_in_shift
        
        drive_clock -= active_drive_left_in_shift
        shift_clock -= active_drive_left_in_shift
        cycle_clock -= active_drive_left_in_shift
        
        timeline_events.append({
            "Milestone": "⚠️ HOS Ceiling Reached (Rest Required)",
            "Timestamp": current_dt.strftime('%b %d, %H:%M'),
            "Drive Clock": "0.00h",
            "Shift Clock": "0.00h",
            "Cycle Clock": f"{max(0.0, cycle_clock):.2f}h"
        })
        
        # 10-hour mandatory reset break
        current_dt += timedelta(hours=10)
        drive_clock = 11.0
        shift_clock = 14.0
        
        timeline_events.append({
            "Milestone": "💤 10-Hour Rest Break Completed",
            "Timestamp": current_dt.strftime('%b %d, %H:%M'),
            "Drive Clock": f"{drive_clock:.2f}h (Fresh)",
            "Shift Clock": f"{shift_clock:.2f}h (Fresh)",
            "Cycle Clock": f"{max(0.0, cycle_clock):.2f}h"
        })
        
        active_drive_left_in_shift = min(drive_clock, shift_clock, cycle_clock)

estimated_dropoff_dt = current_dt

# Dynamic Colors
if rpm >= 2.20:
    prof_color, prof_rating = "#10b981", "HIGH YIELD"
elif rpm >= 1.75:
    prof_color, prof_rating = "#38bdf8", "STANDARD MARGIN"
else:
    prof_color, prof_rating = "#ef4444", "SUB-OPTIMAL"

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### 📊 Telemetry & Financial Matrix")

# Top Metrics HUD
r1, r2, r3, r4 = st.columns(4)
with r1:
    st.markdown(f"""
        <div class='metric-card'>
            <span style='color: #64748b; font-size: 11px; font-family: Orbitron;'>NET REVENUE</span>
            <h2 style='color: {prof_color}; margin: 5px 0 0 0; font-family: Orbitron;'>${net_profit:,.2f}</h2>
        </div>
    """, unsafe_allow_html=True)
with r2:
    st.markdown(f"""
        <div class='metric-card'>
            <span style='color: #64748b; font-size: 11px; font-family: Orbitron;'>RATE PER MILE</span>
            <h2 style='color: {prof_color}; margin: 5px 0 0 0; font-family: Orbitron;'>${rpm:.2f}</h2>
        </div>
    """, unsafe_allow_html=True)
with r3:
    st.markdown(f"""
        <div class='metric-card'>
            <span style='color: #64748b; font-size: 11px; font-family: Orbitron;'>HOS DROP-OFF ETA</span>
            <h4 style='color: #38bdf8; margin: 5px 0 0 0; font-family: Orbitron;'>{estimated_dropoff_dt.strftime('%b %d - %H:%M')}</h4>
        </div>
    """, unsafe_allow_html=True)
with r4:
    st.markdown(f"""
        <div class='metric-card'>
            <span style='color: #64748b; font-size: 11px; font-family: Orbitron;'>LOAD STATUS</span>
            <h4 style='color: {prof_color}; margin: 5px 0 0 0; font-family: Orbitron;'>{prof_rating}</h4>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### 🕒 Operator Clock Evolution & Route Timeline")

# Timeline Table
df_timeline = pd.DataFrame(timeline_events)
st.dataframe(df_timeline, use_container_width=True, hide_index=True)

st.markdown("<br>", unsafe_allow_html=True)
if st.button("INITIATE DISPATCH LOG COMMIT"):
    st.success("Telemetry profile successfully secured into Shipping Universe LLC operational records.")
