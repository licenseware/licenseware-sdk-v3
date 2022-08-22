from abc import ABCMeta, abstractmethod
from typing import Callable, List, Tuple, Union


class RepositoryInterface(metaclass=ABCMeta):

    # RAW

    @abstractmethod
    def execute_query(self, table_or_collection: str, query: List[dict]):
        ...

    # finding data

    @abstractmethod
    def find_one(self, table_or_collection: str, filters: dict) -> dict:
        ...

    @abstractmethod
    def find_by_id(self, table_or_collection: str, id: str) -> dict:
        ...

    @abstractmethod
    def find_many(
        self,
        table_or_collection: str,
        filters: dict,
        limit: int = 0,
        skip: int = 0,
        sort: List[Tuple[str, int]] = None,
    ) -> List[dict]:
        ...

    @abstractmethod
    def distinct(
        self, table_or_collection: str, field: str, filters: dict = None
    ) -> List[str]:
        ...

    @abstractmethod
    def count(self, table_or_collection: str, filters: dict = None) -> int:
        ...

    # Inserting new data

    @abstractmethod
    def insert_one(
        self, table_or_collection: str, data_validator: Callable, data: dict
    ) -> dict:
        ...

    @abstractmethod
    def insert_with_id(
        self,
        table_or_collection: str,
        id: Union[str, int],
        data_validator: Callable,
        data: dict,
        overwrite: bool = False,
    ) -> dict:
        ...

    @abstractmethod
    def insert_many(
        self,
        table_or_collection: str,
        data_validator: Callable,
        data: List[dict],
        overwrite: bool = False,
    ) -> List[dict]:
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
        upsert: bool = True,
        array_filters: List[dict] = None,
    ) -> dict:
        ...

    @abstractmethod
    def update_on_id(
        self,
        table_or_collection: str,
        filters: dict,
        data_validator: Callable,
        data: List[dict],
        append: bool = False,
        upsert: bool = True,
        array_filters: List[dict] = None,
    ) -> int:
        ...

    @abstractmethod
    def update_many(
        self,
        table_or_collection: str,
        filters: dict,
        data_validator: Callable,
        data: List[dict],
        append: bool = False,
        upsert: bool = True,
        array_filters: List[dict] = None,
    ) -> int:
        ...

    @abstractmethod
    def replace_one(
        self,
        table_or_collection: str,
        filters: dict,
        data_validator: Callable,
        data: dict,
        upsert: bool = True,
    ) -> dict:
        ...

    @abstractmethod
    def replace_on_id(
        self,
        table_or_collection: str,
        id: str,
        data_validator: Callable,
        data: dict,
        upsert: bool = True,
    ) -> dict:
        ...

    @abstractmethod
    def replace_many(
        self,
        table_or_collection: str,
        filters: dict,
        data_validator: Callable,
        data: dict,
        upsert: bool = True,
    ) -> int:
        ...

    # Deleting existing data

    @abstractmethod
    def delete_one(self, table_or_collection: str, filters: dict) -> int:
        ...

    @abstractmethod
    def delete_on_id(self, table_or_collection: str, id: str) -> int:
        ...

    @abstractmethod
    def delete_many(self, table_or_collection: str, filters: dict) -> int:
        ...
