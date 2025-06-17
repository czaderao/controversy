import sys
from flagger import process_csv
from merge_res import patch_missing_geocodes
from ri_data_geocoder import semgis_geocode

# run for a single file processing. Input filename as just FILENAME without the .csv; ex. python3 main.py RI_all
if __name__ == '__main__':
    process_csv(f'{sys.argv[1]}')
    semgis_geocode(f'{sys.argv[1]}')
    patch_missing_geocodes(f'{sys.argv[1]}')
    print(f'File {sys.argv[1]} has been processed')