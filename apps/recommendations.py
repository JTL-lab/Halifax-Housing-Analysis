from dash import html
import dash_bootstrap_components as dbc

layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Row([
                dbc.Col(html.H1("Recommendations to improve accessibility to housing in Halifax", className="text-center"),
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
                           "'house-scale buildings that happen to have more than one unit within them' [1]. Examples "
                           "of middle housing include duplexes, triplexes, courtyard apartments, and bungalow courts."),

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
        ]),
    dbc.Container([
        dbc.Row([
            dbc.Row([
                dbc.Col(html.H3('Resources Consulted: [1] Daniel Parolek. "Missing Middle Housing: Thinking Big and '
                                'Building Small to Respond to Today\'s Housing Crisis". 2020.',
                                className="text-center"),
                        className="mb-5 mt-5")
            ])
        ])
    ]),
])
