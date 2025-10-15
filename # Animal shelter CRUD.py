# Animal shelter CRUD
import os
import numpy as np
import pandas as pd
from pymongo import MongoClient
from bson.json_util import dumps
import re #needed for the regex pattern matching

import base64 #need for images




# Setup the Jupyter version of Dash
from jupyter_dash import JupyterDash

# Configure the necessary Python module imports
import dash_leaflet as dl
from dash import dcc
from dash import html
import plotly.express as px
from dash import dash_table
from dash.dependencies import Input, Output, State


# Configure the plotting routines
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


import os
import numpy as np
import pandas as pd
from pymongo import MongoClient
from bson.json_util import dumps
import re #needed for the regex pattern matching

import base64 #need for images

#### FIX ME #####
# change animal_shelter and AnimalShelter to match your CRUD Python module file name and class name
from CRUD import AnimalShelter

###########################
# Data Manipulation / Model
###########################
username = "aacuser"
password = "password"
shelter = AnimalShelter()

#create the default dataframe
df = pd.DataFrame.from_records(shelter.getRecordCriteria({}))


#########################
# Dashboard Layout / View
#########################
app = JupyterDash('SimpleExample')

#add the customers branding
image_filename = 'Grazioso Salvare Logo.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

app.layout = html.Div([
    #create an anchor for the image/logo
    #make the image an href to the website, www.snhu.edu
    #open the link in a new tab by setting a blank target
    html.A([
        html.Center(html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), 
               height = 250, width = 251))], href = 'https://www.snhu.edu', target = "_blank"),
    html.Center(html.B(html.H1('Teisha Yoder\' SNHU CS-340 Dashboard'))),
    html.Hr(),
    #create the radio buttons to act as a filter
    #set the default on initial load to to 'All'
    dcc.RadioItems(
        id='filter-type',
        options=[
            {'label': 'All', 'value': 'All'},
            {'label':'Water Rescue', 'value': 'Water'},
            {'label':'Mountain or Wilderness Rescue', 'value': 'Mountain'},
            {'label':'Disaster Rescue or Individual Tracking', 'value':'Disaster'},
        ],
        value='All'
    ),
    html.Hr(),
    dash_table.DataTable(
        id='datatable-id',
        columns=[
            {"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns
        ],
        data=df.to_dict('records'),
        editable=True,
        row_selectable="single", #allow a row to be selected
        selected_rows=[],
        filter_action="native", #allow a filter
        sort_action="native", #allow sorting
        page_action="native", #enable pagination
        page_current=0, #set start page
        page_size=10, #set rows per page

    ),
    html.Br(),
    html.Hr(),
#This sets up the dashboard so that your chart and your geolocation chart are side-by-side
    html.Div(className='row',
         style={'display' : 'flex', 'justify-content':'center'},
             children=[
        html.Div(
            id='graph-id',
            className='col s12 m6',
            ),
        html.Div(
            id='map-id',
            className='col s12 m6',
            )
        ])
])

#############################################
# Interaction Between Components / Controller
#############################################
   
@app.callback([Output('datatable-id','data'),
               Output('datatable-id','columns')],
              [Input('filter-type', 'value')])
