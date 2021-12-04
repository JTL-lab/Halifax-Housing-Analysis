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
    census_file_path = 'data/hfxCensusData2006-2016.csv'
    census_file = pd.read_csv(census_file_path)
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

def get_gentrified_tracts():
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

    :return: gentrification_2006: dataframe of 2006 census data containing column 'Gentrified' with binary labels
             gentrification_2011: dataframe of 2011 census data containing column 'Gentrified' with binary labels
             gentrification_2016: dataframe of 2006 census data containing column 'Gentrified' with binary labels
    """

    # Get census data for 2006, 2011, and 2016
    census_2001_path = 'data/hfxGentrificationData2001.csv'
    census_2006_path = 'data/hfxTractData2006.csv'
    census_2011_path = 'data/hfxTractData2011.csv'
    census_2016_path = 'data/hfxTractData2016.csv'

    hfx_2001 = pd.read_csv(census_2001_path)
    hfx_2006 = pd.read_csv(census_2006_path)
    hfx_2011 = pd.read_csv(census_2011_path)
    hfx_2016 = pd.read_csv(census_2016_path)

    # Make gentrification dataframes for each year to keep track of gentrification eligibility for tracts
    gentrification_2006_df = pd.DataFrame(columns=['tid', 'geometry', 'educ_eligible', 'home_value_increase',
                                                   'home_eligible', 'gentrified'])

    gentrification_2011_df = pd.DataFrame(columns=['tid', 'geometry', 'educ_eligible', 'home_value_increase',
                                                   'home_eligible', 'gentrified'])

    gentrification_2016_df = pd.DataFrame(columns=['tid', 'geometry', 'educ_eligible', 'home_value_increase',
                                                   'home_eligible', 'gentrified'])

    hfx_census = return_dataframe()
    for df in [gentrification_2006_df, gentrification_2011_df, gentrification_2016_df]:
        df['tid'] = hfx_census['CTUID']
        df['geometry'] = hfx_census['geometry']

    # 1) Calculate educational attainment increase
    education_2001 = np.array(hfx_2001['education'])
    education_2006 = np.array(hfx_2006['education'])
    education_2011 = np.array(hfx_2011['education'])
    education_2016 = np.array(hfx_2016['education'])

    # 2) Calculate increase in home value
    # Obtain inflation rates from https://www.bankofcanada.ca/rates/related/inflation-calculator/
    inflation_to_2006 = 1.1111
    inflation_to_2011 = 1.1083
    inflation_to_2016 = 1.0687

    # Determine gentrification status from 2001 - 2006, 2006 - 2011, and 2011 - 2016




