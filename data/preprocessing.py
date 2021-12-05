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
def return_dataframe(census_file_path):
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


hfx_census = return_dataframe('data/hfxCensusData2006-2016.csv')

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

    :return: gentrification_2011: dataframe of 2011 census data containing column 'gentrified' with binary labels
             gentrification_2016: dataframe of 2006 census data containing column 'gentrified' with binary labels
    """

    # Get census data for 2006, 2011, and 2016
    census_2006_path = 'hfxTractData2006.csv'
    census_2011_path = 'hfxTractData2011.csv'
    census_2016_path = 'hfxTractData2016.csv'

    hfx_2006 = pd.read_csv(census_2006_path)
    hfx_2011 = pd.read_csv(census_2011_path)
    hfx_2016 = pd.read_csv(census_2016_path)

    print(hfx_2011.head())

    # Replace NaN values with column mean
    hfx_2011.fillna(hfx_2011.groupby('tid').transform('mean'))

    # Make gentrification dataframes for each year to keep track of gentrification eligibility for tracts
    gentrification_2011_df = pd.DataFrame(columns=['tid', 'geometry', 'educ_eligible', 'home_value_increase',
                                                   'home_eligible', 'gentrified'])

    gentrification_2016_df = pd.DataFrame(columns=['tid', 'geometry', 'educ_eligible', 'home_value_increase',
                                                   'home_eligible', 'gentrified'])

    educ_eligible_2011 = []
    home_value_increase_2011 = []
    home_eligible_2011 = []

    educ_eligible_2016 = []
    home_value_increase_2016 = []
    home_eligible_2016 = []

    gentrified_2011 = []
    gentrified_2016 = []

    gentrification_2011_df['tid'] = hfx_census['CTUID']
    gentrification_2011_df['geometry'] = hfx_census['geometry']

    gentrification_2016_df['tid'] = hfx_census['CTUID']
    gentrification_2016_df['geometry'] = hfx_census['geometry']

    # 1) Calculate educational attainment increase
    education_2006 = np.array(hfx_2006['p_educ'])
    education_2011 = np.array(hfx_2011['p_educ'])
    education_2016 = np.array(hfx_2016['p_educ'])

    ed_diff_2011 = []
    ed_diff_2016 = []
    for i in range(len(education_2006)):
        ed_diff_2011.append(education_2011[i] - education_2006[i])
        ed_diff_2016.append(education_2016[i] - education_2011[i])

    ed_diff_2011 = np.array(ed_diff_2011)
    print(ed_diff_2011)
    ed_diff_2016 = np.array(ed_diff_2016)

    min_ed_2011 = ed_diff_2011.min()
    print("Min ed. in 2011: " + str(min_ed_2011))
    max_ed_2011 = ed_diff_2011.max()
    print("Max ed. in 2011: " + str(max_ed_2011))

    min_ed_2016 = ed_diff_2016.min()
    max_ed_2016 = ed_diff_2016.max()

    percentile_66_2011 = np.percentile(ed_diff_2011, 66)
    print("66th percentile value: " + str(percentile_66_2011))
    percentile_66_2016 = np.percentile(ed_diff_2016, 66)

    # Determine which tracts in 2011 and in 2016 saw an increase in educational attainment above the 66th percentile
    for i in range(len(gentrification_2011_df['tid'])):
        if ed_diff_2011[i] > percentile_66_2011:
            gentrification_2011_df['educ_eligible'][i] = True
            educ_eligible_2011.append(1)
        else:
            gentrification_2011_df['educ_eligible'][i] = False
            educ_eligible_2011.append(0)

    for i in range(len(gentrification_2011_df['tid'])):
        if ed_diff_2016[i] > percentile_66_2016:
            gentrification_2016_df['educ_eligible'][i] = True
            educ_eligible_2016.append(1)
        else:
            gentrification_2016_df['educ_eligible'][i] = False
            educ_eligible_2016.append(0)

    # 2) Calculate increase in home value

    # Obtain inflation rates from https://www.bankofcanada.ca/rates/related/inflation-calculator/
    #inflation_to_2011 = 1.1083
    #inflation_to_2016 = 1.0687
    inflation_to_2011 = 1.000
    inflation_to_2016 = 1.000

    # Determine if home price increased from 2006 - 2011 and 2011 - 2016 per tract area
    for i in range(len(hfx_census['CTUID'])):
        if (hfx_2006['HomeMean'][i] * inflation_to_2011) < hfx_2011['HomeMean'][i]:
            gentrification_2011_df['home_value_increase'][i] = True
            home_value_increase_2011.append(1)
        else:
            gentrification_2011_df['home_value_increase'][i] = False
            home_value_increase_2011.append(0)

        if (hfx_2011['HomeMean'][i] * inflation_to_2016) < hfx_2016['HomeMean'][i]:
            gentrification_2016_df['home_value_increase'][i] = True
            home_value_increase_2016.append(1)
        else:
            gentrification_2016_df['home_value_increase'][i] = False
            home_value_increase_2016.append(0)

    # Determine if the increase is enough that the tract may have been gentrified
    home_2006 = np.array(hfx_2006['HomeMean'])
    home_2011 = np.array(hfx_2011['HomeMean'])
    home_2016 = np.array(hfx_2016['HomeMean'])

    home_difference_2011 = []
    home_difference_2016 = []

    for i in range(len(home_2006)):

        home_difference_2011.append(home_2011[i] - (home_2006[i] * inflation_to_2011))
        home_difference_2016.append(home_2016[i] - (home_2011[i] * inflation_to_2016))

    home_difference_2011 = np.array(home_difference_2011)
    home_difference_2016 = np.array(home_difference_2016)

    home_2011_percentile_66 = np.percentile(home_difference_2011, 66)
    print(home_2011_percentile_66)
    home_2016_percentile_66 = np.percentile(home_difference_2016, 66)

    for i in range(len(hfx_census['CTUID'])):
        if home_difference_2011[i] > home_2011_percentile_66:
            gentrification_2011_df['home_eligible'][i] = True
            home_eligible_2011.append(1)
        else:
            gentrification_2011_df['home_eligible'][i] = False
            home_eligible_2016.append(0)

        if home_difference_2016[i] > home_2016_percentile_66:
            gentrification_2016_df['home_eligible'][i] = True
            home_eligible_2016.append(1)
        else:
            gentrification_2016_df['home_eligible'][i] = False
            home_value_increase_2016.append(0)

    for i in range(len(hfx_census['CTUID'])):
        #if (gentrification_2011_df['educ_eligible'][i] == True) and (gentrification_2011_df['home_value_increase'][i] == True) and (gentrification_2011_df['home_eligible'][i] == True):
        if educ_eligible_2011[i] == 1 and home_value_increase_2011[i] == 1 and home_eligible_2011[i] == 1:
            #gentrification_2011_df['gentrified'][i] = 1
            gentrified_2011.append(1)
        else:
            #print(str(gentrification_2011_df['educ_eligible'][i]) + " " + str(gentrification_2011_df['home_value_increase'][i]) + str(gentrification_2011_df['home_eligible'][i]))
            #gentrification_2011_df['gentrified'][i] = 0
            gentrified_2011.append(0)

        #if (gentrification_2016_df['educ_eligible'][i] == True) and (gentrification_2016_df['home_value_increase'][i] == True) and (gentrification_2016_df['home_eligible'][i] == True):
        if educ_eligible_2016[i] == 1 and home_value_increase_2016[i] == 1 and home_eligible_2016[i] == 1:
            #gentrification_2016_df['gentrified'][i] = 1
            gentrified_2016.append(1)
        else:
            #gentrification_2016_df['gentrified'][i] = 0
            gentrified_2016.append(0)

    gentrified_2011 = gentrification_2011_df['gentrified'].to_numpy()
    gentrified_2016 = gentrification_2016_df['gentrified'].to_numpy()

    # Assign target variable of gentrified to the 2011 and 2016 dataframes
    hfx_2011 = hfx_2011.assign(gentrified=gentrified_2011)
    hfx_2016 = hfx_2016.assign(gentrified=gentrified_2016)

    #return hfx_2011, hfx_2016
    return gentrified_2011, gentrified_2016


if __name__ == "__main__":
    hfx_2011, hfx_2016 = get_gentrified_tracts()
    print(hfx_2011)
    print(hfx_2016)
    #print(hfx_2011.head(39))
    #print(hfx_2016.head(39))















