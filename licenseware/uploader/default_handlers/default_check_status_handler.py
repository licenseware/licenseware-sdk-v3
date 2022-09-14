from licenseware.constants.states import States
from licenseware.constants.web_response import WebResponse
from licenseware.redis_cache.redis_cache import RedisCache


def default_check_status_handler(
    tenant_id: str, authorization: str, uploader_id: str, redisdb: RedisCache
):  # pragma no cover

    result = redisdb.get_key(f"{tenant_id}:{uploader_id}")

    if not result:
        return WebResponse(
            content={"status": States.IDLE},
            status_code=200,
        )

    return WebResponse(
        content={"status": result["status"]},
        status_code=200,
    )
