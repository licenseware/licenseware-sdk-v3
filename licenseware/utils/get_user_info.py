# In python 3.11+ this will not be necessary (typing hack)
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma no cover
    from licenseware.config.config import Config

import requests

from .logger import log


def get_user_info(tenant_id: str, authorization: str, config: Config) -> dict:

    response = requests.get(
        url=config.USER_INFO_URL,
        headers={
            "tenant_id": tenant_id,
            "auth_jwt": authorization,
        },
    )

    if response.status_code != 200:  # pragma no cover
        log.error(response.content)
        raise Exception(f"Failed to get user info from '{config.USER_INFO_URL}'")

    return response.json()
