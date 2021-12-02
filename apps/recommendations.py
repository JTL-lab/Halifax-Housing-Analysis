from dash import html
import dash_bootstrap_components as dbc

layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Row([
                dbc.Col(html.H1("Recommendations to solve the housing crisis coming soon", className="text-center"),
                        className="mb-5 mt-5")
            ])
        ])
    ])
])