import unittest
from mock import MagicMock
from copy import deepcopy
from collections import OrderedDict
from engines.hybrid.weighted import HybridEngine
from core.engine import Engine
from core.taxonomy import Taxonomy

class HybridTestCase(unittest.TestCase):
    def setUp(self):
        taxonomy = Taxonomy('base', {'key': 'value', 'key2': 'value2'})
        component1 = Engine('recommender1', taxonomy, {
            'base_url': 'http://localhost'
        })
        component1.requests = MagicMock()
        component1.requests.get = MagicMock()

        component2 = Engine('recommender2', taxonomy, {
            'base_url': 'http://localhost2'
        })
        component2.requests = MagicMock()
        component2.requests.get = MagicMock()

        components = {'component1': component1, 'component2': component2}
        settings = {'weight': {'component1': 0.25, 'component2': 0.75}}
        self.engine = HybridEngine('hybrid', components, settings)

    def test_recommend(self):
        result1 = {'item1': 6, 'item2': 2, 'item3': 1}
        result2 = {'item1': 2, 'item2': 4, 'item3': 3}
        component1 = component2 = MagicMock()
        component1.json = MagicMock(return_value=result1)
        component2.json = MagicMock(return_value=result2)
        self.engine.components['component1'].requests.get.return_value = component1
        self.engine.components['component2'].requests.get.return_value = component2

        self.assertEqual(self.engine.recommend({'key': 'value'}), [
            'item2', 'item3', 'item1'
        ])

    def test_get_results(self):
        result1 = {'item1': 6, 'item2': 2}
        result2 = {'item1': 2, 'item2': 4}
        component1 = MagicMock()
        component1.json = MagicMock(return_value=result1)
        self.engine.components['component1'].requests.get.return_value = component1
        component2 = MagicMock()
        component2.json = MagicMock(return_value=result2)
        self.engine.components['component2'].requests.get.return_value = component2

        self.assertEqual(self.engine.get_results({'key': 'value'}), {
            'component1': result1, 'component2': result2
        })

    def test_apply_weight(self):
        results = {
            'component1': {'item1': 5, 'item2': 2},
            'component2': {'item1': 2, 'item2': 4}
        }
        self.assertEqual(self.engine.apply_weight(deepcopy(results)), {
            'component1': {'item1': 1.25, 'item2': 0.5},
            'component2': {'item1': 1.5, 'item2': 3}
        })

        old_settings = self.engine.settings
        self.engine.settings = {}
        self.assertEqual(self.engine.apply_weight(deepcopy(results)), results)

        self.engine.settings['weight'] = {'component1': 0.5}
        self.assertEqual(self.engine.apply_weight(deepcopy(results)), {
            'component1': {'item1': 2.5, 'item2': 1},
            'component2': {'item1': 2, 'item2': 4}
        })

        self.engine.settings = old_settings

    def test_merge(self):
        data = {
            'component1': {'item1': 1, 'item2': 2, 'item3': 1.1},
            'component2': {'item1': 1.5, 'item2': 1, 'item3': 1, 'item4': 0.5}
        }

        self.assertEqual(self.engine.merge(data), ['item2', 'item1', 'item3', 'item4'])
