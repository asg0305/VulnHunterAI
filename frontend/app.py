import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import requests
import dash_cytoscape as cyto

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Buscador de Servicios y Sistemas Operativos"),

    html.Div([
        html.Label("Search Alias"),
        dcc.Input(id="alias_input", type="text", placeholder="Introducir alias"),
    ], style={"padding": "10px"}),

    html.Div([
        html.Label("Servicio o Sistema Operativo"),
        dcc.Input(id="service_input", type="text", placeholder="Introducir servicio/SO"),
    ], style={"padding": "10px"}),

    html.Div([
        html.Label("Versión"),
        dcc.Input(id="version_input", type="text", placeholder="Introducir versión"),
    ], style={"padding": "10px"}),

    

    html.Button("Buscar", id="search_button", n_clicks=0),

    dcc.Loading(
        id="loading",
        children=[
            cyto.Cytoscape(
                id="cytoscape-graph",
                layout={"name": "breadthfirst"},
                style={"width": "100%", "height": "600px"},
                elements=[]
            )
        ],
        type="circle",
    )
])

@app.callback(
    Output("cytoscape-graph", "elements"),
    [Input("search_button", "n_clicks")],
    [Input("alias_input", "value"),
     Input("service_input", "value"),
     Input("version_input", "value")]
)
def update_graph(n_clicks, service, version, alias):
    if n_clicks > 0:
        # Llamada al backend para obtener datos del grafo
        try:
            response = requests.get(f"http://localhost:5000/graph?service={service}&version={version}&alias={alias}")
            data = response.json()

            elements = []
            for node in data["nodes"]:
                elements.append({
                    "data": {"id": node["id"], "label": node["id"]}
                })
            for edge in data["links"]:
                elements.append({
                    "data": {"source": edge["source"], "target": edge["target"]}
                })

            return elements
        except Exception as e:
            print(f"Error fetching graph data: {e}")
            return []
    return []

if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8050)
