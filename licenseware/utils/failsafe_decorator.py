import traceback
from functools import wraps

from licenseware.constants.web_response import WebResponse

from .logger import log


def failsafe(*dargs, catch_error=True):
    """Prevents a function to raise an exception and break the app"""

    def _decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                response = f(*args, **kwargs)
                return response
            except Exception as err:
                log.error(traceback.format_exc())
                if catch_error is False:
                    raise err
                return WebResponse(
                    content={"status": "failed", "message": "Something went wrong"},
                    status_code=500,
                )

        return wrapper

    return _decorator(dargs[0]) if dargs and callable(dargs[0]) else _decorator
