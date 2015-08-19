import logging
import os
from logging import FileHandler
from flask import Flask
from config import config

# setting up flask
app = Flask(__name__)
celery = config.get_celery('worker')

# setting up logging
file_handler = FileHandler(os.path.join(os.path.dirname(__file__), '..', 'log', 'api.log'))
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

app.logger.addHandler(file_handler)

# registering submodules
from api.event import event
from api.recommend import recommend

app.register_blueprint(event, url_prefix='/event')
app.register_blueprint(recommend, url_prefix='/recommend')

# default test route

@app.route("/")
def hello():
    return "Welcome to the Multi-Purpose Recommender System!"
