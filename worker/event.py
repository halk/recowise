import os, sys
from worker import celery, logger
from config import config

@celery.task(name='worker.event.process_event', ignore_result=True)
def process_event(name, body):
    if name not in config.get_events():
        logger.error('Unknown event name %s' % name)
        return False

    observers = config.get_events()[name]
    for observer in observers:
        try:
            if getattr(observer['recommender'], observer['action'])(body) == False:
                raise Exception('event did not run successfully')
        except:
            import traceback, os, sys
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logger.error(traceback.format_exception(
                exc_type, exc_value, exc_traceback
            ))
            return False

    return True
