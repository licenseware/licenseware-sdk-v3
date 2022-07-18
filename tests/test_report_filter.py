import pytest
import unittest
from licenseware import ReportFilter


# pytest -v -s tests/test_report_filter.py


t = unittest.TestCase()


# pytest -v -s tests/test_report_filter.py::test_report_filter
def test_report_filter():
    
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

    # print(filters.metadata)

    assert isinstance(filters.metadata, list)
    assert len(filters.metadata) == 2

    for f in filters.metadata:
        assert f['column'] in ["result", "total_number_of_cores"]
        if f['column'] == "result":
            assert f['visible_name'] == "Result"
        if f['column'] == "total_number_of_cores":
            assert f['visible_name'] == 'Total Number Of Cores'



    # {
    #     "column": "total_number_of_cores",
    #     "allowed_filters": [
    #         "equals",
    #         "greater_than",
    #         "greater_or_equal_to",
    #         "less_than",
    #         "less_or_equal_to",
    #     ],
    #     "visible_name": "Total Number of Cores",
    #     "column_type": "number",
    # },