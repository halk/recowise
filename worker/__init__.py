import os
from config import config
from kombu import Queue, Exchange
from celery.utils.log import get_task_logger

# setting up celery
celery = config.get_celery('worker')
logger = get_task_logger(__name__)

exchange = Exchange('default')
celery.conf.update(
    CELERY_QUEUES = (
        Queue('event', exchange, routing_key='event'),
        Queue('recommend', exchange, routing_key='recommend'),
    ),
    CELERY_ROUTES = ({
        'worker.event.process_event': {'queue': 'event', 'routing_key': 'event'},
        'worker.recommend.recommend': {'queue': 'recommend', 'routing_key': 'recommend'},
    })
)
