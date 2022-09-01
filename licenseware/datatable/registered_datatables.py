from enum import Enum
from typing import Any, Dict, List

from licenseware.config.config import Config
from licenseware.constants.web_response import WebResponse
from licenseware.datatable.datatable import DataTable
from licenseware.utils.alter_string import get_altered_strings
from licenseware.utils.failsafe_decorator import failsafe


class RegisteredDataTables:
    def __init__(self, datatables: List[DataTable], config: Config) -> None:
        self.config = config
        self.datatables = datatables
        self.datatables_metadata = self._create_and_order_datatables(datatables)
        self.component_enum = Enum(
            "ComponentEnum",
            {
                u.component_id: get_altered_strings(u.component_id).dash
                for u in self.datatables
            },
        )
        self.component_dispacher: Dict[str, DataTable] = {
            u.component_id: u for u in datatables
        }

    @failsafe
    def get_datatables_metadata(self):
        return WebResponse(status_code=200, content=self.datatables_metadata)

    @failsafe
    def get_data(
        self,
        tenant_id: str,
        authorization: str,
        db_connection: Any,
        component_id: str,
        id: str,
        foreign_key: str = None,
        distinct_key: str = None,
        limit: int = 0,
        skip: int = 0,
    ):
        component = self._get_current_component(component_id)
        result = component.crud_handler.get(
            tenant_id,
            authorization,
            db_connection,
            id,
            foreign_key,
            distinct_key,
            limit,
            skip,
            self.config.MONGO_COLLECTION.DATA,
        )
        return WebResponse(status_code=200, content=result)

    @failsafe
    def update_data(
        self,
        tenant_id: str,
        authorization: str,
        db_connection: Any,
        component_id: str,
        id: str,
        new_data: dict,
    ):
        component = self._get_current_component(component_id)
        result = component.crud_handler.put(
            tenant_id,
            authorization,
            db_connection,
            id,
            new_data,
            self.config.MONGO_COLLECTION.DATA,
        )
        return WebResponse(status_code=200, content=result)

    @failsafe
    def delete_data(
        self,
        tenant_id: str,
        authorization: str,
        db_connection: Any,
        component_id: str,
        id: str,
    ):
        component = self._get_current_component(component_id)
        result = component.crud_handler.delete(
            tenant_id,
            authorization,
            db_connection,
            id,
            self.config.MONGO_COLLECTION.DATA,
        )
        return WebResponse(status_code=200, content=result)

    # PRIVATE

    def _get_current_component(self, component_id: Enum):
        if isinstance(component_id, str):
            return self.component_dispacher[component_id]
        component_id = str(component_id).replace("ComponentEnum.", "")
        return self.component_dispacher[component_id]

    def _create_and_order_datatables(self, datatables: List[DataTable]):
        order = 0
        ordered_datatables = []
        for dt in datatables:
            data = dt.metadata
            data["order"] = order
            ordered_datatables.append(data)
            order += 1
        return ordered_datatables
