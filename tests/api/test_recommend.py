import json
from mock import MagicMock, patch
from tests.api import ApiTestCase

class ApiRecommendTestCase(ApiTestCase):
    def test_recommend(self):
        data = {'user_id': 'userA', 'limit': 1}
        self._test_recommend(
            '/recommend/common_products_viewed',
            data,
            data
        )

    def test_recommend_multidict(self):
        data = 'item_id=itemA&item_id=itemB&limit=1'
        expected_data = {'item_id': ['itemA', 'itemB'], 'limit': 1}
        self._test_recommend(
            '/recommend/common_products_viewed',
            data,
            expected_data
        )

    def _test_recommend(self, subject, query_string, expected_data):
        with patch('worker.recommend.recommend.delay') as mock_task:
            expected_result = ['result1', 'result2']

            worker_result = MagicMock()
            worker_result.get = MagicMock(return_value=expected_result)

            mock_task.return_value = worker_result

            response = self.app.get(subject, query_string=query_string)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(json.loads(response.get_data()), expected_result)
            self.assertTrue(mock_task.delay.called_with(subject, expected_data))
