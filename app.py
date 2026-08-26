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
st.markdown("<p style='color: #9ca3af; margin-top: -15px;'>Unified HOS Compliance, Profitability & Timeline Command Center</p>", unsafe_allow_html=True)
st.markdown("---")

# --- Section 1: Operator HOS Baseline ---
st.markdown("#### ⚡ 1. Active Operator HOS Baseline")
c1, c2, c3, c4 = st.columns(4)
with c1:
    driver_name = st.text_input("Driver Name", "Unit-01 Operator")
with c2:
    driving_hours_left = st.number_input("Driving Hours Left (11h max)", min_value=0.0, max_value=11.0, value=8.5, step=0.25)
with c3:
    shift_hours_left = st.number_input("Shift Window Left (14h max)", min_value=0.0, max_value=14.0, value=11.0, step=0.25)
with c4:
    cycle_hours_left = st.number_input("70-Hour Cycle Available", min_value=0.0, max_value=70.0, value=45.25, step=0.25)

st.markdown("---")

# --- Section 2: Load Financials & Route Parameters ---
st.markdown("#### 💰 2. Spot Market Financials & Route Parameters")
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

t1, t2 = st.columns(2)
with t1:
    pickup_date = st.date_input("Scheduled Pickup Date", datetime.now())
    pickup_time = st.time_input("Scheduled Pickup Time", time(8, 0))
with t2:
    fixed_expenses = st.number_input("Other Expenses (Tolls, Lumper, etc. $)", min_value=0.0, value=150.0, step=10.0)

# --- Calculations ---
total_miles = loaded_miles + deadhead_miles
total_gallons = total_miles / truck_mpg if truck_mpg > 0 else 0
total_fuel_cost = total_gallons * fuel_cost_per_gallon
total_cost = total_fuel_cost + fixed_expenses
net_profit = gross_pay - total_cost
rpm = gross_pay / total_miles if total_miles > 0 else 0

# Strict HOS-Based ETA & Step-by-Step Timeline Simulation Engine
total_trip_hours_needed = total_miles / average_speed if average_speed > 0 else 0
current_dt = datetime.combine(pickup_date, pickup_time)

remaining_drive_to_complete = total_trip_hours_needed
drive_clock = driving_hours_left
shift_clock = shift_hours_left
cycle_clock = cycle_hours_left

active_drive_left_in_shift = min(drive_clock, shift_clock, cycle_clock)
timeline_events = []

# Log initial state
timeline_events.append({
    "Milestone": "Trip Pickup Started",
    "Time": current_dt.strftime('%b %d, %H:%M'),
    "Driving Clock": f"{drive_clock:.2f}h",
    "Shift Clock": f"{shift_clock:.2f}h",
    "Cycle Clock": f"{cycle_clock:.2f}h"
})

while remaining_drive_to_complete > 0:
    if active_drive_left_in_shift >= remaining_drive_to_complete:
        # Finishes trip on current shift
        current_dt += timedelta(hours=remaining_drive_to_complete)
        drive_clock -= remaining_drive_to_complete
        shift_clock -= remaining_drive_to_complete
        cycle_clock -= remaining_drive_to_complete
        
        timeline_events.append({
            "Milestone": "Final Drop-Off Reached",
            "Time": current_dt.strftime('%b %d, %H:%M'),
            "Driving Clock": f"{max(0.0, drive_clock):.2f}h",
            "Shift Clock": f"{max(0.0, shift_clock):.2f}h",
            "Cycle Clock": f"{max(0.0, cycle_clock):.2f}h"
        })
        remaining_drive_to_complete = 0
    else:
        # Drive until limit reached
        current_dt += timedelta(hours=active_drive_left_in_shift)
        remaining_drive_to_complete -= active_drive_left_in_shift
        
        drive_clock -= active_drive_left_in_shift
        shift_clock -= active_drive_left_in_shift
        cycle_clock -= active_drive_left_in_shift
        
        timeline_events.append({
            "Milestone": "HOS Limit Reached (Driving/Shift Max)",
            "Time": current_dt.strftime('%b %d, %H:%M'),
            "Driving Clock": "0.00h (Exhausted)",
            "Shift Clock": "0.00h (Exhausted)",
            "Cycle Clock": f"{max(0.0, cycle_clock):.2f}h"
        })
        
        # Take mandatory 10-hour reset break
        current_dt += timedelta(hours=10)
        
        # Fresh shift reset values
        drive_clock = 11.0
        shift_clock = 14.0
        
        timeline_events.append({
            "Milestone": "10-Hour Rest Break Completed",
            "Time": current_dt.strftime('%b %d, %H:%M'),
            "Driving Clock": f"{drive_clock:.2f}h (Reset)",
            "Shift Clock": f"{shift_clock:.2f}h (Reset)",
            "Cycle Clock": f"{max(0.0, cycle_clock):.2f}h"
        })
        
        active_drive_left_in_shift = min(drive_clock, shift_clock, cycle_clock)

