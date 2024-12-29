from dash import html
from components.result_component import result_component

def results_container(results):
    # Crear filas de resultados usando result_component
    result_rows = [result_component(result['url'], result['search_group'], result['extractable_info']) for result in results]

    return html.Div(result_rows, className="results-container")
