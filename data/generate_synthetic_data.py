import numpy as np
import pandas as pd

N = 50000  # number of synthetic orders

rng = np.random.default_rng(42)

# Basic features
order_id = np.arange(1, N + 1)

# distance between restaurant and customer (km)
distance_km = rng.uniform(0.5, 12, N).round(2)

# restaurant preparation time (minutes)
prep_time_min = rng.integers(5, 35, N)

# baseline travel time (min) = distance / avg speed (km/min)
avg_speed_km_per_min = rng.uniform(0.35, 0.7, N)  # ~21–42 km/h
estimated_travel_time_min = (distance_km / avg_speed_km_per_min).round(1)

# time features
hour_of_day = rng.integers(0, 24, N)
day_of_week = rng.integers(0, 7, N)  # 0 = Monday

# weather (0 = clear, 1 = rain)
is_raining = rng.binomial(1, 0.25, N)

# courier experience: 0=new, 1=regular, 2=expert
courier_experience = rng.choice([0, 1, 2], size=N, p=[0.2, 0.5, 0.3])

# peak hours: lunch (11–13) & dinner (18–21)
is_peak = ((hour_of_day >= 11) & (hour_of_day <= 13)) | \
          ((hour_of_day >= 18) & (hour_of_day <= 21))

# Construct "true" actual delivery time
base_time = prep_time_min + estimated_travel_time_min

# add peak hour delay
peak_delay = np.where(is_peak, rng.uniform(5, 15, N), rng.uniform(0, 5, N))

# add weather penalty
weather_delay = np.where(is_raining == 1, rng.uniform(5, 12, N), rng.uniform(0, 3, N))

# courier effect
experience_adjustment = np.select(
    [
        courier_experience == 0,  # new
        courier_experience == 1,  # regular
        courier_experience == 2,  # expert
    ],
    [
        rng.uniform(3, 7, N),     # slower
        rng.uniform(-1, 2, N),
        rng.uniform(-5, -1, N),   # faster
    ],
    default=0.0,
)

# gaussian noise
noise = rng.normal(0, 3, N)

actual_delivery_time_min = (
    base_time + peak_delay + weather_delay + experience_adjustment + noise
).clip(min=10).round(1)

# Promised ETA (baseline estimation ignoring some complexities)
promised_eta_min = (
    prep_time_min + estimated_travel_time_min + np.where(is_peak, 5, 0)
).round(1)

# label: late if actual > promised + 10 minutes
is_late = (actual_delivery_time_min - promised_eta_min > 10).astype(int)

df = pd.DataFrame({
    "order_id": order_id,
    "distance_km": distance_km,
    "prep_time_min": prep_time_min,
    "estimated_travel_time_min": estimated_travel_time_min,
    "hour_of_day": hour_of_day,
    "day_of_week": day_of_week,
    "is_raining": is_raining,
    "courier_experience": courier_experience,
    "actual_delivery_time_min": actual_delivery_time_min,
    "promised_eta_min": promised_eta_min,
    "is_late": is_late,
})

df.to_csv("synthetic_orders.csv", index=False)
print("Saved synthetic_orders.csv with", len(df), "rows")
