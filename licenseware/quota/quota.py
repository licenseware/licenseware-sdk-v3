import sys
from typing import Any
from datetime import datetime
from licenseware.constants.uploader_types import UploaderQuotaResponse, QuotaType, QuotaPlan
from licenseware import tenant


# TODO

class Quota:

    def __init__(self, tenant_id: str, auth_jwt: str, uploader_id: str, units: int, db: Any):
        self.tenant_id = tenant_id
        self.auth_jwt = auth_jwt
        self.uploader_id = uploader_id
        self.units = units
        self.db = db

        self.tenants = tenant.get_tenants_list(tenant_id, auth_jwt)
        self.user_profile = tenant.get_user_profile(tenant_id, auth_jwt)
        self.plan_type = self.user_profile["plan_type"].upper()


    def get_current_quota(self):
        return self.db.fetch(
            match=self.tenant_query,
            collection=self.collection
        )

    def get_monthly_quota(self):
        if self.plan_type == QuotaPlan.UNLIMITED:
            return sys.maxsize
        return self.units

    def get_quota_reset_date(self, current_date: datetime = datetime.utcnow()):
        quota_reset_date = current_date + datetime.timedelta(days=30)
        return quota_reset_date.isoformat()


    def initialize(self):

        QuotaType(
            tenant_id=self.tenant_id,
            uploader_id=self.uploader_id,
            monthly_quota=self.get_monthly_quota(),
            monthly_quota_consumed=0,
            quota_reset_date=self.get_quota_reset_date()
        )
