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
from pandas_profiling import ProfileReport

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

        dcc.Graph(id="housing_choropleth", style={'width': '90vh', 'height': '60vh'}),

        # Section 2: Rent prices
        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='Rent prices',
                                     className='text-center text-light bg-dark'), body=True, color="dark")
                    , className='mb-4')
        ]),

        # Dropdown menu for housing choropleth
        html.P("Census Year:"),
        dcc.Dropdown(
            id='rent_year',
            options=[
                {'label': '2006', 'value': 'RentPrices2006'},
                {'label': '2011', 'value': 'RentPrices2011'},
                {'label': '2016', 'value': 'RentPrices2016'}
            ],
            value='RentPrices2006',
            style={'width': '50%', 'margin-left': '5px'}
        ),

        dcc.Graph(id="rent_choropleth", style={'width': '90vh', 'height': '60vh'}),

        # Section 3: Housing Pandas Profiling Report
        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='Pandas Profiling for Exploratory Data Analysis (EDA)',
                                     className='text-center text-light bg-dark'), body=True, color="dark")
                    , className='mb-4')
        ]),

        dbc.Row([
            dbc.Col([
                html.P("The above shows the exploratory data analysis that was used to better understand the housing "
                       "trends in Metro Halifax.")
            ])
        ], className='text-center'),

        dbc.Row([
            dbc.Col(dbc.Card(html.Embed(src=app.get_asset_url('housing_report.html'), style={'height': '90vh'})))
        ], style={'marginBottom': 50}),


        # Section 4: Housing Price Regressor
        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='Training a regressor for housing price prediction',
                                     className='text-center text-light bg-dark'), body=True, color="dark")
                    , className='mb-4')
        ]),

        dbc.Row([
            html.P("Model Goodness-of-Fit with only training data from 2006 - 2011"),
            dbc.Col(html.Img(src=app.get_asset_url('ModelsWithOnly2011Data.png'))),
            html.P("Model Goodness-of-Fit when half of the 2016 data was included in the training data"),
            dbc.Col(html.Img(src=app.get_asset_url('ModelsWithHalf2016Data.png'))),
        ], style={'marginBottom': 50}),

        dbc.Row([
            html.P("To create a regression capable of predicting the average housing cost of a tract based on historical"
                   " data, we attempted to use an XGBoost Regressor, Random Forest Regressor, and Linear Regression model"
                   ". The model accuracy was not ideal due to challenges posed by limited training data: because the 2021"
                   " census will only be released in February 2022, the 2016 average house prices were used as the target "
                   "variable. This meant that only the 2006 and 2011 data was used in training initially. We instead "
                   "looked at Goodness-of-Fit (R squared coefficient) for the model performance as "
                   "we believe this would be a better indicator of how the model would perform if the training data size "
                   "was not an issue. We also attempted retraining each of the models with an added random 50% of the "
                   "2016 data, and used the remaining 2016 data as the test set. This improved model performance for "
                   "most of the models.")
        ], style={'marginBottom': 50})
    ]),

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
        zoom=11,
        opacity=0.4,
        mapbox_style="carto-positron",
    )

    return housing_figure


# Gets user input from dropdown to choose year for rent visualization
@app.callback(
    Output("rent_choropleth", "figure"),
    [Input("rent_year", "value")]
)
def display_rent_choropleth(rent_year):
    rent_figure = px.choropleth_mapbox(
        data_frame=hfx_census,
        geojson=hfx_json,
        color=rent_year,
        locations='CTUID',
        featureidkey="properties.CTUID",
        center={"lat": 44.651070, "lon": -63.582687},
        zoom=11,
        opacity=0.4,
        mapbox_style="carto-positron",
    )

    return rent_figure
