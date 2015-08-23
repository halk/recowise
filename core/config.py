from collections import OrderedDict
import xml.etree.ElementTree as ElementTree
from importlib import import_module
from celery import Celery
from core.taxonomy import Taxonomy

class Config(object):
    def __init__(self, file):
        self.taxonomies = {}
        self.recommenders = {}
        self.events = {}
        self.settings = {}
        self.celery = None

        self.tree = ElementTree.parse(file)
        self.root = self.tree.getroot()

        self.parse_global_settings()
        self.parse_taxonomies()
        self.parse_recommenders()
        self.parse_hybrid_recommenders()

    def parse_global_settings(self):
        self.settings = self.parse_settings(self.root.findall('./settings/*'))

    def get_celery(self, name):
        if self.celery != None:
            return self.celery

        # setting up celery
        self.celery = Celery(
            name,
            broker=self.settings['celery']['broker'],
            backend=self.settings['celery']['backend']
        )

        return self.celery

    def get_taxonomies(self):
        return self.taxonomies

    def get_recommenders(self):
        return self.recommenders

    def get_events(self):
        return self.events

    def parse_taxonomies(self):
        # load elements into a dict so that they can be looked up
        taxonomies = {}
        for taxonomy in self.root.findall('./taxonomies/taxonomy'):
            taxonomies[taxonomy.get('name')] = taxonomy

        # process them
        for name in taxonomies.iterkeys():
            self.parse_taxonomy(name, taxonomies)

    def parse_taxonomy(self, name, taxonomies):
        taxonomyEl = taxonomies[name]

        # check if taxonomy is already processed
        if name in self.taxonomies:
            return self.taxonomies[name]

        # create taxonomy object
        self.taxonomies[name] = Taxonomy(name, self.parse_taxons(taxonomyEl))

        # check inheritance
        if taxonomyEl.get('inherit'):
            parent_taxonomy = self.parse_taxonomy(taxonomyEl.get('inherit'), taxonomies)
            self.taxonomies[name].inherit(parent_taxonomy)

        return self.taxonomies[name]

    def parse_taxons(self, taxonomyEl):
        taxons = {}
        for taxon in taxonomyEl.iterfind('taxon'):
            taxons[taxon.get('name')] = taxon.text

        return taxons

    def parse_recommenders(self):
        for recommenderEl in self.root.findall('./recommenders/recommender'):
            # get taxonomy (per recommender)
            taxonomy = self.parse_taxonomy_for_recommender(recommenderEl)

            # get settings for engine
            engine = recommenderEl.get('engine')
            settings = self.parse_settings(
                self.root.findall('./engines/engine[@name="%s"]/settings/*' % engine)
            )

            # load engine adapter
            engine = '' if engine == 'base' else '.' + engine
            adapter = import_module('engines%s' % engine)

            # create engine adapter object
            name = recommenderEl.get('name')
            self.recommenders[name] = adapter.Engine(name, taxonomy, settings)
            self.parse_events(recommenderEl, self.recommenders[name])

    def parse_hybrid_recommenders(self):
        for hybridRecommenderEl in self.root.findall('./recommenders/hybrid_recommender'):
            # get components
            components = OrderedDict()
            for componentEl in hybridRecommenderEl.findall('./components/component'):
                components[componentEl.get('name')] = self.recommenders[componentEl.get('recommender')]

            # get taxonomy
            taxonomy = self.parse_taxonomy_for_recommender(hybridRecommenderEl)

            # get settings
            settings = self.parse_settings(hybridRecommenderEl.findall('./settings/*'))

            # load hybrid engine class
            engine = hybridRecommenderEl.get('engine')
            engine = '' if engine == 'base' else '.' + engine
            adapter = import_module('engines.hybrid%s' % engine)

            # create engine object
            name = hybridRecommenderEl.get('name')
            self.recommenders[name] = adapter.HybridEngine(
                name, taxonomy, components, settings
            )

    def parse_taxonomy_for_recommender(self, recommenderEl):
        taxonomyEl = recommenderEl.find('taxonomy')
        taxonomy = Taxonomy(taxonomyEl.get('name'), self.parse_taxons(taxonomyEl))
        if taxonomyEl.get('inherit'):
            taxonomy.inherit(self.taxonomies[taxonomyEl.get('inherit')])

        return taxonomy

    def parse_events(self, recommenderEl, recommender):
        for eventEl in recommenderEl.findall('./on'):
            eventName = eventEl.get('event')
            if eventName not in self.events:
                self.events[eventName] = []

            self.events[eventName].append(
                {'recommender': recommender, 'action': eventEl.get('do')}
            )

    def parse_settings(self, elements):
        settings = {}
        for setting in elements:
            if setting.getchildren() == []:
                settings[setting.tag] = setting.text
            else:
                settings[setting.tag] = self.parse_settings(setting.getchildren())

        return settings
