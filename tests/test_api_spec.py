import pytest
import unittest
from typing import List
from dataclasses import dataclass
from licenseware import ApiSpec


# pytest -s -v tests/test_api_spec.py


t = unittest.TestCase()


# pytest -s -v tests/test_api_spec.py::test_adding_routes_to_api_spec
def test_adding_routes_to_api_spec():


    FileUploadApiSpecs = ApiSpec(
        title="File Upload", 
        description="Validate filenames, upload files and check quota or status",
    )

    (
        FileUploadApiSpecs
        .route("/uploads/{uploader_id}/validation", handler="function_name")
        .path_param(name="uploader_id")
        .request_body({
            "filenames": [
                "string"
            ]
        })
        .response(method="GET", response="Some response", status_code=200)
    )

    # print(filename_validation_specs.metadata.routes)

    assert len(FileUploadApiSpecs.routes) == 1
    assert len(FileUploadApiSpecs.routes[0].path_params) == 1
    assert FileUploadApiSpecs.routes[0].route == "/uploads/{uploader_id}/validation"
    assert FileUploadApiSpecs.routes[0].path_params[0].name == "uploader_id"


    @dataclass
    class Files:
        files: List[bytes]

    (
        FileUploadApiSpecs
        .route("/uploads/{uploader_id}/files", handler="function_name")
        .path_param(name="uploader_id")
        .request_files(Files)
    )

    # print(fileupload_specs.metadata.routes)

    assert len(FileUploadApiSpecs.routes) == 2
    assert FileUploadApiSpecs.routes[1].route == "/uploads/{uploader_id}/files"
    assert FileUploadApiSpecs.routes[1].path_params[0].name == "uploader_id"


# pytest -s -v tests/test_api_spec.py::test_adding_route_prefix
def test_adding_route_prefix():
    
    FileUploadApiSpecs = ApiSpec(
        title="File Upload", 
        description="Validate filenames, upload files and check quota or status",
        prefix="/uploads"
    )

    FileUploadApiSpecs.route("/test", handler="function_name")

    FileUploadApiSpecs.routes[0].route == "/uploads/test"




# pytest -s -v tests/test_api_spec.py::test_fail_overwrite_params
def test_fail_overwrite_params():

    with t.assertRaises(ValueError):
        (
            ApiSpec(title="SomeTitle")
            .route("/uploads/{uploader_id}/files", handler="function_name")
            .route("/uploads/{uploader_id}/files", handler="function_name")
        )


    with t.assertRaises(ValueError):
        (
            ApiSpec(title="SomeTitle")
            .route("/uploads/{uploader_id}/files", handler="function_name")
            .path_param("some_param")
            .path_param("some_param")
        )


    with t.assertRaises(ValueError):
        (
            ApiSpec(title="SomeTitle")
            .route("/uploads/{uploader_id}/files", handler="function_name")
            .header_param("some_param")
            .header_param("some_param")
        )

    
    with t.assertRaises(ValueError):
        (
            ApiSpec(title="SomeTitle")
            .route("/uploads/{uploader_id}/files", handler="function_name")
            .query_param("some_param")
            .query_param("some_param")
        )


    with t.assertRaises(ValueError):
        (
            ApiSpec(title="SomeTitle")
            .route("/uploads/{uploader_id}/files", handler="function_name")
            .cookie_param("some_param")
            .cookie_param("some_param")
        )

    with t.assertRaises(ValueError):
        (
            ApiSpec(title="SomeTitle")
            .route("/uploads/{uploader_id}/files", handler="function_name")
            .request_body(bytes)
            .request_body(bytes)
        )

    
    with t.assertRaises(ValueError):
        (
            ApiSpec(title="SomeTitle")
            .route("/uploads/{uploader_id}/files", handler="function_name")
            .request_form(bytes)
            .request_form(bytes)
        )


    with t.assertRaises(ValueError):
        (
            ApiSpec(title="SomeTitle")
            .route("/uploads/{uploader_id}/files", handler="function_name")
            .request_files(bytes)
            .request_files(bytes)
        )


    with t.assertRaises(ValueError):
        (
            ApiSpec(title="SomeTitle")
            .route("/uploads/{uploader_id}/files", handler="function_name")
            .response(method="GET", response="Some response", status_code=200)
            .response(method="GET", response="Some response", status_code=200)
        )




