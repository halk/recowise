
class Taxonomy(object):
    def __init__(self, name, taxons={}):
        self.name = name
        self.taxons = taxons

    def inherit(self, parentTaxonomy):
        for name, value in parentTaxonomy.get_taxons().iteritems():
            if name in self.taxons:
                continue
            self.taxons[name] = value

    def get_name(self):
        return self.name

    def get_taxons(self):
        return self.taxons

    def get(self, name):
        if name in self.taxons:
            return self.taxons[name]
        return None

    def translate(self, values):
        data = {}
        for key, translatedKey in self.taxons.iteritems():
            # translating the key
            if translatedKey in values:
                data[key] = values[translatedKey]
            # take static value from config
            else:
                data[key] = translatedKey

        return data
