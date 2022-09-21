import os
import sys
import time
from datetime import datetime
from threading import Thread

from licenseware.config.config import Config
from licenseware.dependencies import requests
from licenseware.utils.logger import log


def login_user(email: str, password: str, login_url: str):
    creds = {"email": email, "password": password}
    response = requests.post(url=login_url, json=creds)
    return response.json()


def login_machine(name: str, password: str, login_url: str):

    try:
        response = requests.post(
            login_url,
            json={
                "machine_name": name,
                "password": password,
            },
        )

        if response.status_code != 200:
            log.error(f"Could not login with {name}")
            time.sleep(2)
            login_machine(name, password, login_url)
    except:
        log.error(f"Could not login with {name}")
        time.sleep(2)
        login_machine(name, password, login_url)

    os.environ["MACHINE_TOKEN"] = response.json()["Authorization"]
    os.environ["MACHINE_TOKEN_DATETIME"] = datetime.utcnow().isoformat()
    log.success("Machine login successful!")


def _login_machine(name: str, password: str, login_url: str, refresh_interval: int):

    try:
        login_machine(name, password, login_url)

        while True:
            time.sleep(refresh_interval)
            login_machine(name, password, login_url)
            log.info(f"Refreshed machine token")
    except KeyboardInterrupt:
        log.info("Shutting down login_machine...")
        sys.exit(0)


def login_machine_in_thread(config: Config, start_thread: bool = True):

    t = Thread(
        target=_login_machine,
        args=(
            config.MACHINE_NAME,
            config.MACHINE_PASSWORD,
            config.AUTH_MACHINE_LOGIN_URL,
            config.REFRESH_MACHINE_TOKEN_INTERVAL,
        ),
        daemon=True,
    )

    if start_thread:
        t.start()
    return t
