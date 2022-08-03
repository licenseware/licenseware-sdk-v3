from dataclasses import asdict, dataclass
from typing import List
from urllib.parse import urlencode

from licenseware.constants.column_types import ColumnTypes
from licenseware.report.style_attributes import StyleAttrs
from licenseware.utils.alter_string import get_altered_strings

from .crud_handler import CrudHandler


def _update_name(name: str, prop: str):

    if name is None:
        altstr = get_altered_strings(prop)
        name = altstr.title

    return name


def _update_bools(
    prop: str, editable: bool, visible: bool, hashable: bool, required: bool
):

    if prop in {"tenant_id", "_id", "updated_at"}:
        editable = False
        visible = False
        hashable = False
        required = True

    return editable, visible, hashable, required


def _update_type(type: str, values: List[str], distinct_key: str, foreign_key: str):

    if type is None:
        if values is not None:
            type = ColumnTypes.ENUM
        elif distinct_key is not None and foreign_key is not None:
            type = ColumnTypes.ENTITY
        else:
            type = ColumnTypes.STRING

    assert isinstance(type, ColumnTypes)
    return type


def _update_entities_url(path: str, distinct_key: str, foreign_key: str):

    entities_url = None
    if distinct_key is not None or foreign_key is not None:
        query_params = {"_id": "{entity_id}"}
        if distinct_key is not None:
            query_params.update({"distinct_key": distinct_key})
        if foreign_key is not None:
            query_params.update({"foreign_key": foreign_key})

        entities_url = f"{path}?{urlencode(query_params)}"

    return entities_url


@dataclass
class DataTableColumn:
    name: str
    prop: str
    editable: bool
    type: str
    values: list
    required: bool
    visible: bool
    hashable: bool
    entities_url: str
    distinct_key: str
    foreign_key: str

    def dict(self):
        return asdict(self)


@dataclass
class DataTable:
    title: str
    component_id: str
    crud_handler: CrudHandler
    simple_indexes: List[str] = None
    compound_indexes: List[List[str]] = None

    def __post_init__(self):

        if not isinstance(self.crud_handler, CrudHandler):
            self.crud_handler = self.crud_handler()

        assert isinstance(self.crud_handler, CrudHandler)

        self.columns: List[DataTableColumn] = []
        self.type = "editable_table"
        self.style_attributes: StyleAttrs = StyleAttrs().width_full
        self.url = None
        self.path = "/" + self.component_id
        self.order = 0
        self._added_props = set()

    def column(
        self,
        prop: str,
        *,
        name: str = None,
        values: list = None,
        type: ColumnTypes = None,
        editable: bool = True,
        visible: bool = True,
        hashable: bool = True,
        required: bool = False,
        distinct_key: str = None,
        foreign_key: str = None,
    ):

        if prop in self._added_props:
            raise ValueError(f"Column '{prop}' is already added")
        self._added_props.add(prop)

        name = _update_name(name, prop)
        editable, visible, hashable, required = _update_bools(
            prop, editable, visible, hashable, required
        )
        type = _update_type(type, values, distinct_key, foreign_key)
        entities_url = _update_entities_url(self.path, distinct_key, foreign_key)

        col = DataTableColumn(
            name=name,
            prop=prop,
            editable=editable,
            type=type,
            values=values,
            required=required,
            visible=visible,
            hashable=hashable,
            entities_url=entities_url,
            distinct_key=distinct_key,
            foreign_key=foreign_key,
        )

        self.columns.append(col)

        return self

    def dict(self):
        return {**asdict(self), "columns": [col.dict() for col in self.columns]}
