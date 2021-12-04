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
from data import preprocessing

hfx_census = preprocessing.return_dataframe()
hfx_json = preprocessing.return_geojson()
census_cols = list(hfx_census.columns)

layout = html.Div([

    dbc.Container([

        # Sub-heading description of page purpose
        dbc.Row([
            dbc.Col(html.H6("Visualizing housing price trends in Halifax during the 2006, 2011, and 2016 census years"))
        ]),

        # Section 1: Housing prices
        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='Housing prices',
                                     className='text-center text-light bg-dark'), body=True, color="dark")
                    , className='mb-4')
        ]),

        # Dropdown menu for housing choropleth
        html.P("Census Year:"),
        dcc.Dropdown(
            id='housing_year',
            options=[
                {'label': '2006', 'value': 'HomePrices2006'},
                {'label': '2011', 'value': 'HomePrices2011'},
                {'label': '2016', 'value': 'HomePrices2016'}
            ],
            value='HomePrices2006',
            style={'width': '50%', 'margin-left': '5px'}
        ),

        dcc.Graph(id="housing_choropleth"),
    ])
])


# Gets user input from dropdown to choose year for housing visualization
@app.callback(
    Output("housing_choropleth", "figure"),
    [Input("housing_year", "value")]
)
def display_housing_choropleth(housing_year):
    housing_figure = px.choropleth_mapbox(
        data_frame=hfx_census,
        geojson=hfx_json,
        color=housing_year,
        locations='CTUID',
        featureidkey="properties.CTUID",
        center={"lat": 44.651070, "lon": -63.582687},
        zoom=10,
        opacity=0.4,
        mapbox_style="carto-positron",
    )

    return housing_figure