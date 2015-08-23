from collections import OrderedDict
import json
import requests
from . import AbstractEngine

class Engine(AbstractEngine):

    def __init__(self, name, taxonomy, settings={}):
        super(Engine, self).__init__(name, taxonomy, settings)

        self.base_url = self.settings.get('base_url')

        self.requests = requests

    def call(self, method, uri, body, expected_response=204):
        headers = {'Content-Type': 'application/json'}
        response = self.requests.request(
            method,
            self.base_url + uri,
            data=json.dumps(self.translate(body)),
            headers=headers
        )

        return response.status_code == expected_response

    def post(self, uri, body):
        return self.call('post', uri, body)

    def delete(self, uri, body):
        return self.call('delete', uri, body)

    def recommend(self, body, return_with_score=False):
        data = self.translate(body)
        results = self.requests.get(self.base_url + '/recommend', params=data).json(
            object_pairs_hook=OrderedDict
        )

        if return_with_score is False:
            return results.keys()
        return results

    # GET parameters with more than one value seem to have better compatibility
    # with brackets behind (looking at you, PHP)
    def add_brackets_to_lists(self, data):
        for key, value in data.iteritems():
            if isinstance(value, list):
                data[key + '[]'] = value
                data.pop(key, None)

        return data
