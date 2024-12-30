from dash import html, dcc

query_bar = html.Div([
    dcc.Input(id='queryInput', type='text', placeholder='Introduce tu consulta...', value='', style={'width': '60%', 'padding': '0.5rem', 'margin': '10px auto'}),
    html.Button('Buscar', id='queryButton', n_clicks=0, style={'padding': '0.5rem 1rem'}),
    html.Div(id='queryOutput')
], style={'width': '100%', 'padding': '10px 0', 'backgroundColor': '#f8f9fa', 'textAlign': 'center'})
