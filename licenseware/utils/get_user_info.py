# In python 3.11+ this will not be necessary (typing hack)
from __future__ import annotations
import requests
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from licenseware.config.config import Config


def get_user_info(tenant_id: str, authorization: str, config: Config) -> dict:

    if config.USER_PROFILE_URL is None:
        raise Exception("Please provide `USER_PROFILE_URL` in config")

    response = requests.get(
        url=config.USER_PROFILE_URL,
        headers={
            "TenantId": tenant_id,
            "Authorization": authorization,
        },
    )

    if response.status_code != 200:
        raise Exception(f"Failed to get user info from '{config.USER_PROFILE_URL}'")

    return response.json()
