from . import AbstractEngine

class HybridEngine(AbstractEngine):
    def __init__(self, name, taxonomy, components, settings = {}):
        super(HybridEngine, self).__init__(name, taxonomy, settings)
        self.components = components

    def get_components(self):
        return self.components

    def recommend(self, body):
        raise NotImplementedError('this method must be overridden and implemented')
