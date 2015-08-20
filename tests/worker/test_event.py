from mock import MagicMock, patch
from worker.event import process_event
from tests.worker import WorkerTestCase

class WorkerEventTestCase(WorkerTestCase):
    def test_event_with_single_observer(self):
        recommender = MagicMock()
        recommender.perform = MagicMock(return_value=True)

        self._test_event('event1', [{
            'recommender': recommender,
            'action': 'perform'
        }])

    def test_event_with_two_observers(self):
        recommender1 = MagicMock()
        recommender1.add = MagicMock(return_value=True)
        recommender2 = MagicMock()
        recommender2.add = MagicMock(return_value=True)

        self._test_event('event2', [
            {'recommender': recommender1, 'action': 'add'},
            {'recommender': recommender2, 'action': 'add'}
        ])

    def test_event_with_unknown_name(self):
        self._test_event('unknown_event', None, False)

    def test_event_exception(self):
        recommender = MagicMock()
        recommender.perform = MagicMock(return_value=False)

        self._test_event('event1', [{
            'recommender': recommender,
            'action': 'perform'
        }], False)

    def _test_event(self, name, observers, expected_result=True):
        with patch('worker.event.config', new=self.config) as mock_config:
            if observers is not None:
                mock_config.events[name] = observers

            body = {'item': 'itemA'}
            result = process_event(name, body)

            self.assertEqual(result, expected_result)

            if observers is not None:
                for observer in observers:
                    self.assertTrue(
                        observer['recommender'][observer['action']].called_with(name, body)
                    )
