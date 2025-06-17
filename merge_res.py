import pandas as pd
from pathlib import Path

def patch_missing_geocodes(raw_file: str):
    data_folder = Path('./out')
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

if __name__ == "__main__":
    patch_missing_geocodes('konrad')
    patch_missing_geocodes('heinrich')
