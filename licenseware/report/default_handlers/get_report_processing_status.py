from licenseware.constants.states import States
from licenseware.repository.mongo_repository.mongo_repository import MongoRepository


def get_report_processing_status(
    tenant_id: str, repo: MongoRepository
):  # pragma no cover

    result = repo.find_one(filters={"tenant_id": tenant_id, "status": States.RUNNING})
    if not result:
        return States.IDLE
    return States.RUNNING
