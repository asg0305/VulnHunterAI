class Response:
    def __init__(self, URL=None, group=None):
        self.URL = URL
        self.group = group

    def get_response(self):
        return {
            'URL': self.URL,
            'group': self.group,
        }

    @classmethod
    def get_attributes(cls):
        return {
            'URL': None,
            'group': None
        }

    def set_attribute(self, attribute, value):
        if hasattr(self, attribute):
            setattr(self, attribute, value)
        else:
            raise AttributeError(f"{attribute} no es un atributo válido.")

    def __repr__(self):
        return f"Response(URL={self.URL}, group={self.group})"
