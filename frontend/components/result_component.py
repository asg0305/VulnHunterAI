@app.callback(
    Output('data-table-container', 'children'),
    [Input('attribute-filter', 'value')]
)
def update_table(selected_attributes):
    # Simulación de datos filtrados, normalmente vendrían del backend
    data = [
        {"url": "http://example.com", "source": "source1", "CVE": "CVE-2021-1234", "cve_url": "http://example.com/cve", "CVSSv3": "7.5", "Description": "Description1", "exploit": "exploit1", "exploit_url": "http://example.com/exploit"},
        {"url": "http://example.org", "source": "source2", "CVE": "CVE-2021-5678", "cve_url": "http://example.org/cve", "CVSSv3": "8.0", "Description": "Description2", "exploit": "exploit2", "exploit_url": "http://example.org/exploit"}
    ]

    table_header = [html.Th(attr) for attr in selected_attributes]
    table_rows = [
        html.Tr([html.Td(row[attr]) for attr in selected_attributes])
        for row in data
    ]

    return html.Table(
        [html.Tr(table_header)] + table_rows,
        style={'width': '100%', 'border': '1px solid black', 'borderCollapse': 'collapse'}
    )

# Añadir la barra horizontal superior debajo de la tabla
app.layout.children.append(html.Div([
    dcc.Input(id='query-input', type='text', placeholder='Introduce tu consulta...'),
    html.Button('Buscar', id='query-button', n_clicks=0),
    html.Div(id='query-output')
], style={'width': '100%', 'textAlign': 'center', 'margin-top': '20px'}))

# Callback para manejar las consultas a la base de datos (to be added)
