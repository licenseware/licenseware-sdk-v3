import pytest
from pymongo import MongoClient

from licenseware import Config, MongoRepository, Quota, login_user
from licenseware.config import config as cfg


class CustomConfig(Config):
    CURRENT_ENVIRONMENT: cfg.Environment = cfg.Environment.DESKTOP


config = CustomConfig()


@pytest.fixture
def mongo_connection():
    MONGO_DATABASE_NAME = "testdb"
    MONGO_CONNECTION_STRING = "mongodb://lware:lware-secret@localhost:27017"
    mongo_connection = MongoClient(MONGO_CONNECTION_STRING)[MONGO_DATABASE_NAME]
    return mongo_connection


# pytest -s -v tests/test_quota.py


# pytest -s -v tests/test_quota.py::test_quota
def test_quota(mongo_connection):

    repo = MongoRepository(mongo_connection, collection=config.MONGO_COLLECTION.QUOTA)

    user = login_user("alin@licenseware.io", "super-secret", config.AUTH_USER_LOGIN_URL)

    quota = Quota(
        tenant_id=user["TenantId"],
        authorization=user["Authorization"],
        uploader_id="rv_tools",
        free_units=1000,
        repo=repo,
        config=config,
    )

    response = quota.init()
    assert response.status_code == 200
    assert response.content.monthly_quota_consumed == 0

    response = quota.update(units=2)
    assert response.status_code == 200
    assert response.content.monthly_quota_consumed == 2

    result = repo.find_one(filters=quota.quota_filters)
    assert result["monthly_quota_consumed"] == 2

    response = quota.update(units=2)
    assert response.status_code == 200
    assert response.content.monthly_quota_consumed == 4

    result = repo.find_one(filters=quota.quota_filters)
    assert result["monthly_quota_consumed"] == 4

    response = quota.check(units=2)
    assert response.status_code == 200
    assert response.content.monthly_quota_consumed == 4

    response = quota.reset()
    assert response["monthly_quota_consumed"] == 0

    response = quota.check(units=0)
    assert response.status_code == 200
    assert response.content.monthly_quota_consumed == 0

    past_isodate = "2021-09-24T11:50:23.132560"
    repo.update_one(
        filters=quota.quota_filters,
        data={
            "monthly_quota": 1,
            "monthly_quota_consumed": 1,
            "quota_reset_date": past_isodate,
        },
    )

    response = quota.check(units=0)
    assert response.status_code == 200
    assert response.content.quota_reset_date != past_isodate
    assert response.content.monthly_quota_consumed == 0

    repo.update_one(
        filters=quota.quota_filters,
        data={
            "monthly_quota": 1,
            "monthly_quota_consumed": 5,
        },
    )

    response = quota.check(units=0)
    assert response.status_code == 402
    assert response.content.monthly_quota_consumed == 5

    response = quota.check(units=2)
    assert response.status_code == 402
    assert response.content.monthly_quota_consumed == 5

    response = quota.update(units=2)
    assert response.status_code == 402
    assert response.content.monthly_quota_consumed == 5

    response = quota.update(units=0)
    assert response.status_code == 402
    assert response.content.monthly_quota_consumed == 5

    repo.delete_many({})
