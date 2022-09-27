import unittest

from licenseware import (
    Config,
    ErrorAlreadyAttached,
    Flags,
    Icons,
    NewApp,
    NewReport,
    NewReportComponent,
    NewUploader,
    StyleAttrs,
    SummaryAttrs,
    get_mongodb_connection,
    get_redis_cache,
)

# pytest -s -v tests/test_new_app.py

t = unittest.TestCase()


# pytest -s -v tests/test_new_app.py::test_new_app
def test_new_app():

    config = Config(APP_ID="fmw", FRONTEND_URL="", PUBLIC_TOKEN_REPORT_URL="")

    fmw = NewApp(
        name="Oracle Middleware Manager",
        description="""OMWM Automate the analysis and determination of Oracle Middleware usage.""",
        flags=[Flags.BETA],
        config=config,
    )

    metadata = fmw.get_full_metadata()

    assert isinstance(metadata, dict)
    assert "app" in metadata
    assert "uploaders" in metadata
    assert "reports" in metadata
    assert "report_components" in metadata


# pytest -s -v tests/test_new_app.py::test_adding_objects
def test_adding_objects():

    config = Config(APP_ID="fmw", FRONTEND_URL="", PUBLIC_TOKEN_REPORT_URL="")
    db_connection = get_mongodb_connection(config)
    redis_cache = get_redis_cache(config)

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
        return "ok"

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
        config=config,
        connected_apps=["odb-service", "ifmp-service"],
        db_connection=db_connection,
        redis_cache=redis_cache,
    )

    def workerfunc(event):
        pass

    rv_tools_uploader = NewUploader(
        name="RVTools",
        description="XLSX export from RVTools after scanning your Vmware infrastructure.",
        uploader_id="rv_tools",
        accepted_file_types=[".xlsx"],
        worker=workerfunc,
        config=config,
        redis_cache=redis_cache,
    )

    app = NewApp(
        name="Oracle Middleware Manager",
        description="""OMWM Automate the analysis and determination of Oracle Middleware usage.""",
        flags=[Flags.BETA],
        config=config,
    )

    app.attach_uploaders([rv_tools_uploader])
    app.attach_reports([fmw_deployment_report])
    app.attach_components([fmw_summary_component])

    assert rv_tools_uploader.uploader_id in app.attached_uploaders
    assert fmw_deployment_report.report_id in app.attached_reports
    assert fmw_summary_component.component_id in app.attached_components

    with t.assertRaises(ErrorAlreadyAttached):
        app.attach_uploaders([rv_tools_uploader])

    with t.assertRaises(ErrorAlreadyAttached):
        app.attach_reports([fmw_deployment_report])

    with t.assertRaises(ErrorAlreadyAttached):
        app.attach_components([fmw_summary_component])

    assert isinstance(app.get_metadata(), dict)
    assert "app_id" in app.get_metadata()

    # print(json.dumps(app.get_full_metadata(), sort_keys=True, indent=4, default=str))

    # assert isinstance(app.get_full_metadata(), dict)
    # assert "reports" in app.get_full_metadata()
