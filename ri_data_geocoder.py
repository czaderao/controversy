import pandas as pd
import json
from pathlib import Path

def semgis_geocode(raw_file: str):
    # Define platform-neutral paths
    raw_folder = Path('./raw')
    data_folder = Path('./out')
    csv_path = data_folder / f'{raw_file}_flagged.csv'
    json_path = raw_folder / 'charter_locations_1-_centers_added.json'
    output_path = data_folder / f'{raw_file}_matched_by_locality.csv'

    data_folder.mkdir(parents=True, exist_ok=True)

    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        print(f"CSV file not found: {csv_path}")
        return

    # Load JSON
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            loc_data = json.load(f)
    except FileNotFoundError:
        print(f"JSON file not found: {json_path}")
        return

    # Build lookup dict keyed by used_name.lower()
    used_name_to_entry = {
        entry.get('used name').strip().lower(): entry
        for entry in loc_data.values()
        if entry.get('used name') and entry.get('used name') != "UNKNOWN"
    }

    def match_locality(row):
        locality = str(row.get('locality_string', '')).strip().lower()
        entry = used_name_to_entry.get(locality)
        if entry:
            prediction = entry.get('prediction-center') or entry.get('prediction:')
            if prediction:
                return pd.Series({
                    'matched_name': prediction.get('name'),
                    'matched_lat': prediction.get('latitude'),
                    'matched_lon': prediction.get('longitude'),
                    'used_name': entry.get('used name')
                })
        # No match found
        return pd.Series({
            'matched_name': None,
            'matched_lat': None,
            'matched_lon': None,
            'used_name': None
        })

    matches = df.apply(match_locality, axis=1)
    df = pd.concat([df, matches], axis=1)
    df.to_csv(output_path, index=False)

if __name__ == "__main__":
    semgis_geocode('konrad')
    semgis_geocode('heinrich')
