from flask import Blueprint, request
from flask.ext import restful
from worker.event import process_event

event = Blueprint('event', __name__)
api = restful.Api(event)

# api
class Event(restful.Resource):
    def post(self, subject):
        process_event.delay(subject, request.get_json())
        return '', 204

api.add_resource(Event, '/<string:subject>')
