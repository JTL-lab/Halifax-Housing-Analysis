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

        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='Dwelling Types',
                                     className='text-center text-light bg-dark'), body=True, color="dark")
                    , className='mb-4')
        ]),

        # Dropdown menu for dwelling barchart
        html.P("Dwelling types by tract:"),
        dcc.Dropdown(
            id='dwelling_year',
            options=[
                {'label': '2006', 'value': 'sums_2006'},
                {'label': '2011', 'value': 'sums_2011'},
                {'label': '2016', 'value': 'sums_2016'}
            ],
            value='sums_2006',
            style={'width': '50%', 'margin-left': '5px'}
        ),

        dcc.Graph(id="dwelling_barchart", style={'width': '90vh', 'height': '60vh'}),

        dbc.Row([
            html.Img(src=app.get_asset_url('correlations_with_average_value.png'), style={'height': '50vh', 'width': '50vh'})
        ]),

        dbc.Row([
            dbc.Col([
                html.P("The above diagram shows the correlation between the type of dwelling and the average dwelling value of a census tract. "
                       "If the correlation is positive, that means that when there is a high number of dwellings of the specified dwelling type in a tract, "
                       "the average dwelling value of the tract increases. If the correlation is negative, that means that when there is a high number of the "
                       "specified dwelling type in a tract, the average dwelling value of the tract decreases. There is a moderate negative correlation between average dwelling value and "
                       "semi detached homes, row houses, apartments in buildings with less thn five stories, and other dwellings (mobile homes etc.). There is also a "
                       "weak-moderate negative correlation between the number of dwellings in a tract and the average dwelling value of the tract. "
                       "Halifax is lacking in many of the dwelling types that have a negative correlation with average value. It is safe to assume "
                       "that if these dwelling types were greater in number, the negative correlation would be even stronger. "
                       "This is because a small number of dwellings can not decrease the average dwelling value of an entire tract substantially, "
                       "although a large number of dwellings can. There is a strong positive correlation between median household income "
                       "and average dwelling value. Generally, wealthier people can afford more valuable homes.")
            ])
        ]),

        dbc.Row([
            dbc.Col(dbc.Card(html.Embed(src=app.get_asset_url('housing_report.html'), style={'height': '90vh'})))
        ]),

        dbc.Row([
            dbc.Col([
                html.P("The above shows the exploratory data analysis that was used to better understand the housing "
                       "trends in Metro Halifax.")
            ])
        ]),
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

# Gets user input from dropdown to choose year for dwelling type visualization
@app.callback(
    Output("dwelling_barchart", "figure"),
    [Input("dwelling_year", "value")]
)
def display_dwelling_barchart(dwelling_year):
    dwelling_barchart = px.bar(
        housing_data,
        x='dwellings',
        y=dwelling_year,
        labels={"dwellings": "Dwelling types",
                dwelling_year: "Total"}
    )

    return dwelling_barchart
