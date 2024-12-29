from dash.dependencies import Input, Output
import dash

def register_filter_callback(app):
    @app.callback(
        Output('attribute-filter', 'options'),
        [Input('attribute-search', 'value')]
    )
    def filter_attributes(search_value):
        all_options = [
            {'label': 'URL', 'value': 'url'},
            {'label': 'Source', 'value': 'source'},
            {'label': 'CVE', 'value': 'CVE'},
            {'label': 'CVE URL', 'value': 'cve_url'},
            {'label': 'CVSSv3', 'value': 'CVSSv3'},
            {'label': 'Description', 'value': 'Description'},
            {'label': 'Exploit', 'value': 'exploit'},
            {'label': 'Exploit URL', 'value': 'exploit_url'}
        ]
        if search_value:
            return [option for option in all_options if search_value.lower() in option['label'].lower()]
        return all_options
