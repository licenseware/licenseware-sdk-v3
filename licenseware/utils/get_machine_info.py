from licenseware.redis_cache.redis_cache import RedisCache


def get_machine_headers(redis_cache: RedisCache, key: str = "auth_jwt"):
    return {key: redis_cache.get_key("MACHINE_TOKEN")}


def get_machine_token(redis_cache: RedisCache):
    return redis_cache.get_key("MACHINE_TOKEN")
