from dash import html

def table_rows(data, selected_attributes):
    rows = []
    for row in data:
        rows.append(html.Tr([html.Td(row[attr], style={'border': '1px solid #ddd', 'paddingLeft': '10px'}) for attr in selected_attributes]))
    return html.Tbody(rows)
