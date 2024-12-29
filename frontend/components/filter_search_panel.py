import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.H3('Filtrar por Atributos'),
        dcc.Checklist(
            id='attribute-filter',
            options=[
                {'label': 'URL', 'value': 'url'},
                {'label': 'Source', 'value': 'source'},
                {'label': 'CVE', 'value': 'CVE'},
                {'label': 'CVE URL', 'value': 'cve_url'},
                {'label': 'CVSSv3', 'value': 'CVSSv3'},
                {'label': 'Description', 'value': 'Description'},
                {'label': 'Exploit', 'value': 'exploit'},
                {'label': 'Exploit URL', 'value': 'exploit_url'}
            ],
            value=['url']  # Atributos predeterminados seleccionados
        )
    ], style={'width': '20%', 'display': 'inline-block', 'vertical-align': 'top'}),
    
    # Placeholder for the table and top bar, these will be added below
    html.Div(id='data-table-container', style={'width': '75%', 'display': 'inline-block'})
])

# Callback to update the table based on selected attributes (to be added)
