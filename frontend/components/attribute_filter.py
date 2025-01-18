from dash import html, dcc

attribute_filter = html.Div([
    html.H3('Filtrar por Atributos', style={'margin': '0', 'textAlign': 'center', 'padding': '10px 0'}),
    dcc.Input(id='attributeSearch', type='text', value='', placeholder='Buscar atributos...', style={'width': '100%', 'marginBottom': '10px'}),
    html.Div([
        dcc.Checklist(
            id='attributeFilter',
            options=[
                {'label': 'Project Alias', 'value': 'Project.alias'},
                {'label': 'Project Num Sources', 'value': 'Project.source_num'},
                {'label': 'Project Num CVE', 'value': 'Project.cve_num'},
                {'label': 'Project Num Exploits', 'value': 'Project.exploit_num'},
                {'label': 'SrvOS', 'value': 'SrvOS.srv_os'},
                {'label': 'SrvOS Num Sources', 'value': 'SrvOS.source_num'},
                {'label': 'SrvOS Num CVE', 'value': 'SrvOS.cve_num'},
                {'label': 'SrvOS Num Exploits', 'value': 'SrvOS.exploit_num'},
                {'label': 'Version', 'value': 'Version.version'},
                {'label': 'Version Num Sources', 'value': 'Version.source_num'},
                {'label': 'Version Num CVE', 'value': 'Version.cve_num'},
                {'label': 'Version Num Exploits', 'value': 'Version.exploit_num'},
                {'label': 'URL', 'value': 'URL.url'},
                {'label': 'Source', 'value': 'URL.source'},
                {'label': 'URL Num CVE', 'value': 'URL.num_cve'},
                {'label': 'URL Num Exploits', 'value': 'URL.num_exploits'},
                {'label': 'CVE URL', 'value': 'CVE.url'},
                {'label': 'CVE', 'value': 'CVE.CVE'},
                {'label': 'CVSSv3', 'value': 'CVE.CVSSv3'},
                {'label': 'Description', 'value': 'CVE.description'},
                {'label': 'CVE Num Exploits', 'value': 'CVE.num_exploits'},
                {'label': 'Exploit URL', 'value': 'Exploit.url'}
            ],
            value=[],
            style={'display': 'flex', 'flexDirection': 'column', 'gap': '10px'}
        )
    ])
], style={'width': '80%', 'float': 'left', 'padding': '1rem', 'backgroundColor': '#f8f9fa', 'height': '100vh', 'boxSizing': 'borderBox'})
