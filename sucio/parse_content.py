import output_config.config as config
from output_config.processors.processor import Processor
from output_config.processors.web_search_processor import WebSearchProcessor
from output_config.processors.web_analysis_processor import WebAnalysisProcessor
import output_config.processors.register_modes as RegisterModes

class ParseContent:
    def __init__(self, sec_domains, gen_domains):
        RegisterModes.register_modes()
        self.sec_domains = sec_domains
        self.gen_domains = gen_domains
        self.mode_processors = Processor.get_all_modes()

    def parse_content(self, content, mode):
        if mode in self.mode_processors:
            processor_class = self.mode_processors[mode]
            processor = processor_class(self.sec_domains, self.gen_domains)
            response = processor.extract(content, None)
            result = {}

            available_attributes = response.get_attributes()

            for attribute in available_attributes:
                result[attribute] = response.get_response().get(attribute)
                    
            return result
        else:
            print("Unknown MODE")
            exit(1)
