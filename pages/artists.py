from dash import dcc, html, Input, Output, callback, dash_table
import plotly.express as px
import dash 
from sql_connect import db_connect
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc

## connecting to psql database
db = db_connect()

## creating a list of all the distinct departments to be used in dropdown menus
departments = db.q("SELECT DISTINCT department from artwork")
department_vals = [{"label":str(i[0]), "value":str(i[0])} for i in departments.values]
department_vals.append({"label":"All departments", "value":"All departments"})

## creating a list of date ranges which will be used in the dropdown menus
date_range = [{"label":f'{i} to {i+19}', "value":i} for i in range(1920, 2000, 20)]
date_range.append({"label":"currently active", "value":0})
date_range.append({"label":"inactive for 5 years", "value":5})
date_range.append({"label":"inactive for 10 years", "value":10})
date_range.append({"label":"inactive for 15 years", "value":15})
date_range.append({"label":"All artists to date", "value":"All artists to date"})


### joining 'department' column from artwork table to artists table
artist_art = db.q("""SELECT t1.*, t2.department FROM artist AS t1
            JOIN artwork AS t2
            ON t1.artist_id = t2.artist_id
            """)

unique_artist = artist_art.drop_duplicates(subset='artist_name', keep="last")

###### Selecting all rows from the artist table in the database ##########

artist_db = db.q("""SELECT * FROM artist""")

## total number of artists
artist_num = len(artist_db)

## adding artists page to registry and setting path to / so it loads when firing up dashboard
dash.register_page(__name__, path='/')

## initialising layout of page
layout = html.Div(
    ## page header
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
        ## first department drop down menu
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
                ## first date range drop down menu
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

        ## card to contain content of graph and provide more appealing layout

        dbc.Card(
            [
                dbc.CardBody(
                    children=[

                ## graph placeholder referenced in callback
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
        ## second drop down menu for department for nationality graph
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
        ## second drop down menu for date range for nationality graph
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
        ## second card to hold nationality graph
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

## first callback which takes input from both first department and date range dropdowns
## using the inputs we modify the dataframe to suit the filters accordingly
## output is shown on the graph by referencing it's id: artists_gender1

@callback(
    Output(component_id='artists_gender1', component_property='figure'),
    [Input(component_id='department-filter3', component_property='value')], Input(component_id='daterange-filter3', component_property='value'))

def update_graphs(department, daterange):
    """Creates the figure to be displayed based on the drop down selections"""
    
    ## updates the data used in the graph depending on which department is selected
    if department == 'All departments':
        new_df = unique_artist
        department = 'All departments'
    else:
        new_df = unique_artist
        new_df = new_df[new_df["department"] == f'{department}']
    
    
    ## updates the data used in the graph depending on which date range is selected
    ## also takes into account the department since it uses the same df 

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

    ## selecting male and female artists and their counts stored in a list

    male_artists = new_df[new_df['gender'] == 'Male']
    female_artists = new_df[new_df['gender'] == 'Female']
    m_f_list = ['Male', 'Female']

    m_f_artists = [len(male_artists), len(female_artists)] 

    fig = px.pie(values=m_f_artists, names=m_f_list, title='Proportion of artists by gender')

    ## return fig which will be used as the output for the graph
    return fig

## second callback which takes input from both second department and date range dropdowns
## using the inputs we modify the dataframe to suit the filters accordingly
## output is shown on the graph by referencing it's id: artists_nationality1
## working in a similar fashion to 1st callback function

@callback(
    Output(component_id='artists_nationality1', component_property='figure'),
    [Input(component_id='department-filter4', component_property='value'), Input('daterange-filter4', 'value')])

def update_graphs(department, daterange):
    """Creates the figure to be displayed based on the drop down selections"""
    

    if department == 'All departments':
        new_df = unique_artist
        artist_nationality = new_df.groupby('nationality').count()
        department = 'All departments'
    else:
        new_df = unique_artist
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
                    title='Proportion of artists by nationality',
                    color=artist_nationality.index)

    nationality_quantity.update_layout(yaxis_title="artist count")

    return nationality_quantity