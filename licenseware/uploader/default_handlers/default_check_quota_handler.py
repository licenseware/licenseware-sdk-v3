from licenseware.config.config import Config
from licenseware.quota.quota import Quota
from licenseware.repository.mongo_repository.mongo_repository import MongoRepository


def default_check_quota_handler(
    tenant_id: str,
    authorization: str,
    uploader_id: str,
    free_units: int,
    repo: MongoRepository,
    config: Config,
):

    quota = Quota(
        tenant_id=tenant_id,
        authorization=authorization,
        uploader_id=uploader_id,
        free_units=free_units,
        repo=repo,
        config=config,
    )

    return quota.check()
