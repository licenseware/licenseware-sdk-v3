import uuid

import pytest

from licenseware import Config, get_user_info

# pytest -s -v tests/test_get_user_info.py


def test_get_user_info():

    # python3 mock_server.py

    config = Config(USER_INFO_URL="http://localhost:4000/user-info")

    result = get_user_info(
        tenant_id=str(uuid.uuid4()), authorization="some-jwt", config=config
    )

    assert result["plan_type"] == "UNLIMITED"
