Add geodata to regesta imperii charters. Flag that data for church-related personel.

A very much work in progress.

Pre-requirements:

charter_locations_1-centers_added.json from https://github.com/flipz357/regesta-imperii-to-semgis in /res

a subset or the entire Regesta Imperii .csv export https://gitlab.rlp.net/adwmainz/regesta-imperii/lab/regesta-imperii-data/-/tree/main/data/regesta-csv (res already contains example subset from HeinrichIV) (ideally with the Batch nominatim geocoder already run and exported with X,Y coordinates) in /res

Output file NEEDS to be run through the QGIS find nearest node tool and add geometry tool. Without it, there can be no visualisation. (/res already contains the dist.csv which is this step done for the Heinrich IV data)
