"""
Population analysis of Halifax using census data from 2006, 2011, and 2016 censuses by Statistics Canada.
"""

import io
import urllib.request as urllib2
from urllib.request import urlopen
from zipfile import ZipFile
import shapefile
import pandas as pd
import geopandas as gpd
import json

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px

from app import app

# -----------------------------------------------------
# DATA PROCESSING
# -----------------------------------------------------

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

# Visualization 1: Interactive population density visualization for 2006, 2011, and 2016 using Dash
geojson = 'https://github.com/JTL-lab/Halifax-Housing-Analysis/blob/main/data/HFXTractsGEO.geojson?raw=true'

with urlopen(geojson) as response:
    hfx_json = json.load(response)

census_cols = list(hfx_census.columns)

layout = html.Div([

    dbc.Container([

        # Sub-heading description of page purpose
        dbc.Row([
            dbc.Col(html.H6("Visualizing population trends in Halifax during the 2006, 2011, and 2016 census years"))
        ]),

        # Section 1: Population Density
        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='Population Density',
                                     className='text-center text-light bg-dark'), body=True, color="dark")
                    , className='mb-4')
        ]),

        # Dropdown menu for population density choropleth
        html.P("Census Year:"),
        dcc.Dropdown(
            id='density_year',
            options=[
                {'label': '2006', 'value': 'PopulationDensity2006'},
                {'label': '2011', 'value': 'PopulationDensity2011'},
                {'label': '2016', 'value': 'PopulationDensity2016'}
            ],
            value='PopulationDensity2006',
            style={'width': '50%', 'margin-left': '5px'}
        ),

        dcc.Graph(id="density_choropleth"),

        # Section 2: Population Change
        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='Population Change Between Census Years',
                                     className='text-center text-light bg-dark'), body=True, color="dark")
                    , className='mb-4')
        ]),

        # Dropdown menu for population change choropleth
        html.P("Census Years:"),
        dcc.Dropdown(
            id='pop_change_year',
            options=[
                {'label': '2001-2006', 'value': 'PopulationChange2001-2006'},
                {'label': '2006-2011', 'value': 'PopulationChange2006-2011'},
                {'label': '2011-2016', 'value': 'PopulationChange2011-2016'}
            ],
            value='PopulationChange2001-2006',
            style={'width': '50%', 'margin-left': '5px'}
        ),

        dcc.Graph(id="pop_change_choropleth")
    ])
])


# Gets user input from dropdown to choose year for population density visualization
@app.callback(
    Output("density_choropleth", "figure"),
    [Input("density_year", "value")]
)
def display_density_choropleth(density_year):
    density_figure = px.choropleth_mapbox(
        data_frame=hfx_census,
        geojson=hfx_json,
        color=density_year,
        locations='CTUID',
        featureidkey="properties.CTUID",
        center={"lat": 44.651070, "lon": -63.582687},
        zoom=10,
        opacity=0.4,
        mapbox_style="carto-positron",
    )

    return density_figure

# Gets user input from dropdown to choose year for population change visualization
@app.callback(
    Output("pop_change_choropleth", "figure"),
    [Input("pop_change_year", "value")]
)
def display_population_change_choropleth(pop_change_year):
    pop_change_figure = px.choropleth_mapbox(
        data_frame=hfx_census,
        geojson=hfx_json,
        color=pop_change_year,
        locations='CTUID',
        featureidkey="properties.CTUID",
        center={"lat": 44.651070, "lon": -63.582687},
        zoom=10,
        opacity=0.4,
        mapbox_style="carto-positron",
    )

    return pop_change_figure
