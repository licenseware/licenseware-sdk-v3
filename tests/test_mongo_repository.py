import pytest
import unittest
from pymongo import MongoClient
from licenseware import MongoRepository
from licenseware.repository.mongo_repository import utils

import json
from bson.json_util import dumps
from bson.objectid import ObjectId
from typing import Union


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


# pytest -s -v tests/test_mongo_repository.py::test_mongo_raw_connection
def test_mongo_raw_connection(mongo_connection):

    mongo_connection["TestCollection"].insert_one({"test": "data"})
    result = mongo_connection["TestCollection"].find_one({"test": "data"})

    assert "_id" in result

    mongo_connection["TestCollection"].delete_one({"test": "data"})

    result = mongo_connection["TestCollection"].find_one({"test": "data"})
    assert result is None


# pytest -s -v tests/test_mongo_repository.py::test_mongo_repository
def test_mongo_repository(mongo_connection):

    repo = MongoRepository(mongo_connection)

    def data_validator_func(_data):
        assert "field_name" in _data

    data = {"field_name": "some_data"}

    inserted_data = repo.insert_one("TestCollection", data_validator_func, data)

    print(inserted_data)
