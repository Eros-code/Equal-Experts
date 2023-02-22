from dash import dcc, html, Input, Output, callback
import plotly.express as px
import dash 
from sql_connect import db_connect
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
dash.register_page(__name__)

db = db_connect()

###### Selecting all rows from the artist table in the database ##########
no_untitled = db.q("""SELECT * FROM artwork WHERE title NOT LIKE '%Untitled%'""")
artwork_number = len(no_untitled.drop_duplicates(subset='title', keep="last"))
artist_db = db.q("""SELECT * FROM artist""")
artwork_demographs = no_untitled.merge(artist_db[['artist_id','nationality','gender', 'year_start', 'year_end']], on='artist_id', how="left")


male_artists = artwork_demographs[artwork_demographs['gender'] == 'Male']
female_artists = artwork_demographs[artwork_demographs['gender'] == 'Female']
m_f_list = ['Male', 'Female']

m_f_artists = [len(male_artists), len(female_artists)]
fig = px.pie(values=m_f_artists, names=m_f_list, title='Proportion of artwork by gender')

### Artworks created by nationality

artist_nationality = artwork_demographs.groupby('nationality').count()

nationality_quantity = px.bar(
                    artist_nationality,
                    x=artist_nationality.index,
                    y='artwork_id', 
                    color=artist_nationality.index
                )


layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(
                    children="Artwork metrics",
                    className="header-title",
                    id='header_title',
                ),
                html.P(
                    children=f"There are currently {artwork_number} pieces of art in the collection",
                    className='header-description',
                ),
            ], 
            className='page-header'
        ),

        dbc.Card(
            [
                dbc.CardBody(
                    children=[html.Div(
                    children=[
                        html.Div(children="Department", className="menu-title"),
                        dcc.Dropdown(
                            id="chart-filter",
                            options=[
                                {"label": "Bar", "value": "bar"}, {"label":"Pie", "value": "pie"}
                            ],
                            value="bar",
                            clearable=False,
                            className="dropdown",
                        ),
                    ], 
                    className="dropdown-div"
                ),
                html.Div(
                    children=[
                        html.Div(children="Date range", className="menu-title"),
                        dcc.Dropdown(
                            id="chart-filter2",
                            options=[
                                {"label": "Bar", "value": "bar"}, {"label":"Pie", "value": "pie"}
                            ],
                            value="bar",
                            clearable=False,
                            className="dropdown2",
                        ),
                    ], 
                    className="dropdown-div2"
                ),
                
                dcc.Graph(
                        id='artwork_gender',
                        figure=fig,
                        className='card-header'
                    ),
                    html.P('Note that an artist may work on more than one piece hence why proportion may not sum to current number of artworks')
                    ]
                ), 

                dbc.CardHeader(
                    id='artwork-gender-card-header',
                    className='card-header'
                )
            ],
            className='card'
        ),
        dbc.Card(
            [
                dbc.CardBody(
                    children=[
                        html.Div(children=[
                        html.Div(children="Department", className="menu-title"),
                        dcc.Dropdown(
                            id="chart-filter",
                            options=[
                                {"label": "Bar", "value": "bar"}, {"label":"Pie", "value": "pie"}
                            ],
                            value="bar",
                            clearable=False,
                            className="dropdown3",
                        ),
                    ], 
                    className="dropdown-div3"
                ),
                html.Div(
                    children=[
                        html.Div(children="Date range", className="menu-title"),
                        dcc.Dropdown(
                            id="chart-filter2",
                            options=[
                                {"label": "Bar", "value": "bar"}, {"label":"Pie", "value": "pie"}
                            ],
                            value="bar",
                            clearable=False,
                            className="dropdown4",
                        ),
                    ], 
                    className="dropdown-div4"
                ),
                dcc.Graph(
                id='artwork_nationality',
                figure=nationality_quantity
            ), ]),

                dbc.CardHeader(
                    id='artwork-nationality-card-header'
                )
            ],
            className='card'
        )
    ]
)