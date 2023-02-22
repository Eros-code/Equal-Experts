from dash import dcc, html, Input, Output, callback
import plotly.express as px
import dash 
from sql_connect import db_connect
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc

db = db_connect()

###### Selecting all rows from the artist table in the database ##########

artist_db = db.q("""SELECT * FROM artist""")
artist_num = len(artist_db)

############ Seperating artists into male and female #############
male_artists = artist_db[artist_db['gender'] == 'Male']
female_artists = artist_db[artist_db['gender'] == 'Female']

m_f_artists = [len(male_artists), len(female_artists)]
m_f_list = ['Male', 'Female']

############ creating graph for male and female using pie chart #############
fig1 = px.pie(values=m_f_artists, names=m_f_list, title='Proportion of artist gender')


###### grouping all rows from the artist table in the database by nationality ##########

artist_nationality = artist_db.groupby('nationality').count()

########## producing bar graph based on nationality ###################

nationality_quantity = px.bar(
                    artist_nationality,
                    x=artist_nationality.index,
                    y='artist_name', 
                    color=artist_nationality.index,
                    )

################ Creating a joined table which has department attached to each artist
artist_dep_db = db.q("""SELECT t1.*, t2.department FROM artist AS t1
            JOIN artwork AS t2
            ON t1.artist_id = t2.artist_id
            """)
artist_dep_db = artist_dep_db.drop_duplicates(subset='artist_name', keep="last")

dash.register_page(__name__)

layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(
                    children="Artist metrics",
                    className="header-title",
                    id='header_title',
                ),
                html.P(
                    children=f"There are currently {artist_num} artists who have worked on artworks in the collection",
                    className='header-description',
                ),
            ], 
            className='page-header'
        ),

        dbc.Card(
            [
                dbc.CardBody(
                    children=[html.Div(children=[
                        html.Div(children="Department", className="menu-title"),
                        dcc.Dropdown(
                            id="chart-filter",
                            options=[
                                {"label": "Bar", "value": "bar"}, {"label":"Pie", "value": "pie"}
                            ],
                            value="bar",
                            clearable=False,
                            className="dropdown6",
                        ),
                    ], 
                    className="dropdown-div6"
                ),html.Div(
                    children=[
                        html.Div(children="Date range", className="menu-title"),
                        dcc.Dropdown(
                            id="chart-filter2",
                            options=[
                                {"label": "Bar", "value": "bar"}, {"label":"Pie", "value": "pie"}
                            ],
                            value="bar",
                            clearable=False,
                            className="dropdown7",
                        ),
                    ], 
                    className="dropdown-div7"
                ),dcc.Graph(
                        id='artist_gender',
                        figure=fig1
                    )
            ]),

                dbc.CardHeader(
                    id='artist_gender-card-header'
                )
            ],
            className='card'
        ),
        dbc.Card(
            [
                dbc.CardBody(
                    children=[html.Div(children=[
                        html.Div(children="Department", className="menu-title"),
                        dcc.Dropdown(
                            id="chart-filter",
                            options=[
                                {"label": "Bar", "value": "bar"}, {"label":"Pie", "value": "pie"}
                            ],
                            value="bar",
                            clearable=False,
                            className="dropdown7",
                        ),
                    ], 
                    className="dropdown-div7"
                ),html.Div(
                    children=[
                        html.Div(children="Date range", className="menu-title"),
                        dcc.Dropdown(
                            id="chart-filter2",
                            options=[
                                {"label": "Bar", "value": "bar"}, {"label":"Pie", "value": "pie"}
                            ],
                            value="bar",
                            clearable=False,
                            className="dropdown8",
                        ),
                    ], 
                    className="dropdown-div8"
                ),dcc.Graph(
                        id='artist_gender',
                        figure=nationality_quantity
                    )
            ]),

                dbc.CardHeader(
                    id='artist_gender-card-header'
                )
            ],
            className='card'
        )
    ]
)