def update_dashboard(filter_type):
    #set up an if/else if/else block to respond to the radio buttons
    if filter_type == 'All':
        df = pd.DataFrame.from_records(shelter.getRecordCriteria({})) 
    elif filter_type == 'Water':

        #data isn't that clean, use regex for pattern matching
        #build the regex patterns for the different filters
        labRegex = re.compile(".*lab.*", re.IGNORECASE)
        chesaRegex = re.compile(".*chesa.*", re.IGNORECASE)
        newRegex = re.compile(".*newf.*", re.IGNORECASE)
        
        df = pd.DataFrame.from_records(shelter.getRecordCriteria({
            '$or':[ 
                {"breed": {'$regex': newRegex}}, #pass the regex to the filter
                {"breed": {'$regex': chesaRegex}},
                {"breed": {'$regex': labRegex}},
            ],
            "sex_upon_outcome": "Intact Female",
            "age_upon_outcome_in_weeks": {"$gte":26.0, "$lte":156.0}
        }))
    elif filter_type == 'Mountain':
        
        germanRegex = re.compile(".*german.*", re.IGNORECASE)
        alaskanRegex = re.compile(".*mala.*", re.IGNORECASE)
        oldRegex = re.compile(".*old engilish.*", re.IGNORECASE)
        huskyRegex = re.compile(".*husk.*", re.IGNORECASE)
        rottRegex = re.compile(".*rott.*", re.IGNORECASE)
        
        df = pd.DataFrame.from_records(shelter.getRecordCriteria({
            '$or':[
                {"breed": {'$regex': germanRegex}},
                {"breed": {'$regex': alaskanRegex}},
                {"breed": {'$regex': oldRegex}},
                {"breed": {'$regex': huskyRegex}},
                {"breed": {'$regex': rottRegex}},
            ],
            "sex_upon_outcome": "Intact Male",
            "age_upon_outcome_in_weeks": {"$gte":26.0, "$lte":156.0}
        }))
    elif filter_type == 'Disaster':
        
        germanRegex = re.compile(".*german.*", re.IGNORECASE)
        goldenRegex = re.compile(".*golden.*", re.IGNORECASE)
        bloodRegex = re.compile(".*blood.*", re.IGNORECASE)
        doberRegex = re.compile(".*dober.*", re.IGNORECASE)
        rottRegex = re.compile(".*rott.*", re.IGNORECASE)
        
        df = pd.DataFrame.from_records(shelter.getRecordCriteria({
            '$or':[
                {"breed": {'$regex': germanRegex}},
                {"breed": {'$regex': goldenRegex}},
                {"breed": {'$regex': bloodRegex}},
                {"breed": {'$regex': doberRegex}},
                {"breed": {'$regex': rottRegex}},
            ],
            "sex_upon_outcome": "Intact Male",
            "age_upon_outcome_in_weeks": {"$gte":20.0, "$lte":300.0}
        }))
    else:
        raise Exception("Unknown filter")
    
    columns=[{"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns]
    data=df.to_dict('records')        
        
    return (data,columns)


#change the color of a selected cell
@app.callback(
    Output('datatable-id', 'style_data_conditional'),
    [Input('datatable-id', 'selected_columns')]
)
def update_styles(selected_columns):
    return [{
        'if': { 'column_id': i },
        'background_color': '#D2F3FF'
    } for i in selected_columns]

#call back for pie chart
#set to plot all of the data across all of the pages instead of the viewable data
#change to derived_viewport_data if other behavior is wanted
@app.callback(
    Output('graph-id', "children"),
    [Input('datatable-id', "derived_virtual_data")])
def update_graphs(viewData):
    
    dffPie = pd.DataFrame.from_dict(viewData)

    return [
        dcc.Graph(            
            figure = px.pie(dffPie, names='breed',)
        )    
    ]

#call back for slecting a row and then plotting the geomarker
@app.callback(
    Output('map-id', "children"),    
    [Input('datatable-id', "derived_virtual_selected_rows")])
def update_map(virtualRows):
    
    
    #create the views
    if not virtualRows: #build a default view if there are no selected lines
        markerArray = (30.75,-97.48) #default marker at Austin Animal Shelter
        toolTip = "Austin Animal Center"
        popUpHeading = "Austin Animal Center"
        popUpParagraph = "Shelter Home Location"
        
    else: #build the contextual views based on the selection
        dff = pd.DataFrame(df.iloc[virtualRows]) #convert the datatable to a dataframe
        coordLat = float(dff['location_lat'].to_string().split()[1]) #strip out the lat
        coordLong = float(dff['location_long'].to_string().split()[1]) #strip out the long
        markerArray = (coordLat, coordLong) #build the array based on selection
        
        toolTip = dff['breed']
        popUpHeading = "Animal Name"
        popUpParagraph = dff['name']

    #return the map with a child marker
    #marker is set to the values found in markerArray
    #map centers/moves to view the new marker instead of holding a fixed center
    return [dl.Map(style={'width': '700px', 'height': '450px'}, center=markerArray,
                   zoom=10, children=[dl.TileLayer(id="base-layer-id"),
                                      dl.Marker(position=markerArray, children=[
                                          dl.Tooltip(toolTip),
                                          dl.Popup([
                                              html.H1(popUpHeading),
                                              html.P(popUpParagraph)
                                          ])
                                      ])
                                     ])
           ]
app.run_server(debug=True)