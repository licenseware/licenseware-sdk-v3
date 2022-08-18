from typing import Callable, List, Any, Union
from licenseware.repository.repository_interface import RepositoryInterface
from pymongo.collection import Collection
from . import utils


class MongoRepository(RepositoryInterface):
    def __init__(self, db_connection) -> None:
        self.conn = db_connection

    # RAW

    def execute_query(self, query: Any):
        ...

    # finding data

    def find_one(self, table_or_collection: str, **filters) -> dict:
        ...

    def find_by_id(self, table_or_collection: str, id: str) -> dict:
        ...

    def find_many(
        self,
        table_or_collection: str,
        limit: int = None,
        skip: int = None,
        sortby: Any = None,
        **filters,
    ) -> List[dict]:
        ...

    def distinct(self, table_or_collection: str, **filters):
        ...

    def count(self, table_or_collection: str, **filters):
        ...

    # Inserting new data

    def insert_one(
        self, table_or_collection: str, data_validator: Callable, data: dict
    ):
        data_validator(data)
        col: Collection = self.conn[table_or_collection]
        col.insert_one(data)
        data["_id"] = utils.get_object_id_str(data["_id"])
        return data

    def insert_with_id(
        self,
        table_or_collection: str,
        id: Union[str, int],
        data_validator: Callable,
        data: dict,
    ):
        ...

    def insert_many(
        self, table_or_collection: str, data_validator: Callable, data: List[dict]
    ):
        ...

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
