import uuid
from dataclasses import dataclass

import pytest
from pymongo import MongoClient

from licenseware import MongoRepository, history
from licenseware.constants.base_types import BaseTypes
from licenseware.uploader.default_handlers.default_filecontents_validation_handler import (
    default_filecontents_validation_handler,
)
from licenseware.uploader.default_handlers.default_filenames_validation_handler import (
    default_filenames_validation_handler,
)


@pytest.fixture
def mongo_connection():
    MONGO_DATABASE_NAME = "testdb"
    MONGO_CONNECTION_STRING = "mongodb://lware:lware-secret@localhost:27017"
    mongo_connection = MongoClient(MONGO_CONNECTION_STRING)[MONGO_DATABASE_NAME]
    return mongo_connection


class Collections(BaseTypes):
    MONGO_COLLECTION_DATA_NAME = "Data"
    MONGO_COLLECTION_UTILIZATION_NAME = "Quota"
    MONGO_COLLECTION_HISTORY_NAME = "ProcessingHistory"
    MONGO_COLLECTION_UPLOADERS_STATUS_NAME = "UploadersStatus"
    MONGO_COLLECTION_REPORT_SNAPSHOTS_NAME = "ReportSnapshots"
    MONGO_COLLECTION_FEATURES_NAME = "Features"
    MONGO_COLLECTION_TOKEN_NAME = "Tokens"
    # Outdated
    MONGO_COLLECTION_ANALYSIS_NAME = "History"


# pytest -s -v tests/test_history.py


# pytest -s -v tests/test_history.py::test_history_log_decorator
def test_history_log_decorator(mongo_connection):
    @dataclass
    class Config:
        pass

    Config()
    MongoRepository(mongo_connection)

    history.log_filename_validation()


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
