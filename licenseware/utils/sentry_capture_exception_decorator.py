import sentry_sdk
from functools import wraps


def sentry_capture_exception(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as err:
            sentry_sdk.capture_exception(err)
            raise err

    return decorated
