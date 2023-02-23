from dash import dcc, html, Input, Output, callback
import plotly.express as px
import dash 
from sql_connect import db_connect
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc

db = db_connect()
## creating a list of all the distinct departments
departments = db.q("SELECT DISTINCT department from artwork")
department_vals = [{"label":str(i[0]), "value":str(i[0])} for i in departments.values]
department_vals.append({"label":"All departments", "value":"All departments"})

date_range = [{"label":f'{i} to {i+19}', "value":i} for i in range(1920, 2000, 20)]
date_range.append({"label":"currently active", "value":0})
date_range.append({"label":"inactive for 5 years", "value":5})
date_range.append({"label":"inactive for 10 years", "value":10})
date_range.append({"label":"inactive for 15 years", "value":15})
date_range.append({"label":"All artists to date", "value":"All artists to date"})


artist_art = db.q("""SELECT t1.*, t2.department FROM artist AS t1
            JOIN artwork AS t2
            ON t1.artist_id = t2.artist_id
            """)

###### Selecting all rows from the artist table in the database ##########

artist_db = db.q("""SELECT * FROM artist""")
artist_num = len(artist_db)

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
        html.Div(
            children=[
                        html.Div(children="Department", className="menu-title"),
                        dcc.Dropdown(
                            id="department-filter3",
                            options=
                                department_vals
                            ,
                            value="All departments",
                            clearable=False,
                            className="dropdown",
                        ),
                    ], 
                    className="dropdown-div2"
                ),
                html.Div(
                    children=[
                        html.Div(children="Date range", className="menu-title"),
                        dcc.Dropdown(
                            id="daterange-filter3",
                            options=date_range,
                            value="All artists to date",
                            clearable=False,
                            className="dropdown",
                        ),
                    ], 
                    className="dropdown-div2"
                ),

        dbc.Card(
            [
                dbc.CardBody(
                    children=[
                
                dcc.Graph(
                        id='artists_gender1',
                        className='card-header'
                    ),
                    ]
                ), 

                dbc.CardHeader(
                    id='artists-gender-card-header1',
                    className='card-header'
                )
            ],
            className='card'
        ),
        html.Div(
            children=[
                        html.Div(children="Department", className="menu-title"),
                        dcc.Dropdown(
                            id="department-filter4",
                            options=
                                department_vals
                            ,
                            value="All departments",
                            clearable=False,
                            className="dropdown",
                        ),
                    ], 
                    className="dropdown-div2"
                ),
        html.Div(
                    children=[
                        html.Div(children="Date range", className="menu-title"),
                        dcc.Dropdown(
                            id="daterange-filter4",
                            options=date_range,
                            value="All artists to date",
                            clearable=False,
                            className="dropdown",
                        ),
                    ], 
                    className="dropdown-div2"
                ),
        dbc.Card(
            [
                dbc.CardBody(
                    children=[
                
                dcc.Graph(
                        id='artists_nationality1',
                        className='card-header'
                    ),
                    ]
                ), 

                dbc.CardHeader(
                    id='artists-nationality-card-header1',
                    className='card-header'
                )
            ],
            className='card'
        ),
    ])

@callback(
    Output(component_id='artists_gender1', component_property='figure'),
    [Input(component_id='department-filter3', component_property='value')], Input(component_id='daterange-filter3', component_property='value'))

def update_graphs(department, daterange):
    """Creates the figure to be displayed based on the drop down selections"""
    

    if department == 'All departments':
        new_df = artist_art.drop_duplicates(subset='artist_name', keep="last")
        department = 'All departments'
    else:
        new_df = artist_art.drop_duplicates(subset='artist_name', keep="last")
        new_df = new_df[new_df["department"] == f'{department}']

    if daterange == "All artists to date":
        new_df = new_df
    elif daterange == 5:
        new_df = new_df[new_df['year_end'] >= max(new_df['year_end']) - 5]
    elif daterange == 10:
        new_df = new_df[new_df['year_end'] >= max(new_df['year_end']) - 10]
    elif daterange == 15:
        new_df = new_df[new_df['year_end'] >= max(new_df['year_end']) - 15]
    elif daterange == 0:
        new_df = new_df[new_df['year_end'] == 0]
    else:
        new_df = new_df[(new_df['year_start'] >= daterange) & (new_df['year_start'] <= daterange+19)]

    male_artists = new_df[new_df['gender'] == 'Male']
    female_artists = new_df[new_df['gender'] == 'Female']
    m_f_list = ['Male', 'Female']

    m_f_artists = [len(male_artists), len(female_artists)] 

    fig = px.pie(values=m_f_artists, names=m_f_list, title='Proportion of artists by gender')

    return fig

@callback(
    Output(component_id='artists_nationality1', component_property='figure'),
    [Input(component_id='department-filter4', component_property='value'), Input('daterange-filter4', 'value')])

def update_graphs(department, daterange):
    """Creates the figure to be displayed based on the drop down selections"""
    

    if department == 'All departments':
        new_df = db.q("""SELECT t1.*, t2.department FROM artist AS t1
            JOIN artwork AS t2
            ON t1.artist_id = t2.artist_id
            """)
        new_df = new_df.drop_duplicates(subset='artist_name', keep="last")
        artist_nationality = new_df.groupby('nationality').count()
        department = 'All departments'
    else:
        artist_dep_db = db.q("""SELECT t1.*, t2.department FROM artist AS t1
            JOIN artwork AS t2
            ON t1.artist_id = t2.artist_id
            """)
        new_df = artist_dep_db.drop_duplicates(subset='artist_name', keep="last")
        new_df = new_df[new_df['department'] == f"{department}"]
        artist_nationality = new_df.groupby('nationality').count()

    if daterange == "All artists to date":
        new_df = new_df
    elif daterange == 5:
        new_df = new_df[new_df['year_end'] >= max(new_df['year_end']) - 5]
    elif daterange == 10:
        new_df = new_df[new_df['year_end'] >= max(new_df['year_end']) - 10]
    elif daterange == 15:
        new_df = new_df[new_df['year_end'] >= max(new_df['year_end']) - 15]
    elif daterange == 0:
        new_df = new_df[new_df['year_end'] == 0]
    else:
        new_df = new_df[(new_df['year_start'] >= daterange) & (new_df['year_start'] <= daterange+19)]

    artist_nationality = new_df.groupby('nationality').count()
        

    nationality_quantity = px.bar(
                    artist_nationality,
                    x=artist_nationality.index,
                    y='artist_name', 
                    color=artist_nationality.index)

    return nationality_quantity