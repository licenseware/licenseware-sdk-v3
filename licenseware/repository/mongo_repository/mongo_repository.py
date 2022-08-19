from typing import Callable, List, Tuple, Union

from pymongo.collection import Collection

from licenseware.repository.repository_interface import RepositoryInterface

from . import utils


class MongoRepository(RepositoryInterface):
    def __init__(self, db_connection) -> None:
        self.db = db_connection

    # RAW

    def execute_query(self, collection: str, query: List[dict]):
        col: Collection = self.db[collection]
        cursor = col.aggregate(pipeline=query, allowDiskUse=True)
        return [
            {**doc, **{"_id": utils.get_object_id_str(doc["_id"])}} for doc in cursor
        ]

    # finding data

    def find_one(self, collection: str, filters: dict) -> dict:
        col: Collection = self.db[collection]
        data = col.find_one(filters)
        if data is None:
            return []
        data["_id"] = utils.get_object_id_str(data["_id"])
        return data

    def find_by_id(self, collection: str, id: str) -> dict:
        col: Collection = self.db[collection]
        data = col.find_one({"_id": utils.get_object_id(id)})
        if data is None:
            return []
        data["_id"] = utils.get_object_id_str(data["_id"])
        return data

    def find_many(
        self,
        collection: str,
        filters: dict,
        limit: int = 0,
        skip: int = 0,
        sort: List[Tuple[str, int]] = None,
    ) -> List[dict]:
        col: Collection = self.db[collection]

        if "_id" in filters:
            filters["_id"] = utils.get_object_id(filters["_id"])

        cursor = col.find(filter=filters, skip=skip, limit=limit, sort=sort)

        return [
            {**doc, **{"_id": utils.get_object_id_str(doc["_id"])}} for doc in cursor
        ]

    def distinct(self, collection: str, field: str, filters: dict = None) -> List[str]:
        col: Collection = self.db[collection]

        if filters is not None:
            if "_id" in filters:
                filters["_id"] = utils.get_object_id(filters["_id"])

        cursor = col.distinct(key=field, filter=filters)
        return cursor

    def count(self, collection: str, filters: dict = None) -> int:
        col: Collection = self.db[collection]

        if filters is None:
            filters = {}

        return col.count_documents(filter=filters)

    # Inserting new data

    def insert_one(self, collection: str, data_validator: Callable, data: dict) -> dict:
        if data_validator is not None:
            data = data_validator(data)
        col: Collection = self.db[collection]
        col.insert_one(data)
        data["_id"] = utils.get_object_id_str(data["_id"])
        return data

    def insert_with_id(
        self,
        collection: str,
        id: Union[str, int],
        data_validator: Callable,
        data: dict,
        overwrite: bool = False,
    ) -> dict:
        if data_validator is not None:
            data = data_validator(data)
        col: Collection = self.db[collection]
        data["_id"] = utils.get_object_id(id)
        if overwrite:
            col.delete_one({"_id": data["_id"]})
        col.insert_one(data)
        return data

    def insert_many(
        self,
        collection: str,
        data_validator: Callable,
        data: List[dict],
        overwrite: bool = False,
    ) -> List[dict]:
        if data_validator is not None:
            data = data_validator(data)
        col: Collection = self.db[collection]
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
        collection: str,
        filters: dict,
        data_validator: Callable,
        data: dict,
        append: bool = False,
        upsert: bool = True,
    ) -> dict:
        if data_validator is not None:
            data = data_validator(data)
        col: Collection = self.db[collection]
        col.update_one(
            filter=filters,
            update=utils.add_update_operators(data, append),
            upsert=upsert,
        )
        return self.find_one(collection, data)

    def update_on_id(
        self,
        collection: str,
        id: dict,
        data_validator: Callable,
        data: dict,
        append: bool = False,
        upsert: bool = True,
    ):
        if data_validator is not None:
            data = data_validator(data)
        col: Collection = self.db[collection]
        col.update_one(
            filter={"_id": utils.get_object_id(id)},
            update=utils.add_update_operators(data, append),
            upsert=upsert,
        )
        return self.find_one(collection, data)

    def update_many(
        self,
        collection: str,
        filters: dict,
        data_validator: Callable,
        data: dict,
        append: bool = False,
        upsert: bool = True,
    ):
        if data_validator is not None:
            data = data_validator(data)
        col: Collection = self.db[collection]
        col.update_many(
            filter=filters,
            update=utils.add_update_operators(data, append),
            upsert=upsert,
        )
        return self.find_many(collection, data)

    def replace_one(
        self,
        collection: str,
        filters: dict,
        data_validator: Callable,
        data: List[dict],
    ):
        ...

    def replace_on_id(
        self,
        collection: str,
        id: str,
        data_validator: Callable,
        data: List[dict],
    ):
        ...

    def replace_many(
        self,
        collection: str,
        filters: dict,
        data_validator: Callable,
        data: List[dict],
    ):
        ...

    # Deleting existing data

    def delete(self, collection: str, filters: dict, first: bool = False):
        ...

    def delete_one(self, collection: str, **filters):
        ...

    def delete_by_id(self, collection: str, id: str):
        ...

    def delete_many(self, collection: str, **filters):
        ...
