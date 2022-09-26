import unittest

from licenseware import (
    BarHorizontalAttrs,
    Config,
    ErrorAlreadyAttached,
    Icons,
    NewReport,
    NewReportComponent,
    ReportFilter,
    StyleAttrs,
    SummaryAttrs,
)

# pytest -s -v tests/test_report.py

t = unittest.TestCase()


# pytest -s -v tests/test_report.py::test_parse_report_components
def test_parse_report_components():

    config = Config(FRONTEND_URL="", PUBLIC_TOKEN_REPORT_URL="")

    # Declaring some attributes
    summary = (
        SummaryAttrs()
        .attr(
            value_key="missing_parent_details",
            value_description="Missing parent details",
            icon=Icons.FEATURES,
        )
        .attr(value_key="unknown_types")
    )

    styles = StyleAttrs().width_one_third.set("height", "full")

    def get_fmw_summary_component_data():
        return "mock_response"

    # Declaring the report component
    fmw_summary_component = NewReportComponent(
        title="Summary",
        component_id="fmw_summary",
        attributes=summary,
        style_attributes=styles,
        get_component_data_handler=get_fmw_summary_component_data,
        config=config,
    )

    fmw_deployment_report = NewReport(
        name="Oracle Fusion Middleware Deployment",
        report_id="fmw_deployment_report",
        description="Provides overview of Oracle Fusion Middleware deployed components and product bundles.",
        filters=[],
        components=[fmw_summary_component],
        config=config,
    )

    # fmw_deployment_report.attach("fmw_summary")

    res = fmw_deployment_report._get_report_components_metadata()

    print(res)

    assert isinstance(res[0]["style_attributes"], dict)
    assert isinstance(res[0]["attributes"], dict)

    # print(json.dumps(res, sort_keys=True, indent=4, default=str))


# pytest -s -v tests/test_report.py::test_report_creation
def test_report_creation(mocker):
    class RequestsResponse:
        status_code = 200

        @staticmethod
        def json():
            return [{"status": ["success"]}]

    mocker.patch("requests.post", return_value=RequestsResponse)
    mocker.patch("requests.get", return_value=RequestsResponse)

    config = Config(APP_ID="fmw", FRONTEND_URL="", PUBLIC_TOKEN_REPORT_URL="")

    FMW_FILTERS = (
        ReportFilter()
        .add(
            column="result",
            allowed_filters=[
                ReportFilter.FILTER.EQUALS,
                ReportFilter.FILTER.CONTAINS,
                ReportFilter.FILTER.IN_LIST,
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
                ReportFilter.FILTER.LESS_OR_EQUAL_TO,
            ],
            column_type=ReportFilter.TYPE.STRING,
            allowed_values=["Verify", "Used", "Licensable", "Restricted"],
        )
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
            icon=Icons.FEATURES,
        )
        .attr(value_key="unknown_types")
    )

    styles = StyleAttrs().width_one_third.set("height", "full")

    # Declaring the report component
    fmw_summary_component = NewReportComponent(
        title="Summary",
        component_id="fmw_summary",
        attributes=summary,
        style_attributes=styles,
        get_component_data_handler=get_fmw_summary_component_data,
        config=config,
    )

    # COMPONENT 2
    # Declaring some attributes
    bar_horizontal = BarHorizontalAttrs().attr(
        xaxis_key="product_name", yaxis_key="oracle_processors_required"
    )

    styles = StyleAttrs().width_full

    # Declaring the report component
    fmw_bar_horizontal_component = NewReportComponent(
        title="Bar chart",
        component_id="bar_devices",
        attributes=bar_horizontal,
        style_attributes=styles,
        get_component_data_handler=get_fmw_summary_component_data,
        config=config,
    )

    report_components = [fmw_bar_horizontal_component, fmw_summary_component]

    # Declaring the report
    fmw_deployment_report = NewReport(
        name="Oracle Fusion Middleware Deployment",
        report_id="fmw_deployment_report",
        description="Provides overview of Oracle Fusion Middleware deployed components and product bundles.",
        filters=FMW_FILTERS,
        components=report_components,
        config=config,
    )

    # Attaching a report component to a report
    fmw_deployment_report.attach("fmw_summary")
    with t.assertRaises(ErrorAlreadyAttached):
        fmw_deployment_report.attach("fmw_summary")

    assert fmw_summary_component.get_component_data_handler() == "mock_component_data"
    assert "component_id" in fmw_summary_component.get_metadata()

    d = fmw_deployment_report.get_metadata()
    print(d)
    firstfilter = d["filters"][0]["allowed_filters"][0]
    assert isinstance(firstfilter, str)

    assert fmw_summary_component.component_id in fmw_deployment_report.report_components

    fmw_deployment_report.attach("bar_devices")

    assert len(fmw_deployment_report.report_components) == 2

    # print(
    #     json.dumps(
    #         fmw_deployment_report.metadata, sort_keys=True, indent=4, default=str
    #     )
    # )


# pytest -s -v tests/test_report.py::test_report_metadata_connected_apps
def test_report_metadata_connected_apps():

    config = Config(APP_ID="odb-service", FRONTEND_URL="", PUBLIC_TOKEN_REPORT_URL="")

    fmw_deployment_report = NewReport(
        name="Oracle Fusion Middleware Deployment",
        report_id="fmw_deployment_report",
        description="Provides overview of Oracle Fusion Middleware deployed components and product bundles.",
        filters=[],
        config=config,
        # connected_apps=["odb-service", "ifmp-service"],
    )

    # app = NewApp(
    #     name="Oracle Middleware Manager",
    #     description="""OMWM Automate the analysis and determination of Oracle Middleware usage.""",
    #     config=config,
    # )

    # app.attach_reports([fmw_deployment_report])

    # assert app.attached_reports

    # metadata = fmw_deployment_report.get_metadata()

    # print(metadata)
