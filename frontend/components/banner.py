from dash import html

banner = html.Div([
    html.Span('VulnhunterAI', style={'float': 'left', 'padding': '10px', 'fontWeight': 'bold'}),
    html.Span('☰', style={'float': 'right', 'padding': '10px', 'fontSize': '20px'}),
], style={'width': '100%', 'backgroundColor': '#f8f9fa', 'borderBottom': '1px solid #ddd', 'boxSizing': 'border-box', 'height': '3rem', 'lineHeight': '3rem'})
