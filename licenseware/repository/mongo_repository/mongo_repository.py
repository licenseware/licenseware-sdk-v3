from typing import Callable, List, Tuple, Union

from pymongo.collection import Collection
from pymongo.cursor import Cursor

from licenseware.repository.repository_interface import RepositoryInterface

from . import utils


class MongoRepository(RepositoryInterface):
    def __init__(self, db_connection) -> None:
        self.db = db_connection

    def _setid(self, data: dict):
        if data is None:  # pragma no cover
            return {}
        data["_id"] = utils.get_object_id_str(data["_id"])
        return data

    def _setids(self, cursor: Cursor):
        return [
            {**doc, **{"_id": utils.get_object_id_str(doc["_id"])}} for doc in cursor
        ]

    # RAW

    def execute_query(self, collection: str, query: List[dict]):
        col: Collection = self.db[collection]
        cursor = col.aggregate(pipeline=query, allowDiskUse=True)
        return self._setids(cursor)

    # finding data

    def find_one(self, collection: str, filters: dict) -> dict:
        col: Collection = self.db[collection]
        data = col.find_one(filters)
        return self._setid(data)

    def find_by_id(self, collection: str, id: str) -> dict:
        col: Collection = self.db[collection]
        data = col.find_one({"_id": utils.get_object_id(id)})
        return self._setid(data)

    def find_many(
        self,
        collection: str,
        filters: dict,
        limit: int = 0,
        skip: int = 0,
        sort: List[Tuple[str, int]] = None,
    ) -> List[dict]:
        col: Collection = self.db[collection]

        if "_id" in filters:  # pragma no cover
            filters["_id"] = utils.get_object_id(filters["_id"])

        cursor = col.find(filter=filters, skip=skip, limit=limit, sort=sort)
        return self._setids(cursor)

    def distinct(self, collection: str, field: str, filters: dict = None) -> List[str]:
        col: Collection = self.db[collection]

        if filters is not None:  # pragma no cover
            if "_id" in filters:
                filters["_id"] = utils.get_object_id(filters["_id"])

        data = col.distinct(key=field, filter=filters)
        return data

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
        if overwrite:  # pragma no cover
            col.delete_many(
                {"_id": {"$in": [utils.get_object_id(d["_id"]) for d in data]}}
            )
        col.insert_many(data)
        return self._setids(data)

    # Updating existing data

    def update_one(
        self,
        collection: str,
        filters: dict,
        data_validator: Callable,
        data: dict,
        append: bool = False,
        upsert: bool = True,
        array_filters: List[dict] = None,
    ) -> dict:
        if data_validator is not None:  # pragma no cover
            data = data_validator(data)
        col: Collection = self.db[collection]
        data = col.find_one_and_update(
            filter=filters,
            update=utils.add_update_operators(data, append),
            upsert=upsert,
            array_filters=array_filters,
            return_document=True,
        )
        return self._setid(data)

    def update_on_id(
        self,
        collection: str,
        id: str,
        data_validator: Callable,
        data: dict,
        append: bool = False,
        upsert: bool = True,
        array_filters: List[dict] = None,
    ) -> dict:
        if data_validator is not None:  # pragma no cover
            data = data_validator(data)
        col: Collection = self.db[collection]
        data = col.find_one_and_update(
            filter={"_id": utils.get_object_id(id)},
            update=utils.add_update_operators(data, append),
            upsert=upsert,
            array_filters=array_filters,
            return_document=True,
        )
        return self._setid(data)

    def update_many(
        self,
        collection: str,
        filters: dict,
        data_validator: Callable,
        data: List[dict],
        append: bool = False,
        upsert: bool = True,
        array_filters: List[dict] = None,
    ) -> int:
        if data_validator is not None:  # pragma no cover
            data = data_validator(data)
        col: Collection = self.db[collection]
        return col.update_many(
            filter=filters,
            update=utils.add_update_operators(data, append),
            upsert=upsert,
            array_filters=array_filters,
        ).matched_count

    def replace_one(
        self,
        collection: str,
        filters: dict,
        data_validator: Callable,
        data: dict,
        upsert: bool = True,
    ) -> dict:
        if data_validator is not None:
            data = data_validator(data)
        col: Collection = self.db[collection]
        data = col.find_one_and_replace(
            filter=filters,
            replacement=data,
            upsert=upsert,
            return_document=True,
        )
        return self._setid(data)

    def replace_on_id(
        self,
        collection: str,
        id: str,
        data_validator: Callable,
        data: dict,
        upsert: bool = True,
    ) -> dict:
        if data_validator is not None:
            data = data_validator(data)
        col: Collection = self.db[collection]
        data = col.find_one_and_replace(
            filter={"_id": utils.get_object_id(id)},
            replacement=data,
            upsert=upsert,
            return_document=True,
        )
        return self._setid(data)

    def replace_many(
        self,
        collection: str,
        filters: dict,
        data_validator: Callable,
        data: dict,
        upsert: bool = True,
    ) -> int:
        if data_validator is not None:
            data = data_validator(data)
        col: Collection = self.db[collection]
        deleted_count = col.delete_many(filter=filters).deleted_count
        modified_count = col.update_many(
            filter=filters,
            update=utils.add_update_operators(data, False),
            upsert=upsert,
        ).modified_count
        return deleted_count or modified_count or int(upsert)

    # Deleting existing data

    def delete_one(self, collection: str, filters: dict) -> int:
        col: Collection = self.db[collection]
        return col.delete_one(filter=filters).deleted_count

    def delete_on_id(self, collection: str, id: str) -> int:
        col: Collection = self.db[collection]
        return col.delete_one(filter={"_id": utils.get_object_id(id)}).deleted_count

    def delete_many(self, collection: str, filters: dict) -> int:
        col: Collection = self.db[collection]
        return col.delete_many(filter=filters).deleted_count
