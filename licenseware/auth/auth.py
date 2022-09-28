import sys
import time

from licenseware.config.config import Config
from licenseware.dependencies import requests
from licenseware.redis_cache.redis_cache import RedisCache
from licenseware.utils.logger import log


def login_user(email: str, password: str, login_url: str):
    creds = {"email": email, "password": password}
    response = requests.post(url=login_url, json=creds)
    return response.json()


def login_machine(config: Config, redis_cache: RedisCache, _retry_in: int = 0):

    if _retry_in > 120:
        _retry_in = 0

    _retry_in = _retry_in + 5

    try:

        response = requests.post(
            config.AUTH_MACHINE_LOGIN_URL,
            json={
                "machine_name": config.MACHINE_NAME,
                "password": config.MACHINE_PASSWORD,
            },
        )

        if response.status_code != 200:
            log.warning(response.content)
            log.error(f"Could not login '{config.MACHINE_NAME}'")
            time.sleep(_retry_in)
            login_machine(config, redis_cache, _retry_in)
    except Exception as err:
        log.warning(err)
        log.error(f"Could not login '{config.MACHINE_NAME}'")
        time.sleep(_retry_in)
        login_machine(config, redis_cache, _retry_in)

    machine_token = response.json()["Authorization"]
    redis_cache.set("MACHINE_TOKEN", machine_token, expiry=None)
    log.success("Machine login successful!")


def cron_login_machine(config: Config, redis_cache: RedisCache):
    try:
        login_machine(config, redis_cache)
        while True:
            time.sleep(config.REFRESH_MACHINE_TOKEN_INTERVAL)
            login_machine(config, redis_cache)
            log.info(f"Refreshed machine token")
    except KeyboardInterrupt:
        log.info("Shutting down login_machine...")
        sys.exit(0)
