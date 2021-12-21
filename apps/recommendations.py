from dash import html
import dash_bootstrap_components as dbc
from app import app

layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Row([
                dbc.Col(
                    html.H1("Recommendations to improve Halifax housing accessibility", className="text-center"),
                    className="mb-5 mt-5")
            ])
        ])
    ]),
    dbc.Accordion(
        [
            dbc.AccordionItem(
                [
                    html.P("'Middle Housing' refers to housing types that lay somewhere between a conventional single-"
                           "family home and large multi-unit apartment buildings. They can be best understood as being"
                           " 'house-scale buildings that happen to have more than one unit within them' [1]. Examples "
                           "of middle housing include duplexes, triplexes, courtyard apartments, and bungalow courts. "),
                    html.P("During the housing analysis and modeling, it was found that the features semiDetached, "
                           "rowHouses, apartmentLessThanFiveStories, and otherDwellings were negatively correlated "
                           "with the average housing costs of a tract which was the target variable. This indicates "
                           "that not only are these forms of middle housing affordable, but they typically keep a "
                           "tract's housing market affordable over time. "),
                    html.P("Beyond just affordability, there are other "
                           "benefits to increasing middle housing options in a metropolitan area. For one thing, it is "
                           "easy to add middle housing units around existing infrastructure like single-unit homes or "
                           "large apartment buildings [1]. Another benefit is that they are typically more space "
                           "efficient, meaning they can provide housing to a greater number of individuals per square "
                           "foot than a single unit home would while maximizing affordability [1]. Finally, because of "
                           "this last factor, middle housing is beneficial for mixed-households which can increase a "
                           "sense of community and togetherness in an area which is helpful for combatting "
                           "gentrification [1]."),
                    html.P("Zoning regulations determine the types of infrastructure which can be built within certain areas. "
                           "Zoning regulations are an obstacle because many areas are not zoned for middle housing. Many Halifax "
                           "neighbourhoods are only zoned for conventional single family homes. So in addition to the construction "
                           "of more middle housing, zoning regulations must first be changed to allow for the construction to "
                           "legally take place."),
                    html.Img(src=app.get_asset_url('MiddleHousingFig1.png'), className='text-center'),
                ],
                title="Recommendation #1: Increase 'Middle Housing' Options in Halifax",
            ),
            dbc.AccordionItem(
                [
                    html.P("During our analysis of the housing and rent prices in Halifax, it was found that these "
                           "values increased quite drastically between 2006 and 2016. This was especially the case for "
                           "the tracts determined to have gentrified."),
                    html.P("For example, the tract 2050022.00 (the area "
                           "formerly known as Africville in the North End) saw an average home value increase of over "
                           "$100,000 between 2006 and 2016. For historically low income neighbourhoods, these increases"
                           " in home values and rent costs lead to significant displacement of residents that can "
                           "no longer afford to live in their communities."),
                    html.P("Housing affordability is central to the "
                           "health and well-being of our citizens. Increasing the amount of affordable housing "
                           "available in Halifax, specifically in communities that have been gentrified, can reduce "
                           "poverty rates and bolster economic growth in the city [2]. Ensuring that everyone in "
                           "Halifax has access to shelter will help keep our communities together."),
                ],
                title="Recommendation #2: Increase quantity of affordable housing",
            ),
            dbc.AccordionItem(
                [
                    html.P("Controlling the prices of rent in Halifax and ensuring that they do not increase "
                           "past a certain percentage each year can lead to greater housing stability in Halifax. "
                           "As mentioned, it was found that rent prices increased quite drastically over the "
                           "course of our analysis. By ensuring that rent prices remain stable over a certain "
                           "period of time, tenants can stay in their units longer which can lead to a greater "
                           "sense of community and stability [3]. Along with neighbourhood diversity and economic "
                           "growth, rent control can benefit low income communities by ensuring that affordable "
                           "housing is readily available for those in the community [3]."),
                ],
                title="Recommendation #3: Extend rent control",
            ),
        ], style={'marginBottom': 100, 'marginLeft': 225, 'marginRight': 225}),

    dbc.Row([
        dbc.Row([
            dbc.Col(html.H5("REFERENCES"), className="mb-5 mt-5")

        ]),
        dbc.Row([
            html.P('[1] Daniel Parolek. "Missing Middle Housing: Thinking Big and '
                                'Building Small to Respond to Today\'s Housing Crisis". 2020.'),
            html.P('[2] National Low Income Housing Coalition. "Why do affordable homes matter?". 2021.'),
            html.P('[3] Centre for Equality Rights in Accommodation. "A look at rent control policies across Canada". 2021.'),
        ])
    ], className='text-center'),

])
