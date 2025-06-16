import pandas as pd
import requests
import time
from tqdm import tqdm

INPUT_CSV = './raw/konrad.csv'
OUTPUT_CSV = './raw/konrad_flagged.csv'
PLACE_ID_COLUMN = "place_id"
BATCH_SIZE = 50
DELAY_BETWEEN_REQUESTS = 1  # seconds (as per Nominatim policy)

USER_AGENT = 'controversy/1.0'

df = pd.read_csv(INPUT_CSV)
results = []

# Process in batches
place_ids = df[PLACE_ID_COLUMN].dropna().astype(str).tolist()
for i in tqdm(range(0, len(place_ids), BATCH_SIZE), desc='Geocoding'):
    batch = place_ids[i:i + BATCH_SIZE]
    ids_str = ",".join(batch)

    url = f'https://nominatim.openstreetmap.org/lookup?place_id={ids_str}&format=json'
    headers = {'User-Agent': USER_AGENT}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f'Error with batch {batch[0]}–{batch[-1]}: {e}')
        data = []

    for item in data:
        results.append({
            "place_id": item.get("place_id"),
            "lat": item.get("lat"),
            "lon": item.get("lon"),
            "display_name": item.get("display_name")
        })

    time.sleep(DELAY_BETWEEN_REQUESTS)

# Convert results to DataFrame
results_df = pd.DataFrame(results)
merged_df = df.merge(results_df, on='place_id', how='left')

# Save to CSV
merged_df.to_csv(OUTPUT_CSV, index=False)
print(f"\n✅ Geocoded data saved to '{OUTPUT_CSV}'")