estimated_dropoff_dt = current_dt

# Profitability Color Codes
if rpm >= 2.20:
    prof_color, prof_rating = "#10b981", "HIGHLY PROFITABLE"
elif rpm >= 1.75:
    prof_color, prof_rating = "#38bdf8", "STANDARD MARGIN"
else:
    prof_color, prof_rating = "#ef4444", "LOW MARGIN / SUB-OPTIMAL"

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("#### 📊 Command Center Output & Drop-Off Projections")

# Top Metrics Row
r1, r2, r3, r4 = st.columns(4)
with r1:
    st.markdown(f"<div class='metric-card'><p style='color: #9ca3af; font-size: 14px;'>NET PROFIT</p><h2 style='color: {prof_color};'>${net_profit:,.2f}</h2></div>", unsafe_allow_html=True)
with r2:
    st.markdown(f"<div class='metric-card'><p style='color: #9ca3af; font-size: 14px;'>RATE PER MILE (RPM)</p><h2 style='color: {prof_color};'>${rpm:.2f}</h2></div>", unsafe_allow_html=True)
with r3:
    st.markdown(f"<div class='metric-card'><p style='color: #9ca3af; font-size: 14px;'>HOS DROP-OFF ETA</p><h4 style='color: #38bdf8; margin-top: 10px;'>{estimated_dropoff_dt.strftime('%b %d, %Y - %H:%M')}</h4></div>", unsafe_allow_html=True)
with r4:
    st.markdown(f"<div class='metric-card'><p style='color: #9ca3af; font-size: 14px;'>LOAD RATING</p><h4 style='color: {prof_color}; margin-top: 10px;'>{prof_rating}</h4></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("#### 🕒 Step-by-Step Trip Clock Timeline (HOS Evolution)")
st.markdown("<p style='color: #9ca3af; font-size: 14px; margin-top: -15px;'>This table tracks how the driver's clock changes dynamically at every stage of transit, including mandatory rest breaks.</p>", unsafe_allow_html=True)

# Render the timeline dataframe cleanly
df_timeline = pd.DataFrame(timeline_events)
st.dataframe(df_timeline, use_container_width=True, hide_index=True)

st.markdown("<br>", unsafe_allow_html=True)
if st.button("Commit Load Profile to Dispatch Log"):
    log_data = pd.DataFrame([{
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Company": "Shipping Universe LLC",
        "Operator": driver_name,
        "Gross Pay": f"${gross_pay:,.2f}",
        "Total Miles": total_miles,
        "RPM": f"${rpm:.2f}",
        "Net Profit": f"${net_profit:,.2f}",
        "HOS Drop-Off": estimated_dropoff_dt.strftime('%Y-%m-%d %H:%M')
    }])
    st.success("Load profile successfully processed and logged.")
    st.dataframe(log_data, use_container_width=True, hide_index=True)
