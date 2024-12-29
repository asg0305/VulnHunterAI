from dash import html

def table_columns(selected_attributes):
    return html.Thead(html.Tr([html.Th(attr, style={'border': '1px solid #ddd'}) for attr in selected_attributes]))
