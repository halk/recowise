import os
import unittest
from core.config import Config

class ConfigTestCase(unittest.TestCase):
    def setUp(self):
        self.config = Config(os.path.join(os.path.dirname(__file__), '..', 'config', 'config.xml'))

    def test_global_settings(self):
        self.assertEqual(self.config.settings, {
            'celery': {
                'broker': 'amqp://framework:framework@localhost:5672/framework',
                'backend': 'redis://localhost'
            },
            'test': 'value'
        })

    def test_get_celery(self):
        self.assertEqual(self.config.get_celery('test').__class__.__name__, 'Celery')

    def test_get_taxonomies(self):
        taxonomies = self.config.get_taxonomies()
        self.assertEqual(len(taxonomies), 2)
        self.assertEqual(taxonomies['taxonomy1'].get_taxons(), {'taxon1': 'value1'})
        self.assertEqual(taxonomies['taxonomy2'].get_taxons(), {
            'taxon1': 'value1', 'taxon2': 'value2', 'taxon3': 'value3'
        })

    def test_get_recommenders(self):
        recommenders = self.config.get_recommenders()
        self.assertEqual(len(recommenders), 4)

        recommender1 = recommenders['recommender1']
        self.assertEqual(recommender1.__class__.__name__, 'Engine')
        self.assertEqual(recommender1.name, 'recommender1')
        self.assertEqual(recommender1.taxonomy.get_taxons(), {
            'taxon1': 'value1', 'taxon2': 'value2', 'taxon3': 'value3', 'taxon4': 'value4'
        })
        self.assertEqual(recommender1.settings, {'base_url': 'http://localhost'})

        recommender3 = recommenders['recommender3']
        self.assertEqual(recommender3.__class__.__name__, 'Engine')
        self.assertEqual(recommender3.taxonomy.get_taxons(), {
            'taxon1': 'value1', 'taxon2': 'value2b', 'taxon3': 'value3b'
        })

        recommender4 = recommenders['recommender4']
        self.assertEqual(recommender4.__class__.__name__, 'HybridEngine')
        self.assertEqual(recommender4.name, 'recommender4')
        self.assertEqual(len(recommender4.components), 2)
        self.assertEqual(recommender4.settings, {'test': 'value2'})

        component1 = recommender4.components['component1']
        self.assertEqual(component1.__class__.__name__, 'Engine')
        self.assertEqual(component1.name, 'recommender1')
        component2 = recommender4.components['component2']
        self.assertEqual(component1.__class__.__name__, 'Engine')
        self.assertEqual(component2.name, 'recommender2')

    def test_get_events(self):
        events = self.config.get_events()
        self.assertEqual(len(events), 3)

        event1 = events['event1']
        self.assertEqual(len(event1), 1)
        self.assertEqual(event1[0]['recommender'].__class__.__name__, 'Engine')
        self.assertEqual(event1[0]['action'], 'perform')

        event2 = events['event2']
        self.assertEqual(len(event2), 2)
        self.assertEqual(event2[0]['recommender'].name, 'recommender2')
        self.assertEqual(event2[0]['action'], 'add')
        self.assertEqual(event2[1]['recommender'].name, 'recommender3')
        self.assertEqual(event2[1]['action'], 'add')
