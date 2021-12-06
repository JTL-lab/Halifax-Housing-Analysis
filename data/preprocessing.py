import io
import urllib.request as urllib2
from urllib.request import urlopen
from zipfile import ZipFile
import shapefile
import pandas as pd
import geopandas as gpd
import numpy as np
import json

tract_data_url = 'https://www12.statcan.gc.ca/census-recensement/2011/geo/bound-limit/files-fichiers/2016/lct_000b16a_e.zip'


# Returns a preprocessed version of the Halifax census data to be used in visualizations
def return_dataframe():
    # Fetch Canadian census tract boundaries shapefile zip
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
    try:
        census_file = pd.read_csv('data/hfxCensusData2006-2016.csv')
    except FileNotFoundError:
        census_file = pd.read_csv('hfxCensusData2006-2016.csv')
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


#hfx_census = return_dataframe()


def find_gentrified_tracts(hfx_census):
    """
    Uses the methodology defined by Governing.com found here for identifying gentrified areas:
    https://www.governing.com/archive/gentrification-report-methodology.html

    An area can be determined to have gentrified given the following criteria:

    1) There is an increase in the tract's educational attainment, measured by the percentage of
    residents above the age of 25 holding bachelor's degrees, that is in the top third percentile of
    all tracts within the city.

    2) The tract's median home value increased when adjusted for inflation.

    3) The percentage increase in the tract's inflation-adjusted median home value was in the top
    third percentile of all tracts within the city.

    :return: gentrification_2016: dataframe of 2016 census data containing column 'gentrified' with binary labels
                                  showing which tracts gentrified from 2006 - 2016
    """

    census_tracts = pd.DataFrame(columns=['CTUID', 'geometry', 'educ_eligible', 'home_value_increase', 'home_eligible',
                                          'gentrified'])
    census_tracts['CTUID'] = hfx_census['CTUID']
    census_tracts['geometry'] = hfx_census['geometry']

    # Step 1: Determine if tract is eligible for gentrification based on educational attainment increase:
    # 1 a) Find the difference in the number of people holding some form of university education from 2006 - 2016
    educ2006 = hfx_census['p_educ2006'].to_numpy()
    educ2016 = hfx_census['p_educ2016'].to_numpy()

    educ_difference = []
    for i in range(len(educ2006)):
        educ_difference.append(educ2016[i] - educ2006[i])
    educ_difference = np.array(educ_difference)

    # 1 b) Find the 66th percentile of educational attainment among the tract differences
    min_educ = np.nanmin(educ_difference)
    max_educ = np.nanmax(educ_difference)
    percentile66 = np.percentile(educ_difference, 66)

    # 1 c) Compare each tract against the 66th percentile: if it's above it, educ_eligible is True
    for i in range(len(census_tracts['CTUID'])):
        if educ_difference[i] > percentile66:
            census_tracts['educ_eligible'][i] = True
        else:
            census_tracts['educ_eligible'][i] = False

    # Step 2: Calculate if there was an increase in home value
    # 2 a) Adjust each home value for inflation between 2006 and 2016 and assign home_value_increase to True or False
    inflation_rate = 1.1777  # obtained from https://www.bankofcanada.ca/rates/related/inflation-calculator/
    for i in range(len(hfx_census['CTUID'])):
        if (hfx_census['HomePrices2006'][i] * inflation_rate) < (hfx_census['HomePrices2016'][i]):
            census_tracts['home_value_increase'][i] = True
        else:
            census_tracts['home_value_increase'][i] = True

    # Step 3: Check if home value increase was above 66th percentile
    # 3 a) Find difference in home prices between 2006 and 2016
    home_2006 = hfx_census['HomePrices2006'].to_numpy()
    home_2016 = hfx_census['HomePrices2016'].to_numpy()

    # 3 b) Calculate 66th percentile
    home_difference = []
    for i in range(len(home_2006)):
        home_difference.append(home_2016[i] - (home_2006[i]*inflation_rate))
    home_difference = np.array(home_difference)

    percentile66 = np.percentile(home_difference, 66)

    # 3 c) If difference was above the 66th percentile, home_eligible is True
    for i in range(len(census_tracts['CTUID'])):
        if home_difference[i] > percentile66:
            census_tracts['home_eligible'][i] = True
        else:
            census_tracts['home_eligible'][i] = False

    # If all of the variables are true, the tract is identified as gentrified
    for i in range(len(census_tracts['CTUID'])):
        if (census_tracts['educ_eligible'][i] == True) and (census_tracts['home_value_increase'][i] == True) and (census_tracts['home_eligible'][i] == True):
            census_tracts['gentrified'][i] = True
        else:
            census_tracts['gentrified'][i] = False

    gentrification_df = gpd.GeoDataFrame(census_tracts, geometry='geometry')

    return gentrification_df
