import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import dash.exceptions
import base64
import io
import dash_bootstrap_components as dbc  # Import dash-bootstrap-components

# Initialize the Dash app with the JOURNAL theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.JOURNAL])

server = app.server

# Define the layout of the app
app.layout = dbc.Container([  # Wrap your layout in a Container from dash-bootstrap-components
    html.H1('Automatic Data Analysis', style={'textAlign': 'center'}),
    
    # Header
    dbc.Row([
        dbc.Col([
            html.H3('Graph Type', style={'margin-bottom': '10px'}),
            dcc.Dropdown(
                id='graph-type-dropdown',
                options=[
                    {'label': 'Scatter Plot', 'value': 'scatter'},
                    {'label': 'Bar Chart', 'value': 'bar'},
                    {'label': 'Line Chart', 'value': 'line'},
                    {'label': 'Histogram', 'value': 'histogram'},
                    {'label': 'Bubble Chart', 'value': 'bubble'},
                    {'label': 'Pie Chart', 'value': 'pie'},
                    {'label': 'Box Plot', 'value': 'box'},
                    {'label': 'Heatmap', 'value': 'heatmap'},
                    {'label': 'Sunburst Plot', 'value': 'sunburst'},
                ],
                value='scatter'  # Default graph type
            ),
        ], width=3),
    ], style={'margin-bottom': '20px'}),
    
    dbc.Row([
        dbc.Col([
            html.Label('Select X-axis:'),
            dcc.Dropdown(
                id='x-axis-dropdown',
                value=None
            ),
        ], width=4),
        dbc.Col([
            html.Label('Select Y-axis:'),
            dcc.Dropdown(
                id='y-axis-dropdown',
                value=None
            ),
        ], width=4),
    ], style={'margin-bottom': '20px'}),
    
    dbc.Row([
        dbc.Col([
            dcc.Upload(
                id='upload-data',
                children=html.Button('Upload CSV File'),
                multiple=False
            ),
        ], width=4),
    ], style={'margin-bottom': '20px'}),
    
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='visualization')
        ], width=12),
    ], style={'height': '60%'}),
])

# Define callback to update the dropdown options for X and Y axes
@app.callback(
    Output('x-axis-dropdown', 'options'),
    Output('y-axis-dropdown', 'options'),
    Input('upload-data', 'contents')
)
def update_dropdown_options(uploaded_data):
    if uploaded_data is None:
        return [], []
    
    uploaded_df = parse_data(uploaded_data)
    # Create dropdown options from columns in the CSV
    options = [{'label': col, 'value': col} for col in uploaded_df.columns]
    return options, options

# Define callback to update the visualization
@app.callback(
    Output('visualization', 'figure'),
    Input('x-axis-dropdown', 'value'),
    Input('y-axis-dropdown', 'value'),
    Input('upload-data', 'contents'),
    Input('graph-type-dropdown', 'value')
)
def update_graph(selected_x, selected_y, uploaded_data, graph_type):
    if uploaded_data is None or not selected_x or not selected_y:
        return {}
    
    uploaded_df = df = parse_data(uploaded_data)
    
    if graph_type == 'scatter':
        fig = px.scatter(uploaded_df, x=selected_x, y=selected_y, title='Scatter Plot')
    elif graph_type == 'bar':
        fig = px.bar(uploaded_df, x=selected_x, y=selected_y, title='Bar Chart')
    elif graph_type == 'line':
        fig = px.line(uploaded_df, x=selected_x, y=selected_y, title='Line Chart')
    elif graph_type == 'histogram':
        fig = px.histogram(uploaded_df, x=selected_x, y=selected_y, title='Histogram')
    elif graph_type == 'bubble':
        fig = px.scatter(uploaded_df, x=selected_x, y=selected_y, size=selected_y, title='Bubble Chart')
    elif graph_type == 'pie':
        fig = px.pie(uploaded_df, names=selected_x, values=selected_y, title='Pie Chart')
    elif graph_type == 'box':
        fig = px.box(uploaded_df, x=selected_x, y=selected_y, title='Box Plot')
    elif graph_type == 'heatmap':
        fig = px.imshow(uploaded_df, x=uploaded_df.columns, y=uploaded_df.index, title='Heatmap')
    elif graph_type == 'sunburst':
        fig = px.sunburst(uploaded_df, path=[selected_x, selected_y], title='Sunburst Plot')
    else:
        fig = {}
    fig.update_layout(
        height=700,
        paper_bgcolor="LightSteelBlue",
    )
    fig.update_xaxes(tickangle=45)
    tickfont = dict(size=16)
    return fig

# parses the dataset
def parse_data(contents):
    content_type, content_string = contents.split(",")

    decoded = base64.b64decode(content_string)
    try:
        df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
    except Exception as e:
        print(e)
        return html.Div(["There was an error processing this file."])

    return df

if __name__ == '__main__':
    app.run_server(debug=True)


