import time
from functools import lru_cache


def ttl_cache(expiry: int, maxsize: int = 10):
    def wrapper(func):
        @lru_cache(maxsize)
        def inner(__ttl, *args, **kwargs):
            return func(*args, **kwargs)

        return lambda *args, **kwargs: inner(time.time() // expiry, *args, **kwargs)

    return wrapper
