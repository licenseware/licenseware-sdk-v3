import os
import time
from datetime import datetime
from licenseware.dependencies import requests
from licenseware.utils.logger import log
from licenseware.config.config import Config


class Authenticator:  # pragma no cover
    """

    ```py

    from licenseware import Authenticator
    response, status_code = Authenticator.connect(max_retries='infinite', wait_seconds=2)

    ```
    """

    def __init__(self, config: Config):
        self.config = config

    @classmethod
    def connect(cls, max_retries: int = 0, wait_seconds: int = 1):
        """
        param: max_retries  - 'infinite' or a number,
        param: wait_seconds - wait time in seconds if authentification fails
        """

        status_code = 500

        if max_retries == "infinite":
            while status_code != 200:
                response, status_code = cls()._retry_login()
                time.sleep(wait_seconds)
        else:
            for _ in range(max_retries + 1):
                response, status_code = cls()._retry_login()
                if status_code == 200:
                    break
                time.sleep(wait_seconds)

        if status_code == 200:
            os.environ["MACHINE_TOKEN"] = response.get(
                "Authorization", "Authorization not found"
            )
            os.environ["MACHINE_TOKEN_DATETIME"] = datetime.utcnow().isoformat()
            os.environ["APP_AUTHENTICATED"] = "true"
        else:
            os.environ["APP_AUTHENTICATED"] = "false"
            log.error("Can't authentificate this machine")

        return response, status_code

    def _retry_login(self):
        response, status_code = {"status": "failed"}, 500
        try:
            response, status_code = self._login()
        except Exception as err:
            log.error(f"{str(err)}\n\nAuthentification failed... retrying... ")
            pass  # ConnectionError
        return response, status_code

    def _login(self):

        payload = {
            "machine_name": self.config.MACHINE_NAME,
            "password": self.config.MACHINE_PASSWORD,
        }

        response = requests.post(self.config.MACHINE_LOGIN_URL, json=payload)

        if response.status_code == 200:
            return response.json(), 200

        log.error(f"Could not login with {self.config.MACHINE_NAME}")
        exit(1)
