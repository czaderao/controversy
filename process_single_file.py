import sys
import pandas as pd
from pathlib import Path
import re
from matplotlib import pyplot as plt
import json
import numpy as np

raw_folder = Path('./raw')
data_folder = Path('./out')

# check if a str contains any words from lst institutions and returns a boolean value and d lst containing the matched words
def check_ecclesiae_with_matches(charter_summary):
    institutions = ['bischof', 'erzbischof', 'abt', 'erzbischöfe', 'bischöfe', 'papst', 'päpste', 'domkapitels',
                    'domkapitel', 'kloster', 'kapitel']
    institution_pattern = re.compile(r'\b(' + '|'.join(institutions) + r')\b', flags=re.IGNORECASE)
    if pd.isna(charter_summary):
        return False, None
    matches = institution_pattern.findall(charter_summary)
    return (bool(matches), matches if matches else None)

# processes a single file, adding two columns with flag, if the charter summary contains 'ecclesiastical institutions' and if so, which
def process_csv(filename):
    csv_path = raw_folder / f'{filename}.csv'
    out_path = data_folder / f'{filename}_flagged.csv'
    df = pd.read_csv(csv_path)
    results = df['summary'].apply(check_ecclesiae_with_matches)
    df['ecclesiastical_flag'] = results.apply(lambda x: x[0])
    df['ecclesiastical_terms'] = results.apply(lambda x: x[1])
    df.to_csv(out_path, index=False)

# takes the semgis .json and matches its guesses to the locality_string from the RI data and adds its columns to the .csv
def semgis_geocode(raw_file: str):
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


# compare the batch nominatim geocoded results together with the RI semgis results. Takes the semgis data as default for coordinates and where unavaliable, keep the nominatim.
def patch_missing_geocodes(raw_file: str):
    input_path = data_folder / f'{raw_file}_matched_by_locality.csv'
    output_path = data_folder / f'{raw_file}_patched.csv'

    # Load data
    try:
        df = pd.read_csv(input_path)
    except FileNotFoundError:
        print(f"[ERROR] Input file not found: {input_path}")
        return

    def is_valid_float(value):
        try:
            return not pd.isna(value) and value != "" and float(value)
        except ValueError:
            return False

    def patch_row(row):
        if pd.isna(row.get('matched_name')):
            x, y = row.get('X'), row.get('Y')
            if is_valid_float(x) and is_valid_float(y):
                row['matched_lon'] = float(x)
                row['matched_lat'] = float(y)
                row['matched_name'] = 'Fallback XY Patch'
        return row

    df = df.apply(patch_row, axis=1)
    df.to_csv(output_path, index=False)

    # take a series of distances in degrees and convert the distances to kilometres
def deg_to_km(series):
    return np.deg2rad(series) * 6371

# run for a single file processing. Input filename as just FILENAME without the .csv; ex. python3 process_single_file.py RI_all
if __name__ == '__main__':
    if len(sys.argv) > 1:
        argv = sys.argv[1]
    else:
        arg = input('Input a .csv filename to process (without the .csv):')
    process_csv(f'{arg}')
    semgis_geocode(f'{arg}')
    patch_missing_geocodes(f'{arg}')
    print(f'File {arg} has been processed')

    df = pd.read_csv('./raw/dist.csv')
    df = df[df['straightdis'] <= 20]

    df[['year', 'month', 'day']] = df['start_date'].str.split('/', expand=True).astype(float)
    yearly_avg = df.groupby('year')['straightdis'].mean().reset_index()

    yearly_all = df.groupby('year')['straightdis'].mean().reset_index()
    yearly_true = df[df['ecclesiastical_flag'] == True].groupby('year')['straightdis'].mean().reset_index()
    yearly_false = df[df['ecclesiastical_flag'] == False].groupby('year')['straightdis'].mean().reset_index()


    plt.figure(figsize=(19, 10))
    plt.plot(yearly_all['year'], deg_to_km(yearly_all['straightdis']), label='All', marker='o')
    plt.plot(yearly_true['year'], deg_to_km(yearly_true['straightdis']), label='Church-related', marker='o')
    plt.plot(yearly_false['year'], deg_to_km(yearly_false['straightdis']), label='Church-unrelated', marker='o')
    plt.title('Average Hub Distance per Year')
    plt.xlabel('Year')
    plt.ylabel('Average Hub Distance (km)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
