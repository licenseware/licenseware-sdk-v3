from licenseware.repository.mongo_repository.mongo_repository import MongoRepository


def default_check_status_handler(
    tenant_id: str, authorization: str, uploader_id: str, repo: MongoRepository
):
    result = repo.find_one(filters={"tenant_id": tenant_id, "uploader_id": uploader_id})
    return result
