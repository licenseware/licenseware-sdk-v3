import os
import sys
import time

from licenseware.config.config import Config
from licenseware.dependencies import requests
from licenseware.utils.logger import log


def login_user(email: str, password: str, login_url: str):
    creds = {"email": email, "password": password}
    response = requests.post(url=login_url, json=creds)
    return response.json()


def login_machine(config: Config, _retry_in: int = 0):

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
            log.error(f"Could not login '{config.MACHINE_NAME}'")
            time.sleep(_retry_in)
            login_machine(config, _retry_in)
    except:
        log.error(f"Could not login '{config.MACHINE_NAME}'")
        time.sleep(_retry_in)
        login_machine(config, _retry_in)

    machine_token = response.json()["Authorization"]
    os.environ["MACHINE_TOKEN"] = machine_token
    config.redisdb.set("MACHINE_TOKEN", machine_token, expiry=None)
    log.success("Machine login successful!")


def cron_login_machine(config: Config):
    try:
        login_machine(config)
        while True:
            time.sleep(config.REFRESH_MACHINE_TOKEN_INTERVAL)
            login_machine(config)
            log.info(f"Refreshed machine token")
    except KeyboardInterrupt:
        log.info("Shutting down login_machine...")
        sys.exit(0)
