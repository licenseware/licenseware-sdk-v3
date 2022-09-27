import uuid

from licenseware import (
    Config,
    FileValidationResponse,
    MongoRepository,
    ValidationResponse,
    get_mongodb_connection,
    login_user,
)
from licenseware.uploader.default_handlers import default_check_quota_handler

# pytest -s -v tests/test_default_check_quota_handler.py

# pytest -s -v tests/test_default_check_quota_handler.py::test_default_check_quota_handler
def test_default_check_quota_handler():

    config = Config()
    db_connection = get_mongodb_connection(config)

    user = login_user("alin@licenseware.io", "super-secret", config.AUTH_USER_LOGIN_URL)

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

    config = Config()
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
