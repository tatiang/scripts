import pandas as pd
import zipfile
import os
import json
import numpy as np

# Set your GTFS .zip file path
GTFS_ZIP = "/Users/tgreenleaf/Downloads/smart-ca-us.zip"
OUTPUT_JSON = "smart_schedule.json"

# Create a helper to fix numpy types
def convert_numpy(obj):
    if isinstance(obj, np.integer):
        return int(obj)
    if isinstance(obj, np.floating):
        return float(obj)
    return str(obj)

# Create a working directory
extract_dir = "gtfs_temp"
os.makedirs(extract_dir, exist_ok=True)

# Extract the GTFS zip
with zipfile.ZipFile(GTFS_ZIP, 'r') as zip_ref:
    zip_ref.extractall(extract_dir)

# Load GTFS files
routes = pd.read_csv(os.path.join(extract_dir, "routes.txt"))
trips = pd.read_csv(os.path.join(extract_dir, "trips.txt"))
stop_times = pd.read_csv(os.path.join(extract_dir, "stop_times.txt"))
stops = pd.read_csv(os.path.join(extract_dir, "stops.txt"))

# Filter SMART routes
smart_routes = routes[routes['route_long_name'].str.contains("SMART", na=False)]

# Join to find SMART trip_ids
smart_trips = trips[trips['route_id'].isin(smart_routes['route_id'])]

# Filter stop_times to SMART only
smart_stop_times = stop_times[stop_times['trip_id'].isin(smart_trips['trip_id'])]

# Merge stop info for names
smart_stop_times = smart_stop_times.merge(stops[['stop_id', 'stop_name']], on='stop_id', how='left')

# Group data by trip_id
output = {}
for trip_id, group in smart_stop_times.groupby('trip_id'):
    output[trip_id] = [
        {
            "stop_id": row["stop_id"],
            "stop_name": row["stop_name"],
            "arrival_time": row["arrival_time"],
            "departure_time": row["departure_time"]
        }
        for _, row in group.sort_values("stop_sequence").iterrows()
    ]

# Save to JSON with numpy fix
with open(OUTPUT_JSON, "w") as f:
    json.dump(output, f, indent=2, default=convert_numpy)

print(f"✅ Successfully created {OUTPUT_JSON} with {len(output)} SMART trips.")
