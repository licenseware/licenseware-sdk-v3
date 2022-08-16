import traceback
from functools import wraps
from .logger import log


def failsafe(*dargs, fail_code=500):
    """Prevents a function to raise an exception and break the app"""

    def _decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                response = f(*args, **kwargs)
                return response
            except Exception as err:
                log.error(traceback.format_exc())
                return {"status": "failed", "message": str(err)[0:30]}, fail_code

        return wrapper

    return _decorator(dargs[0]) if dargs and callable(dargs[0]) else _decorator
