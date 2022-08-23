import uuid

import pytest
from pymongo import MongoClient

from licenseware import Config, MongoRepository, history


@pytest.fixture
def mongo_connection():
    MONGO_DATABASE_NAME = "testdb"
    MONGO_CONNECTION_STRING = "mongodb://lware:lware-secret@localhost:27017"
    mongo_connection = MongoClient(MONGO_CONNECTION_STRING)[MONGO_DATABASE_NAME]
    return mongo_connection


# pytest -s -v tests/test_history.py


# pytest -s -v tests/test_history.py::test_history_log_filename_validation
def test_history_log_filename_validation(mongo_connection):
    class CustomConfig(Config):
        pass

    config = CustomConfig()

    history_repo = MongoRepository(
        mongo_connection, collection=config.MONGO_COLLECTION.HISTORY
    )

    response = history.log_filename_validation(
        tenant_id=str(uuid.uuid4()),
        event_id=str(uuid.uuid4()),
        uploader_id="rv_tools",
        app_id="ifmp-service",
        filename_validation=[
            {
                "status": "success",
                "filename": "okfile.csv",
                "message": "file ok",
            }
        ],
        repo=history_repo,
    )

    # print(response)
    assert "filename_validation" in response


# pytest -s -v tests/test_history.py::test_history_log_filecontent_validation
def test_history_log_filecontent_validation(mongo_connection):
    class CustomConfig(Config):
        pass

    config = CustomConfig()

    history_repo = MongoRepository(
        mongo_connection, collection=config.MONGO_COLLECTION.HISTORY
    )

    response = history.log_filecontent_validation(
        tenant_id=str(uuid.uuid4()),
        event_id=str(uuid.uuid4()),
        uploader_id="rv_tools",
        app_id="ifmp-service",
        filecontent_validation=[
            {
                # status = fields.String()
                # filename = fields.String()
                # filepath = fields.String()
                # message = fields.String()
            }
        ],
        filepaths=["./file1.csv"],
        repo=history_repo,
    )

    # print(response)
    assert "filename_validation" in response


# pytest -s -v tests/test_history.py::test_history_log_success
def test_history_log_success(mongo_connection):

    repo = MongoRepository(mongo_connection)

    response = history.log_success(
        func="some_processing_func_name",
        tenant_id=str(uuid.uuid4()),
        event_id=str(uuid.uuid4()),
        uploader_id="some_uploader_id",
        app_id="ifmp-service",
        filepath="./somefile.xlsx",
        repo=repo,
        on_success_save={"save": "this"},
    )

    # print(response)

    result = repo.find_one(
        filters={"tenant_id": response["tenant_id"]},
        collection=repo.collections.MONGO_COLLECTION_HISTORY_NAME,
    )
    assert result


# pytest -s -v tests/test_history.py::test_history_log_failure
def test_history_log_failure(mongo_connection):

    repo = MongoRepository(mongo_connection)

    response = history.log_failure(
        func="some_processing_func_name",
        tenant_id=str(uuid.uuid4()),
        event_id=str(uuid.uuid4()),
        uploader_id="some_uploader_id",
        app_id="fomo-service",
        filepath="./somefile.csv",
        error_string="missing headers",
        traceback_string=None,
        repo=repo,
        on_failure_save={"save": "this failure"},
    )

    # print(response)

    result = repo.find_one(
        filters={"tenant_id": response["tenant_id"]},
        collection=repo.collections.MONGO_COLLECTION_HISTORY_NAME,
    )
    assert result

    {
        "callable": "some_processing_func_name",
        "step": "some_processing_func_name",
        "source": None,
        "tenant_id": "1015246f-f7a3-417f-be7f-af81aaf48076",
        "event_id": "f215d3c0-6ef9-4666-acac-559e499b1423",
        "app_id": "fomo-service",
        "uploader_id": "some_uploader_id",
        "filepath": "./somefile.csv",
        "file_name": "somefile.csv",
    }


# pytest -s -v tests/test_history.py::test_history_entities
def test_history_entities(mongo_connection):

    repo = MongoRepository(mongo_connection)

    response_failure = history.log_failure(
        func="some_processing_func_name",
        tenant_id=str(uuid.uuid4()),
        event_id=str(uuid.uuid4()),
        uploader_id="some_uploader_id",
        app_id="fomo-service",
        filepath="./somefile.csv",
        error_string="missing headers",
        traceback_string=None,
        repo=repo,
        on_failure_save={"save": "this failure"},
    )

    response = history.add_entities(
        event_id=response_failure["event_id"],
        entities=[str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4())],
        repo=repo,
    )

    # print(response)

    assert isinstance(response["entities"], list)
    assert len(response["entities"]) == 3

    response_remove = history.remove_entities(
        event_id=response["event_id"],
        entities=response["entities"],
        repo=repo,
    )

    # print(response_remove)

    assert isinstance(response_remove["entities"], list)
    assert len(response_remove["entities"]) == 0

    repo.delete_many(filters={}, collection=Collections.MONGO_COLLECTION_HISTORY_NAME)
