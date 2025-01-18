from dash import html

results_table = html.Div(
    id='results-container',
    style={
        'width': '100%', 
        'border': '1px solid black', 
        'borderCollapse': 'collapse',
        'display': 'grid', 
        'gridTemplateColumns': 'auto', 
        'gridAutoRows': 'minmax(20px, auto)'  # Ajustar la altura mínima de las filas
    }
)
