from dash import html, dcc
#import dash
import dash_cytoscape as cyto

search_layout = html.Div([
    html.H1(
        "VulnHunterAI",
        style={
            "textAlign": "center"
        }
    ),
    html.Div([
        html.Div([
            html.Label("Search Alias"),
            dcc.Input(id="alias_input", type="text", placeholder="Introducir alias", value=""),
        ], style={"padding": "10px", "textAlign": "center"}),
        html.Div([
            html.Div([
                html.Label("Servicio o Sistema Operativo"),
                dcc.Input(id="service_input", type="text", placeholder="Introducir servicio/SO", value=""),
            ], style={"padding": "10px", "float": "left", "width": "45%"}),
            html.Div([
                html.Label("Versión"),
                dcc.Input(id="version_input", type="text", placeholder="Introducir versión", value=""),
            ], style={"padding": "10px", "float": "right", "width": "45%"})
        ], style={"display": "flex", "justifyContent": "space-between"}),
        html.Div([
            html.Button("Buscar", id="search_button", n_clicks=0),
        ], style={"padding": "10px", "textAlign": "center"}),
    ], style={
        "margin": "0 auto",
        "width": "50%",
        "border": "2px solid #ccc",
        "padding": "20px",
        "borderRadius": "10px"
    }),
    dcc.Loading(
        id="loading-indicator",
        children=[
            cyto.Cytoscape(
                id="cytoscape-graph",
                layout={"name": "breadthfirst"},
                style={"width": "100%", "height": "600px"},
                elements=[]
            )
        ],
        type="circle",
    ),
    html.Div(id="result-message", style={"padding": "10px", "color": "green"}),
    dcc.Store(id='alias-store', storage_type='memory')
], style={"textAlign": "center"})
