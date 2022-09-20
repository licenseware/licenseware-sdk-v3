from licenseware.config.config import Config
from licenseware.constants.states import States
from licenseware.constants.web_response import WebResponse
from licenseware.redis_cache.redis_cache import RedisCache


def default_check_status_handler(
    tenant_id: str,
    uploader_id: str,
    config: Config,
):  # pragma no cover

    redisdb = RedisCache(config)

    result = redisdb.get_key(f"uploader_status:{uploader_id or '*'}:{tenant_id or '*'}")

    if not result:
        return WebResponse(
            content={"status": States.IDLE},
            status_code=200,
        )

    return WebResponse(
        content={"status": result["status"]},
        status_code=200,
    )
