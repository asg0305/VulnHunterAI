class Processor:
    _modes = {}

    def __init__(self, sec_domains=None, gen_domains=None):
        self.sec_domains = sec_domains
        self.gen_domains = gen_domains

    @classmethod
    def register_mode(cls, mode, processor_class):
        cls._modes[mode] = processor_class

    @classmethod
    def get_all_modes(cls):
        return cls._modes

    @classmethod
    def get_mode(cls):
        raise NotImplementedError("Este método debe ser sobrescrito por la clase derivada")

    def extract(self, content, attribute):
        raise NotImplementedError("Este método debe ser sobrescrito por la clase derivada")
