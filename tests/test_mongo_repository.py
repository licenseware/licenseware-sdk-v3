import unittest

import pymongo
import pytest
from bson.objectid import ObjectId
from pymongo import MongoClient
from pymongo.collection import Collection

from licenseware import MongoRepository
from licenseware.repository.mongo_repository import utils

# pytest -s -v tests/test_mongo_repository.py

t = unittest.TestCase()


@pytest.fixture
def mongo_connection():
    MONGO_DATABASE_NAME = "testdb"
    MONGO_CONNECTION_STRING = "mongodb://lware:lware-secret@localhost:27017"
    mongo_connection = MongoClient(MONGO_CONNECTION_STRING)[MONGO_DATABASE_NAME]
    return mongo_connection


# pytest -s -v tests/test_mongo_repository.py::test_get_object_id_str
def test_get_object_id_str():

    stroid = utils.get_object_id_str(ObjectId("62fe1ef69474f79fe0dca114"))
    assert isinstance(stroid, str)

    stroid = utils.get_object_id_str("62fe1ef69474f79fe0dca114")
    assert isinstance(stroid, str)


# pytest -s -v tests/test_mongo_repository.py::test_get_object_id
def test_get_object_id():

    oid = utils.get_object_id("62fe1ef69474f79fe0dca114")
    assert isinstance(oid, ObjectId)

    oid = utils.get_object_id("4f1daa7c-d032-4e20-a6a2-4445eb576b89")
    assert isinstance(oid, str)

    oid = utils.get_object_id("some-custom-id-str")
    assert isinstance(oid, str)

    oid = utils.get_object_id(1)
    assert isinstance(oid, int)


# pytest -s -v tests/test_mongo_repository.py::test_add_update_operators
def test_add_update_operators():

    # TODO - by default $set operator is used,
    # but a way to traverse the dict and create a update query may be possible

    data = {
        "field1": 1,
        "some_list_int": [1, 2, 3],
        "some_list_dict": [
            {"simplefield1": 1},
            {"simplefield2": 2},
            {"simplefield3": 3},
        ],
        "some_list_dict_nested": [
            {"nestedfield1": [{"nestedfield1": 5}]},
            {"simplefield2": 2},
            {"simplefield3": 3},
        ],
    }

    update_query = utils.add_update_operators(data, append=False)

    # print(update_query)

    assert "$set" in update_query


# pytest -s -v tests/test_mongo_repository.py::test_mongo_raw_connection
def test_mongo_raw_connection(mongo_connection):

    mongo_connection["TestCollection"].insert_one({"test": "data"})
    result = mongo_connection["TestCollection"].find_one({"test": "data"})

    assert "_id" in result

    mongo_connection["TestCollection"].delete_one({"test": "data"})

    result = mongo_connection["TestCollection"].find_one({"test": "data"})
    assert result is None


# pytest -s -v tests/test_mongo_repository.py::test_mongo_repository_insert_one
def test_mongo_repository_insert_one(mongo_connection):

    repo = MongoRepository(mongo_connection)

    def data_validator_func(_data):
        assert "field_name" in _data
        return _data

    data_to_insert = {"field_name": "some_data"}

    inserted_data = repo.insert_one(
        "TestCollection", data_validator_func, data_to_insert
    )

    # print(inserted_data)
    # print(data_to_insert)

    # Using deepcopy is pretty slow, this is a quirk to keep in mind
    assert inserted_data == data_to_insert

    assert "_id" in inserted_data
    assert "field_name" in inserted_data


