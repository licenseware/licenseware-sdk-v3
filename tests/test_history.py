import uuid

import pytest
from pymongo import MongoClient

from licenseware import Config, History, MongoRepository, history


@pytest.fixture
def mongo_connection():
    MONGO_DATABASE_NAME = "testdb"
    MONGO_CONNECTION_STRING = "mongodb://lware:lware-secret@localhost:27017"
    mongo_connection = MongoClient(MONGO_CONNECTION_STRING)[MONGO_DATABASE_NAME]
    return mongo_connection


# pytest -s -v tests/test_history.py


# pytest -s -v tests/test_history.py::test_history_class_log_filename_validation
def test_history_class_log_filename_validation(mongo_connection):
    class CustomConfig(Config):
        pass

    config = CustomConfig()

    history_repo = MongoRepository(
        mongo_connection, collection=config.MONGO_COLLECTION.HISTORY
    )

    history = History(
        tenant_id=str(uuid.uuid4()),
        authorization=str(uuid.uuid4()),
        event_id=str(uuid.uuid4()),
        uploader_id="rv_tools",
        app_id="ifmp-service",
        repo=history_repo,
    )

    response = history.log_filename_validation(
        validation_response=[
            {
                "status": "success",
                "filename": "okfile.csv",
                "message": "file ok",
            }
        ]
    )

    assert "filename_validation" in response


# pytest -s -v tests/test_history.py::test_history_class_log_filecontent_validation
def test_history_class_log_filecontent_validation(mongo_connection):
    class CustomConfig(Config):
        pass

    config = CustomConfig()

    history_repo = MongoRepository(
        mongo_connection, collection=config.MONGO_COLLECTION.HISTORY
    )

    history = History(
        tenant_id=str(uuid.uuid4()),
        authorization=str(uuid.uuid4()),
        event_id=str(uuid.uuid4()),
        uploader_id="rv_tools",
        app_id="ifmp-service",
        repo=history_repo,
    )

    response = history.log_filecontent_validation(
        validation_response=[
            {
                "status": "success",
                "filename": "okfile.csv",
                "message": "file ok",
            }
        ],
        filepaths=["./okfile.csv"],
    )

    assert "filecontent_validation" in response


# pytest -s -v tests/test_history.py::test_history_class_log_success
def test_history_class_log_success(mongo_connection):
    class CustomConfig(Config):
        pass

    config = CustomConfig()

    history_repo = MongoRepository(
        mongo_connection, collection=config.MONGO_COLLECTION.HISTORY
    )

    history = History(
        tenant_id=str(uuid.uuid4()),
        authorization=str(uuid.uuid4()),
        event_id=str(uuid.uuid4()),
        uploader_id="rv_tools",
        app_id="ifmp-service",
        repo=history_repo,
    )

    response = history.log_success(
        step="Gathering data",
        filepath="./somecsv.csv",
        on_success_save=None,
        func_source="app/some_package/some_module/some_func",
    )

    assert "step" in response


# pytest -s -v tests/test_history.py::test_history_class_log_failure
def test_history_class_log_failure(mongo_connection):
    class CustomConfig(Config):
        pass

    config = CustomConfig()

    history_repo = MongoRepository(
        mongo_connection, collection=config.MONGO_COLLECTION.HISTORY
    )

    history = History(
        tenant_id=str(uuid.uuid4()),
        authorization=str(uuid.uuid4()),
        event_id=str(uuid.uuid4()),
        uploader_id="rv_tools",
        app_id="ifmp-service",
        repo=history_repo,
    )

    response = history.log_failure(
        step="Gathering data",
        filepath="./file.csv",
        error_string="str(err)",
        traceback_string="import traceback > traceback.format_exc(err)",
        on_failure_save="Faled gathering data",
        func_source="app/some_package/some_module/some_func",
    )

    assert "step" in response


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
                "status": "success",
                "filename": "file.csv",
                "message": "File is ok",
            }
        ],
        filepaths=["./file1.csv"],
        repo=history_repo,
    )

    # print(response)
    assert "filecontent_validation" in response


# pytest -s -v tests/test_history.py::test_history_log_success
def test_history_log_success(mongo_connection):
    class CustomConfig(Config):
        pass

    config = CustomConfig()

    repo = MongoRepository(mongo_connection, collection=config.MONGO_COLLECTION.HISTORY)

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
        collection=config.MONGO_COLLECTION.HISTORY,
    )
    assert result


# pytest -s -v tests/test_history.py::test_history_log_failure
def test_history_log_failure(mongo_connection):
    class CustomConfig(Config):
        pass

    config = CustomConfig()

    repo = MongoRepository(mongo_connection, collection=config.MONGO_COLLECTION.HISTORY)

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
        collection=config.MONGO_COLLECTION.HISTORY,
    )
    assert result


# pytest -s -v tests/test_history.py::test_history_entities
def test_history_entities(mongo_connection):
    class CustomConfig(Config):
        pass

    config = CustomConfig()

    repo = MongoRepository(mongo_connection, collection=config.MONGO_COLLECTION.HISTORY)

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

    repo.delete_many(filters={}, collection=config.MONGO_COLLECTION.HISTORY)


# pytest -s -v tests/test_history.py::test_history_class_entities
def test_history_class_entities(mongo_connection):
    class CustomConfig(Config):
        pass

    config = CustomConfig()

    history_repo = MongoRepository(
        mongo_connection, collection=config.MONGO_COLLECTION.HISTORY
    )

    history = History(
        tenant_id=str(uuid.uuid4()),
        authorization=str(uuid.uuid4()),
        event_id=str(uuid.uuid4()),
        uploader_id="rv_tools",
        app_id="ifmp-service",
        repo=history_repo,
    )

    response_failure = history.log_failure(
        step="Gathering data",
        filepath="./file.csv",
        error_string="str(err)",
        traceback_string="import traceback > traceback.format_exc(err)",
        on_failure_save="Faled gathering data",
        func_source="app/some_package/some_module/some_func",
    )

    assert "step" in response_failure

    response = history.add_entities(
        entities=[str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4())],
    )

    # print(response)

    assert isinstance(response["entities"], list)
    assert len(response["entities"]) == 3

    response_remove = history.remove_entities(
        entities=response["entities"],
    )

    # print(response_remove)

    assert isinstance(response_remove["entities"], list)
    assert len(response_remove["entities"]) == 0

    history_repo.delete_many(filters={}, collection=config.MONGO_COLLECTION.HISTORY)
