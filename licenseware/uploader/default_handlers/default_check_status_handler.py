from licenseware.config.config import Config
from licenseware.constants.states import States
from licenseware.constants.web_response import WebResponse
from licenseware.redis_cache.redis_cache import RedisCache

from .helpers import get_uploader_status_key


def default_check_status_handler(
    tenant_id: str,
    uploader_id: str,
    config: Config,
):  # pragma no cover

    redisdb = RedisCache(config)

    result = redisdb.get_key(
        get_uploader_status_key(uploader_id, config.APP_ID, tenant_id)
    )

    if not result:
        return WebResponse(
            content={"status": States.IDLE},
            status_code=200,
        )

    return WebResponse(
        content={"status": result["status"]},
        status_code=200,
    )
