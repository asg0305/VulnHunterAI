from dash import html
from components.attribute_filter import attribute_filter
from components.results_table import results_table
from components.query_bar import query_bar
from components.banner import banner

results_layout = html.Div([
    html.Div(banner, style={'width': '100%', 'position': 'fixed', 'top': 0, 'left': 0, 'zIndex': 1, 'backgroundColor': '#f8f9fa', 'textAlign': 'center'}),
    html.Div(query_bar, style={'width': '100%', 'position': 'fixed', 'top': '3rem', 'left': 0, 'zIndex': 1, 'backgroundColor': '#f8f9fa', 'textAlign': 'center'}),
    html.Div(attribute_filter, style={'width': '20%', 'float': 'left', 'paddingTop': '0.5rem', 'backgroundColor': '#f8f9fa', 'height': 'calc(100vh - 9rem)', 'boxSizing': 'borderBox'}),
    html.Div(results_table, style={'marginTop': '8rem', 'marginLeft': '20%', 'padding': '2rem', 'height': 'calc(100vh - 9rem)', 'overflowY': 'auto'})
])
