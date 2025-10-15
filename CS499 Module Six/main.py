# main.py
import os
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import dash_leaflet as dl
import plotly.express as px
from jupyter_dash import JupyterDash
import base64
import re

# Load environment variables
load_dotenv()

from crud import AnimalShelter

#############################################
# Helper Functions
#############################################

def get_breed_regex_patterns(rescue_type):
    patterns = {
        'Water': [r'.*lab.*', r'.*chesa.*', r'.*newf.*'],
        'Mountain': [r'.*german.*', r'.*mala.*', r'.*old engilish.*', r'.*husk.*', r'.*rott.*'],
        'Disaster': [r'.*german.*', r'.*golden.*', r'.*blood.*', r'.*dober.*', r'.*rott.*'],
    }
    return [re.compile(pat, re.IGNORECASE) for pat in patterns.get(rescue_type, [])]

def get_filter_criteria(filter_type):
    """
    Constructs MongoDB query criteria based on filter type.
    """
    if filter_type == 'Water':
        return {
            '$or': [{'breed': {'$regex': pattern}} for pattern in get_breed_regex_patterns('Water')],
            'sex_upon_outcome': 'Intact Female',
            'age_upon_outcome_in_weeks': {'$gte': 26.0, '$lte': 156.0}
        }
    elif filter_type == 'Mountain':
        return {
            '$or': [{'breed': {'$regex': pattern}} for pattern in get_breed_regex_patterns('Mountain')],
            'sex_upon_outcome': 'Intact Male',
            'age_upon_outcome_in_weeks': {'$gte': 26.0, '$lte': 156.0}
        }
    elif filter_type == 'Disaster':
        return {
            '$or': [{'breed': {'$regex': pattern}} for pattern in get_breed_regex_patterns('Disaster')],
            'sex_upon_outcome': 'Intact Male',
            'age_upon_outcome_in_weeks': {'$gte': 20.0, '$lte': 300.0}
        }
    else:
        return {}

#############################################
# Data Model Setup
#############################################

try:
    shelter = AnimalShelter()
except Exception as e:
    raise RuntimeError(f"Could not initialize AnimalShelter: {e}")

try:
    df = pd.DataFrame.from_records(shelter.get_records())
except Exception as e:
    df = pd.DataFrame()
    print(f"Error retrieving data from shelter: {e}")

#############################################
# Dash App Setup
#############################################

app = JupyterDash('AnimalShelterDashboard')

# Load and encode logo image
try:
    image_filename = 'Grazioso Salvare Logo.png'
    with open(image_filename, 'rb') as f:
        encoded_image = base64.b64encode(f.read()).decode()
except Exception as e:
    print(f"Error loading logo image: {e}")
    encoded_image = ''

app.layout = html.Div([
    html.A([
        html.Center(
            html.Img(
                src=f'data:image/png;base64,{encoded_image}',
                height=250, width=251
            )
        )
    ], href='https://www.snhu.edu', target="_blank"),
    html.Center(html.B(html.H1("Teisha Yoder' SNHU CS-340 Dashboard"))),
    html.Hr(),
    dcc.RadioItems(
        id='filter-type',
        options=[
            {'label': 'All', 'value': 'All'},
            {'label': 'Water Rescue', 'value': 'Water'},
            {'label': 'Mountain or Wilderness Rescue', 'value': 'Mountain'},
            {'label': 'Disaster Rescue or Individual Tracking', 'value': 'Disaster'},
        ],
        value='All'
    ),
    html.Hr(),
    dash_table.DataTable(
        id='datatable-id',
        columns=[
            {"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns
        ] if not df.empty else [],
        data=df.to_dict('records') if not df.empty else [],
        editable=True,
        row_selectable="single",
        selected_rows=[],
        filter_action="native",
        sort_action="native",
        page_action="native",
        page_current=0,
        page_size=10,
    ),
    html.Br(),
    html.Hr(),
    html.Div(className='row', style={'display': 'flex', 'justify-content': 'center'}, children=[
        html.Div(id='graph-id', className='col s12 m6'),
        html.Div(id='map-id', className='col s12 m6'),
    ])
])

#############################################
# App Callbacks
#############################################

@app.callback(
    [Output('datatable-id', 'data'),
     Output('datatable-id', 'columns')],
    [Input('filter-type', 'value')]
)
def update_dashboard(filter_type):
    """
    Update table data based on the selected filter type.
    """
    try:
        if filter_type == 'All':
            records = shelter.get_records()
        else:
            criteria = get_filter_criteria(filter_type)
            records = shelter.get_records(criteria)
        df_new = pd.DataFrame.from_records(records)
        columns = [{"name": i, "id": i, "deletable": False, "selectable": True} for i in df_new.columns]
        data = df_new.to_dict('records')
        return data, columns
    except Exception as e:
        print(f"Error updating dashboard: {e}")
        return [], []

@app.callback(
    Output('datatable-id', 'style_data_conditional'),
    [Input('datatable-id', 'selected_columns')]
)
def update_styles(selected_columns):
    """
    Highlight selected columns in data table.
    """
    return [{
        'if': {'column_id': i},
        'background_color': '#D2F3FF'
    } for i in selected_columns]

@app.callback(
    Output('graph-id', "children"),
    [Input('datatable-id', "derived_virtual_data")]
)
def update_graphs(view_data):
    """
    Update pie chart based on (filtered) table data.
    """
    try:
        dff_pie = pd.DataFrame.from_dict(view_data)
        if 'breed' in dff_pie and not dff_pie.empty:
            fig = px.pie(dff_pie, names='breed')
            return [dcc.Graph(figure=fig)]
        else:
            return [html.Div("No breed data available.")]
    except Exception as e:
        print(f"Error updating graph: {e}")
        return [html.Div("Error generating chart")]

@app.callback(
    Output('map-id', "children"),
    [Input('datatable-id', "derived_virtual_selected_rows"),
     Input('datatable-id', "data")]
)
def update_map(virtual_rows, table_data):
    """
    Update map marker based on selected row.
    """
    try:
        dff = pd.DataFrame(table_data)
        if not virtual_rows or len(virtual_rows) == 0 or dff.empty:
            marker_array = (30.75, -97.48)
            tool_tip = "Austin Animal Center"
            pop_up_heading = "Austin Animal Center"
            pop_up_paragraph = "Shelter Home Location"
        else:
            sel = virtual_rows[0]
            coord_lat = float(dff.iloc[sel]['location_lat'])
            coord_long = float(dff.iloc[sel]['location_long'])
            marker_array = (coord_lat, coord_long)
            tool_tip = dff.iloc[sel]['breed']
            pop_up_heading = "Animal Name"
            pop_up_paragraph = dff.iloc[sel]['name']

        return [dl.Map(
            style={'width': '700px', 'height': '450px'},
            center=marker_array,
            zoom=10,
            children=[dl.TileLayer(id="base-layer-id"),
                      dl.Marker(position=marker_array, children=[
                          dl.Tooltip(tool_tip),
                          dl.Popup([html.H1(pop_up_heading), html.P(pop_up_paragraph)])
                      ])]
        )]
    except Exception as e:
        print(f"Error updating map: {e}")
        return [html.Div("Error rendering map.")]

if __name__ == '__main__':
    app.run_server(debug=True)
