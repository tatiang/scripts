import pandas as pd
import zipfile
import os
import json
import numpy as np

# === Paths ===
GTFS_ZIP = "/Users/tgreenleaf/Downloads/smart-ca-us.zip"
OUTPUT_JSON = "smart_schedule.json"
EXTRACT_DIR = "gtfs_temp"

# === Ensure clean extract folder ===
os.makedirs(EXTRACT_DIR, exist_ok=True)

# === Extract ZIP ===
with zipfile.ZipFile(GTFS_ZIP, 'r') as zip_ref:
    zip_ref.extractall(EXTRACT_DIR)

# === Load CSVs ===
routes = pd.read_csv(os.path.join(EXTRACT_DIR, "routes.txt"))
trips = pd.read_csv(os.path.join(EXTRACT_DIR, "trips.txt"))
stop_times = pd.read_csv(os.path.join(EXTRACT_DIR, "stop_times.txt"))
stops = pd.read_csv(os.path.join(EXTRACT_DIR, "stops.txt"))

# === Filter SMART ===
smart_routes = routes[routes['route_long_name'].str.contains("SMART", na=False)]
smart_trips = trips[trips['route_id'].isin(smart_routes['route_id'])]
smart_stop_times = stop_times[stop_times['trip_id'].isin(smart_trips['trip_id'])]

# === Add stop names ===
smart_stop_times = smart_stop_times.merge(stops[['stop_id', 'stop_name']], on='stop_id', how='left')

# === Structure data ===
output = {}
for trip_id, group in smart_stop_times.groupby('trip_id'):
    output[str(trip_id)] = [
        {
            "stop_id": str(row["stop_id"]),
            "stop_name": row["stop_name"],
            "arrival_time": row["arrival_time"],
            "departure_time": row["departure_time"]
        }
        for _, row in group.sort_values("stop_sequence").iterrows()
    ]

# === Helper to clean all NumPy types ===
def clean_numpys(obj):
    if isinstance(obj, dict):
        return {clean_numpys(k): clean_numpys(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_numpys(i) for i in obj]
    elif isinstance(obj, (np.integer, np.int64)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float64)):
        return float(obj)
    elif isinstance(obj, (np.bool_)):
        return bool(obj)
    elif isinstance(obj, (np.ndarray,)):
        return obj.tolist()
    else:
        return obj

# === Save JSON ===
with open(OUTPUT_JSON, "w") as f:
    json.dump(clean_numpys(output), f, indent=2)

print(f"✅ {OUTPUT_JSON} created with {len(output)} SMART trips.")
