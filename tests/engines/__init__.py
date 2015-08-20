from mock import MagicMock
from core.taxonomy import Taxonomy

class BaseEngineTestCase:
    def _setUp(self, engineClass, name):
        taxonomy = Taxonomy('base', {'key': 'value', 'key2': 'value2', 'item_id': 'sku'})
        self.engine = engineClass(name, taxonomy, {
            'base_url': 'http://localhost/',
            'key': 'value'
        })

        self.engine.requests = MagicMock()
        self.engine.requests.request = MagicMock()
        self.engine.requests.post = MagicMock()

    def test_post(self):
        self._test_event('post')

    def test_delete(self):
        self._test_event('delete')

    def _test_event(self, method):
        response_mock = MagicMock()
        response_mock.status_code = 204
        self.engine.requests.request.return_value = response_mock

        self.assertTrue(getattr(self.engine, method)({'value': 'test'}))

        response_mock.status_code = MagicMock(return_value=401)
        self.assertFalse(getattr(self.engine, method)({'value': 'test'}))
