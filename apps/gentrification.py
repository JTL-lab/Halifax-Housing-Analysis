from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from app import app
from data import preprocessing
import plotly.express as px

hfx_census = preprocessing.return_dataframe('data/hfxCensusData2006-2016.csv')
hfx_json = preprocessing.return_geojson()
census_cols = list(hfx_census.columns)

def find_gentrified_tracts():

    return

def gentrification_prediction_model():
    return


# DASHBOARD LAYOUT
layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Row([
                dbc.Col(html.H3("GENTRIFICATION BACKGROUND"),
                        className="mb-5 mt-5")
            ]),
            dbc.Row([
                html.P("Gentrification is a process where college-educated, wealthly individuals move into poor or "
                       "working class communities and cause rising costs of living and/or the community culture to "
                       "change [1].")
            ])
        ]),

        # Section 1: Black population visualization for 2006, 2011, and 2016
        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='BLACK POPULATION',
                                     className='text-center text-light bg-dark'), body=True, color="dark")
                    , className='mb-4')
        ]),

        # Dropdown menu for population density choropleth
        html.P("Census Year:"),
        dcc.Dropdown(
            id='b_census_year',
            options=[
                {'label': '2006', 'value': 'p_black2006'},
                {'label': '2011', 'value': 'p_black2011'},
                {'label': '2016', 'value': 'p_black2016'}
            ],
            value='p_black2006',
            style={'width': '50%', 'margin-left': '5px'}
        ),

        dcc.Graph(id="black_population_choropleth", style={'width': '90vh', 'height': '60vh'}),

        # Section 2: Indigenous population visualization for 2006, 2011, and 2016
        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='INDIGENOUS POPULATION',
                                     className='text-center text-light bg-dark'), body=True, color="dark")
                    , className='mb-4')
        ]),

        # Dropdown menu for indigenous population density choropleth
        html.P("Census Year:"),
        dcc.Dropdown(
            id='i_census_year',
            options=[
                {'label': '2006', 'value': 'p_indig2006'},
                {'label': '2011', 'value': 'p_indig2011'},
                {'label': '2016', 'value': 'p_indig2016'}
            ],
            value='p_indig2006',
            style={'width': '50%', 'margin-left': '5px'}
        ),

        dcc.Graph(id="indig_population_choropleth", style={'width': '90vh', 'height': '60vh'}),

        # Section 3: Minority population visualization for 2006, 2011, and 2016
        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='PEOPLE OF COLOUR (POC) POPULATION',
                                     className='text-center text-light bg-dark'), body=True, color="dark")
                    , className='mb-4')
        ]),

        # Dropdown menu for indigenous population density choropleth
        html.P("Census Year:"),
        dcc.Dropdown(
            id='p_census_year',
            options=[
                {'label': '2006', 'value': 'p_poc2006'},
                {'label': '2011', 'value': 'p_poc2011'},
                {'label': '2016', 'value': 'p_poc2016'}
            ],
            value='p_poc2006',
            style={'width': '50%', 'margin-left': '5px'}
        ),

        dcc.Graph(id="poc_population_choropleth", style={'width': '90vh', 'height': '60vh'}),

        dbc.Row([
            dbc.Row([
                dbc.Col(html.H5("REFERENCES"), className="mb-5 mt-5")

            ]),
            dbc.Row([
                html.P("[1] National Geographic Society, “Gentrification,” National Geographic Society, 9 Sep 2019. "
                       "[Online]. Available: https://www.nationalgeographic.org/encyclopedia/gentrification/.")
            ])
        ])
    ])
])


# Gets user input from dropdown to choose year for black population visualization
@app.callback(
    Output("black_population_choropleth", "figure"),
    [Input("b_census_year", "value")]
)
def display_density_choropleth(census_year):
    density_figure = px.choropleth_mapbox(
        data_frame=hfx_census,
        geojson=hfx_json,
        color=census_year,
        locations='CTUID',
        featureidkey="properties.CTUID",
        center={"lat": 44.651070, "lon": -63.582687},
        zoom=11,
        opacity=0.4,
        mapbox_style="carto-positron",
    )

    return density_figure

# Gets user input from dropdown to choose year for indigenous population visualization
@app.callback(
    Output("indig_population_choropleth", "figure"),
    [Input("i_census_year", "value")]
)
def display_density_choropleth(census_year):
    density_figure = px.choropleth_mapbox(
        data_frame=hfx_census,
        geojson=hfx_json,
        color=census_year,
        locations='CTUID',
        featureidkey="properties.CTUID",
        center={"lat": 44.651070, "lon": -63.582687},
        zoom=11,
        opacity=0.4,
        mapbox_style="carto-positron",
    )

    return density_figure

# Gets user input from dropdown to choose year for people of colour population visualization
@app.callback(
    Output("poc_population_choropleth", "figure"),
    [Input("p_census_year", "value")]
)
def display_density_choropleth(census_year):
    density_figure = px.choropleth_mapbox(
        data_frame=hfx_census,
        geojson=hfx_json,
        color=census_year,
        locations='CTUID',
        featureidkey="properties.CTUID",
        center={"lat": 44.651070, "lon": -63.582687},
        zoom=11,
        opacity=0.4,
        mapbox_style="carto-positron",
    )

    return density_figure
