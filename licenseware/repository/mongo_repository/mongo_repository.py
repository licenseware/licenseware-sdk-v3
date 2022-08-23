from typing import Callable, List, Tuple, Union

from pymongo.collection import Collection
from pymongo.cursor import Cursor

from licenseware.repository.repository_interface import RepositoryInterface
from licenseware.utils.logger import log

from . import utils


class MongoRepository(RepositoryInterface):
    def __init__(
        self,
        db_connection,
        collection: str = None,
        data_validator: Callable = None,
    ):
        self.db_connection = db_connection
        self.collection = collection
        self.data_validator = data_validator

    def _setid(self, data: dict):
        if data is None:  # pragma no cover
            return {}
        data["_id"] = utils.get_object_id_str(data["_id"])
        return data

    def _setids(self, cursor: Cursor):
        return [
            {**doc, **{"_id": utils.get_object_id_str(doc["_id"])}} for doc in cursor
        ]

    def _get_collection(self, collection: str) -> Collection:
        collection = collection or self.collection
        assert collection is not None
        col: Collection = self.db_connection[collection]
        return col

    def _get_validated_data(self, data, data_validator: Callable):
        if data_validator is not None:
            data = data_validator(data)
        elif self.data_validator is not None:
            data = self.data_validator(data)
        else:
            log.warning("Attention! No data validator function provided!")

        return data

    # RAW

    def execute_query(self, query: List[dict], collection: str = None) -> List[dict]:
        col = self._get_collection(collection)
        cursor = col.aggregate(pipeline=query, allowDiskUse=True)
        return self._setids(cursor)

    # finding data

    def find_one(self, filters: dict, collection: str = None) -> dict:
        col = self._get_collection(collection)
        data = col.find_one(filters)
        return self._setid(data)

    def find_by_id(self, id: str, collection: str = None) -> dict:
        col = self._get_collection(collection)
        data = col.find_one({"_id": utils.get_object_id(id)})
        return self._setid(data)

    def find_many(
        self,
        filters: dict,
        limit: int = 0,
        skip: int = 0,
        sort: List[Tuple[str, int]] = None,
        collection: str = None,
    ) -> List[dict]:

        col = self._get_collection(collection)
        if "_id" in filters:  # pragma no cover
            filters["_id"] = utils.get_object_id(filters["_id"])

        cursor = col.find(filter=filters, skip=skip, limit=limit, sort=sort)
        return self._setids(cursor)

    def distinct(
        self,
        field: str,
        filters: dict = None,
        collection: str = None,
    ) -> List[str]:
        col = self._get_collection(collection)
        if filters is not None:  # pragma no cover
            if "_id" in filters:
                filters["_id"] = utils.get_object_id(filters["_id"])

        data = col.distinct(key=field, filter=filters)
        return data

    def count(
        self,
        filters: dict = None,
        collection: str = None,
    ) -> int:
        col = self._get_collection(collection)
        if filters is None:
            filters = {}

        return col.count_documents(filter=filters)

    # Inserting new data

    def insert_one(
        self,
        data: dict,
        data_validator: Callable = None,
        collection: str = None,
    ) -> dict:
        data = self._get_validated_data(data, data_validator)
        col = self._get_collection(collection)
        col.insert_one(data)
        data["_id"] = utils.get_object_id_str(data["_id"])
        return data

    def insert_with_id(
        self,
        id: Union[str, int],
        data: dict,
        overwrite: bool = False,
        data_validator: Callable = None,
        collection: str = None,
    ) -> dict:
        data = self._get_validated_data(data, data_validator)
        col = self._get_collection(collection)
        data["_id"] = utils.get_object_id(id)
        if overwrite:
            col.delete_one({"_id": data["_id"]})
        col.insert_one(data)
        return data

    def insert_many(
        self,
        data: List[dict],
        overwrite: bool = False,
        data_validator: Callable = None,
        collection: str = None,
    ) -> List[dict]:
        data = self._get_validated_data(data, data_validator)
        col = self._get_collection(collection)
        if overwrite:  # pragma no cover
            col.delete_many(
                {"_id": {"$in": [utils.get_object_id(d["_id"]) for d in data]}}
            )
        col.insert_many(data)
        return self._setids(data)

    # Updating existing data

    def update_one(
        self,
        filters: dict,
        data: dict,
        append: bool = False,
        upsert: bool = True,
        array_filters: List[dict] = None,
        data_validator: Callable = None,
        collection: str = None,
    ) -> dict:
        data = self._get_validated_data(data, data_validator)
        col = self._get_collection(collection)
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
        id: str,
        data: dict,
        append: bool = False,
        upsert: bool = True,
        array_filters: List[dict] = None,
        data_validator: Callable = None,
        collection: str = None,
    ) -> dict:
        data = self._get_validated_data(data, data_validator)
        col = self._get_collection(collection)
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
        filters: dict,
        data: List[dict],
        append: bool = False,
        upsert: bool = True,
        array_filters: List[dict] = None,
        data_validator: Callable = None,
        collection: str = None,
    ) -> int:
        data = self._get_validated_data(data, data_validator)
        col = self._get_collection(collection)
        return col.update_many(
            filter=filters,
            update=utils.add_update_operators(data, append),
            upsert=upsert,
            array_filters=array_filters,
        ).matched_count

    def replace_one(
        self,
        filters: dict,
        data: dict,
        upsert: bool = True,
        data_validator: Callable = None,
        collection: str = None,
    ) -> dict:
        data = self._get_validated_data(data, data_validator)
        col = self._get_collection(collection)
        data = col.find_one_and_replace(
            filter=filters,
            replacement=data,
            upsert=upsert,
            return_document=True,
        )
        return self._setid(data)

    def replace_on_id(
        self,
        id: str,
        data: dict,
        upsert: bool = True,
        data_validator: Callable = None,
        collection: str = None,
    ) -> dict:
        data = self._get_validated_data(data, data_validator)
        col = self._get_collection(collection)
        data = col.find_one_and_replace(
            filter={"_id": utils.get_object_id(id)},
            replacement=data,
            upsert=upsert,
            return_document=True,
        )
        return self._setid(data)

    def replace_many(
        self,
        filters: dict,
        data: dict,
        upsert: bool = True,
        data_validator: Callable = None,
        collection: str = None,
    ) -> int:
        data = self._get_validated_data(data, data_validator)
        col = self._get_collection(collection)
        deleted_count = col.delete_many(filter=filters).deleted_count
        modified_count = col.update_many(
            filter=filters,
            update=utils.add_update_operators(data, False),
            upsert=upsert,
        ).modified_count
        return deleted_count or modified_count or int(upsert)

    # Deleting existing data

    def delete_one(self, filters: dict, collection: str = None) -> int:
        col = self._get_collection(collection)
        return col.delete_one(filter=filters).deleted_count

    def delete_on_id(self, id: str, collection: str = None) -> int:
        col = self._get_collection(collection)
        return col.delete_one(filter={"_id": utils.get_object_id(id)}).deleted_count

    def delete_many(self, filters: dict, collection: str = None) -> int:
        col = self._get_collection(collection)
        return col.delete_many(filter=filters).deleted_count
