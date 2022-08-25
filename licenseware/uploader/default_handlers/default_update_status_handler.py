from licenseware.repository.mongo_repository.mongo_repository import MongoRepository


def default_update_status_handler(
    tenant_id: str,
    authorization: str,
    uploader_id: str,
    status: str,
    repo: MongoRepository,
):
    result = repo.insert_one(
        data={"tenant_id": tenant_id, "uploader_id": uploader_id, "status": status}
    )
    return result
