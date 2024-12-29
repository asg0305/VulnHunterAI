@app.callback(
    Output('query-output', 'children'),
    [Input('query-button', 'n_clicks')],
    [State('query-input', 'value')]
)
def handle_query(n_clicks, query):
    if n_clicks > 0:
        # Realizar la solicitud al backend
        response = requests.get('http://application:5000/query_database', params={'query': query})
        results = response.json()

        # Simulación de presentación de resultados (normalmente se formatearían adecuadamente)
        return html.Div([
            html.H5('Resultados de la Consulta:'),
            html.Pre(str(results))
        ])

    return ''

if __name__ == '__main__':
    app.run_server(debug=True)
