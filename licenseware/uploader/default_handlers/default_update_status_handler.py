import datetime

from licenseware.config.config import Config
from licenseware.redis_cache.redis_cache import RedisCache


def default_update_status_handler(
    tenant_id: str,
    uploader_id: str,
    status: str,
    config: Config,
):  # pragma no cover

    redisdb = RedisCache(config)

    data = {
        "tenant_id": tenant_id,
        "uploader_id": uploader_id,
        "status": status,
        "updated_at": datetime.datetime.utcnow().isoformat(),
    }

    return redisdb.set(
        key=f"uploader_status:{uploader_id}:{tenant_id}",
        value=data,
        expiry=config.EXPIRE_UPLOADER_STATUS,
    )
