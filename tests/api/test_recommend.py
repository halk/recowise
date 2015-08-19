import json
from tests.api import ApiTestCase

class ApiRecommendTestCase(ApiTestCase):
    def test_get_recommend_inCommon(self):
        # set data required for recommending
        self.send_event('viewed_product', {
            'user_id': 'recommend_inCommon_userA',
            'sku': 'recommend_inCommon_product1'
        })
        self.send_event('viewed_product', {
            'user_id': 'recommend_inCommon_userA',
            'sku': 'recommend_inCommon_product2'
        })
        self.send_event('viewed_product', {
            'user_id': 'recommend_inCommon_userB',
            'sku': 'recommend_inCommon_product2'
        })
        self.send_event('viewed_product', {
            'user_id': 'recommend_inCommon_userB',
            'sku': 'recommend_inCommon_product3'
        })
        # we are adding another user to test the weight
        # (users B and C who viewed the same product but user A did not)
        self.send_event('viewed_product', {
            'user_id': 'recommend_inCommon_userC',
            'sku': 'recommend_inCommon_product2'
        })
        self.send_event('viewed_product', {
            'user_id': 'recommend_inCommon_userC',
            'sku': 'recommend_inCommon_product3'
        })
        self.send_event('viewed_product', {
            'user_id': 'recommend_inCommon_userC',
            'sku': 'recommend_inCommon_product4'
        })
        # request from recommender
        response = self.app.get(
            '/recommend/common_products_viewed',
            query_string={'user_id': 'recommend_inCommon_userA', 'limit': 5}
        )
        response2 = self.app.get(
            '/recommend/common_products_viewed',
            query_string={'user_id': 'recommend_inCommon_userA', 'limit': 1}
        )
        # tests
        self.assertEqual(
            json.loads(response.get_data()),
            [u'recommend_inCommon_product3', u'recommend_inCommon_product4']
        )
        self.assertEqual(
            json.loads(response2.get_data()),
            [u'recommend_inCommon_product3']
        )
