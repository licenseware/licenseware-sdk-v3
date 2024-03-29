from licenseware import get_user_info

from . import config, tenant_id

# pytest -s -v tests/test_get_user_info.py


def test_get_user_info(mocker):

    # python3 mock_server.py

    class MockResponse:
        status_code = 200

        @staticmethod
        def json():
            return {"user_id": tenant_id, "plan_type": "UNLIMITED"}

    mocker.patch("requests.get", return_value=MockResponse)

    result = get_user_info(tenant_id=tenant_id, authorization="some-jwt", config=config)

    assert result["plan_type"] == "UNLIMITED"
