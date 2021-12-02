from dash import html
import dash_bootstrap_components as dbc

layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Row([
                dbc.Col(html.H1("Housing Analysis Coming Soon", className="text-center"),
                        className="mb-5 mt-5")
            ])
        ])
    ])
])