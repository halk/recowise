import unittest
import json
import api

class ApiTestCase(unittest.TestCase):
    def setUp(self):
        api.app.debug = True
        self.app = api.app.test_client()

    # idiomatic way of method names in Python is under_scored
    def send_event(self, name, data):
        return self.app.post(
            '/event/%s' % name,
            data=json.dumps(data),
            content_type='application/json'
        )

if __name__ == '__main__':
    unittest.main()
