from flask import Blueprint, request, jsonify
from flask.ext import restful
from worker.recommend import recommend as recommend_worker
from api import app

recommend = Blueprint('recommend', __name__)
api = restful.Api(recommend)

# api
class Recommend(restful.Resource):
    def get(self, recommender):
        # convert MultiDict [('sku', 'test1'), ('sku', 'test2'), ('limit', '5')]
        # to {'sku':['test1', 'test2'], 'limit': '5'}
        args = {}
        for argKey in request.args.iterkeys():
            arg = request.args.getlist(argKey)
            if len(arg) > 1:
                args[argKey] = arg
            else:
                args[argKey] = request.args.get(argKey)

        result = recommend_worker.delay(recommender, args)
        return result.get(timeout=4), 200

api.add_resource(Recommend, '/<string:recommender>')
