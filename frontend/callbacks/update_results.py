from dash.dependencies import Input, Output, State
import requests
from dash import html
import data.attribute_config as config
import dash

def parse_query(query):
    parts = query.split(' and ')
    filters = [part.replace("=", ":").replace("'", "") for part in parts]
    return ", ".join(filters)

def filter_existing_data(data, filters):
    filtered_data = []
    for record in data:
        match = True
        for key, value in filters.items():
            print(record.get(key, ''))
            if value not in record.get(key, ''):  # Check if the value is contained in the attribute
                match = False
                break
        if match:
            filtered_data.append(record)
    return filtered_data

def register_results_callbacks(app):
    @app.callback(
        Output('results-container', 'children'),
        [Input('attributeFilter', 'value'), Input('queryButton', 'n_clicks')],
        [State('queryInput', 'value'), State('results-container', 'children')]
    )
    def update_table(selected_attributes, n_clicks, query, existing_data):
        ctx = dash.callback_context
        if ctx.triggered:
            trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

            if trigger_id == 'attributeFilter':

                requested_attributes = (', ').join(selected_attributes)

                response = requests.get(f'http://application:5000/get_results?attributes={requested_attributes}')
                data = response.json()
                print(f"RECEIVED: {data}")
                if data is None:
                    response = requests.get(f'http://application:5000/get_results?attributes={requested_attributes}')
                    data = response.json()
                table_header = [html.Th(attr, style={'border': '1px solid #ddd'}) for attr in selected_attributes]
                table_rows = [
                    html.Tr([html.Td(record.get(attr, ""), style={'border': '1px solid #ddd', 'paddingLeft': '10px'}) for attr in selected_attributes])
                    for record in data
                ]
                return html.Table(
                    [html.Thead(html.Tr(table_header)), html.Tbody(table_rows)],
                    style={'width': '100%', 'border': '1px solid black', 'borderCollapse': 'collapse'}
                )

            elif trigger_id == 'queryButton' and n_clicks > 0 and query:
                requested_attributes = (', ').join(selected_attributes)
                filters = parse_query(query)
                response = requests.get(f'http://application:5000/fetch_results?attributes={requested_attributes}&filters={filters}')
                data = response.json()
                if data is None:
                    response = requests.get(f'http://application:5000/get_results?attributes={requested_attributes}')
                    data = response.json()
                table_header = [html.Th(attr, style={'border': '1px solid #ddd'}) for attr in selected_attributes]
                table_rows = [
                    html.Tr([html.Td(record.get(attr, ""), style={'border': '1px solid #ddd', 'paddingLeft': '10px'}) for attr in selected_attributes])
                    for record in data
                ]
                return html.Table(
                    [html.Thead(html.Tr(table_header)), html.Tbody(table_rows)],
                    style={'width': '100%', 'border': '1px solid black', 'borderCollapse': 'collapse'}
                )

        return ''
