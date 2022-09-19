from licenseware.config.config import Config
from licenseware.constants.states import States
from licenseware.constants.uploader_types import FileValidationResponse
from licenseware.quota.quota import Quota
from licenseware.repository.mongo_repository.mongo_repository import MongoRepository


def default_check_quota_handler(
    tenant_id: str,
    authorization: str,
    uploader_id: str,
    free_units: int,
    validation_response: FileValidationResponse,
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

    if validation_response is None:
        return quota.check(units=0)

    nbr_of_files = 0
    for file in validation_response.validation:
        if file.status == States.SUCCESS:
            nbr_of_files += 1

    return quota.check(units=nbr_of_files)
