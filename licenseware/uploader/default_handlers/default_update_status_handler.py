import datetime

from licenseware.config.config import Config
from licenseware.redis_cache.redis_cache import RedisCache

from .helpers import get_uploader_status_key


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
        "app_id": config.APP_ID,
        "status": status,
        "updated_at": datetime.datetime.utcnow().isoformat(),
    }

    return redisdb.set(
        key=get_uploader_status_key(uploader_id, config.APP_ID, tenant_id),
        value=data,
        expiry=config.EXPIRE_UPLOADER_STATUS,
    )
