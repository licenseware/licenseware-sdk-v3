import pytest
from pymongo import MongoClient

from licenseware import (
    Config,
    MongoRepository,
    NewReport,
    NewReportComponent,
    PieAttrs,
    ReportSnapshot,
    StyleAttrs,
    WebResponse,
)

from . import tenant_id


@pytest.fixture
def mongo_connection():
    MONGO_DATABASE_NAME = "testdb"
    MONGO_CONNECTION_STRING = "mongodb://lware:lware-secret@localhost:27017"
    mongo_connection = MongoClient(MONGO_CONNECTION_STRING)[MONGO_DATABASE_NAME]
    return mongo_connection


@pytest.fixture
def repo(mongo_connection):
    config = Config()
    return MongoRepository(
        mongo_connection,
        collection=config.MONGO_COLLECTION.REPORT_SNAPSHOTS,
        data_validator="ignore",
    )


# pytest -s -v tests/test_report_snapshot.py


def test_report_snaphot(repo, mocker):
    class RequestsResponse:
        status_code = 200

        @staticmethod
        def json():
            return [{"status": ["success"]}]

    mocker.patch("requests.post", return_value=RequestsResponse)
    mocker.patch("requests.get", return_value=RequestsResponse)

    config = Config(FRONTEND_URL="fe url", PUBLIC_TOKEN_REPORT_URL="report public")

    def get_component_data(*args, **kwargs):
        return WebResponse(status_code=200, content=[{"some_field": "some_data"}])

    pie = (
        PieAttrs()
        .attr(
            label_key="product_name",
            label_description="WebLogic Edition",
            value_key="number_of_devices",
            value_description="Number of Devices",
        )
        .attr(label_key="device_name", value_key="devices_numbers")
    )

    all_devices_component = NewReportComponent(
        title="All Devices",
        component_id="all_devices",
        attributes=pie,
        style_attributes=StyleAttrs().width_full,
        get_component_data_handler=get_component_data,
        config=config,
    )

    devices_overview_report = NewReport(
        name="Device Details",
        description="This report collects all the device information captured during processing.",
        report_id="device_details_report",
        components=[all_devices_component],
        config=config,
    )

    devices_overview_report.attach("all_devices")

    rpt = ReportSnapshot(
        tenant_id=tenant_id,
        authorization="not used",
        repo=repo,
        config=config,
        report=devices_overview_report,
    )

    result = rpt.generate_snapshot()

    assert isinstance(result["version"], str)
    assert len(result["version"]) == len("0VLVV8")

    result = rpt.get_available_versions()

    assert isinstance(result["version"], list)
    assert len(result["version"]) > 0

    version = result["version"][0]

    result = rpt.get_snapshot_metadata()

    assert isinstance(result, dict)
    assert len(result) > 0
    assert "report_uuid" in result

    result = rpt.get_snapshot_component("all_devices", version)

    assert isinstance(result, list)
    assert len(result) > 0
    assert isinstance(result[0], dict)
    assert "some_field" in result[0]

    result = rpt.update_component_snapshot(
        result[0]["_id"],
        result[0]["version"],
        result[0]["component_id"],
        {"some_field": "with new data"},
    )

    assert isinstance(result, dict)
    assert result["some_field"] == "with new data"

    # print(result)
