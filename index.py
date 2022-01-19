from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from app import app
from app import server
from apps import home, population, gentrification, housing, recommendations

# Navigation bar!
nav = dbc.DropdownMenu(

    children=[
        dbc.DropdownMenuItem("Home", href='/home'),
        dbc.DropdownMenuItem("Population Analysis", href='/population'),
        dbc.DropdownMenuItem("Gentrification Analysis", href='/gentrification'),
        dbc.DropdownMenuItem("Housing Analysis", href='/housing'),
        dbc.DropdownMenuItem("Recommendations", href='/recommendations')
    ],
    nav=True,
    in_navbar=True,
    label='Explore Halifax'
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=app.get_asset_url('HFXHousingLogo.png'), height='50px')),
                        dbc.Col(dbc.NavbarBrand("HALIFAX HOUSING ANALYSIS", className="ml-2")),
                    ],
                    align='center',
                ),
                href="/home"
            ),
            dbc.NavbarToggler(id="navbar-toggler2"),
            dbc.Collapse(
                dbc.Nav(
                    [nav], className="ml-auto", navbar=True
                ),
                style={'align': 'right'},
                id="navbar-collapse2",
                navbar=True,
            )
        ]
    ),
    color='dark',
    dark=True,
    className='mb-4',
)


# Define behaviour of the nav bar when clicked (vs. when not clicked)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


for i in [2]:
    app.callback(
        Output(f"navbar-collapse{i}", "is_open"),
        [Input(f"navbar-toggler{i}", "n_clicks")],
        [State(f"navbar-collapse{i}", "is_open")],
    )(toggle_navbar_collapse)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content')
])

def func():
    return 1


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_selected_page(pathname):
    if pathname == '/population':
        return population.layout
    elif pathname == '/gentrification':
        return gentrification.layout
    elif pathname == '/housing':
        return housing.layout
    elif pathname == '/recommendations':
        return recommendations.layout
    else:
        return home.layout


if __name__ == "__main__":
    app.run_server(host='127.0.0.1', port='8050', debug=True)
