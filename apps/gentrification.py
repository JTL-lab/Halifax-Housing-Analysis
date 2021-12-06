from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from app import app
from data import preprocessing
import pandas as pd
import numpy as np
import plotly.express as px

hfx_census = preprocessing.return_dataframe()
hfx_json = preprocessing.return_geojson()
census_cols = list(hfx_census.columns)

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
                html.P("Gentrification is a process where college-educated, wealthy individuals move into poor or "
                       "working class communities. This typically causes the cost of living to rise and can also affect"
                       " the community's culture in a detrimental way "
                       "[1]. As a neighborhood becomes more gentrified, more people will typically move into "
                       "the area because of the economic opportunity available. This drives up housing prices and often"
                       " results in the displacement of minority groups living in the area who are typically "
                       "disproportionately affected by these changes [1]. Various news outlets have reported on "
                       "gentrification in Halifax in the past decade [2, 3]. Areas that have been especially mentioned "
                       "by the media in conjunction with gentrification include the North End, South End, Spryfield"
                       ", and Clayton Park [2]."),
                html.P("For our analysis, first we examine the percentages of minority groups (Black, Indigenous, "
                       "People "
                       " of Colour) per each tract. We then apply a methodology to determine which tracts of Metro "
                       "Halifax meet the criteria for having gentrified from 2006 - 2016. Finally, with this combined "
                       "information, we can observe whether gentrification in Halifax appears to be affecting "
                       "neighborhoods with higher minority populations.")
            ], style={'marginBottom': 50}),
            dbc.Row([
                dbc.Col(html.H3('Visualizing minority populations across Halifax from 2006 - 2016')),
            ], style={'marginBottom': 50}, className='text-center'),

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
                       "[Online]. Available: https://www.nationalgeographic.org/encyclopedia/gentrification/."),
                html.P("[2] R. Devet, “Gentrification and income inequality the Halifax Way – An Interview with "
                       "professor Howard Ramos,” Nova Scotia Advocate, 26 Sep, 2019. [Online]. "
                       "Available: https://nsadvocate.org/2019/09/23/gentrification-and-income-inequality-the-"
                       "halifax-way-an-interview-with-professor-howard-ramos/."),
                html.P("[3] M. Adsett, “Halifax residents say gentrification is forcing them from their homes,” "
                       "Atlantic, 25-Aug-2015. [Online]. Available: https://atlantic.ctvnews.ca/halifax-residents-say-"
                       "gentrification-is-forcing-them-from-their-homes-1.2532111."),
            ])
        ])
    ])
], style={'marginBottom': 100})


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


if __name__ == "__main__":
    find_gentrified_tracts(hfx_census)
