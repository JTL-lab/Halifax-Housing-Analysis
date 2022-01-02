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
hfx_gentrification = preprocessing.find_gentrified_tracts(hfx_census)
census_cols = list(hfx_census.columns)

# update poc percentages so that they're consistent with other pages
hfx_census['p_black2006'] = hfx_census['p_black2006'] * 100
hfx_census['p_black2011'] = hfx_census['p_black2011'] * 100
hfx_census['p_black2016'] = hfx_census['p_black2016'] * 100

hfx_census['p_indig2006'] = hfx_census['p_indig2006'] * 100
hfx_census['p_indig2011'] = hfx_census['p_indig2011'] * 100
hfx_census['p_indig2016'] = hfx_census['p_indig2016'] * 100

hfx_census['p_poc2006'] = hfx_census['p_poc2006'] * 100
hfx_census['p_poc2011'] = hfx_census['p_poc2011'] * 100
hfx_census['p_poc2016'] = hfx_census['p_poc2016'] * 100

# Figure for gentrification from 2006 to 2016
gentrification_figure = px.choropleth_mapbox(
        data_frame=hfx_gentrification,
        geojson=hfx_json,
        color='gentrified',
        locations='CTUID',
        featureidkey="properties.CTUID",
        center={"lat": 44.651070, "lon": -63.582687},
        zoom=11,
        opacity=0.4,
        mapbox_style="carto-positron",
)

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
                       "information, we can observe which tracts gentrified by 2016 and observe whether gentrification "
                       "in Halifax appears to be affecting neighborhoods with higher minority populations.")
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

        dcc.Graph(id="black_population_choropleth", style={'width': '90vh', 'height': '60vh'}),

        # Slider for the black population year
        dcc.Slider(
            id = 'b_census_year',
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

        html.Br(),

        dbc.Row([
            dbc.Col([
                html.P("The above visualization shows the percentage of residents in each tract who identify as black.")
            ])
        ]),

        # Section 2: Indigenous population visualization for 2006, 2011, and 2016
        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='INDIGENOUS POPULATION',
                                     className='text-center text-light bg-dark'), body=True, color="dark")
                    , className='mb-4')
        ]),

        dcc.Graph(id="indig_population_choropleth", style={'width': '90vh', 'height': '60vh'}),

        # Slider for indigenous population year
        dcc.Slider(
            id = 'i_census_year',
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

        html.Br(),

        dbc.Row([
            dbc.Col([
                html.P(
                    "The above visualization shows the percentage of residents in each tract who identify as indigenous.")
            ])
        ]),

        # Section 3: Minority population visualization for 2006, 2011, and 2016
        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='PEOPLE OF COLOUR (POC) POPULATION',
                                     className='text-center text-light bg-dark'), body=True, color="dark")
                    , className='mb-4')
        ]),

        dcc.Graph(id="poc_population_choropleth", style={'width': '90vh', 'height': '60vh'}),

        # Slider for the black population year
        dcc.Slider(
            id = 'p_census_year',
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

        html.Br(),

        dbc.Row([
            dbc.Col([
                html.P(
                    "The above visualization shows the percentage of residents in each tract who identify as a person of colour. "
                    "In this case, a person of colour is any person who does not identify as caucasian.")
            ])
        ]),

        dbc.Row([
            dbc.Col(html.H3('Identifying which tracts gentrified from 2006 - 2016')),
        ], style={'marginBottom': 50, 'marginTop': 50}, className='text-center'),

        dbc.Row([
            dbc.Col([
                html.P("According to Governing.com [4], an area can be determined to have gentrified if it meets the "
                       " following criteria: "),
                html.P("1) There is an increase in the tract's educational attainment, measured by the percentage of "
                       " residents above the age of 25 holding bachelor's degrees, that is in the top third percentile"
                       " of all tracts within the city."),
                html.P("2) The tract's median home value increased when adjusted for inflation."),
                html.P("3) The percentage increase in the tract's inflation-adjusted median home value was in the top"
                       " third percentile of all tracts within the city."),
            ])
        ]),

        dcc.Graph(figure=gentrification_figure, style={'width': '90vh', 'height': '60vh'}),

        dbc.Row([
            dbc.Col([
                html.P("Observations on gentrified tracts: "),
                html.P("Tract 2050024 (Fairview) had a population in 2016 that was 22.64% POC."),
                html.P("Tract 2050021 (North End) had a population in 2016 that was 25.07% POC."),
                html.P("Tract 2050019 (West End) had a population in 2016 that was 9.51% POC."),
                html.P("Tract 2050011 (Quinpool District) had a population in 2016 that was 20.05% POC."),
                html.P("Tract 2050010 (North End) had a population in 2016 that was 33.7% POC."),
                html.P("The tract with the highest percentage of minority population in 2016, Tract 2050009 (37.10%) "
                       " was not gentrified, but in general the tracts observed to have gentrified between 2006 to 2016"
                       " did have a higher-than-average percentage of their population that identified as a visible "
                       "minority. The only exception to this was Tract 2050019 which did not have a significantly "
                       "higher "
                       " percentage of POC residents.")
            ])
        ]),

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
                       "Atlantic, 25 August, 2015. [Online]. Available: https://atlantic.ctvnews.ca/halifax-residents"
                       "-say-gentrification-is-forcing-them-from-their-homes-1.2532111."),
                html.P("[4] “Gentrification report methodology,” Governing, 17 April, 2021. [Online]. "
                       "Available: https://www.governing.com/archive/gentrification-report-methodology.html."),
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
    if census_year == 2006:
        census_year = 'p_black2006'
    elif census_year == 2011:
        census_year = 'p_black2011'
    else:
        census_year = 'p_black2016'

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
        range_color=[0, 30]
    )

    return density_figure


# Gets user input from dropdown to choose year for indigenous population visualization
@app.callback(
    Output("indig_population_choropleth", "figure"),
    [Input("i_census_year", "value")]
)
def display_density_choropleth(census_year):
    if census_year == 2006:
        census_year = 'p_indig2006'
    elif census_year == 2011:
        census_year = 'p_indig2011'
    else:
        census_year = 'p_indig2016'

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
        range_color=[0, 10]
    )

    return density_figure


# Gets user input from dropdown to choose year for people of colour population visualization
@app.callback(
    Output("poc_population_choropleth", "figure"),
    [Input("p_census_year", "value")]
)
def display_density_choropleth(census_year):
    if census_year == 2006:
        census_year = 'p_poc2006'
    elif census_year == 2011:
        census_year = 'p_poc2011'
    else:
        census_year = 'p_poc2016'

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
        range_color=[0, 40]
    )

    return density_figure

#if __name__ == "__main__":
#    find_gentrified_tracts(hfx_census)
