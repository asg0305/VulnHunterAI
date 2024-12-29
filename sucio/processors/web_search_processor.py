from output_config.processors.processor import Processor
from output_config.responses.search_response import SearchResponse

class WebSearchProcessor(Processor):
    @classmethod
    def get_mode(cls):
        return "WebSearch"

    def __init__(self, sec_domains=None, gen_domains=None):
        super().__init__(sec_domains, gen_domains)
        self.response = SearchResponse()
        self.atributes_values = self.response.get_attributes()
        self.atributes = 

    def extract(self, content):
        for url in content:
            for sec_domain in self.sec_domains:
                if sec_domain in url:
                    self.atributes_values['group'] = "secure_src"
                else:
                    for gen_domain in self.gen_domains:
                        if gen_domain in url:
                            self.atributes_values['group'] = "general_src"
                        else:
                            self.atributes_values['group'] = "unknown_src"
            self.atributes_values['URL'] = url
            

        # Crea una instancia de SearchResponse con los datos extraídos
        response = SearchResponse(
            URL=URL,
            CVE=CVE,
            Exploit=Exploit,
            CVSS3_v3=CVSS3_v3,
            related_URL=related_URL,
            related_CVE=related_CVE,
            superior_version=superior_version
        )

        return response
