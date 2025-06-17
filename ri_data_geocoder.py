import pandas as pd
import json
from pathlib import Path

# i hate windows - platform neutral paths
raw_folder = Path('./raw')
data_folder = Path('./out')
csv_path = data_folder / 'konrad_flagged.csv'
json_path = raw_folder / 'charter_locations_1-_centers_added.json'
output_path = data_folder / 'konrad_matched_by_locality.csv'

df = pd.read_csv(csv_path)

# Load JSON
with open(json_path, 'r', encoding='utf-8') as f:
    loc_data = json.load(f)

# Build lookup dict keyed by used_name.lower()
used_name_to_entry = {}
for key, entry in loc_data.items():
    used_name = entry.get('used name')
    if used_name and used_name != "UNKNOWN":
        used_name_to_entry[used_name.strip().lower()] = entry

def match_locality(row):
    locality = str(row.get('locality_string', '')).strip().lower()
    if locality in used_name_to_entry:
        entry = used_name_to_entry[locality]

        prediction = entry.get('prediction-center') or entry.get('prediction:')
        if prediction:
            return pd.Series({
                'matched_name': prediction.get('name'),
                'matched_lat': prediction.get('latitude'),
                'matched_lon': prediction.get('longitude'),
                'used_name': entry.get('used name')
            })
    return pd.Series({
        'matched_name': None,
        'matched_lat': None,
        'matched_lon': None,
        'used_name': None
    })

matches = df.apply(match_locality, axis=1)
df = pd.concat([df, matches], axis=1)

# Save result
df.to_csv(output_path, index=False)
print(f"Saved enriched data to '{output_path}'")
