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

############ Seperating artists into male and female #############
male_artists = artist_db[artist_db['gender'] == 'Male']
female_artists = artist_db[artist_db['gender'] == 'Female']

m_f_artists = [len(male_artists), len(female_artists)]
m_f_list = ['Male', 'Female']

############ creating graph for male and female using pie chart #############
fig1 = px.pie(values=m_f_artists, names=m_f_list, title='Proportion of artist gender')


###### grouping all rows from the artist table in the database by nationality ##########

artist_nationality = artist_db.groupby('nationality').count()

artist_nationality

########## producing bar graph based on nationality ###################

nationality_quantity = px.bar(
                    artist_nationality,
                    x=artist_nationality.index,
                    y='artist_name', 
                    color=artist_nationality.index,
                    )


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
                    children="Analysis of the Toothbrush Purchasing Habits of Different Age Groups",
                    className='header-description',
                ),
            ], 
            className='page-header'
        ),

        dbc.Card(
            [
                dbc.CardBody(
                    children=dcc.Graph(
                        id='artist_gender',
                        figure=fig1
                    )
                ),

                dbc.CardHeader(
                    id='artist_gender-card-header'
                )
            ],
            className='card'
        ),
        dbc.Card(
            [
                dbc.CardBody(
                    children=dcc.Graph(
                        id='artist_gender',
                        figure=nationality_quantity
                    )
                ),

                dbc.CardHeader(
                    id='artist_gender-card-header'
                )
            ],
            className='card'
        )
    ]
)