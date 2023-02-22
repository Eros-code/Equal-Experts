from dash import dcc, html, Input, Output, callback
import plotly.express as px
import dash 
from sql_connect import db_connect
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
dash.register_page(__name__)

layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(
                    children="Order Hour",
                    className="header-title",
                    id='header_title',
                ),
                html.P(
                    children="Analysis of the Purchasing Habits of All Customers at Different Hours of the Day",
                    className='header-description',
                ),
            ], 
            className='page-header'
        ),

        dbc.Card(
            [
                dbc.CardBody(
                    children=dcc.Graph(
                        id='quantity-vs-order-hour',
                        className='card-header'
                    )
                ), 

                dbc.CardHeader(
                    id='order-hour-card-header',
                    className='card-header'
                )
            ],
            className='card'
        )
    ]
)