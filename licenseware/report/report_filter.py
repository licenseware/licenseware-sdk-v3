from typing import List
from licenseware.utils.alter_string import get_altered_strings
from licenseware.constants.allowed_filters import AllowedFilters
from licenseware.constants.column_types import ColumnTypes



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

    def add(self, *, column:str,  allowed_filters: List[str], column_type:str = None, allowed_values: List[str] = None, visible_name:str = None):

        if column_type is None:
            column_type = self.TYPE.STRING

        if visible_name is None:
            strver = get_altered_strings(column)
            visible_name = strver.title

        self.metadata.append({
            "column": column,
            "allowed_filters": allowed_filters,
            "column_type": column_type,
            "allowed_values": allowed_values,
            "visible_name": visible_name,
        })

        return self


