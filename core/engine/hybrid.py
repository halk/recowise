
class HybridEngine:
    def __init__(self, name, components, settings = {}):
        self.name = name
        self.components = components
        self.settings = {} if settings is None else settings

    def get_components(self):
        return self.components

    def recommend(self, body):
        raise NotImplementedError('this method must be overridden and implemented')
