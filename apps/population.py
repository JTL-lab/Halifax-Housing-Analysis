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

# Visualization 1: Interactive population density visualization for 2006, 2011, and 2016 using Dash
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