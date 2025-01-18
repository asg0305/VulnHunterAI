from .update_results import register_results_callbacks
from .update_search import register_search_callbacks
from .filter_attributes_callback import register_filter_callback

def register_callbacks(app):
    register_search_callbacks(app)
    register_results_callbacks(app)
    register_filter_callback(app)
