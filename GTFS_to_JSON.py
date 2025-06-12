import pandas as pd
import zipfile
import json

# === CONFIG ===
// GTFS_ZIP = "smart-ca-us.zip"
GTFS_ZIP = "/Users/tgreenleaf/Downloads/smart-ca-us.zip"

SMART_ROUTE_IDS = ["SMART"]  # Add or adjust route IDs as needed
OUTPUT_JSON = "smart_schedule.json"

# === EXTRACT ZIP ===
with zipfile.ZipFile(GTFS_ZIP, 'r') as zip_ref:
    zip_ref.extractall("gtfs_data")

# === LOAD GTFS FILES ===
stops = pd.read_csv("gtfs_data/stops.txt")
routes = pd.read_csv("gtfs_data/routes.txt")
trips = pd.read_csv("gtfs_data/trips.txt")
stop_times = pd.read_csv("gtfs_data/stop_times.txt")

# === FILTER FOR SMART ROUTES ===
smart_routes = routes[routes['route_short_name'].astype(str).str.contains("SMART", na=False)]
smart_route_ids = smart_routes['route_id'].unique()

smart_trips = trips[trips['route_id'].isin(smart_route_ids)]
smart_trip_ids = smart_trips['trip_id'].unique()

smart_stop_times = stop_times[stop_times['trip_id'].isin(smart_trip_ids)]

# === JOIN DATA ===
merged = smart_stop_times.merge(smart_trips, on='trip_id')
merged = merged.merge(stops, on='stop_id')
merged = merged.sort_values(by=['trip_id', 'stop_sequence'])

# === BUILD OUTPUT ===
output = {}

for trip_id, group in merged.groupby('trip_id'):
    trip_info = {
        "trip_id": trip_id,
        "route_id": group.iloc[0]['route_id'],
        "direction_id": int(group.iloc[0]['direction_id']),
        "stops": []
    }
    for _, row in group.iterrows():
        trip_info["stops"].append({
            "stop_id": row["stop_id"],
            "stop_name": row["stop_name"],
            "arrival_time": row["arrival_time"],
            "departure_time": row["departure_time"]
        })
    output[trip_id] = trip_info

# === SAVE TO JSON ===
with open(OUTPUT_JSON, "w") as f:
    json.dump(output, f, indent=2)

print(f"✅ Saved {len(output)} SMART trips to {OUTPUT_JSON}")
