import uuid
import pytest
from pymongo import MongoClient

from licenseware import Config, Quota, MongoRepository
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


def test_quota(mongo_connection):

    repo = MongoRepository(mongo_connection, collection=config.MONGO_COLLECTION.QUOTA)

    quota = Quota(
        tenant_id=str(uuid.uuid4()),
        authorization=str(uuid.uuid4()),
        uploader_id="rv_tools",
        default_units=1,
        db_connection=mongo_connection,
        config=config,
    )

    response = quota.init()
    assert response[1] == 200
    assert response[0]["monthly_quota_consumed"] == 0

    response = quota.update(units=2)
    assert response[1] == 200
    assert response[0]["monthly_quota_consumed"] == 2

    result = repo.find_one(filters=quota.quota_filters)
    assert result["monthly_quota_consumed"] == 2

    response = quota.update(units=2)
    assert response[1] == 200
    assert response[0]["monthly_quota_consumed"] == 4

    result = repo.find_one(filters=quota.quota_filters)
    assert result["monthly_quota_consumed"] == 4

    response = quota.check(units=2)
    assert response[1] == 200
    assert response[0]["monthly_quota_consumed"] == 4

    response = quota.reset()
    assert response["monthly_quota_consumed"] == 0

    response = quota.check(units=0)
    assert response[1] == 200
    assert response[0]["monthly_quota_consumed"] == 0

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
    assert response[1] == 200
    assert response[0]["quota_reset_date"] != past_isodate
    assert response[0]["monthly_quota_consumed"] == 0

    repo.update_one(
        filters=quota.quota_filters,
        data={
            "monthly_quota": 1,
            "monthly_quota_consumed": 5,
        },
    )

    response = quota.check(units=0)
    assert response[1] == 402
    assert response[0]["monthly_quota_consumed"] == 5

    response = quota.check(units=2)
    assert response[1] == 402
    assert response[0]["monthly_quota_consumed"] == 5

    response = quota.update(units=2)
    assert response[1] == 402
    assert response[0]["monthly_quota_consumed"] == 5

    response = quota.update(units=0)
    assert response[1] == 402
    assert response[0]["monthly_quota_consumed"] == 5
