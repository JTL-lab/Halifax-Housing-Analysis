"""
Dashboard homepage! Should be updated to contain project overview, background, and goals.
"""

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
                dbc.Col(html.H5(children='Created by Julia Lewandowski, Lauryn Marchand, and Grant Sutherland',
                                className="text-center"),
                        className="mb-4")
            ])
        ])
    ])
])
