import requests
from collections import OrderedDict
from core.engine import Engine as BaseEngine

class Engine(BaseEngine):
    def post(self, body):
        return self.call('post', 'event', body)

    def delete(self, body):
        return self.call('delete', 'event', body)
