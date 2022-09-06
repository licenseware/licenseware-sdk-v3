import unittest

import pytest

from licenseware.utils.xss_protection import xss_protection

# pytest -s -v tests/test_xss_protection.py

t = unittest.TestCase()


def test_xss_protection():

    data = {
        "integration_id": "lansweeper",
        "updated_at": "2022-05-17T04:46:12.205750",
        "tenant_id": "437fe9d0-39c7-55bd-b12d-95025991cc4a",
        "logo": None,
        "description": "Integration with Lansweeper API's",
        "test_url": "https://www.lansweeper.com/",
        "inputs": [
            {
                "label": "Lansweeper Password",
                "id": "lansweeper_password",
                "value": "https://lansweeper.123.com",
                "error_message": "URL should start with https://lansweeper.123.com",
                "rules": None,
                "type": "password",
            }
        ],
        "name": "Lansweeper",
        "status": "disabled",
        "apps": [
            {
                "app_id": "odb-service",
                "name": "Oracle Database",
                "description": "Analyse oracle database",
                "integration_id": "lansweeper",
                "imported_data": ["oracle_databases"],
                "exported_data": ["reports"],
                "triggers": [
                    "database_created",
                    "database_deleted",
                    "< HTTP-EQUIV charset=network_scan",
                ],
            }
        ],
    }

    with t.assertRaises(Exception):
        xss_protection(data)
