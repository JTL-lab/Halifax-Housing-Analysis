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
housing_data = preprocessing.return_dwelling_types('data/housingData2006.csv', 'data/housingData2011.csv', 'data/housingData2016.csv')

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

        dcc.Graph(id="housing_choropleth", style={'width': '90vh', 'height': '60vh'}, className='text-center'),

        dcc.Slider(
            id = 'housing_year',
            min = 2006,
            max = 2016,
            step = 5,
            value = 2006,
            marks = {
                2006: {'label': '2006', 'style': {'font-size': '150%'}},
                2011: {'label': '2011', 'style': {'font-size': '150%'}},
                2016: {'label': '2016', 'style': {'font-size': '150%'}},
            },
        ),

        dbc.Row([
            dbc.Col([
                html.P(
                    "The above visualization shows the average home value of each tract.")
            ])
        ], style={'marginBottom': 25, 'margin-top': 50}),

        # Section 2: Rent prices
        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='Rent prices',
                                     className='text-center text-light bg-dark'), body=True, color="dark")
                    , className='mb-4')
        ]),

        dcc.Graph(id="rent_choropleth", style={'width': '90vh', 'height': '60vh'}, className='text-center'),

        dcc.Slider(
            id = 'rent_year',
            min = 2006,
            max = 2016,
            step = 5,
            value = 2006,
            marks = {
                2006: {'label': '2006', 'style': {'font-size': '150%'}},
                2011: {'label': '2011', 'style': {'font-size': '150%'}},
                2016: {'label': '2016', 'style': {'font-size': '150%'}},
            },
        ),

        dbc.Row([
            dbc.Col([
                html.P(
                    "The above visualization shows the average monthly rent of each tract.")
            ])
        ], style={'marginBottom': 25, 'margin-top': 50}),

        #Section 3: dwelling types
        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='Dwelling Types',
                                     className='text-center text-light bg-dark'), body=True, color="dark")
                    , className='mb-4')
        ]),

        dbc.Row([
            dcc.Graph(id="dwelling_barchart", style={'width': '90vh', 'height': '60vh'}),
        ], style={'marginBottom': 25, "display": "inline-block"}),

        dcc.Slider(
            id = 'dwelling_year',
            min = 2006,
            max = 2016,
            step = 5,
            value = 2006,
            marks = {
                2006: {'label': '2006', 'style': {'font-size': '150%'}},
                2011: {'label': '2011', 'style': {'font-size': '150%'}},
                2016: {'label': '2016', 'style': {'font-size': '150%'}},
            },
        ),

        dbc.Row([
            dbc.Col([
                html.P("The above bar chart shows the number of each type of dwelling in Metro Halifax.")
            ])
        ], style={'marginBottom': 25, 'margin-top': 50}),

        # Section 4: Dwelling type correlation with tract dwelling prices

        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='Dwelling types and their correlation with average tract prices',
                                     className='text-center text-light bg-dark'), body=True, color="dark")
                    , className='mb-4')
        ]),

        dbc.Row([
            html.Img(src=app.get_asset_url('correlations_with_average_value.png'), style={'height': '50vh', 'width': '50vh'})
        ]),

        dbc.Row([
            dbc.Col([
                html.P("The above diagram shows the correlation between each type of dwelling and the average dwelling value of a census tract. "
                       "If the correlation is positive, the average dwelling value of the tract increases when the number of the specified dwelling type increases. "
                       "If the correlation is negative, the average dwelling value of the tract decreases when the number of the specified dwelling type increases. "
                       "There is a moderate negative correlation between average dwelling value and the number of "
                       "semi-detached homes, row houses, apartments in buildings with less thn five stories, and other dwellings (mobile homes etc.). There is also a "
                       "weak-moderate negative correlation between the number of dwellings in a tract and the average dwelling value of the tract. "
                       "Halifax is lacking in many of the dwelling types that have a negative correlation with average value. It is safe to assume "
                       "that if these dwelling types were greater in number, the negative correlation would be even stronger. "
                       "This is because a small number of dwellings can not decrease the average dwelling value of an entire tract substantially, "
                       "although a large number of dwellings can. There is a strong positive correlation between median household income "
                       "and average dwelling value. Generally, wealthier people can afford more valuable homes.")
            ])
        ], style={'margin-bottom': 25, 'margin-top': 50}),
        
        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='Pandas Profiling for Exploratory Data Analysis (EDA)',
                                     className='text-center text-light bg-dark'), body=True, color="dark")
                    , className='mb-4')
        ]),

        dbc.Row([
            dbc.Col(dbc.Card(html.Embed(src=app.get_asset_url('housing_report.html'), style={'height': '90vh'})))
        ]),

        html.Br(),

        dbc.Row([
            dbc.Col([
                html.P("The above shows the exploratory data analysis that was used to better understand the housing "
                       "trends in Metro Halifax.")
            ])
        ], style={'marginBottom': 25, 'margin-top': 50}),
        
         # Section 4: Housing Price Regressor
        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='Training a regressor for housing price prediction',
                                     className='text-center text-light bg-dark'), body=True, color="dark")
                    , className='mb-4')
        ]),

        dbc.Row([
            html.H5("Model Goodness-of-Fit with only training data from 2006 - 2011"),
            dbc.Col(html.Img(src=app.get_asset_url('ModelsWithOnly2011Data.png'), style={'height': '45vh', 'width': '97.5vh', 'margin-bottom': 25}))
        ], style={'marginBottom': 25}),

        html.Br(),

        dbc.Row([
            html.H5("Model Goodness-of-Fit when half of the 2016 data was included in the training data"),
            dbc.Col(html.Img(src=app.get_asset_url('ModelsWithHalf2016Data.png'), style={'height': '45vh', 'width': '97.5vh', 'margin-bottom': 25}))
        ], style={'marginBottom': 25}),

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
        ], style={'marginBottom': 50, 'margin-top': 50})
    ]),
], style={'fontSize': 18})


# Gets user input from dropdown to choose year for housing visualization
@app.callback(
    Output("housing_choropleth", "figure"),
    [Input("housing_year", "value")]
)
def display_housing_choropleth(housing_year):
    if housing_year == 2006:
        housing_year = 'HomePrices2006'
    elif housing_year == 2011:
        housing_year = 'HomePrices2011'
    else:
        housing_year = 'HomePrices2016'

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
        range_color=[100000, 1000000]
    )

    return housing_figure


# Gets user input from dropdown to choose year for rent visualization
@app.callback(
    Output("rent_choropleth", "figure"),
    [Input("rent_year", "value")]
)
def display_rent_choropleth(rent_year):
    if rent_year == 2006:
        rent_year = 'RentPrices2006'
    elif rent_year == 2011:
        rent_year = 'RentPrices2011'
    else:
        rent_year = 'RentPrices2016'

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
        range_color=[450, 1500]
    )

    return rent_figure

# Gets user input from dropdown to choose year for dwelling type visualization
@app.callback(
    Output("dwelling_barchart", "figure"),
    [Input("dwelling_year", "value")]
)
def display_dwelling_barchart(dwelling_year):
    if dwelling_year == 2006:
        dwelling_year = 'sums_2006'
    elif dwelling_year == 2011:
        dwelling_year = 'sums_2011'
    else:
        dwelling_year = 'sums_2016'

    dwelling_barchart = px.bar(
        housing_data,
        x='dwellings',
        y=dwelling_year,
        labels={"dwellings": "Dwelling types",
                dwelling_year: "Total"}
    )

    return dwelling_barchart
