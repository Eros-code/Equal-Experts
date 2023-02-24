from dash import dcc, html, Input, Output, callback
import plotly.express as px
import dash 
from sql_connect import db_connect
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc

## adding artworks page to registry
dash.register_page(__name__)

## connecting to psql database
db = db_connect()

###### Selecting all rows from the artist table in the database and join to artworks table ##########
no_untitled = db.q("""SELECT * FROM artwork WHERE title NOT LIKE '%Untitled%'""")
artwork_number = len(no_untitled.drop_duplicates(subset='title', keep="last"))
artist_db = db.q("""SELECT * FROM artist""")
no_untitled_dup = no_untitled.drop_duplicates(subset=['title', 'artist_id'], keep="last")
artwork_demographs = no_untitled_dup.merge(artist_db[['artist_id','nationality','gender', 'year_start', 'year_end']], on='artist_id', how="left")

## creating a list of all the distinct departments
departments = db.q("SELECT DISTINCT department from artwork")
department_vals = [{"label":str(i[0]), "value":str(i[0])} for i in departments.values]
department_vals.append({"label":"All departments", "value":"All departments"})

### creating a list of date ranges for which artworks were completed:

date_range = [{"label":f'{i} to {i+3}', "value":i} for i in range(2000, 2020, 4)]
date_range.append({"label":f'{2020} onward', "value":2020})
date_range.append({"label": 'past 15 years', "value":15})
date_range.append({"label":'past 10 years', "value":10})
date_range.append({"label":'past 5 years', "value":5})
date_range.append({"label":'since earliest completed', "value":'since earliest completed'})

## initialising layout of page
layout = html.Div(
    ## page header
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

        ## first department drop down menu
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

                ## first date range drop down menu
                html.Div(
                    children=[
                        html.Div(children="Date range", className="menu-title"),
                        dcc.Dropdown(
                            id="daterange-filter1",
                            options=date_range,
                            value='since earliest completed',
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
        ## second drop down menu for department for nationality graph
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

        ## second drop down menu for date range for nationality graph
        html.Div(
                    children=[
                        html.Div(children="Date range", className="menu-title"),
                        dcc.Dropdown(
                            id="daterange-filter2",
                            options=date_range,
                            value='since earliest completed',
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

## first callback which takes input from both first department and date range dropdowns
## using the inputs we modify the dataframe to suit the filters accordingly
## output is shown on the graph by referencing it's id: artwork_gender1

@callback(
    Output(component_id='artwork_gender1', component_property='figure'),
    [Input(component_id='department-filter1', component_property='value'), Input('daterange-filter1', 'value')])

def update_graphs(department, daterange):
    """Creates the figure to be displayed based on the drop down selections"""

    ## updates the data used in the graph depending on which department is selected
    if department == 'All departments':
        new_df = artwork_demographs
        department = 'All departments'
    else:
        new_df = artwork_demographs[artwork_demographs["department"] == f'{department}']

    ## updates the data used in the graph depending on which date range is selected
    ## also takes into account the department since it uses the same df 

    if daterange == "since earliest completed":
        new_df = new_df
    elif daterange == 5:
        new_df = new_df[new_df['year_completed'] >= max(new_df['year_completed']) - 5]
    elif daterange == 10:
        new_df = new_df[new_df['year_completed'] >= max(new_df['year_completed']) - 10]
    elif daterange == 15:
        new_df = new_df[new_df['year_completed'] >= max(new_df['year_completed']) - 15]
    elif daterange == 2020:
        new_df = new_df[new_df['year_completed'] >= 2020]
    else:
        new_df = new_df[(new_df['year_completed'] >= daterange) & (new_df['year_completed'] <= daterange+3)]

    ## selecting male and female artists and their counts stored in a list

    male_artists = new_df[new_df['gender'] == 'Male']
    female_artists = new_df[new_df['gender'] == 'Female']
    m_f_list = ['Male', 'Female']

    m_f_artists = [len(male_artists), len(female_artists)] 

    fig = px.pie(values=m_f_artists, names=m_f_list, title='Proportion of artwork by gender')

    ## return fig which will be used as the output for the graph
    return fig


## second callback which takes input from both second department and date range dropdowns
## using the inputs we modify the dataframe to suit the filters accordingly
## output is shown on the graph by referencing it's id: artwork_nationality1
## working in a similar fashion to 1st callback function

@callback(
    Output(component_id='artwork_nationality1', component_property='figure'),
    [Input(component_id='department-filter2', component_property='value'), Input('daterange-filter2', 'value')])

def update_graphs(department, daterange):
    """Creates the figure to be displayed based on the drop down selections"""

    if department == 'All departments':
        artwork_dep = artwork_demographs
        artwork_nationality = artwork_demographs.groupby('nationality').count()
        department = 'All departments'
    else:
        artwork_dep = artwork_demographs[artwork_demographs['department'] == f'{department}']
        artwork_nationality = artwork_demographs[artwork_demographs['department'] == f'{department}'].groupby('nationality').count()

    if daterange == "since earliest completed":
        artwork_nationality = artwork_nationality
    elif daterange == 5:
        artwork_nationality = artwork_dep[artwork_dep['year_completed'] >= max(artwork_dep['year_completed']) - 5].groupby('nationality').count()
    elif daterange == 10:
        artwork_nationality = artwork_dep[artwork_dep['year_completed'] >= max(artwork_dep['year_completed']) - 10].groupby('nationality').count()
    elif daterange == 15:
        artwork_nationality = artwork_dep[artwork_dep['year_completed'] >= max(artwork_dep['year_completed']) - 15].groupby('nationality').count()
    elif daterange == 2020:
        artwork_nationality = artwork_dep[artwork_dep['year_completed'] >= 2020].groupby('nationality').count()
    else:
        artwork_nationality = artwork_dep[(artwork_dep['year_completed'] >= daterange) & (artwork_dep['year_completed'] >= daterange+3)].groupby('nationality').count()

    nationality_quantity = px.bar(
                    artwork_nationality,
                    x=artwork_nationality.index,
                    y='artist_id', 
                    title='Proportion of artwork by nationality',
                    color=artwork_nationality.index)

    nationality_quantity.update_layout(yaxis_title="artist count who have worked on artwork")
    return nationality_quantity