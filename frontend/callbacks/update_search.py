from dash.dependencies import Input, Output, State
import requests
from dash import dcc, html

def register_search_callback(app):
    @app.callback(
        [Output("result-message", "children"),
         Output("result-message", "style")],
        # Output("hidden_layout_for_redirect", "children")],
        [Input("search_button", "n_clicks")],
        [State("alias_input", "value"),
         State("service_input", "value"),
         State("version_input", "value")]
    )
    def update_search(n_clicks, alias, service, version):
        if n_clicks > 0:
            try:
                response = requests.post("http://application:5000/execute_search", json={'alias': alias, 'service': service, 'version': version})
                response.raise_for_status()
                if response.status_code == 200:
                    #result_layout = dcc.Location(pathname="/results", id="result-redirect")
                    message = "Petición enviada correctamente"
                    style = {"color": "green"}
                    return message, style
                else:
                    message = "Error en la solicitud"
                    style = {"color": "red"}
                    return message, style
            except requests.exceptions.RequestException as e:
                message = f"Error: {str(e)}"
                style = {"color": "red"}
                return message, style
        return "", {"color": "green"}
