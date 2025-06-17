import sys
from flagger import process_csv
from ri_data_geocoder import semgis_geocode

if __name__ == '__main__':
    process_csv(sys.argv[1])
    semgis_geocode(sys.argv[1])