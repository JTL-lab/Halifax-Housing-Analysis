import io
import urllib.request as urllib2
from urllib.request import urlopen
from zipfile import ZipFile
import shapefile
import pandas as pd
import geopandas as gpd
import json

from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px

from app import app


# Returns a preprocessed version of the Halifax census data to be used in visualizations
def return_dataframe():
    # Fetch Canadian census tract boundaries shapefile zip
    tract_data_url = 'https://www12.statcan.gc.ca/census-recensement/2011/geo/bound-limit/files-fichiers/2016/lct_000b16a_e.zip'
    zipfile = ZipFile(io.BytesIO(urllib2.urlopen(tract_data_url).read()))

    # Obtain all filenames from zip and process files (shapefile dependent on other files)
    filenames = [name for name in sorted(zipfile.namelist()) for ending in ['dbf', 'prj', 'shp', 'shx'] if
                 name.endswith(ending)]
    dbf, prj, shp, shx = [io.BytesIO(zipfile.read(filename)) for filename in filenames]
    shape_file = shapefile.Reader(shp=shp, shx=shx, dbf=dbf)

    # Fetch tracts dataframe
    tract_df = gpd.read_file(io.BytesIO(urllib2.urlopen(tract_data_url).read()))
    tracts = tract_df.to_crs(epsg=3857)

    # Fetch census data for Halifax from 2006 - 2016 (3 censuses)
    census_file = 'data/hfxCensusData2006-2016.csv'
    census_file = pd.read_csv(census_file)
    census_file['geometry'] = None

    # Assign geometries to 2016 census dataframe for only the areas in Halifax according to their boundary tract
    for index, row in tracts.iterrows():
        tract_num = float(row.CTUID)
        for i in range(len(census_file)):
            if tract_num == (census_file['tid']).any():
                census_file['geometry'][i] = row.geometry

    # Finalize dataframe with correct geometries
    hfx_census = gpd.GeoDataFrame(census_file, geometry='geometry')

    # Rename the tid to CTUID
    hfx_census.rename(columns={'tid': 'CTUID'}, inplace=True)

    # Modify the CTUID column to be a string value: needed to link it up to the GeoJSON later
    hfx_census['CTUID'] = hfx_census['CTUID'].astype(str)

    return hfx_census


def return_geojson():
    geojson = 'https://github.com/JTL-lab/Halifax-Housing-Analysis/blob/main/data/HFXTractsGEO.geojson?raw=true'

    with urlopen(geojson) as response:
        hfx_json = json.load(response)
        return hfx_json
