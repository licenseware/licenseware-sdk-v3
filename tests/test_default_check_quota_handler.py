import uuid

from licenseware import (
    FileValidationResponse,
    MongoRepository,
    ValidationResponse,
    get_mongodb_connection,
)
from licenseware.uploader.default_handlers import default_check_quota_handler

from . import config, tenant_id

# pytest -s -v tests/test_default_check_quota_handler.py

# pytest -s -v tests/test_default_check_quota_handler.py::test_default_check_quota_handler
def test_default_check_quota_handler(mocker):

    user = {"TenantId": tenant_id, "Authorization": tenant_id}

    mocker.patch(
        "licenseware.quota.get_user_info",
        return_value={"user": {"id": tenant_id, "plan_type": "Free"}},
    )

    db_connection = get_mongodb_connection(config)

    fileResponse = FileValidationResponse(
        status="success",
        message="All good",
        event_id=str(uuid.uuid4()),
        validation=[
            ValidationResponse(
                status="success", filename="rv_tools.xlsx", message="All good"
            )
        ],
    )

    repo = MongoRepository(
        db_connection,
        collection=config.MONGO_COLLECTION.QUOTA,
        data_validator="ignore",
    )

    result = default_check_quota_handler(
        user["TenantId"],
        user["Authorization"],
        "rv_tools",
        1,
        fileResponse,
        repo,
        config,
    )

    assert result.status_code == 200


# pytest -s -v tests/test_default_check_quota_handler.py::test_raw_find
def test_raw_find():

    conn = get_mongodb_connection(config)

    conn["QuotaTest"].insert_one(
        {
            "user_id": "d137c718-fdca-4687-89db-9d4c0a50774f",
            "app_id": "app",
            "uploader_id": "rv_tools",
        }
    )

    result_raw = conn["QuotaTest"].find_one(
        {
            "user_id": "d137c718-fdca-4687-89db-9d4c0a50774f",
            "app_id": "app",
            "uploader_id": "rv_tools",
        }
    )

    # print(result_raw)
    assert result_raw
