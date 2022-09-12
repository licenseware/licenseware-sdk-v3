import datetime

from licenseware.repository.mongo_repository.mongo_repository import MongoRepository


def default_update_status_handler(
    tenant_id: str,
    authorization: str,
    uploader_id: str,
    status: str,
    repo: MongoRepository,
):  # pragma no cover
    result = repo.update_one(
        filters={"tenant_id": tenant_id, "uploader_id": uploader_id},
        data={
            "tenant_id": tenant_id,
            "uploader_id": uploader_id,
            "status": status,
            "updated_at": datetime.datetime.utcnow().isoformat(),
        },
    )
    return result
