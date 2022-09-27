import datetime

from licenseware.config.config import Config
from licenseware.redis_cache.redis_cache import RedisCache


def default_update_status_handler(
    tenant_id: str,
    uploader_id: str,
    status: str,
    redis_cache: RedisCache,
    config: Config,
):  # pragma no cover

    data = {
        "tenant_id": tenant_id,
        "uploader_id": uploader_id,
        "status": status,
        "updated_at": datetime.datetime.utcnow().isoformat(),
    }

    return redis_cache.set(
        key=f"uploader_status:{uploader_id}:{tenant_id}",
        value=data,
        expiry=config.EXPIRE_UPLOADER_STATUS,
    )
