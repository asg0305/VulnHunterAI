from dash import dcc, html

def loading_indicator():
    return dcc.Loading(
        id="loading-indicator",
        children=[
            html.Div(id="result-message", style={"padding": "10px", "color": "green"})
        ],
        type="circle"
    )
