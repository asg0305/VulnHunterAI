from dash.dependencies import Input, Output, State
import requests
from dash import dcc, html
import dash

def register_search_callbacks(app):
    @app.callback(
        [Output("result-message", "children"),
         Output("result-message", "style"),
         Output("url", "pathname")],  # Añadir salida para cambiar la URL
        [Input("search_button", "n_clicks")],
        [State("alias_input", "value"),
         State("service_input", "value"),
         State("version_input", "value")]
    )
    def update_search(n_clicks, alias, service, version):
        if n_clicks > 0:
            try:
                response = requests.post("http://application:5000/execute_search_sync", json={'alias': alias, 'service': service, 'version': version})
                response.raise_for_status()
                if response.status_code == 200:
                    message = "Petición enviada correctamente"
                    style = {"color": "green"}
                    # Redireccionar a la página de resultados
                    return message, style, "/results"
                else:
                    message = "Error en la solicitud"
                    style = {"color": "red"}
                    return message, style, dash.no_update
            except requests.exceptions.RequestException as e:
                message = f"Error: {str(e)}"
                style = {"color": "red"}
                return message, style, dash.no_update
        return "", {"color": "green"}, dash.no_update
