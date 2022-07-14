import pytest
import json
from dataclasses import dataclass
from licenseware import (
    NewReport, 
    NewReportComponent,
    RCFilter,
    ColumnTypes,
    Filters,
    RCTypes,
)


# pytest -s -v tests/test_report.py

def test_report(mocker):

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
                column="device_name",
                allowed_filters=[Filters.EQUALS, Filters.CONTAINS, Filters.IN_LIST],
                column_type=ColumnTypes.STRING,
            ),
            
            # {
            #     "column": "device_name",
            #     "allowed_filters": ["equals", "contains", "in_list"],
            #     "visible_name": "Device Name",
            #     "column_type": "string",
            # },

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
            # {
            #     "column": "updated_at",
            #     "allowed_filters": [
            #         "equals",
            #         "greater_than",
            #         "greater_or_equal_to",
            #         "less_than",
            #         "less_or_equal_to",
            #     ],
            #     "visible_name": "Last Update Date",
            #     "column_type": "date",
            # },
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

            # {
            #     "column": "result",
            #     "allowed_filters": ["equals", "contains", "in_list"],
            #     "visible_name": "Result",
            #     "column_type": "string",
            #     "allowed_values": ["Verify", "Used", "Licensable", "Restricted"],
            # },
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
        return {}

    # Declaring the report component
    fmw_summary_component = NewReportComponent(
        title="Summary", 
        component_id="fmw_summary", 
        component_type=RCTypes.SUMMARY,
        attributes={},
        style_attributes={},
        get_component_data_handler=get_fmw_summary_component_data,
        config=config
    )

    # Attaching a report component to a report
    fmw_deployment_report.register_component(fmw_summary_component)


    d = fmw_deployment_report.metadata["data"][0]
    firstfilter = d['filters'][0]['allowed_filters'][0]
    assert isinstance(firstfilter, str)

    assert fmw_summary_component.component_id in fmw_deployment_report.report_components

    





