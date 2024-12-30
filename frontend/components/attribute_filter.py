from dash import html, dcc

attribute_filter = html.Div([
    html.H3('Filtrar por Atributos', style={'margin': '0', 'textAlign': 'center', 'padding': '10px 0'}),
    dcc.Input(id='attributeSearch', type='text', placeholder='Buscar atributos...', style={'width': '100%', 'marginBottom': '10px'}),
    html.Div([
        dcc.Checklist(
            id='attributeFilter',
            options=[
                {'label': 'URL', 'value': 'url'},
                {'label': 'Source', 'value': 'source'},
                {'label': 'CVE', 'value': 'CVE'},
                {'label': 'CVE URL', 'value': 'cve_url'},
                {'label': 'CVSSv3', 'value': 'CVSSv3'},
                {'label': 'Description', 'value': 'description'},
                {'label': 'Exploit URL', 'value': 'exploit_url'},
                {'label': 'Related CVE', 'value': 'related_CVE'},
                {'label': 'Related CVE URL', 'value': 'related_cve_url'},
                {'label': 'Related CVSSv3', 'value': 'related_CVSSv3'},
                {'label': 'Related Description', 'value': 'related_description'},
                {'label': 'Related Exploit URL', 'value': 'related_exploit_url'}
            ],
            value=['url', 'source'],  # Atributos predeterminados seleccionados
            style={'display': 'flex', 'flexDirection': 'column', 'gap': '10px'}
        )
    ])
], style={'width': '80%', 'float': 'left', 'padding': '1rem', 'backgroundColor': '#f8f9fa', 'height': '100vh', 'boxSizing': 'borderBox'})
