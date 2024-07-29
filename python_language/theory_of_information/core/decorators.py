import functools
import logging

logger = logging.getLogger(__name__)


def loggable(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug('function / method - {}, args - {}, kwargs - {} started'.format(func.__name__, args, kwargs))
        result = func(*args, **kwargs)

        if result is not None:
            logger.debug('function / method - {}, result - {} ended'.format(func.__name__, result))
        else:
            logger.debug('function / method - {} ended'.format(func.__name__))

        return result

    return wrapper
