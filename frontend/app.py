import dash
from dash import html, dcc
from callbacks.callbacks import register_callbacks
from callbacks.routing import register_routing_callbacks
from layouts.search_layout import search_layout

app = dash.Dash(__name__, suppress_callback_exceptions=True)

content = html.Div(id="page-content")
app.layout = html.Div([dcc.Location(id="url"), content])

# Registrar callbacks
register_callbacks(app)
register_routing_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True, host="0.0.0.0", port=8050)