# pytest -s -v tests/test_mongo_repository.py::test_mongo_repository_insert_one_with_id
def test_mongo_repository_insert_one_with_id(mongo_connection):

    repo = MongoRepository(mongo_connection)

    def data_validator_func(_data):
        assert "field_name" in _data
        return _data

    data_to_insert = {"field_name": "some_data"}

    inserted_data = repo.insert_with_id(
        "TestCollection",
        "custom-id",
        data_validator_func,
        data_to_insert,
        overwrite=False,
    )

    # print(inserted_data)
    # print(data_to_insert)

    assert "_id" in inserted_data
    assert "field_name" in inserted_data

    with t.assertRaises(pymongo.errors.DuplicateKeyError):
        inserted_data1 = repo.insert_with_id(
            "TestCollection",
            "custom-id",
            data_validator_func,
            data_to_insert,
            overwrite=False,
        )

    inserted_data2 = repo.insert_with_id(
        "TestCollection",
        "custom-id",
        data_validator_func,
        data_to_insert,
        overwrite=True,
    )

    assert "_id" in inserted_data2
    assert "field_name" in inserted_data2

    inserted_data3 = repo.insert_with_id(
        "TestCollection",
        "62fe1ef69474f79fe0dca114",
        data_validator_func,
        data_to_insert,
        overwrite=False,
    )

    assert "_id" in inserted_data3
    assert "field_name" in inserted_data3

    inserted_data4 = repo.insert_with_id(
        "TestCollection",
        "62fe1ef69474f79fe0dca114",
        data_validator_func,
        data_to_insert,
        overwrite=True,
    )

    assert "_id" in inserted_data4
    assert "field_name" in inserted_data4


# pytest -s -v tests/test_mongo_repository.py::test_mongo_repository_db_raw_operations
def test_mongo_repository_db_raw_operations(mongo_connection):

    repo = MongoRepository(mongo_connection)

    col: Collection = repo.db["TestCollection"]
    col.drop()
    docs = col.count_documents({})

    assert docs == 0


# pytest -s -v tests/test_mongo_repository.py::test_mongo_repository_insert_many
def test_mongo_repository_insert_many(mongo_connection):

    repo = MongoRepository(mongo_connection)

    def data_validator_func(_data):
        for d in _data:
            assert "field_name" in d
        return _data

    data_to_insert = [
        {"field_name": "some_data1"},
        {"field_name": "some_data2"},
        {"field_name": "some_data3"},
        {"field_name": "some_data4"},
    ]

    inserted_data = repo.insert_many(
        "TestCollection",
        data_validator_func,
        data_to_insert,
        overwrite=False,
    )

    # print(inserted_data)

    assert len(inserted_data) == 4
    assert isinstance(inserted_data[0]["_id"], str)


# pytest -s -v tests/test_mongo_repository.py::test_mongo_repository_find
def test_mongo_repository_find(mongo_connection):

    repo = MongoRepository(mongo_connection)

    results = repo.find_one("TestCollection", {"field_name": "some_data1"})
    assert isinstance(results["_id"], str)

    res1 = repo.find_by_id("TestCollection", id=results["_id"])
    assert isinstance(res1["_id"], str)

    resmany = repo.find_many("TestCollection", {})

    assert len(resmany) > 0
    assert isinstance(resmany[0]["_id"], str)

    resmany1 = repo.find_many(
        "TestCollection",
        {},
        sort=[("field_name", pymongo.ASCENDING), ("_id", pymongo.DESCENDING)],
    )

    assert len(resmany1) > 0


# pytest -s -v tests/test_mongo_repository.py::test_mongo_repository_distinct
def test_mongo_repository_distinct(mongo_connection):

    repo = MongoRepository(mongo_connection)

    results = repo.distinct(
        "TestCollection",
        field="field_name",
    )

    assert isinstance(results, list)
    assert len(results) > 0
    assert len(set(results)) == len(results)

    results1 = repo.distinct(
        "TestCollection",
        field="field_name",
        filters={"field_name": "some_data1"},
    )

    assert len(set(results1)) == 1

    docs = repo.count("TestCollection")

    assert isinstance(docs, int)
    assert docs > 0


# pytest -s -v tests/test_mongo_repository.py::test_mongo_repository_execute_query
def test_mongo_repository_execute_query(mongo_connection):

    repo = MongoRepository(mongo_connection)

    results = repo.execute_query(
        "TestCollection",
        [
            {
                "$match": {"field_name": "some_data1"},
            }
        ],
    )

    assert isinstance(results, list)
    assert len(results) > 0


