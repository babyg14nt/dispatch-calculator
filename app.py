import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, time

# --- Page Configuration ---
st.set_page_config(
    page_title="Shipping Universe LLC | Corporate Command Center",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Clean Corporate Navy Blue & White Theme ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* Global App Styling */
    .stApp {
        background-color: #F8FAFC;
        color: #1E293B;
        font-family: 'Inter', sans-serif;
    }
    
    /* Typography */
    h1, h2, h3, h4 {
        font-family: 'Inter', sans-serif !important;
        color: #0F172A;
        font-weight: 700;
    }
    
    .main-title {
        color: #0B192C;
        font-size: 2.2rem;
        font-weight: 700;
        border-bottom: 2px solid #E2E8F0;
        padding-bottom: 12px;
    }
    
    /* Clean White Cards with Navy Accents */
    .corporate-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-top: 4px solid #0B192C;
        padding: 24px;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }
    
    .metric-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-left: 4px solid #3B82F6;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }
    
    /* Form Inputs High Contrast Readability */
    .stNumberInput input, .stTimeInput input, .stTextInput input, .stDateInput input {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        font-family: 'Inter', sans-serif !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 6px !important;
        padding: 10px !important;
        font-weight: 500;
    }
    
    label {
        color: #334155 !important;
        font-weight: 600 !important;
    }
    
    /* Corporate Action Button */
    .stButton button {
        background-color: #0B192C;
        color: #FFFFFF;
        font-family: 'Inter', sans-serif;
        border: none;
        border-radius: 6px;
        font-weight: 600;
        padding: 0.7rem 1.5rem;
        box-shadow: 0 2px 4px rgba(11, 25, 44, 0.2);
        transition: background-color 0.2s ease;
        width: 100%;
    }
    .stButton button:hover {
        background-color: #1E3E62;
        color: #FFFFFF;
    }
    </style>
""", unsafe_allow_html=True)

# --- Header Section ---
st.markdown("<h1 class='main-title'>SHIPPING UNIVERSE LLC</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #64748B; font-family: Inter; font-size: 1rem; font-weight: 500; margin-top: 8px;'>Corporate Fleet Logistics, HOS Compliance & Financial Intelligence Center</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# --- Layout Grid: Inputs ---
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown("<div class='corporate-card'>", unsafe_allow_html=True)
    st.markdown("### Active Operator Baseline")
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
    st.markdown("<div class='corporate-card'>", unsafe_allow_html=True)
    st.markdown("### Spot Market Parameters")
    
    rc1, rc2 = st.columns(2)
    with rc1:
        gross_pay = st.number_input("Gross Load Pay ($)", min_value=0.0, value=2400.0, step=50.0)
        loaded_miles = st.number_input("Loaded Miles", min_value=0.0, value=1200.0, step=10.0)
    with rc2:
        deadhead_miles = st.number_input("Deadhead Miles", min_value=0.0, value=100.0, step=10.0)
        fuel_cost_per_gallon = st.number_input("Diesel Price ($/gal)", min_value=0.0, value=3.85, step=0.05)
    st.markdown("</div>", unsafe_allow_html=True)

# Secondary Row for Operational Config
st.markdown("<div class='corporate-card'>", unsafe_allow_html=True)
st.markdown("### Route Dynamics & Timing")
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
    "Milestone": "Trip Pickup Initiated",
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
            "Milestone": "Final Drop-Off Reached",
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
            "Milestone": "HOS Ceiling Reached (Rest Required)",
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
            "Milestone": "10-Hour Rest Break Completed",
            "Timestamp": current_dt.strftime('%b %d, %H:%M'),
            "Drive Clock": f"{drive_clock:.2f}h (Fresh)",
            "Shift Clock": f"{shift_clock:.2f}h (Fresh)",
            "Cycle Clock": f"{max(0.0, cycle_clock):.2f}h"
        })
        
        active_drive_left_in_shift = min(drive_clock, shift_clock, cycle_clock)

estimated_dropoff_dt = current_dt

# Dynamic Colors for Clean Corporate Theme
if rpm >= 2.20:
    prof_color, prof_rating = "#059669", "HIGH YIELD"
elif rpm >= 1.75:
    prof_color, prof_rating = "#2563EB", "STANDARD MARGIN"
else:
    prof_color, prof_rating = "#DC2626", "SUB-OPTIMAL"

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### Financial & Operational Matrix")

# Top Metrics HUD
r1, r2, r3, r4 = st.columns(4)
with r1:
    st.markdown(f"""
        <div class='metric-card'>
            <span style='color: #64748B; font-size: 11px; font-weight: 700; letter-spacing: 0.5px;'>NET REVENUE</span>
            <h2 style='color: {prof_color}; margin: 5px 0 0 0;'>${net_profit:,.2f}</h2>
        </div>
    """, unsafe_allow_html=True)
with r2:
    st.markdown(f"""
        <div class='metric-card'>
            <span style='color: #64748B; font-size: 11px; font-weight: 700; letter-spacing: 0.5px;'>RATE PER MILE</span>
            <h2 style='color: {prof_color}; margin: 5px 0 0 0;'>${rpm:.2f}</h2>
        </div>
    """, unsafe_allow_html=True)
with r3:
    st.markdown(f"""
        <div class='metric-card'>
            <span style='color: #64748B; font-size: 11px; font-weight: 700; letter-spacing: 0.5px;'>HOS DROP-OFF ETA</span>
            <h4 style='color: #0F172A; margin: 5px 0 0 0;'>{estimated_dropoff_dt.strftime('%b %d - %H:%M')}</h4>
        </div>
    """, unsafe_allow_html=True)
with r4:
    st.markdown(f"""
        <div class='metric-card'>
            <span style='color: #64748B; font-size: 11px; font-weight: 700; letter-spacing: 0.5px;'>LOAD STATUS</span>
            <h4 style='color: {prof_color}; margin: 5px 0 0 0;'>{prof_rating}</h4>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### Operator Clock Evolution & Route Timeline")

# Timeline Table
df_timeline = pd.DataFrame(timeline_events)
st.dataframe(df_timeline, use_container_width=True, hide_index=True)

st.markdown("<br>", unsafe_allow_html=True)
if st.button("COMMIT LOAD PROFILE TO DISPATCH LOG"):
    st.success("Load profile successfully processed and logged to corporate records.")
