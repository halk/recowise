import unittest
from core.engine.hybrid import HybridEngine
from core.engine.simple import Engine
from core.taxonomy import Taxonomy

class HybridTestCase(unittest.TestCase):
    def setUp(self):
        taxonomy = Taxonomy('base', {'key': 'value', 'key2': 'value2'})
        component1 = Engine('recommender1', taxonomy, {
            'base_url': 'http://localhost'
        })
        component2 = Engine('recommender2', taxonomy, {
            'base_url': 'http://localhost2'
        })
        components = {'component1': component1, 'component2': component2}
        settings = {'test': 'value'}
        self.engine = HybridEngine('hybrid', taxonomy, components, settings)

    def test_components(self):
        components = self.engine.get_components()
        self.assertEqual(len(components), 2)
        self.assertEqual(components['component1'].name, 'recommender1')
        self.assertEqual(components['component2'].name, 'recommender2')

    def test_recommend(self):
        self.assertRaises(NotImplementedError, self.engine.recommend, {})
