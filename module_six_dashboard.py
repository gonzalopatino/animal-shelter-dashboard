"""
============================================================
Title:       Project 2
Author:      Gonzalo Patino
Date:        2024-12-13 
Description:
    This script implements a Dash web application for querying
    and visualizing data from a MongoDB database. The application
    features a data table for viewing and selecting records and a
    geolocation map for visualizing selected records.

Usage:
    - Run the script in a Python environment (e.g., Jupyter Notebook, IDE).
    - Connect to a MongoDB instance using the custom CRUD module.
    - Select rows in the DataTable to update the map dynamically.

Modules and Libraries:
    - dash: For building the web interface.
    - jupyter_dash: For rendering Dash applications in Jupyter Notebook.
    - dash_leaflet: For interactive maps and geolocation visualization.
    - pandas: For data manipulation and preparation.
    - crud_operations: Custom CRUD module for MongoDB operations.
    - plotly.express: For creating dynamic visualizations.

File Dependencies:
    - crud_operations.py: Implements CRUD (Create, Read, Update, Delete) operations for MongoDB.

License:
    This software is released under the MIT License. See LICENSE file
    in the project root for license information.

============================================================
"""

# Import necessary libraries
from jupyter_dash import JupyterDash
import dash_leaflet as dl
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import pandas as pd
from crud_operations import AnimalShelter
import plotly.express as px

# ============================================================
# Constants for Default Values
# ============================================================
DEFAULT_LAT = 30.75
DEFAULT_LON = -97.48

# ============================================================
# Initialize the AnimalShelter class and fetch data
# ============================================================
# Create an instance of the AnimalShelter class
shelter = AnimalShelter()

# Fetch data from MongoDB and load it into a DataFrame
df = pd.DataFrame.from_records(shelter.read({}))

# Remove MongoDB's '_id' field to avoid compatibility issues
if '_id' in df.columns:
    df.drop(columns=['_id'], inplace=True)

# Handle case where DataFrame is empty
if df.empty:
    df = pd.DataFrame(columns=['location_lat', 'location_lon', 'breed', 'sex_upon_outcome', 'age_upon_outcome_in_weeks', 'name'])

# ============================================================
# Initialize the Dash application
# ============================================================
# Create a Dash app instance
app = JupyterDash('CS-340 Dashboard')

