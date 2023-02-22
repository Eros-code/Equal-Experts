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


app = Dash(name=__name__, use_pages=True, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.LITERA])
pages = list(dash.page_registry.values())

app.layout=html.Div(
    children=[
        html.Div(
            children=[
                html.H2("MoMA Dashboard", className="display-4"),
                html.P(
                    "Navigation", className="lead"
                ),
                dbc.Nav(
                    [
                        dbc.NavLink(f"{pages[0]['name']}", href=pages[0]['relative_path'], active="exact"),
                        dbc.NavLink(f"{pages[1]['name']}", href=pages[1]['relative_path'], active="exact"),
                    ],
                    vertical=True,
                    pills=True,
                ),
            ],
            className='sidebar',
        ),
        html.Div(
            children=dash.page_container,
            className='content'
        )
    ]
)

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", debug=True, port=8080)