import unittest

import pytest

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
                ReportFilter.FILTER.IN_LIST,
            ],
            allowed_values=["Verify", "Used", "Licensable", "Restricted"],
        )
        .add(
            column="total_number_of_cores",
            allowed_filters=[
                ReportFilter.FILTER.EQUALS,
                ReportFilter.FILTER.GREATER_THAN,
                ReportFilter.FILTER.GREATER_OR_EQUAL_TO,
                ReportFilter.FILTER.LESS_THAN,
                ReportFilter.FILTER.LESS_OR_EQUAL_TO,
            ],
            column_type=ReportFilter.TYPE.STRING,
            allowed_values=["Verify", "Used", "Licensable", "Restricted"],
        )
        .add(
            column="total_number_of_cores_intel",
            allowed_values=["Verify", "Used", "Licensable", "Restricted"],
        )
    )

    # print(filters.metadata)

    assert isinstance(filters.metadata, list)
    assert len(filters.metadata) == 3

    assert filters.metadata == [
        {
            "column": "result",
            "allowed_filters": ["equals", "contains", "in_list"],
            "column_type": "enum",
            "allowed_values": ["Verify", "Used", "Licensable", "Restricted"],
            "visible_name": "Result",
        },
        {
            "column": "total_number_of_cores",
            "allowed_filters": [
                "equals",
                "greater_than",
                "greater_or_equal_to",
                "less_than",
                "less_or_equal_to",
            ],
            "column_type": "string",
            "allowed_values": ["Verify", "Used", "Licensable", "Restricted"],
            "visible_name": "Total Number Of Cores",
        },
        {
            "column": "total_number_of_cores_intel",
            "allowed_filters": ["equals", "contains", "in_list"],
            "column_type": "enum",
            "allowed_values": ["Verify", "Used", "Licensable", "Restricted"],
            "visible_name": "Total Number Of Cores Intel",
        },
    ]


# pytest -v -s tests/test_report_filter.py::test_report_filter_utils
def test_report_filter_utils():

    allowed_filters = ReportFilter()._determine_allowed_filters(
        ReportFilter.TYPE.STRING
    )

    assert allowed_filters == [ReportFilter.FILTER.EQUALS, ReportFilter.FILTER.CONTAINS]

    allowed_filters = ReportFilter()._determine_allowed_filters(
        ReportFilter.TYPE.NUMBER
    )

    assert allowed_filters == [
        ReportFilter.FILTER.EQUALS,
        ReportFilter.FILTER.GREATER_THAN,
        ReportFilter.FILTER.GREATER_OR_EQUAL_TO,
        ReportFilter.FILTER.LESS_THAN,
        ReportFilter.FILTER.LESS_OR_EQUAL_TO,
    ]

    column_type = ReportFilter()._determine_column_type("column", ["allowed_values"])

    assert column_type == ReportFilter.TYPE.ENUM

    column_type = ReportFilter()._determine_column_type("number_of_devices", None)

    assert column_type == ReportFilter.TYPE.NUMBER
