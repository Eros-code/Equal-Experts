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
no_untitled_dup = no_untitled.drop_duplicates(subset=['title', 'artist_id'], keep="last")
artwork_demographs = no_untitled_dup.merge(artist_db[['artist_id','nationality','gender', 'year_start', 'year_end']], on='artist_id', how="left")

## creating a list of all the distinct departments
departments = db.q("SELECT DISTINCT department from artwork")
department_vals = [{"label":str(i[0]), "value":str(i[0])} for i in departments.values]
department_vals.append({"label":"All departments", "value":"All departments"})

### Artworks created by nationality


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
        html.Div(
            children=[
                        html.Div(children="Department", className="menu-title"),
                        dcc.Dropdown(
                            id="department-filter1",
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
                            id="daterange-filter1",
                            options=[
                                {"label": "Bar", "value": "bar"}, {"label":"Pie", "value": "pie"}
                            ],
                            value="bar",
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
                        id='artwork_gender1',
                        className='card-header'
                    ),
                    html.P('Note that an artist may work on more than one piece hence why proportion may not sum to current number of artworks. This pie chart represents the number of times a Male or Female has worked on a piece of artwork')
                    ]
                ), 

                dbc.CardHeader(
                    id='artwork-gender-card-header1',
                    className='card-header'
                )
            ],
            className='card'
        ),
        html.Div(
            children=[
                        html.Div(children="Department", className="menu-title"),
                        dcc.Dropdown(
                            id="department-filter2",
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
                            id="daterange-filter2",
                            options=[
                                {"label": "Bar", "value": "bar"}, {"label":"Pie", "value": "pie"}
                            ],
                            value="bar",
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
                        id='artwork_nationality1',
                        className='card-header'
                    ),
                    ]
                ), 

                dbc.CardHeader(
                    id='artwork-nationality-card-header1',
                    className='card-header'
                )
            ],
            className='card'
        ),
    ]
)

@callback(
    Output(component_id='artwork_gender1', component_property='figure'),
    Input(component_id='department-filter1', component_property='value'))

def update_graphs(department):
    """Creates the figure to be displayed based on the drop down selections"""

    if department == 'All departments':
        new_df = artwork_demographs
        department = 'All departments'
    else:
        new_df = artwork_demographs[artwork_demographs["department"] == f'{department}']

    male_artists = new_df[new_df['gender'] == 'Male']
    female_artists = new_df[new_df['gender'] == 'Female']
    m_f_list = ['Male', 'Female']

    m_f_artists = [len(male_artists), len(female_artists)] 

    fig = px.pie(values=m_f_artists, names=m_f_list, title='Proportion of artwork by gender')

    return fig


@callback(
    Output(component_id='artwork_nationality1', component_property='figure'),
    Input(component_id='department-filter2', component_property='value'))

def update_graphs(department):
    """Creates the figure to be displayed based on the drop down selections"""

    if department == 'All departments':
        artwork_nationality = artwork_demographs.groupby('nationality').count()
        department = 'All departments'
    else:
        artwork_nationality = artwork_demographs[artwork_demographs['department'] == f'{department}'].groupby('nationality').count()

    nationality_quantity = px.bar(
                    artwork_nationality,
                    x=artwork_nationality.index,
                    y='artist_id', 
                    color=artwork_nationality.index)

    return nationality_quantity