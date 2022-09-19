# In python 3.11+ this will not be necessary (typing hack)
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma no cover
    from licenseware.config.config import Config

import requests

from .logger import log


def get_user_info(tenant_id: str, authorization: str, config: Config) -> dict:
    """
    {
        "user": {
            "id": "a083d6a1-9db0-41a6-9a0d-b135505e314f",
            "email": "alin@licenseware.io",
            "admin": false,
            "email_verified": true,
            "plan_type": "Free"
        },
        "tenants": [
            {
            "id": "ca4ade7d-fafc-4598-b939-54da01744085",
            "company_name": "dev",
            "is_default": true,
            "user_id": "a083d6a1-9db0-41a6-9a0d-b135505e314f"
            }
        ],
        "shared_tenants": []
    }
    """

    response = requests.get(
        url=config.AUTH_USER_INFO_URL,
        headers={
            "TenantId": tenant_id,
            "Authorization": authorization,
        },
    )

    if response.status_code != 200:  # pragma no cover
        log.error(response.content)
        raise Exception(f"Failed to get user info from '{config.AUTH_USER_INFO_URL}'")

    return response.json()
