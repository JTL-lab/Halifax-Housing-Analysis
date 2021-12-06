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
                           "of middle housing include duplexes, triplexes, courtyard apartments, and bungalow courts. "
                           "During the housing analysis and modeling, it was found that the features semiDetached,"
                           "rowHouses, apartmentLessThanFiveStories, and otherDwellings were negatively correlated "
                           "with "
                           "the average housing costs of a tract which was the target variable. This indicates that "
                           "not "
                           "only are these forms of middle housing affordable, but they typically keep a tract's "
                           "housing "
                           "market affordable over time. Beyond just affordability, there are other benefits to "
                           "increasing middle housing options in a metropolitan area. For one thing, it is easy to add"
                           " middle housing units around existing infrastructure like single-unit homes or large "
                           "apartment buildings [1]. Another benefit is that they are typically more space efficient, "
                           "meaning they can provide housing to a greater number of individuals per square foot than a "
                           "single unit home would while maximizing affordability [1]. Finally, because of this last "
                           "factor, middle housing is beneficial for mixed-households which can increase a sense of "
                           "community and togetherness in an area which is helpful for combatting gentrification [1]."
                           ),
                    html.Img(src=app.get_asset_url('MiddleHousingFig1.png'))
                ],
                title="Recommendation #1: Increase 'Middle Housing' Options in Halifax",
            ),
            dbc.AccordionItem(
                [
                    html.P("This is some content for the second recommendation"),
                ],
                title="Recommendation #2",
            ),
            dbc.AccordionItem(
                [
                    html.P("This is some content for the third recommendation"),
                ],
                title="Recommendation #3",
            ),
        ], style={'marginBottom': 100, 'marginLeft': 500, 'marginRight': 500}),

    dbc.Row([
        dbc.Row([
            dbc.Col(html.H5("REFERENCES"), className="mb-5 mt-5")

        ]),
        dbc.Row([
            html.P('[1] Daniel Parolek. "Missing Middle Housing: Thinking Big and '
                                'Building Small to Respond to Today\'s Housing Crisis". 2020.'),
        ])
    ], className='text-center'),

])
