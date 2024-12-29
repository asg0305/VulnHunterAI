from output_config.responses.response import Response

class SearchResponse(Response):
    def __init__(self, URL=None, group=None, CVE=False, Exploit=False, CVSS3_v3=None, related_URL=None, related_CVE=None, superior_version=None):
        super().__init__(URL, group)
        self.CVE = CVE
        self.Exploit = Exploit
        self.CVSS3_v3 = CVSS3_v3
        self.related_URL = related_URL
        self.related_CVE = related_CVE
        self.superior_version = superior_version

    def get_response(self):
        # Llama al método get_response de la clase base y añade los atributos específicos
        response = super().get_response()
        response.update({
            'CVE': self.CVE,
            'Exploit': self.Exploit,
            'CVSS3_v3': self.CVSS3_v3,
            'related_URL': self.related_URL,
            'related_CVE': self.related_CVE,
            'superior_version': self.superior_version,
        })
        return response

    @classmethod
    def get_attributes(cls):
        # Llama al método get_attributes de la clase base y añade los atributos específicos
        attributes = super().get_attributes()
        attributes.update({
            'CVE': False,
            'Exploit': False,
            'CVSS3_v3': None,
            'related_URL': None,
            'related_CVE': None,
            'superior_version': None
        })
        return attributes

    def set_attribute(self, attribute, value):
        if hasattr(self, attribute):
            setattr(self, attribute, value)
        else:
            raise AttributeError(f"{attribute} no es un atributo válido.")

    def __repr__(self):
        return (
            f"SearchResponse(URL={self.URL}, group={self.group}, "
            f"CVE={self.CVE}, Exploit={self.Exploit}, CVSS3_v3={self.CVSS3_v3}, "
            f"related_URL={self.related_URL}, related_CVE={self.related_CVE}, superior_version={self.superior_version})"
        )
