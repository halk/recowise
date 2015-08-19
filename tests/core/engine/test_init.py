import unittest
from collections import OrderedDict
from mock import MagicMock
from core.taxonomy import Taxonomy
from core.engine import Engine

class EngineTestCase(unittest.TestCase):
    def setUp(self):
        taxonomy = Taxonomy('base', {'key': 'value', 'key2': 'value2'})
        self.engine = Engine('recommender1', taxonomy, {
            'base_url': 'http://localhost',
            'key': 'value'
        })

        self.engine.requests = MagicMock()
        self.engine.requests.request = MagicMock()
        self.engine.requests.get = MagicMock()

    def test_translate(self):
        body = {'value': 'test', 'value3': 'test3'}
        translated = self.engine.translate(body)
        self.assertDictEqual(translated, {'key': 'test', 'key2': 'value2'})

    def test_post(self):
        response_mock = MagicMock()
        response_mock.status_code = 204
        self.engine.requests.request.return_value = response_mock

        self.assertTrue(self.engine.post('/test', {'value': 'test'}))

        response_mock.status_code = MagicMock(return_value=401)
        self.assertFalse(self.engine.post('/test', {'value': 'test'}))

    def test_delete(self):
        response_mock = MagicMock()
        response_mock.status_code = 204
        self.engine.requests.request.return_value = response_mock

        self.assertTrue(self.engine.delete('/test', {'value': 'test'}))

        response_mock.status_code = MagicMock(return_value=401)
        self.assertFalse(self.engine.delete('/test', {'value': 'test'}))

    def test_recommend(self):
        response_mock = MagicMock()
        response_mock.json = MagicMock(return_value=OrderedDict((
            ('result1', 1.5), ('result2', 1)
        )))
        self.engine.requests.get.return_value = response_mock

        results = self.engine.recommend({'value': 'test'})
        self.assertEqual(results, ['result1', 'result2'])

        results = self.engine.recommend({'value': 'test'}, True)
        self.assertEqual(results, OrderedDict((('result1', 1.5), ('result2', 1))))

    def test_add_brackets_to_lists(self):
        data = {'test': 'value', 'test2': ['value2', 'value3']}
        self.assertEqual(self.engine.add_brackets_to_lists(data), {
            'test': 'value', 'test2[]': ['value2', 'value3']
        })
