from collections import OrderedDict
from core.engine.simple import Engine as BaseEngine

class Engine(BaseEngine):

    def post(self, body):
        return self.call('post', self.name, body)

    def delete(self, body):
        params = self.translate(body)
        response = self.requests.delete(
            '%s%s/%s' % (self.base_url, self.name, params['item_id'])
        )

        return response.status_code == 204

    def recommend(self, body, return_with_score=False):
        data = self.add_brackets_to_lists(self.translate(body))
        results = self.requests.get(self.base_url + self.name, params=data).json(
            object_pairs_hook=OrderedDict
        )

        if return_with_score is False:
            return results.keys()
        return results
