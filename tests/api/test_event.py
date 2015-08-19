from tests.api import ApiTestCase

class ApiEventTestCase(ApiTestCase):
    def test_post_event_product_viewed(self):
        response = self.send_event('viewed_product', {
            'user_id': 'abcdef',
            'sku': 'sku1'
        })
        self.assertEqual(response.status_code, 204)
