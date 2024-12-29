from output_config.processors.processor import Processor
from output_config.responses.search_response import SearchResponse

class WebAnalysisProcessor(Processor):
    @classmethod
    def get_mode(cls):
        return "WebAnalysis"

    def __init__(self, sec_domains=None, gen_domains=None):
        super().__init__(sec_domains, gen_domains)

    def extract(self, content, attribute):
        # Implementa la lógica de extracción específica para WebAnalysis
        URL = "http://example-analysis.com"
        CVE = "CVE-2023-5678"
        Exploit = False
        CVSS3_v3 = 7.5
        related_URL = "http://example-analysis.com/details"
        related_CVE = ["CVE-2022-3333", "CVE-2021-4444"]
        superior_version = "2.3.4"

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