# pytest -s -v tests/test_mongo_repository.py::test_mongo_repository_update_one
def test_mongo_repository_update_one(mongo_connection):

    repo = MongoRepository(mongo_connection)

    result = repo.update_one(
        "TestCollection",
        filters={"field_name": "some_data1"},
        data={"field_name": "some_data_updated1"},
        data_validator=None,
    )

    # print(result)
    assert result["field_name"] == "some_data_updated1"


# pytest -s -v tests/test_mongo_repository.py::test_mongo_repository_update_on_id
def test_mongo_repository_update_on_id(mongo_connection):

    repo = MongoRepository(mongo_connection)

    result = repo.update_on_id(
        "TestCollection",
        id="somssse-id",
        data={"field_name": "some_data1"},
        data_validator=None,
        upsert=True,
    )

    # print(result)
    assert result["field_name"] == "some_data1"


# pytest -s -v tests/test_mongo_repository.py::test_mongo_repository_update_many
def test_mongo_repository_update_many(mongo_connection):

    repo = MongoRepository(mongo_connection)

    result = repo.update_many(
        "TestCollection",
        filters={"field_name": "some_data1"},
        data={"field_name": "some_data_reupdated_1"},
        data_validator=None,
    )

    # print(result)
    assert result > 0


# pytest -s -v tests/test_mongo_repository.py::test_mongo_repository_replace_one
def test_mongo_repository_replace_one(mongo_connection):

    repo = MongoRepository(mongo_connection)

    result = repo.replace_one(
        "TestCollection",
        filters={"field_name": "some_data1"},
        data={"field_name": "some_data_reupdated_1"},
        data_validator=None,
    )

    # print(result)
    assert isinstance(result, dict)
    assert result["field_name"] == "some_data_reupdated_1"


# pytest -s -v tests/test_mongo_repository.py::test_mongo_repository_replace_on_id
def test_mongo_repository_replace_on_id(mongo_connection):

    repo = MongoRepository(mongo_connection)

    result = repo.replace_on_id(
        "TestCollection",
        id="some-id",
        data={"field_name": "some_data_reupdated_1"},
        data_validator=None,
    )

    # print(result)
    assert isinstance(result, dict)
    assert result["field_name"] == "some_data_reupdated_1"


# pytest -s -v tests/test_mongo_repository.py::test_mongo_repository_replace_many
def test_mongo_repository_replace_many(mongo_connection):

    repo = MongoRepository(mongo_connection)

    result = repo.replace_many(
        "TestCollection",
        filters={"field_name": "some_data1"},
        data={"field_name": "some_data_reupdated_1"},
        data_validator=None,
    )

    # print(result)
    assert result > 0


# pytest -s -v tests/test_mongo_repository.py::test_mongo_repository_delete_one
def test_mongo_repository_delete_one(mongo_connection):

    repo = MongoRepository(mongo_connection)

    repo.insert_one(
        "TestCollection", data_validator=None, data={"field_name": "some_data1"}
    )

    result = repo.delete_one(
        "TestCollection",
        filters={"field_name": "some_data1"},
    )

    # print(result)
    assert result > 0


# pytest -s -v tests/test_mongo_repository.py::test_mongo_repository_delete_on_id
def test_mongo_repository_delete_on_id(mongo_connection):

    repo = MongoRepository(mongo_connection)

    data = repo.insert_one(
        "TestCollection", data_validator=None, data={"field_name": "some_data1"}
    )

    result = repo.delete_on_id(
        "TestCollection",
        id=data["_id"],
    )

    # print(result)
    assert result > 0


# pytest -s -v tests/test_mongo_repository.py::test_mongo_repository_delete_many
def test_mongo_repository_delete_many(mongo_connection):

    repo = MongoRepository(mongo_connection)

    repo.insert_many(
        "TestCollection",
        data_validator=None,
        data=[
            {"field_name": "some_data1"},
            {"field_name": "some_data2"},
        ],
    )

    result = repo.delete_many(
        "TestCollection",
        filters={"field_name": {"$exists": True}},
    )

    # print(result)
    assert result > 0
