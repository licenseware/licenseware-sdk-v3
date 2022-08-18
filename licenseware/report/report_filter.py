from typing import List, Union

from licenseware.constants.allowed_filters import AllowedFilters
from licenseware.constants.column_types import ColumnTypes
from licenseware.utils.alter_string import get_altered_strings


class ReportFilter:
    """
    Usage:
    ```py

    filters = (
        ReportFilter()
        .add(
            column="result",
            allowed_filters=[
                ReportFilter.FILTER.EQUALS,
                ReportFilter.FILTER.CONTAINS,
                ReportFilter.FILTER.IN_LIST
            ],
            # column_type=ReportFilter.TYPE.STRING, # string type is the default
            allowed_values=["Verify", "Used", "Licensable", "Restricted"],
            # visible_name="Result" # Optional
        )
        .add(
            column="total_number_of_cores",
            allowed_filters=[
                ReportFilter.FILTER.EQUALS,
                ReportFilter.FILTER.GREATER_THAN,
                ReportFilter.FILTER.GREATER_OR_EQUAL_TO,
                ReportFilter.FILTER.LESS_THAN,
                ReportFilter.FILTER.LESS_OR_EQUAL_TO
            ],
            column_type=ReportFilter.TYPE.STRING,
            allowed_values=["Verify", "Used", "Licensable", "Restricted"],
        )
    )

    ```

    Filter sample
    {
        "column": "result",
        "allowed_filters": ["equals", "contains", "in_list"],
        "visible_name": "Result",
        "column_type": "string",
        "allowed_values": ["Verify", "Used", "Licensable", "Restricted"],
    }
    """

    TYPE = ColumnTypes
    FILTER = AllowedFilters

    def __init__(self):
        self.metadata = []

    def add(
        self,
        *,
        column: str,
        column_type: str = None,
        allowed_filters: List[str] = None,
        allowed_values: List[str] = None,
        visible_name: str = None
    ):

        if column_type is None:
            column_type = self._determine_column_type(column, allowed_values)

        if visible_name is None:
            strver = get_altered_strings(column)
            visible_name = strver.title

        if allowed_filters is None:
            allowed_filters = self._determine_allowed_filters(column_type)

        self.metadata.append(
            {
                "column": column,
                "allowed_filters": allowed_filters,
                "column_type": column_type,
                "allowed_values": allowed_values,
                "visible_name": visible_name,
            }
        )

        return self

    def _determine_column_type(
        self, column: str, allowed_values: Union[List[str], None]
    ):
        if allowed_values is not None:
            return self.TYPE.ENUM

        if "number" in column:
            return self.TYPE.NUMBER

        return self.TYPE.STRING

    def _determine_allowed_filters(self, column_type: str):

        if column_type == self.TYPE.STRING:
            return [self.FILTER.EQUALS, self.FILTER.CONTAINS]

        if column_type == self.TYPE.NUMBER or column_type == self.TYPE.DATE:
            return [
                self.FILTER.EQUALS,
                self.FILTER.GREATER_THAN,
                self.FILTER.GREATER_OR_EQUAL_TO,
                self.FILTER.LESS_THAN,
                self.FILTER.LESS_OR_EQUAL_TO,
            ]

        if column_type == self.TYPE.BOOL:
            return [self.FILTER.EQUALS]

        if column_type == self.TYPE.ENUM:
            return [self.FILTER.EQUALS, self.FILTER.CONTAINS, self.FILTER.IN_LIST]

        if column_type == self.TYPE.JSON or column_type == self.TYPE.ENTITY:
            return [
                self.FILTER.EQUALS,
                self.FILTER.CONTAINS,
                self.FILTER.IN_LIST,
                self.FILTER.GREATER_THAN,
                self.FILTER.GREATER_OR_EQUAL_TO,
                self.FILTER.LESS_THAN,
                self.FILTER.LESS_OR_EQUAL_TO,
            ]