# Define the application layout
app.layout = html.Div([
    # Header Section with Logo Fully Aligned to the Left
html.Div([
    # Logo aligned to the left
    html.Div(
        html.Img(src='assets/company_logo.png', style={'width': '100px', 'margin-left': '0px'}),
        style={'width': '20%', 'textAlign': 'left', 'display': 'inline-block', 'padding': '0'}
    ),

    # Title and Developer Credit aligned to the right
    html.Div([
        html.B(html.H1('SNHU CS-340 Dashboard - Gonzalo Patino')),
        html.P("Developed by: Gonzalo Patino",
               style={'fontSize': '18px', 'fontWeight': 'bold', 'color': 'darkblue'})
    ], style={'width': '75%', 'display': 'inline-block', 'textAlign': 'center', 'padding': '0'})
], style={'display': 'flex', 'align-items': 'center', 'padding': '0'}),

    html.Hr(),

    # Filter options
    html.Div([
        html.Label("Interactive Filter Options", title="Filter dogs by rescue type to update all widgets dynamically."),
        dcc.RadioItems(
            id='filter-rescue-type',
            options=[
                {'label': 'Water Rescue', 'value': 'Water'},
                {'label': 'Mountain Rescue', 'value': 'Mountain'},
                {'label': 'Disaster Rescue', 'value': 'Disaster'},
                {'label': 'Reset', 'value': 'Reset'}
            ],
            value='Reset',
            labelStyle={'display': 'inline-block', 'margin-right': '10px'}
        )
    ], style={'textAlign': 'center', 'margin': '20px'}),

    # Main content
    html.Div([
        # DataTable spans full width
        html.Div([
            dash_table.DataTable(
                id='datatable-id',
                columns=[
                    {"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns
                ],
                data=df.to_dict('records'),
                sort_action="native",
                filter_action="native",
                row_selectable="single",
                selected_rows=[0],
                page_size=10,
                style_table={'overflowX': 'auto'},
                style_cell={'textAlign': 'left', 'padding': '5px'},
                style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'}
            )
        ], style={'width': '100%', 'margin-bottom': '20px'}),  # Full width and margin below

        # Pie chart and map on the second row
        html.Div([
            # Pie chart on the left
            html.Div([
                dcc.Graph(id='pie-chart-id')
            ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),

            # Map on the right
            html.Div([
                dl.Map(
                    id='map-id',
                    style={'width': '100%', 'height': '500px'},
                    center=[DEFAULT_LAT, DEFAULT_LON],
                    zoom=10,
                    children=[dl.TileLayer(id="base-layer-id")]
                )
            ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top', 'margin-left': '2%'})
        ], style={'display': 'flex', 'justify-content': 'space-between'})  # Flexbox for side-by-side layout
    ]),
])


# ============================================================
# Define callback functions for interactivity
# ============================================================

@app.callback(
    [Output('datatable-id', 'data'),
     Output('pie-chart-id', 'figure')],
    Input('filter-rescue-type', 'value')
)
def filter_data_and_update_charts(rescue_type):
    """
    Dynamically filter the data table and update the pie chart based on the selected rescue type.
    """
    # Define query for MongoDB based on the rescue type
    query = {}

    if rescue_type == 'Water':
        query = {
            "breed": {"$in": ["Labrador Retriever Mix", "Chesapeake Bay Retriever", "Newfoundland"]},
            "sex_upon_outcome": "Intact Female",
            "age_upon_outcome_in_weeks": {"$gte": 26, "$lte": 156}
        }
    elif rescue_type == 'Mountain':
        query = {
            "breed": {"$in": ["German Shepherd", "Alaskan Malamute", "Old English Sheepdog", "Siberian Husky", "Rottweiler"]},
            "sex_upon_outcome": "Intact Male",
            "age_upon_outcome_in_weeks": {"$gte": 26, "$lte": 156}
        }
    elif rescue_type == 'Disaster':
        query = {
            "breed": {"$in": ["Doberman Pinscher", "German Shepherd", "Golden Retriever", "Bloodhound", "Rottweiler"]},
            "sex_upon_outcome": "Intact Male",
            "age_upon_outcome_in_weeks": {"$gte": 20, "$lte": 300}
        }

    # Fetch data from MongoDB based on the query
    filtered_records = pd.DataFrame.from_records(shelter.read(query))

    # Handle the "Reset" case: fetch all data
    if rescue_type == 'Reset':
        filtered_records = pd.DataFrame.from_records(shelter.read({}))

    # Remove '_id' column for compatibility
    if '_id' in filtered_records.columns:
        filtered_records.drop(columns=['_id'], inplace=True)

    # If no records match, return an empty DataTable and a placeholder pie chart
    if filtered_records.empty:
        return [], px.pie(title="No Data Available")

    # Create a pie chart for the filtered data
    if rescue_type == 'Reset':
        # Aggregate smaller breeds into "Others" for "Reset"
        breed_counts = filtered_records['breed'].value_counts(normalize=True) * 100
        common_breeds = breed_counts[breed_counts >= 2].index  # Breeds contributing >= 2%
        filtered_records['breed_grouped'] = filtered_records['breed'].apply(lambda x: x if x in common_breeds else 'Others')

        # Create pie chart for aggregated data
        pie_chart = px.pie(
            filtered_records,
            names='breed_grouped',
            title="Breed Distribution (Aggregated)",
            color_discrete_sequence=px.colors.qualitative.Set2  # Consistent color scheme
        )
    else:
        # Create pie chart for filtered data
        pie_chart = px.pie(
            filtered_records,
            names='breed',
            title=f"Breed Distribution for {rescue_type} Rescue"
        )

    # Return filtered DataTable data and the updated pie chart
    return filtered_records.to_dict('records'), pie_chart


#Callback for map update
@app.callback(
    [Output('map-id', 'center'),
     Output('map-id', 'children')],
    [Input('datatable-id', "derived_virtual_data"),
     Input('datatable-id', "derived_virtual_selected_rows")]
)
def update_map(viewData, selected_rows):
    """
    Update the map's center and marker based on the selected row in the DataTable.
    """
    # Default center and tile layer if no rows are selected
    if not viewData or not selected_rows:
        print("No data or selected rows provided.")
        return [DEFAULT_LAT, DEFAULT_LON], [dl.TileLayer(id="base-layer-id")]

    try:
        # Convert the virtual data into a DataFrame
        dff = pd.DataFrame.from_dict(viewData)

        # Ensure a row is selected
        if selected_rows:
            row_index = selected_rows[0]  # Get the selected row index

            # Extract latitude and longitude
            lat = dff.iloc[row_index].get('location_lat', DEFAULT_LAT)
            lon = dff.iloc[row_index].get('location_long', DEFAULT_LON)

            # Validate and convert latitude and longitude
            try:
                lat = float(lat)
                lon = float(lon)
                print(f"Valid coordinates for row {row_index}: lat={lat}, lon={lon}")
            except (ValueError, TypeError):
                print(f"Invalid coordinates for row {row_index}: lat={lat}, lon={lon}")
                lat, lon = DEFAULT_LAT, DEFAULT_LON

            # Extract the dog's name for the tooltip
            name = dff.iloc[row_index].get('name', 'Unknown')
            #Extract the dog's breed for the tooltip
            breed = dff.iloc[row_index].get('breed', 'Unknown').strip()

            
            if not name:  # If the name is empty or missing
                name = "No name found"
                
            if not breed:  # If the name is empty or missing
                breed = "No breed found"
            # Debug: Print final coordinates and marker details
            print(f"Updating map with center: [{lat}, {lon}] and marker for: {name}")

            # Return updated map center and marker
            return [lat, lon], [
                dl.TileLayer(id="base-layer-id"),
                dl.Marker(
                    position=[lat, lon],
                    children=[
                        dl.Tooltip(name),  # Show dog's name in the tooltip
                        dl.Popup([
                            html.H1("Animal Name"),
                            html.P(name),
                            html.P(f"Breed: {breed}")
                        ])
                    ]
                )
            ]
        else:
            # If no row is selected, return the default map view
            print("No row selected.")
            return [DEFAULT_LAT, DEFAULT_LON], [dl.TileLayer(id="base-layer-id")]

    except Exception as e:
        print(f"Error in update_map callback: {e}")
        return [DEFAULT_LAT, DEFAULT_LON], [dl.TileLayer(id="base-layer-id")]

#Callback for highlighting column
@app.callback(
    Output('datatable-id', 'style_data_conditional'),
    [Input('datatable-id', 'selected_columns')]
)
def update_styles(selected_columns):
    """
    Highlight the selected columns in the DataTable.
    """
    if not selected_columns:
        return []
    return [
        {
            'if': {'column_id': i},
            'background_color': '#D2F3FF'
        } for i in selected_columns
    ]

# ============================================================
# Run the Dash application
# ============================================================
if __name__ == "__main__":
    app.run_server(debug=True)
