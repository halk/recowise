from tests.api import ApiTestCase

class ApiIndexTestCase(ApiTestCase):
    def test_homepage(self):
        response = self.app.get('/')
        assert 'Welcome to the Multi-Purpose Recommender System!' in response.data
