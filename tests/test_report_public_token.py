import datetime

import pytest

from licenseware import Config, ReportPublicToken

from . import tenant_id

# pytest -s -v tests/test_report_public_token.py


def get_quota_reset_date(current_date: datetime.datetime = datetime.datetime.utcnow()):
    quota_reset_date = current_date + datetime.timedelta(days=30)
    return quota_reset_date.isoformat()


def test_report_public_token(mocker):
    class MockResponseGet:
        status_code = 200
        content = "mock content"

        @staticmethod
        def json():
            return {"expiration_date": get_quota_reset_date()}

    class MockResponseDelete:
        status_code = 200
        content = "mock content"

        @staticmethod
        def json():
            return "some token ------------"

    mocker.patch("requests.get", return_value=MockResponseGet)
    mocker.patch("requests.delete", return_value=MockResponseDelete)

    # Start python3 mock_server.py for this test
    config = Config(PUBLIC_TOKEN_REPORT_URL="http://localhost:4000/report-public-token")

    rpt = ReportPublicToken(
        tenant_id=tenant_id,
        authorization="mock-jwt",
        report_id="all_devices_report",
        config=config,
    )

    # token = rpt.valid_token("notvalid")
    # assert token is False

    token = rpt.get_token()
    assert isinstance(token, str) and len(token) > 10

    tokendata = rpt.get_token_data(token)
    assert isinstance(tokendata, dict)
    assert tokendata["report_id"] == "all_devices_report"

    token = rpt.delete_token(token)
    assert isinstance(token, str) and len(token) > 10
