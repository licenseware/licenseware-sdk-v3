from licenseware import Config, RedisCache

# pytest -s -v tests/test_redis_cache.py


def test_redis_cache():

    config = Config()

    rc = RedisCache(config)

    rc.set(
        key="apps:ifmp-service", value={"app": {"app_id": "ifmp-service"}}, expiry=10
    )

    rc.set(key="apps:odb-service", value={"app": {"app_id": "odb-service"}}, expiry=10)

    result = rc.get("apps:*")

    assert isinstance(result, list)
    assert len(result) == 2

    result = rc.get("*:odb-service")

    assert isinstance(result, list)
    assert len(result) == 1

    result = rc.get("apps:odb-service")

    assert isinstance(result, list)
    assert len(result) == 1

    result = rc.get_key("apps:odb-service")

    assert isinstance(result, dict)

    rc.delete("apps:odb-service")

    result = rc.get_key("apps:odb-service")

    assert result is None
