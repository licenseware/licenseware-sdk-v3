import uuid
import pytest
from licenseware import ReportPublicToken, Config

# pytest -s -v tests/test_report_public_token.py


def test_report_public_token():

    # Start python3 mock_server.py for this test
    config = Config(PUBLIC_TOKEN_REPORT_URL="http://localhost:4000/report-public-token")

    rpt = ReportPublicToken(
        tenant_id=str(uuid.uuid4()),
        authorization=str(uuid.uuid4()),
        report_id="all_devices_report",
        config=config,
    )

    token = rpt.valid_token("notvalid")
    assert token is False

    token = rpt.get_token()
    assert isinstance(token, str) and len(token) > 10

    tokendata = rpt.get_token_data(token)
    assert isinstance(tokendata, dict)
    assert tokendata["report_id"] == "all_devices_report"

    token = rpt.delete_token(token)
    assert isinstance(token, str) and len(token) > 10
