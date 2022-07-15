import pytest
import unittest
import json
from dataclasses import dataclass
from licenseware import (
    NewReport, 
    NewReportComponent,
    RCFilter,
    ColumnTypes,
    Filters,
    StyleAttrs,
    SummaryAttrs,
    BarHorizontalAttrs,
    Icons
)

from licenseware.report.report import _update_connected_apps, _update_filters, _parse_report_components


# pytest -s -v tests/test_report.py

t = unittest.TestCase()




# pytest -s -v tests/test_report.py::test_parse_report_components
def test_parse_report_components():

    @dataclass
    class Config:
        APP_ID = "fmw"
        REGISTER_REPORT_URL = ""
        REGISTER_REPORT_COMPONENT_URL = ""

        @staticmethod
        def get_machine_token():
            return "machine token from envs"


    config = Config()


    # Declaring some attributes
    summary = (
        SummaryAttrs()
        .attr(
            value_key="missing_parent_details", 
            value_description="Missing parent details",
            icon=Icons.FEATURES
        )
        .attr(value_key="unknown_types")
    )

    styles = (
        StyleAttrs()
        .width_one_third
        .set("height", "full")
    )

    def get_fmw_summary_component_data():
        return "mock_response"

    # Declaring the report component
    fmw_summary_component = NewReportComponent(
        title="Summary", 
        component_id="fmw_summary", 
        attributes=summary,
        style_attributes=styles,
        get_component_data_handler=get_fmw_summary_component_data,
        config=config
    )

    res = _parse_report_components({fmw_summary_component.component_id: fmw_summary_component})

    assert isinstance(res[0]['style_attributes'], dict)
    assert isinstance(res[0]['attributes'], dict)

    # print(json.dumps(res, sort_keys=True, indent=4, default=str))





# pytest -s -v tests/test_report.py::test_update_connected_apps
def test_update_connected_apps():
    
    @dataclass
    class Config:
        APP_ID = "fmw"
    config = Config()

    connected_apps = None
    updated_connected_apps = _update_connected_apps(connected_apps, config)

    # print(updated_connected_apps)
    assert "fmw" in updated_connected_apps


    connected_apps = ["ifmp"]
    updated_connected_apps = _update_connected_apps(connected_apps, config)

    # print(updated_connected_apps)
    assert "fmw" in updated_connected_apps
    assert "ifmp" in updated_connected_apps



# pytest -s -v tests/test_report.py::test_update_filters
def test_update_filters():

    filters = [
        {
            "column": "result",
            "allowed_filters": ["equals", "contains", "in_list"],
            "visible_name": "Result",
            "column_type": "string",
            "allowed_values": ["Verify", "Used", "Licensable", "Restricted"],
        },
        RCFilter(
            column="result",
            allowed_filters=[
                Filters.EQUALS, 
                Filters.CONTAINS, 
                Filters.IN_LIST,
            ],
            column_type=ColumnTypes.STRING,
            allowed_values=["Verify", "Used", "Licensable", "Restricted"]
        )
    ]

    updated_filters = _update_filters(filters)

    # print(updated_filters)
    assert isinstance(updated_filters, list)
    for fltr in updated_filters:
        assert isinstance(fltr, dict)


    filters = [
        ["fail"]
    ]

    with t.assertRaises(ValueError):
        _update_filters(filters)



# pytest -s -v tests/test_report.py::test_report_creation
def test_report_creation(mocker):

    class RequestsResponse:
        status_code = 200

    mocker.patch(
        "requests.post",
        return_value=RequestsResponse
    )
    
    # External configuration
    @dataclass
    class Config:
        APP_ID = "fmw"
        REGISTER_REPORT_URL = ""
        REGISTER_REPORT_COMPONENT_URL = ""

        @staticmethod
        def get_machine_token():
            return "machine token from envs"


    config = Config()


    FMW_FILTERS = {
        "BASE": [
            RCFilter(
                column="updated_at",
                allowed_filters=[
                    Filters.EQUALS, 
                    Filters.GREATER_THAN, 
                    Filters.GREATER_THAN_OR_EQUAL_TO,
                    Filters.LESS_THAN,
                    Filters.LESS_THAN_OR_EQUAL_TO,
                ],
                column_type=ColumnTypes.DATE,
                visible_name="Last Update Date"
            ),
        ],
        "DEPLOYMENT": [
            RCFilter(
                column="result",
                allowed_filters=[
                    Filters.EQUALS, 
                    Filters.CONTAINS, 
                    Filters.IN_LIST,
                ],
                column_type=ColumnTypes.STRING,
                allowed_values=["Verify", "Used", "Licensable", "Restricted"]
            ),
        ]
    }


    # Declaring the report
    fmw_deployment_report = NewReport(
        name="Oracle Fusion Middleware Deployment",
        report_id="fmw_deployment_report",
        description="Provides overview of Oracle Fusion Middleware deployed components and product bundles.", 
        filters=[*FMW_FILTERS["BASE"], *FMW_FILTERS["DEPLOYMENT"]],
        config=config
    )

    # Function responsible for getting report component data
    def get_fmw_summary_component_data(*args, **kwargs):
        return "mock_component_data"

    # COMPONENT 1
    # Declaring some attributes
    summary = (
        SummaryAttrs()
        .attr(
            value_key="missing_parent_details", 
            value_description="Missing parent details",
            icon=Icons.FEATURES
        )
        .attr(value_key="unknown_types")
    )

    styles = (
        StyleAttrs()
        .width_one_third
        .set("height", "full")
    )

    # Declaring the report component
    fmw_summary_component = NewReportComponent(
        title="Summary", 
        component_id="fmw_summary", 
        attributes=summary,
        style_attributes=styles,
        get_component_data_handler=get_fmw_summary_component_data,
        config=config
    )

    
    # Attaching a report component to a report
    fmw_deployment_report.attach(fmw_summary_component)
    with t.assertRaises(ValueError):
        fmw_deployment_report.attach(fmw_summary_component)


    assert fmw_summary_component.get_component_data() == "mock_component_data"
    assert "data" in fmw_summary_component.metadata

    d = fmw_deployment_report.metadata["data"][0]
    firstfilter = d['filters'][0]['allowed_filters'][0]
    assert isinstance(firstfilter, str)

    assert fmw_summary_component.component_id in fmw_deployment_report.report_components


    # COMPONENT 2
    # Declaring some attributes
    bar_horizontal = (
        BarHorizontalAttrs()
        .attr(
            xaxis_key="product_name", 
            yaxis_key="oracle_processors_required"
        )
    )

    styles = StyleAttrs().width_full
    
    # Declaring the report component
    fmw_bar_horizontal_component = NewReportComponent(
        title="Bar chart", 
        component_id="bar_devices", 
        attributes=bar_horizontal,
        style_attributes=styles,
        get_component_data_handler=get_fmw_summary_component_data,
        config=config
    )

    fmw_deployment_report.attach(fmw_bar_horizontal_component)

    assert len(fmw_deployment_report.report_components) == 2

    print(json.dumps(fmw_deployment_report.metadata, sort_keys=True, indent=4, default=str))

    





