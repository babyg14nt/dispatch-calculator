#!/usr/bin/env python3
"""
Spot-market load calculator — box truck + semi
==============================================
Inputs : loaded miles, deadhead miles, rate (total revenue for the load),
         pickup date & time, driver's remaining HOS hours, fuel price
Outputs: rate per mile, net profit, margin, estimated drop-off date/time,
         and a HOS clock showing DRIVING / LOAD / BREAK / OFF-DUTY periods.

Run:  python load_calc.py
"""
from datetime import datetime, timedelta

# ---------------- EDITABLE ASSUMPTIONS ----------------
DEFAULT_FUEL_PRICE = 3.65   # $/gal  (your chosen average)
MPG                = 6.5    # semis ~6-7; diesel box trucks ~8-10
AVG_SPEED          = 62.0   # mph blended loaded + deadhead
OPS_COST_PER_MI    = 0.50   # $/mi non-fuel cost (maint, tires, insurance, misc)

# ---------------- FMCSA HOS LIMITS (property-carrying) ----------------
MAX_DRIVE_SHIFT = 11.0      # hours driving before 10-hr reset
ON_DUTY_WINDOW  = 14.0      # hours on-duty window per shift
DRIVE_BREAK_CAP = 8.0       # hour of drive that triggers a break
BREAK_MIN       = 30        # min break length (minutes)
REST_HRS        = 10.0      # off-duty reset between shifts

LOAD_T  = 2.0               # hours loading at pickup
DROP_T  = 1.5               # hours unloading at drop-off
CLOCK_RESET_HRS = 24.0      # your "remaining HOS clock" reference per day


def parse_dt(text: str) -> datetime:
    for fmt in ("%Y-%m-%d %H:%M", "%m-%d %H:%M", "%Y-%m-%d"):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            continue
    raise ValueError('Use format "YYYY-MM-DD HH:MM" (or "MM-DD HH:MM" / "YYYY-MM-DD")')


# ------------------------------------------------------------------------
# HOS clock simulator
# ------------------------------------------------------------------------
class HosClock:
    def __init__(self, start_dt: datetime, start_clock_hrs: float):
        self.now = start_dt
        self.day_on_duty = 0.0
        self.day_drive = 0.0
        self.drive_since_break = 0.0
        self.timeline = []

    def _add(self, kind: str, hrs: float):
        start, end = self.now, self.now + timedelta(hours=hrs)
        self.timeline.append((kind, start, end, hrs))
        self.now = end

    def _take_break(self):
        self._add("BREAK", BREAK_MIN / 60.0)
        self.drive_since_break = 0.0

    def _take_rest(self):
        self._add("OFF-DUTY", REST_HRS)
        self.day_on_duty = 0.0
        self.day_drive = 0.0
        self.drive_since_break = 0.0

    def drive(self, miles: float, label: str):
        """Drive `miles` respecting the 8 / 11 / 14 HOS rules."""
        remain_h = miles / AVG_SPEED
        while remain_h > 1e-6:
            # 10-hr reset: hit 11-hr drive cap
            if self.day_drive >= MAX_DRIVE_SHIFT:
                self._take_rest()
            # enforce 8-hr continuous-driving break
            if self.drive_since_break >= DRIVE_BREAK_CAP:
                self._take_break()
            # 14-hr window end -> rest
            if self.day_on_duty >= ON_DUTY_WINDOW:
                self._take_rest()

            avail_8   = DRIVE_BREAK_CAP - self.drive_since_break
            avail_11  = MAX_DRIVE_SHIFT - self.day_drive
            avail_14  = ON_DUTY_WINDOW - self.day_on_duty
            step = min(remain_h, avail_8, avail_11, avail_14)
            if step <= 1e-6:
                # cannot advance inside current constraints; consume a break/rest
                if self.drive_since_break >= DRIVE_BREAK_CAP:
                    self._take_break()
                else:
                    self._take_rest()
                continue

            self._add(label, step)
            remain_h -= step
            self.day_drive += step
            self.day_on_duty += step
            self.drive_since_break += step
            # small fixed overhead (start/stop/idle) per leg, if any
        self.drive_since_break = 0.0  # arriving resets the clock for the next task


