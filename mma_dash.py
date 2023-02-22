from dash import Dash, html, Input, Output, dcc
from dash_bootstrap_templates import load_figure_template
import dash
import plotly.express as px
import dash_bootstrap_components as dbc


dash_app = Dash(name=__name__, use_pages=True, routes_pathname_prefix="/dashapp/", external_stylesheets=[dbc.themes.CYBORG], suppress_callback_exceptions=True)