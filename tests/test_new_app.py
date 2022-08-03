import json
import unittest
from dataclasses import dataclass

import pytest

from licenseware import (
    Flags,
    Icons,
    NewApp,
    NewReport,
    NewReportComponent,
    NewUploader,
    StyleAttrs,
    SummaryAttrs,
)

# pytest -s -v tests/test_new_app.py

t = unittest.TestCase()


@dataclass
class Config:
    APP_ID = "fmw"
    REGISTER_REPORT_URL = ""
    REGISTER_REPORT_COMPONENT_URL = ""
    REGISTER_APP_URL = ""
    REGISTER_UPLOADER_URL = ""
    REGISTER_ALL_URL = ""

    @staticmethod
    def get_machine_token():
        return "machine token from envs"


# pytest -s -v tests/test_new_app.py::test_new_app
def test_new_app():

    config = Config()

    fmw = NewApp(
        name="Oracle Middleware Manager",
        description="""OMWM Automate the analysis and determination of Oracle Middleware usage.""",
        flags=[Flags.BETA],
        config=config,
    )

    print(fmw)


# pytest -s -v tests/test_new_app.py::test_adding_objects
def test_adding_objects():

    config = Config()

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
    )

    rv_tools_uploader = NewUploader(
        name="RVTools",
        description="XLSX export from RVTools after scanning your Vmware infrastructure.",
        uploader_id="rv_tools",
        accepted_file_types=[".xlsx"],
        config=config,
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

    with t.assertRaises(ValueError):
        app.attach_uploaders([rv_tools_uploader])

    with t.assertRaises(ValueError):
        app.attach_reports([fmw_deployment_report])

    with t.assertRaises(ValueError):
        app.attach_components([fmw_summary_component])

    assert isinstance(app.metadata, dict)
    assert "data" in app.metadata

    print(json.dumps(app.full_metadata, sort_keys=True, indent=4, default=str))

    assert isinstance(app.full_metadata, dict)
    assert "data" in app.full_metadata