# ------------------------------------------------------------------------
def main():
    print("\n=== SPOT LOAD / HOS CALCULATOR ===\n")
    loaded = float(input("Loaded miles        : "))
    dh     = float(input("Deadhead miles      : "))
    rate   = float(input("Rate (total revenue): $"))
    pick_s = input("Pickup date/time (YYYY-MM-DD HH:MM): ")
    pick   = parse_dt(pick_s)
    clock  = float(input("Remaining HOS clock hrs (0-14, often 11): "))
    if clock <= 0 or clock > 24:
        clock = 11.0
    fprice = input(f"Fuel price/gal  [${DEFAULT_FUEL_PRICE}]: ").strip()
    fuel_price = float(fprice) if fprice else DEFAULT_FUEL_PRICE

    # ------------------ PROFITABILITY ------------------
    total_miles = dh + loaded
    rate_per_loaded = rate / loaded_mi
    rate_per_total  = rate / total_miles

    fuel_gallons = total_miles / MPG
    fuel_cost    = fuel_gallons * fuel_price
    ops_cost     = total_miles * OPS_COST_PER_MI
    total_cost   = fuel_cost + ops_cost
    net          = rate - total_cost
    margin = (net / rate) * 100 if rate else 0.0
    net_per_mi = net / total_miles                 if total_miles else 0.0

    # ------------------ HOS CLOCK ------------------
    h = HosClock(pick, clock)
    h._add("START", 0.0)                       # leave toward pickup
    h.drive(dh, "DEADHEAD")                    # deadhead to shipper
    h._add("LOAD (on-duty)", LOAD_T)
    h.day_on_duty += LOAD_T
    h.drive(loaded_miles, "LOADED")
    h._add("UNLOAD (on-duty)", DROP_T)
    h.day_on_duty += DROP_T
    # (break rules apply to on-duty too; keep simple — driving is the constraint)
    drop_off = h.now
    trip_hours = (drop_off - pick).total_seconds() / 3600.0

    # ------------------ OUTPUT ------------------
    print("\n" + "=" * 56)
    print("FINANCIALS")
    print("=" * 56)
    print(f"Loaded miles           : {loaded_miles:.1f}")
    print(f"Deadhead miles         : {dh:.1f}")
    print(f"Total miles            : {total_miles:.1f}")
    print(f"Revenue                : ${rate:,.2f}")
    print(f"Fuel used              : {fuel_gallons:.1f} gal")
    print(f"Fuel cost  (${fuel_price:.2f}/gal): ${fuel_cost:,.2f}")
    print(f"Other op cost  (${OPS_COST_PER_MI:.2f}/mi): ${ops_cost:,.2f}")
    print(f"Total cost             : ${total_cost:,.2f}")
    print(f"NET PROFIT             : ${net:,.2f}")
    print(f"Profit margin          : {margin:.1f}%")
    print("-" * 56)
    print(f"Rate per LOADED mile   : ${rate_per_loaded:,.2f}")
    print(f"Rate per TOTAL mile    : ${rate_per_total:,.2f}")
    print(f"Net  per TOTAL mile    : ${net_per_mile:,.2f}")
    print(f"Fuel per TOTAL mile    : ${fuel_cost / total_miles:,.2f}" if total_miles else "")

    print("\n" + "=" * 56)
    print("HOS / TIMELINE")
    print("=" * 56)
    print(f"Pickup / start         : {pick:%-%m }  ... ")
    for kind, start, end, hrs in h.timeline:
        marker = kind if kind else ""
        if hrs == 0:
            print(f"  {start:%m-%d %H:%M}  {kind}")
        else:
            print(f"  {start:%m-%d %H:%M} -> {end:%m-%d %H:%M}   {kind:<10} {hrs:5.2f} h")
    print(f"\nESTIMATED DROP-OFF     : {drop_off:%Y-%m-%d %H:%M}")
    print(f"Total elapsed (door-to-door): {trip_hours:.1f} h")

    # ------------------ CLOCK DIAGRAM ------------------
    print("\n" + "=" * 56)
    print("DRIVER CLOCK (24-hr bar)")
    print("=" * 56)
    for tpl in h.timeline:
        pass  # build compact bar below
    draw_clock(h.timeline, pick)


def draw_clock(segments, start):
    """Print one 'day' line per 24-h window with segments plotted."""
    start_day = start.replace(hour=0, minute=0)
    # group into up to a few days
    width = 48
    lo = start_day
    hi = max((e for _, _, e, _ in segments)) if segments else start_day
    days = (hi - lo).days + 1
    for d in range(days):
        day_start = start_day + timedelta(days=d)
        day_end   = day_start + timedelta(days=1)
        cols = [" "] * width
        for kind, s, e, _ in segments:
            mark = {"DRIVING": "#", "LOAD": "L", "UNLOAD":"D",
                    "BREAK":"-", "OFF-DUTY":".", "START":"S"}.get(kind, "*")
            i0 = max(0, int((s - day_start).total_seconds() / 3600 / 24 * width))
            i1 = min(width, max(0, int((e - day_start).total_seconds() / 3600 / 24 * width)))
            for i in range(i0, i1):
                cols[i] = mark
        print(f"  {day:%b %d} |{''.join(cols)}|")
    print("        0" + " "*(width-1) + "24h")


# wrap input-protected for zero-length
if __name__ == "__main__":
    try:
        main()
    except (ValueError, TypeError) as e:
        print(f"\nInput error: {e}")
        print("Re-run and format date as  YYYY-MM-DD HH:MM")
