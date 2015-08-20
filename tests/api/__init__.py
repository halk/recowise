import unittest
import api

class ApiTestCase(unittest.TestCase):
    def setUp(self):
        api.app.debug = True
        self.app = api.app.test_client()
