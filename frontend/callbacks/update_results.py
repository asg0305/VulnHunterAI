from dash.dependencies import Input, Output, State
import requests
from dash import html
import data.attribute_config as config
import dash

def parse_query(query):
    filters = {}
    parts = query.split(' and ')
    for part in parts:
        key, value = part.split('=')
        filters[key.strip()] = value.strip().strip("'")
    return filters

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

        if not selected_attributes:
            selected_attributes = ['url', 'source']

        if ctx.triggered:
            trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

            if trigger_id == 'attributeFilter':
                if any(attr in selected_attributes for attr in config.RELATED_CVE_EXPLOIT):
                    query_type = 'related_CVE_exploit'
                elif any(attr in selected_attributes for attr in config.RELATED_CVE):
                    query_type = 'related_CVE'
                elif any(attr in selected_attributes for attr in config.EXPLOIT):
                    query_type = 'exploit'
                elif any(attr in selected_attributes for attr in config.CVE):
                    query_type = 'CVE'
                else:
                    query_type = 'default'

                response = requests.get(f'http://application:5000/get_results?query_type={query_type}')
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
                filters = parse_query(query)
                attributes_in_filters = set(filters.keys())
                if any(attr in selected_attributes for attr in config.RELATED_CVE_EXPLOIT):
                    query_type = 'related_CVE_exploit'
                elif any(attr in selected_attributes for attr in config.RELATED_CVE):
                    query_type = 'related_CVE'
                elif any(attr in selected_attributes for attr in config.EXPLOIT):
                    query_type = 'exploit'
                elif any(attr in selected_attributes for attr in config.CVE):
                    query_type = 'CVE'
                else:
                    query_type = 'default'

                try:
                    existing_attributes = {header.children for header in existing_data[0]['props']['children'][0]['props']['children']}
                except (IndexError, KeyError, TypeError):
                    existing_attributes = set()

                if attributes_in_filters.issubset(existing_attributes):
                    # Filtrar los datos existentes
                    existing_data_list = [
                        {existing_data[0]['props']['children'][0]['props']['children'][i]['props']['children']: cell['props']['children'] for i, cell in enumerate(row['props']['children'])}
                        for row in existing_data[1]['props']['children']
                    ]
                    filtered_data = filter_existing_data(existing_data_list, filters)
                    data = filtered_data
                else:
                    # Realizar la solicitud al backend
                    attribute = list(filters.keys())[0] 
                    filter_value = list(filters.values())[0] 
                    params = {'query_type': query_type, 'attribute': attribute, 'filter': filter_value} 
                    response = requests.get('http://application:5000/fetch_results', params=params) 
                    data = response.json()

                table_header = [html.Th(attr, style={'border': '1px solid #ddd'}) for attr in filters.keys()]
                table_rows = [
                    html.Tr([html.Td(record.get(attr, ""), style={'border': '1px solid #ddd', 'paddingLeft': '10px'}) for attr in filters.keys()])
                    for record in data
                ]
                return html.Table(
                    [html.Thead(html.Tr(table_header)), html.Tbody(table_rows)],
                    style={'width': '100%', 'border': '1px solid black', 'borderCollapse': 'collapse'}
                )

        return ''
