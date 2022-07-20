from typing import List
from urllib.parse import urlencode
from dataclasses import dataclass, asdict
from licenseware.report.style_attributes import StyleAttrs
from licenseware.utils.alter_string import get_altered_strings
from licenseware.constants.column_types import ColumnTypes


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
    distinct_key:str
    foreign_key:str

    def dict(self):
        return asdict(self)


@dataclass
class DataTable:
    title: str
    component_id: str
    simple_indexes: List[str] = None
    compound_indexes: List[List[str]] = None
    
    def __post_init__(self):
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
        distinct_key:str = None,
        foreign_key:str = None,
    ):

        if prop in self._added_props:
            raise ValueError(f"Column '{prop}' is already added")
        self._added_props.add(prop)


        if prop in {"tenant_id", "_id", "updated_at"}:
            editable = False
            visible = False
            hashable = False
            required = True


        if name is None:
            altstr = get_altered_strings(prop)
            name = altstr.title
        

        if type is None:
            if values is not None:
                type = ColumnTypes.ENUM
            elif distinct_key is not None and foreign_key is not None:
                type = ColumnTypes.ENTITY
            else:
                type = ColumnTypes.STRING

        entities_url = None
        if distinct_key is not None or foreign_key is not None:
            query_params = {'_id': '{entity_id}'}
            if distinct_key is not None:
                query_params.update({"distinct_key": distinct_key})
            if foreign_key is not None:
                query_params.update({"foreign_key": foreign_key})

            entities_url = f"{self.path}?{urlencode(query_params)}"


        assert isinstance(type, ColumnTypes)


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
        return {
            **asdict(self), 
            "columns":[col.dict() for col in self.columns]
        }

        