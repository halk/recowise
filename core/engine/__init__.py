
class AbstractEngine(object):

    def __init__(self, name, taxonomy, settings={}):
        self.name = name
        self.taxonomy = taxonomy

        self.settings = {} if settings is None else settings

    def translate(self, body):
        return self.taxonomy.translate(body)
