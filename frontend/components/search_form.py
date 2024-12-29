from dash import html, dcc
from components.search_form import search_form

search_layout = html.Div([
    search_form,
    dcc.Store(id='alias-store', storage_type='memory')
])
