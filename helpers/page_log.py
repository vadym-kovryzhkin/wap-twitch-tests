import functools
import logging

logger = logging.getLogger(__name__)


def log_method_call(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        method_name = func.__name__
        positional_args = args[1:]  # ignore 'self'
        logger.info(f"{method_name} with: {positional_args}, kwargs: {kwargs}")
        result = func(*args, **kwargs)
        return result

    return wrapper
