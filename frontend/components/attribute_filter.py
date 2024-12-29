from dash import html, dcc

attribute_filter = html.Div([
    html.H3('Filtrar por Atributos', style={'margin': '0', 'textAlign': 'center', 'padding': '10px 0'}),
    dcc.Input(id='attribute-search', type='text', placeholder='Buscar atributos...', style={'width': '100%', 'marginBottom': '10px'}),
    html.Div([
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
            value=['url'],  # Atributos predeterminados seleccionados
            style={'display': 'flex', 'flexDirection': 'column', 'gap': '10px'}
        )
    ])
], style={'width': '80%', 'float': 'left', 'padding': '1rem', 'backgroundColor': '#f8f9fa', 'height': '100vh', 'boxSizing': 'borderBox'})
