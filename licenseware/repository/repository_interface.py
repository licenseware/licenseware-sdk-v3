from typing import List, Union, Any, Callable
from abc import ABCMeta, abstractmethod


class RepositoryInterface(metaclass=ABCMeta):

    # RAW

    @abstractmethod
    def execute_query(self, query: Any):
        ...

    # finding data

    @abstractmethod
    def find_one(self, table_or_collection: str, **filters) -> dict:
        ...

    @abstractmethod
    def find_by_id(self, table_or_collection: str, id: str) -> dict:
        ...

    @abstractmethod
    def find_many(
        self,
        table_or_collection: str,
        limit: int = None,
        skip: int = None,
        sortby: Any = None,
        **filters,
    ) -> List[dict]:
        ...

    @abstractmethod
    def distinct(self, table_or_collection: str, **filters):
        ...

    @abstractmethod
    def count(self, table_or_collection: str, **filters):
        ...

    # Inserting new data

    @abstractmethod
    def insert_one(
        self, table_or_collection: str, data_validator: Callable, data: dict
    ):
        ...

    @abstractmethod
    def insert_with_id(
        self,
        table_or_collection: str,
        id: Union[str, int],
        data_validator: Callable,
        data: dict,
    ):
        ...

    @abstractmethod
    def insert_many(
        self, table_or_collection: str, data_validator: Callable, data: List[dict]
    ):
        ...

    # Updating existing data

    @abstractmethod
    def update_one(
        self,
        table_or_collection: str,
        filters: dict,
        data_validator: Callable,
        data: dict,
        append: bool = False,
    ) -> dict:
        ...

    @abstractmethod
    def update_on_id(
        self,
        table_or_collection: str,
        id: Union[str, int],
        data_validator: Callable,
        data: dict,
    ):
        ...

    @abstractmethod
    def update_many(
        self,
        table_or_collection: str,
        filters: dict,
        data_validator: Callable,
        data: List[dict],
    ):
        ...

    @abstractmethod
    def replace_one(
        self,
        table_or_collection: str,
        filters: dict,
        data_validator: Callable,
        data: List[dict],
    ):
        ...

    @abstractmethod
    def replace_on_id(
        self,
        table_or_collection: str,
        id: str,
        data_validator: Callable,
        data: List[dict],
    ):
        ...

    @abstractmethod
    def replace_many(
        self,
        table_or_collection: str,
        filters: dict,
        data_validator: Callable,
        data: List[dict],
    ):
        ...

    # Deleting existing data

    @abstractmethod
    def delete(self, table_or_collection: str, filters: dict, first: bool = False):
        ...

    @abstractmethod
    def delete_one(self, table_or_collection: str, **filters):
        ...

    @abstractmethod
    def delete_by_id(self, table_or_collection: str, id: str):
        ...

    @abstractmethod
    def delete_many(self, table_or_collection: str, **filters):
        ...
