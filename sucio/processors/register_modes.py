from output_config.processors.processor import Processor
from output_config.processors.web_analysis_processor import WebAnalysisProcessor
from output_config.processors.web_search_processor import WebSearchProcessor

def register_modes():
    Processor.register_mode(WebSearchProcessor.get_mode(), WebSearchProcessor)
    Processor.register_mode(WebAnalysisProcessor.get_mode(), WebAnalysisProcessor)