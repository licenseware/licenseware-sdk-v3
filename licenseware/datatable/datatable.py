import re
from dataclasses import asdict, dataclass
from typing import List
from urllib.parse import urlencode

from licenseware.config.config import Config
from licenseware.constants.column_types import ColumnTypes
from licenseware.report.style_attributes import StyleAttrs
from licenseware.utils.alter_string import get_altered_strings
from licenseware.exceptions.custom_exceptions import ErrorAlreadyAttached
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


def _update_type(
    type: str, values: List[str], prop: str, distinct_key: str, foreign_key: str
):

    if type is None:
        if values is not None:
            type = ColumnTypes.ENUM
        elif distinct_key is not None and foreign_key is not None:
            type = ColumnTypes.ENTITY
        elif "number" in prop:
            type = ColumnTypes.NUMBER
        else:
            type = ColumnTypes.STRING

    assert isinstance(type, ColumnTypes)
    return type


def _update_entities_url(path: str, distinct_key: str, foreign_key: str):

    entities_url = None
    if distinct_key is not None or foreign_key is not None:
        query_params = {"id": "{entity_id}"}
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
    config: Config
    crud_handler: CrudHandler = None

    def __post_init__(self):

        assert self.config.APP_ID is not None

        self.crud_handler = self.crud_handler() if self.crud_handler else CrudHandler()
        assert isinstance(self.crud_handler, CrudHandler)

        ns = get_altered_strings(self.config.APP_ID).dash
        compdash = get_altered_strings(self.component_id).dash
        self.metadata_path = f"/{ns}/datatables"
        self.path = f"/{ns}/datatables/{compdash}"
        self.type = "editable_table"
        self.style_attributes = StyleAttrs().width_full.metadata

        self.order = 0
        self.columns: List[DataTableColumn] = []
        self.url = None
        self._added_props = set()
        self._non_editable_fields = set()

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
            raise ErrorAlreadyAttached(f"Column '{prop}' is already attached")
        self._added_props.add(prop)

        name = _update_name(name, prop)
        editable, visible, hashable, required = _update_bools(
            prop, editable, visible, hashable, required
        )
        type = _update_type(type, values, prop, distinct_key, foreign_key)
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

        if not col.editable:
            self._non_editable_fields.add(col.prop)

        return self

    def dict(self):
        return {**asdict(self), "columns": [col.dict() for col in self.columns]}

    @property
    def metadata(self):
        data = {
            "url": self.path,
            "path": self.path,
            "type": self.type,
            "order": self.order,
            "style_attributes": self.style_attributes,
        }

        selfdata = self.dict()
        for k in ["crud_handler", "config"]:
            selfdata.pop(k)

        return {**data, **selfdata}

    def validate(self, data: dict):
        data = self._check_non_editable_fields(data)
        self._check_data_types(data)
        return data

    def _check_non_editable_fields(self, data: dict):
        for field in self._non_editable_fields:
            data.pop(field, None)
        return data

    def _check_data_types(self, data: dict):

        for col in self.columns:
            for field, value in data.items():

                if col.prop != field:
                    continue

                if col.required is False and value is None:
                    continue

                if col.type == ColumnTypes.STRING:
                    if not isinstance(value, str):
                        raise ValueError(
                            f"Field '{field}' must be 'string'  (ex: 'some-string')"
                        )
                elif col.type == ColumnTypes.NUMBER:
                    if not isinstance(value, (int, float)):
                        raise ValueError(
                            f"Field '{field}' must be 'number' (ex: 12, or 14.3)"
                        )
                elif col.type == ColumnTypes.DATE:
                    if not re.fullmatch(
                        r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}", value
                    ):
                        raise ValueError(
                            f"Field '{field}' must be 'date' (ex: '2022-09-01T06:01:38.621461')"
                        )
                elif col.type == ColumnTypes.BOOL:
                    if not isinstance(value, bool):
                        raise ValueError(f"Field '{field}' must be 'bool'")
                elif col.type == ColumnTypes.JSON:
                    if not isinstance(value, (dict, list)):
                        raise ValueError(f"Field '{field}' must be 'json'")
                elif col.type == ColumnTypes.ENUM:
                    if value not in col.values:
                        raise ValueError(
                            f"Field '{field}' must be an 'enum' from {col.values}"
                        )
                elif col.type == ColumnTypes.ENTITY:
                    continue
