import dash_cytoscape as cyto

cytoscape_graph = cyto.Cytoscape(
    id="cytoscape-graph",
    layout={"name": "breadthfirst"},
    style={"width": "100%", "height": "600px"},
    elements=[]
)
