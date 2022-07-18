from dataclasses import dataclass
import pytest
import unittest
from licenseware import (
    ApiSpec
)


# pytest -s -v tests/test_api_spec.py


t = unittest.TestCase()


# pytest -s -v tests/test_api_spec.py::test_api_spec
def test_api_spec():

    @dataclass
    class Payload:
        name: str
        age: int

    @dataclass
    class PayloadFiles:
        file: bytes


    api_specs = (
        ApiSpec()
        .route("/some-path")
        .header_param(
            name="Authorization", 
            description="Token used to authorize requests"
        )
        .header_param(
            name="TenantId", 
            description="Tenant id for this request"
        )
        .query_param(name="clear_data", description="Clear existing data before uploading files")
        .path_param(name="report_id")
        .cookie_param(name="expire")
        .request_body(Payload)
        .request_form(Payload)
        .request_files(PayloadFiles)
        .response(method="GET", response=Payload, status_code=200)
        .response(method="POST", response=Payload, status_code=201)
    )

    # print(api_specs.metadata)

    assert api_specs.metadata.route == "/some-path"
    assert api_specs.metadata.header_params[0].name == "Authorization"
    assert api_specs.metadata.header_params[1].name == "TenantId"


    with t.assertRaises(ValueError):
        api_specs = (
            ApiSpec()
            .route("/some-path")
            .path_param(name="report_id")
            .path_param(name="report_id")
        )


    