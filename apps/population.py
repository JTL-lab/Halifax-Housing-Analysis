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

tract_data_url2006 = 'https://raw.githubusercontent.com/JTL-lab/Halifax-Housing-Analysis/main/data/hfxTractages2006.csv'
tractAges2006 = pd.read_csv(tract_data_url2006, index_col=0)
pop_2006 = tractAges2006.reset_index(drop = True)

tract_data_url2011 = 'https://raw.githubusercontent.com/JTL-lab/Halifax-Housing-Analysis/main/data/hfxTractages2011.csv'
tractAges2011 = pd.read_csv(tract_data_url2011, index_col=0)
pop_2011 = tractAges2011.reset_index(drop = True)

tract_data_url2016 = 'https://raw.githubusercontent.com/JTL-lab/Halifax-Housing-Analysis/main/data/hfxTractages2016.csv'
tractAges2016 = pd.read_csv(tract_data_url2016, index_col=0)
pop_2016 = tractAges2016.reset_index(drop = True)

def find_growth_without_childbirth():
    """
    Calculates the average growth without childbirth factored in per age demographic in Halifax between census years.
    This is intended to give an idea of displacement trends.
    :return:
    """

    for year in [2006, 2011, 2016]:

        year_before = str(year-5)
        year = str(year)
        col_name = 'GrowthWithoutChildbirth' + year_before + '-' + year

        # Subtract the number of births and population since the last census from the current population,
        # divide it by the total population from the previous census, and multiply by 100 to obtain % growth
        hfx_census[col_name] = ((hfx_census['Population'+year] - hfx_census['BornSince'+year_before] -
                                hfx_census['Population'+year_before]) / hfx_census['Population'+year_before]) * 100

def getAgeGroupTotals(dfPop):
    total1519 = 0
    total2024 = 0
    total2529 = 0
    total3034 = 0
    total3539 = 0
    total4044 = 0
    total4549 = 0
    total5054 = 0
    total5559 = 0
    total6064 = 0
    for index, row in dfPop.iterrows():
        total1519 += row['15-19']
        total2024 += row['20-24']
        total2529 += row['25-29']
        total3034 += row['30-34']
        total3539 += row['35-39']
        total4044 += row['40-44']
        total4549 += row['45-49']
        total5054 += row['50-54']
        total5559 += row['55-59']
        total6064 += row['60-64']

    ageGroupDict = {'15-19': total1519, '20-24': total2024, '25-29': total2529, '30-34': total3034, '35-39': total3539, '40-44': total4044, '45-49': total4549, '50-54': total5054, '55-59': total5559, '60-64': total6064}
    return ageGroupDict

ageGroupPops2006 = getAgeGroupTotals(pop_2006)
ageGroupPops2011 = getAgeGroupTotals(pop_2011)
ageGroupPops2016 = getAgeGroupTotals(pop_2016)

    # first_census and second_census are 2 out of the three dictionaries (ageGroupPops2006, ageGroupPops2011, ageGroupPops2016)
    # this function follows a specific group of people over five years to see how their demographic grew
    # for example, it will measure growth by comparing thr 15-19 year old population in 2006 to the 20-24 year old population in 2011
    # this tells us specifically what age people are when they are come to and/or leave Halifax
def measureDemographicGrowth(firstCensus, secondCensus):
    ageRanges = ['15-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64']

    growthOfRanges = []

    for i in range(len(ageRanges) - 1):
        popFirstCensus = firstCensus[ageRanges[i]]
        popSecondCensus = secondCensus[ageRanges[i + 1]]

        growthToSecondCensus = (popSecondCensus - popFirstCensus) / popFirstCensus * 100
        growthOfRanges.append(growthToSecondCensus)

    return growthOfRanges

def getAgeBarGraph20112016():
    # growth of age demographics from 2011 to 2016
    growthOfAgeDemographics = measureDemographicGrowth(ageGroupPops2011, ageGroupPops2016)

    lowerAges = [15, 20, 25, 30, 35, 40, 45, 50, 55]
    birthYearRanges = []

    for i in lowerAges:
      firstBirthYear = 2011 - i
      secondBirthYear = 2011 - (i + 4)
      birthYearRanges.append(str(firstBirthYear) + '-' + str(secondBirthYear))

    fig = px.bar(x=birthYearRanges, y=growthOfAgeDemographics)
    fig.update_layout(title = 'Population Growth of Age Demographics 2011-2016', xaxis_title = 'Year of Birth', yaxis_title = 'Population Growth Percentage 2011-2016')
    return fig

def getAgeBarGraph20062011():
    # growth of age demographics from 2011 to 2016

    growthOfAgeDemographics = measureDemographicGrowth(ageGroupPops2006, ageGroupPops2011)

    lowerAges = [15, 20, 25, 30, 35, 40, 45, 50, 55]
    birthYearRanges = []

    for i in lowerAges:
      firstBirthYear = 2006 - i
      secondBirthYear = 2006 - (i + 4)
      birthYearRanges.append(str(firstBirthYear) + '-' + str(secondBirthYear))

    fig = px.bar(x=birthYearRanges, y=growthOfAgeDemographics)
    fig.update_layout(title = 'Population Growth of Age Demographics 2006-2011', xaxis_title = 'Year of Birth', yaxis_title = 'Population Growth Percentage 2006-2011')
    return fig

# Ensure that population growth without childbirth cols are added to dataframe
find_growth_without_childbirth()

