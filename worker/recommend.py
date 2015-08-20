from worker import celery, logger
from config import config

@celery.task(name='worker.recommend.recommend')
def recommend(name, body):
    if name not in config.get_recommenders():
        logger.error('Unknown recommender name %s' % name)
        return False

    try:
        return config.get_recommenders()[name].recommend(body)
    except:
        import traceback, os, sys
        exc_type, exc_value, exc_traceback = sys.exc_info()
        logger.error(traceback.format_exception(
            exc_type, exc_value, exc_traceback
        ))
        return False
