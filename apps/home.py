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
                       "trends for the city of Halifax between the years of 2006 - 2016. The goal of analysis was to "
                       "inform recommendations for how to resolve modern challenges to housing accessibility and "
                       "gentrification. To accomplish this, we analyzed housing and rental cost trends for areas of "
                       "Halifax over three census years: 2006, 2011, and 2016. It was of interest to consider changes "
                       " through the lens of gentrification and its impact on various citizens, especially minority and "
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
            #dbc.Row([
            #    dbc.Col(html.H2("DATA UNDERSTANDING"), className="mb-5 mt-5")
            #]),
            #dbc.Row([
            #    dbc.Card(children=[html.H2(children='Statistics Canada Geographical Boundary Files:',
            #                               className='text-center'),
            #                       dbc.Button("GO TO STATISTICS CANADA",
            #                                  href='https://www12.statcan.gc.ca/census-recensement/index-eng.cfm',
            #                                  color='primary',
            #                                  className='mt-3'),
            #                       ],
            #             body=True, color='dark', outline=True, style={'width': 4}, className='mb-4'),
            #]),
        ]),
    ])
])
