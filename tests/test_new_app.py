import pytest
import unittest
from dataclasses import dataclass
from licenseware import (
    NewApp,
    Flags
)


# pytest -s -v tests/test_new_app.py

t = unittest.TestCase()


# pytest -s -v tests/test_new_app.py::test_new_app
def test_new_app():

    @dataclass
    class Config:
        APP_ID = "fmw"
        REGISTER_REPORT_URL = ""
        REGISTER_REPORT_COMPONENT_URL = ""
        REGISTER_APP_URL = ""

        @staticmethod
        def get_machine_token():
            return "machine token from envs"


    config = Config()

    fmw = NewApp(
        name="Oracle Middleware Manager",
        description="""OMWM Automate the analysis and determination of Oracle Middleware usage.""",
        flags=[Flags.BETA],
        get_tenants_with_app_activated_handler = None,
        get_tenants_with_data_available_handler = None,
        get_tenants_with_public_reports_handler = None,
        get_tenant_features_handler = None,
        config = config
    )

    print(fmw)


