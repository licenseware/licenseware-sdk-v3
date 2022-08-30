import pytest
import uuid
from pymongo import MongoClient
from licenseware import ReportSnapshot, MongoRepository, Config

# pytest -s -v tests/test_report_snaphot.py


@pytest.fixture
def mongo_connection():
    MONGO_DATABASE_NAME = "testdb"
    MONGO_CONNECTION_STRING = "mongodb://lware:lware-secret@localhost:27017"
    mongo_connection = MongoClient(MONGO_CONNECTION_STRING)[MONGO_DATABASE_NAME]
    print(type(mongo_connection))
    return mongo_connection


def test_report_snaphot(mongo_connection):

    config = Config()

    # rs = ReportSnapshot(
    #     tenant_id=str(uuid.uuid4()),
    # )
