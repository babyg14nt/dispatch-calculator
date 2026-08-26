import streamlit as st
import datetime
import math

st.set_page_config(page_title="Dispatch Calculator", layout="wide")
st.title("🚛 Spot Market Load & Dispatch Calculator")

# Sidebar: Settings & Overhead Controls
st.sidebar.header("Equipment & Cost Settings")
equipment = st.sidebar.selectbox("Equipment Type", ["Sleeper Tractor", "Box Truck", "Day Cab"])
fuel_price = st.sidebar.number_input("Fuel Price ($/gal)", value=3.65, step=0.05)
avg_mpg = st.sidebar.number_input("Average MPG", value=7.0, step=0.1)
avg_speed = st.sidebar.number_input("Avg Speed (mph)", value=60, step=5)
other_cpm = st.sidebar.number_input("Other Overhead ($/mi)", value=0.00, step=0.05)
load_buffer = st.sidebar.number_input("Loading Buffer (hrs)", value=2.0, step=0.5)

# Driver HOS Input (Will be populated by ELD API)
st.sidebar.subheader("Driver HOS Status")
cycle_rem = st.sidebar.number_input("70hr Cycle Remaining", value=70.0, step=1.0)

# Main Dashboard Layout
col1, col2 = st.columns(2)
with col1:
    st.subheader("Load Input")
    pickup_date = st.date_input("Pickup Date", datetime.date.today())
    pickup_time = st.time_input("Pickup Time", datetime.time(16, 0))
    loaded_miles = st.number_input("Loaded Miles", value=1000, step=50)
    deadhead_miles = st.number_input("Deadhead Miles", value=50, step=10)
    flat_rate = st.number_input("Load Flat Rate ($)", value=2500.0, step=100.0)

# Core Logic & Calculations
total_miles = loaded_miles + deadhead_miles
fuel_cost = (total_miles / avg_mpg) * fuel_price if avg_mpg > 0 else 0
other_costs = total_miles * other_cpm
total_cost = fuel_cost + other_costs
gross_rpm = flat_rate / total_miles if total_miles > 0 else 0
net_profit = flat_rate - total_cost
margin = (net_profit / flat_rate) * 100 if flat_rate > 0 else 0

drive_hrs = total_miles / avg_speed if avg_speed > 0 else 0
on_duty_needed = drive_hrs + load_buffer

if on_duty_needed > cycle_rem:
    hos_status = "Requires 34hr Restart"
elif drive_hrs > 11:
    hos_status = "Requires 10hr Break"
else:
    hos_status = "Within Available Hours"

ten_hr_breaks = math.ceil((drive_hrs - 11) / 11) * 10 if drive_hrs > 11 else 0
total_transit_hrs = drive_hrs + load_buffer + ten_hr_breaks + (34 if on_duty_needed > cycle_rem else 0)

pickup_datetime = datetime.datetime.combine(pickup_date, pickup_time)
est_completion = pickup_datetime + datetime.timedelta(hours=total_transit_hrs)

with col2:
    st.subheader("Profitability & Scheduling")
    st.metric("Gross Rate Per Mile", f"${gross_rpm:.2f}")
    st.metric("Net Profit", f"${net_profit:,.2f}", delta=f"{margin:.1f}% Margin")
    st.metric("HOS Compliance", hos_status)
    st.metric("Total Transit Time", f"{total_transit_hrs:.2f} hrs")
    st.metric("Est. Completion Date", est_completion.strftime("%Y-%m-%d %I:%M %p"))
