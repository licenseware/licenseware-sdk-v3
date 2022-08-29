import jwt
import requests
import datetime
import dateutil.parser as dateparser
from licenseware.config.config import Config
from licenseware.utils.logger import log


class ReportPublicToken:
    def __init__(
        self, tenant_id: str, authorization: str, report_id: str, config: Config
    ):
        self.tenant_id = tenant_id
        self.authorization = authorization
        self.report_id = report_id
        self.config = config
        self.auth_headers = {"Authorization": authorization, "TenantId": tenant_id}

    def get_token(self, expire: int = 90):

        token = jwt.encode(
            {
                "tenant_id": self.tenant_id,
                "expire": expire,
                "app_id": self.config.APP_ID,
                "report_id": self.report_id,
                "ui_public_url": self.config.FRONTEND_URL,
            },
            self.config.APP_SECRET,
            algorithm="HS256",
        )

        data = dict(
            tenant_id=self.tenant_id,
            report_id=self.report_id,
            app_id=self.config.APP_SECRET,
            token=token,
            expiration_date=(
                datetime.datetime.utcnow() + datetime.timedelta(minutes=expire)
            ).isoformat(),
        )

        if self.valid_token(token):
            return token

        response = requests.post(
            self.config.PUBLIC_TOKEN_REPORT_URL,
            json=data,
            headers=self.auth_headers,
        )

        if response.status_code != 200:
            log.error(response.content)
            raise Exception("Can't save public report token")

        return token

    def valid_token(self, token: str):

        response = requests.get(
            self.config.PUBLIC_TOKEN_REPORT_URL,
            params={"token": token},
            headers=self.auth_headers,
        )

        if response.status_code != 200:
            log.error(response.content)
            raise Exception("Can't get public report token")

        results = response.json()

        if not results:
            return False

        now = datetime.datetime.utcnow()
        exp = dateparser.parse(results["expiration_date"])

        if now > exp:
            response = requests.delete(
                self.config.PUBLIC_TOKEN_REPORT_URL,
                params={"token": token},
                headers=self.auth_headers,
            )
            if response.status_code != 200:
                log.warning("Can't delete expired token")
            return False

        return True

    def get_token_data(self, token: str):
        data = jwt.decode(token, self.config.APP_SECRET, algorithms=["HS256"])
        return data

    def delete_token(self, token: str):
        response = requests.delete(
            self.config.PUBLIC_TOKEN_REPORT_URL,
            params={"token": token},
            headers=self.auth_headers,
        )
        if response.status_code != 200:
            log.warning(response.content)
            raise Exception("Can't delete public token")

        return response.json()
