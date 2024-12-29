from dash.dependencies import Input, Output
from dash import html
from layouts.search_layout import search_layout
from layouts.results_layout import results_layout

def register_routing_callbacks(app):
    @app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
    def display_page(pathname):
        if pathname == '/results':
            return results_layout
        elif pathname == '/':
            return search_layout
        return html.Div(
        [
            html.H1("Page not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )
