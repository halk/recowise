import json
from mock import MagicMock, patch
from tests.api import ApiTestCase

class ApiEventTestCase(ApiTestCase):
    def test_post_event_product_viewed(self):
        with patch('worker.event.process_event.delay') as mock_task:
            subject = 'viewed_product'
            data = {
                'user_id': 'abcdef',
                'sku': 'sku1'
            }

            response = self.send_event(subject, data)
            self.assertEqual(response.status_code, 204)
            self.assertTrue(mock_task.called_with(subject, data))

    def send_event(self, name, data):
        return self.app.post(
            '/event/%s' % name,
            data=json.dumps(data),
            content_type='application/json'
        )
