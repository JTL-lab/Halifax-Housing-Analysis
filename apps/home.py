from dash import html
import dash_bootstrap_components as dbc

layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Row([
                dbc.Col(html.H1("Welcome to the Halifax Housing Dashboard!", className="text-center"),
                        className="mb-5 mt-5")
            ]),
            dbc.Row([
                dbc.Col(html.H5(children='Created by Julia Lewandowski, Grant Sutherland, and Lauryn Marchand',
                                className="text-center"),
                        className="mb-4")
            ])
        ]),

        # Describe the business problem
        dbc.Row([
            dbc.Row([
                dbc.Col(html.H2("BUSINESS UNDERSTANDING"),
                        className="mb-5 mt-5")
            ]),

            dbc.Row([
                html.P("This project focuses on the analysis of housing prices and gentrification "
                       "trends for the city of Halifax, NS between the years of 2006 - 2016. The goal of analysis was "
                       "to "
                       "inform recommendations for how to resolve modern challenges to housing accessibility and "
                       "gentrification. To accomplish this, we analyzed housing and rental cost trends for areas of "
                       "Halifax over three census years: 2006, 2011, and 2016. It was of interest to consider changes "
                       "through the lens of gentrification and its impact on various citizens, especially minority and "
                       "low-income Haligonians. Much of the project focus involved creating effective visualizations "
                       "that showcase trends in population growth, housing and rental costs, and types of housing "
                       "available. This was intended to help prioritize explainability."
                       ),
                html.P("The goals of our project were the following: "),
                html.P("1) Visualize population density, growth, and changes over census years for tracts of "
                       "Metro Halifax."),
                html.P("2) Visualize how specific age demographics have grown or shrunk over time."),
                html.P("3) Visualize average housing costs for each metro Halifax tract in 2006, 2011, and 2016."),
                html.P("4) Visualize median rental prices for each metro Halifax tract in 2006, 2011, and 2016"),
                html.P("5) Determine what kinds of housing are prevalent in different metro Halifax tracts."),
                html.P("5) Visualize which census tracts in metro Halifax have gentrified from 2006 - 2016."),
                html.P(
                    "6) Train a machine learning classifier to be able to determine which census tracts will gentrify"
                    " given historical and up-to-date census data on housing and demographics data for Metro Halifax"
                    " tracts."),
                html.P(
                    "7) Train a machine learning regressor to be able to determine the average housing cost per tract"
                    " given historical and up-to-date housing data for Metro Halifax tracts."),
                html.P("8) Based on the previous analysis, make three recommendations for how to improve housing "
                       "conditions in Halifax.")
            ])
        ]),

        dbc.Row([
            dbc.Row([
                dbc.Col(html.H2("DATA UNDERSTANDING"), className="mb-5 mt-5")
            ]),
            dbc.Row([
                html.P("For this project, Statistics Canada Census Data was used to analyze data for all 38 respective "
                       "census tracts of Halifax, Nova Scotia. The Census Tract Profiles contained information on "
                       "population counts, the number of occupied dwellings and occupied private dwellings, private "
                       "dwelling characteristics, and educational attainment of residents for 2006, 2011, and 2016. "
                ),
                html.P("Any data regarding characteristics of residents for tracts was obtained through the Statistics "
                       "Canada National Household Survey (NHS) for the same census years. This included data such as "
                       "age demographics, educational attainment, and counts for the racial and/or ethnic groups that "
                       "respondents identified with."),
                html.P("The boundaries for the 38 Metro Halifax tracts were taken from the Cartographic "
                       " Boundary Files available for Census Tracts in 2016. Because the boundary files obtained "
                       "contained geographical data for all tracts in the census, we filtered out the irrelevant "
                       "tracts. Additionally, for our choropleth visualizations it was necessary to generate a GeoJSON "
                       "file for the Halifax tracts. This was done by obtaining the 2016 Digital Boundary File for the "
                       "census tracts, using the geographic information system software QGIS to filter for the "
                       "Halifax tracts, and converting the final shapefile obtained to GeoJSON. "),
                html.P("Because all data was obtained from Statistics Canada, a national statistics agency tied to the "
                       "Canadian federal government, data was for the most part high-quality and clean. There were some "
                       "minor considerations needed for missing data addressed in the next section."),
            ]),
            dbc.Row([
                dbc.Col(html.H2("DATA PREPARATION"), className="mb-5 mt-5"),
            ]),
            dbc.Row([
                dbc.Col(dbc.Card(children=[html.H2(children='SHAPEFILES',
                                                   className='text-center'),
                                           dbc.Button("Statistics Canada",
                                                      href='https://www12.statcan.gc.ca/census-recensement/2011/geo/bound-limit/bound-limit-2016-eng.cfm',
                                                      color='primary',
                                                      className='text-center',),
                                           ],
                                 body=True, color='dark', style={'padding': '3px'}, className='text-center', outline=True)
                        , width=4, className='mb-4'),
                dbc.Col(dbc.Card(children=[html.H2(children='POPULATION DATA',
                                                   className='text-center'),
                                           dbc.Button("Statistics Canada",
                                                      href='https://www12.statcan.gc.ca/census-recensement/2021/dp-pd/index-eng.cfm',
                                                      color='primary',
                                                      className='text-center'),
                                           ],
                                 body=True, color='dark', style={'padding': '3px'}, className='text-center', outline=True)
                        , width=4, className='mb-4'),
                dbc.Col(dbc.Card(children=[html.H2(children='HOUSING DATA',
                                                   className='text-center'),
                                           dbc.Button("NHS Canada",
                                                      href='https://www12.statcan.gc.ca/census-recensement/index-eng.cfm',
                                                      color='primary',
                                                      className='text-center'),
                                           ],
                                 body=True, color='dark', style={'padding': '3px'}, className='text-center', outline=True)
                        , width=4, className='mb-4')
            ]),
        ]),
        dbc.Row([
            html.P("Certain tracts had this information suppressed during 2011, so any affected rows lacking information "
                   "(i.e containing NaN values) were dropped during analysis.")
        ])
    ])
])
