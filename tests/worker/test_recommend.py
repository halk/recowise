from mock import MagicMock, patch
from worker.recommend import recommend
from tests.worker import WorkerTestCase

class WorkerEventTestCase(WorkerTestCase):
    def test_recommend(self):
        recommend = MagicMock(return_value=True)

        self._test_recommend('recommender1', recommend)

    def test_recommend_with_unknown_name(self):
        self._test_recommend('unknown_recommender', None, False)

    def test_recommend_exception(self):
        recommend = MagicMock(side_effect=Exception('oops'), return_value=False)

        self._test_recommend('recommender1', recommend, False)

    def _test_recommend(self, name, mock_recommend, expected_result=True):
        with patch('worker.recommend.config', new=self.config) as mock_config:
            if mock_recommend is not None:
                mock_config.recommenders[name] = MagicMock()
                mock_config.recommenders[name].recommend = mock_recommend

            body = {'item': 'itemA'}
            result = recommend(name, body)

            self.assertEqual(result, expected_result)

            if mock_recommend is not None:
                self.assertTrue(mock_recommend.called_with(name, body))
