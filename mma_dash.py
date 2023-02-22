from dash import Dash, html, Input, Output, dcc
from dash_bootstrap_templates import load_figure_template
from sql_connect import db_connect
import dash
import plotly.express as px
import dash_bootstrap_components as dbc
from dotenv import load_dotenv
load_dotenv()

## connecting to the database containing artist and artworks tables

load_figure_template('LITERA')

## setting path for image

image_path='assets/MoMA.png'

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "20rem",
    "padding": "2rem 1rem",
    "background-color": "white",
    "color": "black"
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "20rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "color": "black"
}

sidebar = html.Div(
    [
        html.H2("MoMA dashboard", className="display-4"),
        html.Hr(),
        html.P(
            "Navigation", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Artworks", href="/", active="exact"),
                dbc.NavLink("Artists", href="/page-1", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)


app = Dash(name=__name__, use_pages=True, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.LITERA])
pages = list(dash.page_registry.values())

app.layout= html.Div([dcc.Location(id="url"), sidebar, content])

from pages import artists, artworks

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return artworks.layout
    elif pathname == "/page-1":
        return artists.layout
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", debug=True, port=8080)