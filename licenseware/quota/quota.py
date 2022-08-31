import datetime
import sys

import dateutil.parser as dateparser

from licenseware.config.config import Config
from licenseware.constants.states import States
from licenseware.constants.uploader_types import UploaderQuotaResponse
from licenseware.constants.web_response import WebResponse
from licenseware.repository.mongo_repository.mongo_repository import MongoRepository
from licenseware.utils.get_user_info import get_user_info


def get_quota_reset_date(current_date: datetime.datetime = datetime.datetime.utcnow()):
    quota_reset_date = current_date + datetime.timedelta(days=30)
    return quota_reset_date.isoformat()


class Quota:
    def __init__(
        self,
        tenant_id: str,
        authorization: str,
        uploader_id: str,
        free_units: int,
        repo: MongoRepository,
        config: Config,
    ):
        self.tenant_id = tenant_id
        self.authorization = authorization
        self.uploader_id = uploader_id
        self.app_id = config.APP_ID
        self.repo = repo

        if config.CURRENT_ENVIRONMENT != config.ENVIRONMENTS.DESKTOP:  # pragma no cover
            user_info = get_user_info(tenant_id, authorization, config)
        else:
            user_info = {"user_id": tenant_id, "plan_type": "UNLIMITED"}

        self.user_id = user_info["user_id"]
        self.monthly_quota = (
            sys.maxsize if user_info["plan_type"].upper() == "UNLIMITED" else free_units
        )

        self.quota_filters = {
            "user_id": self.user_id,
            "app_id": self.app_id,
            "uploader_id": self.uploader_id,
        }

        # Ensure quota is initialized
        self.init()

    def init(self):

        utilization_data = self.repo.find_one(filters=self.quota_filters)

        if utilization_data:
            utilization_data.pop("_id")
            return WebResponse(
                content=UploaderQuotaResponse(
                    **{
                        "status": States.SUCCESS,
                        "message": "Quota already initialized",
                        **utilization_data,
                    }
                ),
                status_code=200,
            )

        utilization_data = {
            "app_id": self.app_id,
            "user_id": self.tenant_id,
            "uploader_id": self.uploader_id,
            "monthly_quota": self.monthly_quota,
            "monthly_quota_consumed": 0,
            "quota_reset_date": get_quota_reset_date(),
        }

        self.repo.insert_one(data=utilization_data)
        utilization_data.pop("_id")

        return WebResponse(
            content=UploaderQuotaResponse(
                **{
                    "status": States.SUCCESS,
                    "message": "Quota initialized",
                    **utilization_data,
                }
            ),
            status_code=200,
        )

    def update(self, units: int):

        check_response = self.check(units)
        if check_response.status_code == 402:
            return check_response

        current_quota = self.repo.find_one(filters=self.quota_filters)
        current_quota = self.repo.update_one(
            filters=self.quota_filters,
            data={"$inc": {"monthly_quota_consumed": units}},
        )
        current_quota.pop("_id")
        return WebResponse(
            content=UploaderQuotaResponse(
                **{
                    "status": States.SUCCESS,
                    "message": "Quota initialized",
                    **current_quota,
                }
            ),
            status_code=200,
        )

    def reset(self):
        return self.repo.update_one(
            filters=self.quota_filters,
            data={
                "monthly_quota_consumed": 0,
                "quota_reset_date": get_quota_reset_date(),
            },
        )

    def check(self, units: int = 0):

        current_quota = self.repo.find_one(filters=self.quota_filters)
        current_date = datetime.datetime.utcnow()
        quota_consumed = current_quota["monthly_quota_consumed"]
        reset_date = dateparser.parse(current_quota["quota_reset_date"])

        if current_date >= reset_date:
            current_quota = self.reset()

        quota_within_limits = quota_consumed + units <= current_quota["monthly_quota"]
        current_quota.pop("_id")

        if not quota_within_limits:
            return WebResponse(
                content=UploaderQuotaResponse(
                    **{
                        "status": States.FAILED,
                        "message": "Monthly quota exceeded",
                        **current_quota,
                    }
                ),
                status_code=402,
            )

        return WebResponse(
            content=UploaderQuotaResponse(
                **{
                    "status": States.SUCCESS,
                    "message": "Utilization within monthly quota",
                    **current_quota,
                }
            ),
            status_code=200,
        )
