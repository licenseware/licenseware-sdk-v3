from typing import Callable, List, Tuple, Union

from pymongo.collection import Collection

from licenseware.repository.repository_interface import RepositoryInterface

from . import utils


class MongoRepository(RepositoryInterface):
    def __init__(self, db_connection) -> None:
        self.db = db_connection

    # RAW

    def execute_query(self, table_or_collection: str, query: List[dict]):
        col: Collection = self.db[table_or_collection]
        cursor = col.aggregate(pipeline=query)
        return [
            {**doc, **{"_id": utils.get_object_id_str(doc["_id"])}} for doc in cursor
        ]

    # finding data

    def find_one(self, table_or_collection: str, filters: dict) -> dict:
        col: Collection = self.db[table_or_collection]
        data = col.find_one(filters)
        data["_id"] = utils.get_object_id_str(data["_id"])
        return data

    def find_by_id(self, table_or_collection: str, id: str) -> dict:
        col: Collection = self.db[table_or_collection]
        data = col.find_one({"_id": utils.get_object_id(id)})
        data["_id"] = utils.get_object_id_str(data["_id"])
        return data

    def find_many(
        self,
        table_or_collection: str,
        filters: dict,
        limit: int = 0,
        skip: int = 0,
        sort: List[Tuple[str, int]] = None,
    ) -> List[dict]:
        col: Collection = self.db[table_or_collection]

        if "_id" in filters:
            filters["_id"] = utils.get_object_id(filters["_id"])

        cursor = col.find(filter=filters, skip=skip, limit=limit, sort=sort)

        return [
            {**doc, **{"_id": utils.get_object_id_str(doc["_id"])}} for doc in cursor
        ]

    def distinct(
        self, table_or_collection: str, field: str, filters: dict = None
    ) -> List[str]:
        col: Collection = self.db[table_or_collection]

        if filters is not None:
            if "_id" in filters:
                filters["_id"] = utils.get_object_id(filters["_id"])

        cursor = col.distinct(key=field, filter=filters)
        return cursor

    def count(self, table_or_collection: str, filters: dict = None) -> int:
        col: Collection = self.db[table_or_collection]

        if filters is None:
            filters = {}

        return col.count_documents(filter=filters)

    # Inserting new data

    def insert_one(
        self, table_or_collection: str, data_validator: Callable, data: dict
    ) -> dict:
        data_validator(data)
        col: Collection = self.db[table_or_collection]
        col.insert_one(data)
        data["_id"] = utils.get_object_id_str(data["_id"])
        return data

    def insert_with_id(
        self,
        table_or_collection: str,
        id: Union[str, int],
        data_validator: Callable,
        data: dict,
        overwrite: bool = False,
    ) -> dict:
        data_validator(data)
        col: Collection = self.db[table_or_collection]
        data["_id"] = utils.get_object_id(id)
        if overwrite:
            col.delete_one({"_id": data["_id"]})
        col.insert_one(data)
        return data

    def insert_many(
        self,
        table_or_collection: str,
        data_validator: Callable,
        data: List[dict],
        overwrite: bool = False,
    ) -> List[dict]:
        data_validator(data)
        col: Collection = self.db[table_or_collection]
        if overwrite:
            col.delete_many(
                {"_id": {"$in": [utils.get_object_id(d["_id"]) for d in data]}}
            )
        col.insert_many(data)
        data = [{**d, **{"_id": utils.get_object_id_str(d["_id"])}} for d in data]
        return data

    # Updating existing data

    def update_one(
        self,
        table_or_collection: str,
        filters: dict,
        data_validator: Callable,
        data: dict,
        append: bool = False,
    ) -> dict:
        ...

    def update_on_id(
        self,
        table_or_collection: str,
        id: Union[str, int],
        data_validator: Callable,
        data: dict,
    ):
        ...

    def update_many(
        self,
        table_or_collection: str,
        filters: dict,
        data_validator: Callable,
        data: List[dict],
    ):
        ...

    def replace_one(
        self,
        table_or_collection: str,
        filters: dict,
        data_validator: Callable,
        data: List[dict],
    ):
        ...

    def replace_on_id(
        self,
        table_or_collection: str,
        id: str,
        data_validator: Callable,
        data: List[dict],
    ):
        ...

    def replace_many(
        self,
        table_or_collection: str,
        filters: dict,
        data_validator: Callable,
        data: List[dict],
    ):
        ...

    # Deleting existing data

    def delete(self, table_or_collection: str, filters: dict, first: bool = False):
        ...

    def delete_one(self, table_or_collection: str, **filters):
        ...

    def delete_by_id(self, table_or_collection: str, id: str):
        ...

    def delete_many(self, table_or_collection: str, **filters):
        ...
