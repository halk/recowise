import unittest
from collections import OrderedDict
from mock import MagicMock
from engines.item_similarity import Engine
from tests.engines import BaseEngineTestCase

class EngineTestCase(BaseEngineTestCase, unittest.TestCase):
    def setUp(self):
        self._setUp(Engine, 'recommender1')

    def test_delete(self):
        response_mock = MagicMock()
        response_mock.status_code = 204
        self.engine.requests.delete = MagicMock()
        self.engine.requests.delete.return_value = response_mock

        self.assertTrue(self.engine.delete({'sku': 'test'}))

        response_mock.status_code = MagicMock(return_value=401)
        self.assertFalse(self.engine.delete({'sku': 'test'}))

    def test_recommend(self):
        response_mock = MagicMock()
        response_mock.json = MagicMock(return_value=OrderedDict((
            ('result1', 1.5), ('result2', 1)
        )))
        self.engine.requests.get.return_value = response_mock

        results = self.engine.recommend({'value': ['test', 'test2']})
        self.assertEqual(results, ['result1', 'result2'])

        results = self.engine.recommend({'value': 'test'}, True)
        self.assertEqual(results, OrderedDict((('result1', 1.5), ('result2', 1))))
