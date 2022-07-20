import pytest
from licenseware import (
    NewUploader, 
    UploaderValidationParameters,
    UploaderEncryptionParameters, 
    FileTypes
)

from licenseware.uploader.defaults import (
    default_filenames_validation_handler, 
    default_filecontents_validation_handler,
    default_check_quota_handler,
    default_check_status_handler,
)

# pytest -s -v tests/test_new_uploader.py


# pytest -s -v tests/test_new_uploader.py::test_new_uploader
def test_new_uploader(mocker):

    class RequestsResponse:
        status_code = 200

    mocker.patch(
        "requests.post",
        return_value=RequestsResponse
    )
    
    # External configuration
    class Config:
        APP_ID = "ifmp"
        REGISTER_UPLOADER_URL = ""

        @staticmethod
        def get_machine_token():
            return "machine token from envs"

    config = Config()


    filenames = ["notok.csv", "rv_tools.xlsx"]

    assert isinstance(FileTypes.GENERIC_EXCEL, tuple)

    rv_tools_encryption_parameters = UploaderEncryptionParameters()
    rv_tools_validation_parameters = UploaderValidationParameters(
        filename_contains=['rv', 'tools'],
        filename_endswith=FileTypes.GENERIC_EXCEL # or [".xls", ".xlsx"] 
    )

    rv_tools_uploader = NewUploader(
        name="RVTools",
        description="XLSX export from RVTools after scanning your Vmware infrastructure.",
        uploader_id="rv_tools",
        accepted_file_types=FileTypes.GENERIC_EXCEL,
        validation_parameters=rv_tools_validation_parameters,
        encryption_parameters=rv_tools_encryption_parameters,
        config=config
    )

    response = rv_tools_uploader.validate_filenames(filenames)

    for resp in response.validation:
        if resp.filename == "notok.csv":
            assert resp.status == "failed"
        if resp.filename == "rv_tools.xlsx":
            assert resp.status == "success"
        

    fp = "./test_files/RVTools.xlsx"
    files = [fp]
    response = rv_tools_uploader.validate_filecontents(files)

    for resp in response.validation:
        if resp.filename == "notok.csv":
            assert resp.status == "failed"
        if resp.filename == "rv_tools.xlsx":
            assert resp.status == "success"


    assert "data" in rv_tools_uploader.metadata

    response, status_code = rv_tools_uploader.register()
    assert status_code == 200
    assert "success" == response['status']

    # TODO
    # response = rv_tools_uploader.check_quota()
    # response = rv_tools_uploader.check_status()



# pytest -s -v tests/test_new_uploader.py::test_new_uploader_custom_handlers
def test_new_uploader_custom_handlers(mocker):

    class RequestsResponse:
        status_code = 200

    mocker.patch(
        "requests.post",
        return_value=RequestsResponse
    )
    
    # External configuration
    class Config:
        APP_ID = "ifmp"
        REGISTER_UPLOADER_URL = ""

        @staticmethod
        def get_machine_token():
            return "machine token from envs"

    config = Config()


    filenames = ["notok.csv", "rv_tools.xlsx"]

    assert isinstance(FileTypes.GENERIC_EXCEL, tuple)

    rv_tools_encryption_parameters = UploaderEncryptionParameters()
    rv_tools_validation_parameters = UploaderValidationParameters(
        filename_contains=['rv', 'tools'],
        filename_endswith=FileTypes.GENERIC_EXCEL # or [".xls", ".xlsx"] 
    )


    def custom_validate_filenames(*args, **kwargs):
        # some extra processing here
        return default_filenames_validation_handler(*args, **kwargs)

    def custom_validate_filecontents(*args, **kwargs):
        # some extra processing here
        return default_filecontents_validation_handler(*args, **kwargs)

    # TODO custom funcs for
    # response = rv_tools_uploader.check_quota()
    # response = rv_tools_uploader.check_status()


    rv_tools_uploader = NewUploader(
        name="RVTools",
        description="XLSX export from RVTools after scanning your Vmware infrastructure.",
        uploader_id="rv_tools",
        accepted_file_types=FileTypes.GENERIC_EXCEL,
        validation_parameters=rv_tools_validation_parameters,
        encryption_parameters=rv_tools_encryption_parameters,
        filenames_validation_handler=custom_validate_filenames,
        filecontents_validation_handler=custom_validate_filecontents,
        config=config
    )

    response = rv_tools_uploader.validate_filenames(filenames)

    for resp in response.validation:
        if resp.filename == "notok.csv":
            assert resp.status == "failed"
        if resp.filename == "rv_tools.xlsx":
            assert resp.status == "success"
        

    fp = "./test_files/RVTools.xlsx"
    files = [fp]
    response = rv_tools_uploader.validate_filecontents(files)

    for resp in response.validation:
        if resp.filename == "notok.csv":
            assert resp.status == "failed"
        if resp.filename == "rv_tools.xlsx":
            assert resp.status == "success"


    assert "data" in rv_tools_uploader.metadata

    response, status_code = rv_tools_uploader.register()
    assert status_code == 200
    assert "success" == response['status']