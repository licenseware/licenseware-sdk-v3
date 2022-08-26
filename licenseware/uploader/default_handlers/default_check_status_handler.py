from licenseware.constants.states import States
from licenseware.constants.web_response import WebResponse
from licenseware.repository.mongo_repository.mongo_repository import MongoRepository


def default_check_status_handler(
    tenant_id: str, authorization: str, uploader_id: str, repo: MongoRepository
):

    result = repo.find_one(filters={"tenant_id": tenant_id, "uploader_id": uploader_id})
    if not result:
        return WebResponse(
            content={"status": States.IDLE},
            status_code=200,
        )
    result.pop("_id")
    result.pop("uploader_id")
    result.pop("tenant_id")
    return WebResponse(
        content=result,
        status_code=200,
    )
