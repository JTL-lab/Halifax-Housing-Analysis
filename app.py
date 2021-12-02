import dash
import dash_bootstrap_components as dbc

stylesheet = [dbc.themes.LUX]

app = dash.Dash(__name__, external_stylesheets=stylesheet)

server = app.server
app.config.suppress_callback_exceptions = True