layout = html.Div([

    dbc.Container([

        # Sub-heading description of page purpose
        dbc.Row([
            dbc.Col(html.H6("Visualizing population trends in Halifax during the 2006, 2011, and 2016 census years"))
        ]),

        # Section 1: Population Density visualization for 2006, 2011, and 2016
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

        dbc.Row([
            dbc.Col([
                html.P("The above visualization shows the population per square kilometre in each tract.")
            ])
        ]),

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

        dcc.Graph(id="pop_change_choropleth"),

        dbc.Row([
            dbc.Col([
                html.P("The above visualization shows the population growth from one census to the next as a percentage for each tract.")
            ])
        ]),

        # Section 3: Population Growth and Shrinkage Without Childbirths
        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='Population Change Without Childbirth',
                                     className='text-center text-light bg-dark'), body=True, color="dark")
                    , className='mb-4')
        ]),

        # Dropdown menu for population growth without childbirth choropleth
        html.P("Census Years:"),
        dcc.Dropdown(
            id='no_childbirths_year',
            options=[
                {'label': '2001-2006', 'value': 'GrowthWithoutChildbirth2001-2006'},
                {'label': '2006-2011', 'value': 'GrowthWithoutChildbirth2006-2011'},
                {'label': '2011-2016', 'value': 'GrowthWithoutChildbirth2011-2016'}
            ],
            value='GrowthWithoutChildbirth2001-2006',
            style={'width': '50%', 'margin-left': '5px'}
        ),

        dcc.Graph(id="no_childbirths_choropleth"),

        dbc.Row([
            dbc.Col([
                html.P("The above visualization shows the percentage of population growth that each tract would have experienced " 
                       "if no children had been born since the last census. If the growth is positive, it means that "
                       "since the last census, the number of people who moved in is greater than the number of people "
                       "who moved away or died. If the the growth is negative, there were more people who died or moved away "
                       "than people who moved in. We calculated that the growth of Metro Halifax without child birth from 2001-2006 was -3.97%. "
                       "The total growth was 0.999%. From 2006-2011 the growth of Metro Halifax without child birth was -0.094%. The total "
                       "growth was 1.04%. From 2011-2016 the growth of Metro Halifax without child birth was -1.04%. The total growth was 1.03%. "
                       "Given that Canada has a steadily declining birthrate which is one of the lowest in the world [1], the current population trends "
                       "are likely not sustainable for the long term future as Halifax still depends on child birth for a small boost "
                       "to keep the population growing.")
            ])
        ]),

        # section 4 population trends of age groups

        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='Population Trends of Age Groups',
                                     className='text-center text-light bg-dark'), body=True, color="dark")
                    , className='mb-4')
        ]),

        # Dropdown menu for age group growth bar graph
        html.P("Census Years:"),
        dcc.Dropdown(
            id='age_bar_graph_year',
            options=[
                {'label': '2006-2011', 'value': 2006},
                {'label': '2011-2016', 'value': 2011},
            ],
            value=2006,
            style={'width': '50%', 'margin-left': '5px'}
        ),

        dcc.Graph(id="age_bar_graph"),

        dbc.Row([
            dbc.Col([
                html.P("The above bar graph shows the percentage growth of each individual age group from one census to the next for all of Metro Halifax. "
                       "For example, growth of the youngest age group is measured by comparing the population of 15-19 year olds in 2006, to the population of 20-24 year olds in 2011. "
                       "This is the population growth of people born in a specific range of years ageing five years from one census to the next. "
                       "This measurement of population growth identifies when people are most likely to move to Halifax, and move away. "
                       "As we can see from the graph, the population of 15-19 year olds more than doubles by the time they are in the 20-24 year old age group. "
                       "This is the only age demographic that saw significant growth from 2006-2016. "
                       "The most obvious explanation for this repeated increase is the fact that Halifax is home to several post-secondary academic "
                       "institutions. The reason behind the lack of growth in every other age demographic is less obvious. "
                       "However, it is clear that more work needs to be done to keep and attract more people outside of the typical post-secondary age group.")
            ])
        ]),

        dbc.Row([
            dbc.Row([
                dbc.Col(html.H5("REFERENCES"), className="mb-5 mt-5")

            ]),
            dbc.Row([
                html.P("[1] “Fertility rate, total (births per woman) - canada,” Data. [Online]. Available: https://data.worldbank.org/indicator/SP.DYN.TFRT.IN?locations=CA. [Accessed: 06-Dec-2021]. ")
            ])
        ])
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

# Gets user input from dropdown to choose year for growth without childbirth visualization
@app.callback(
    Output("no_childbirths_choropleth", "figure"),
    [Input("no_childbirths_year", "value")]
)
def display_population_change_choropleth(no_childbirths_year):
    no_childbirths_choropleth = px.choropleth_mapbox(
        data_frame=hfx_census,
        geojson=hfx_json,
        color=no_childbirths_year,
        locations='CTUID',
        featureidkey="properties.CTUID",
        center={"lat": 44.651070, "lon": -63.582687},
        zoom=10,
        opacity=0.4,
        mapbox_style="carto-positron",
    )

    return no_childbirths_choropleth

@app.callback(
    Output("age_bar_graph", "figure"),
    [Input("age_bar_graph_year", "value")]
)
def display_population_change_choropleth(age_bar_graph):
    if age_bar_graph == 2006:
        return getAgeBarGraph20062011()
    elif age_bar_graph == 2011:
        return getAgeBarGraph20112016()
