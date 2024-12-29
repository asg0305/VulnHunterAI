from dash.dependencies import Input, Output, State
import requests
from dash import html
from components.table_columns import table_columns
from components.table_rows import table_rows

def register_results_callbacks(app):
    # Callback para actualizar la tabla basada en los filtros seleccionados
    @app.callback(
        Output('results-container', 'children'),
        [Input('attribute-filter', 'value')]
    )
    def update_table(selected_attributes):
        # Simulación de datos filtrados, normalmente vendrían del backend
        data = [
            {"url": "http://example.com", "source": "source1", "CVE": "CVE-2021-1234", "cve_url": "http://example.com/cve", "CVSSv3": "7.5", "Description": "Description1", "exploit": "exploit1", "exploit_url": "http://example.com/exploit"},
            {"url": "http://example.org", "source": "source2", "CVE": "CVE-2021-5678", "cve_url": "http://example.org/cve", "CVSSv3": "8.0", "Description": "Description2", "exploit": "exploit2", "exploit_url": "http://example.org/exploit"}
        ]

        return html.Table(
            [table_columns(selected_attributes), table_rows(data, selected_attributes)],
            style={'width': '100%', 'border': '1px solid black', 'borderCollapse': 'collapse'}
        )

    # Callback para manejar las consultas directas a la base de datos
    @app.callback(
        Output('query-output', 'children'),
        [Input('query-button', 'n_clicks')],
        [State('query-input', 'value')]
    )
    def handle_query(n_clicks, query):
        if n_clicks > 0:
            # Realizar la solicitud al backend
            response = requests.get('http://application:5000/query_database', params={'query': query})
            results = response.json()

            # Simulación de presentación de resultados (normalmente se formatearían adecuadamente)
            return html.Div([
                html.H5('Resultados de la Consulta:'),
                html.Pre(str(results))
            ])

        return ''
