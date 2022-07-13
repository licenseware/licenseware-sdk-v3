import pytest
from licenseware.uploader import (
    NewUploader, 
    UploaderValidationParameters,
    UploaderEncryptionParameters, 
)


# pytest -s -v tests/test_uploader.py

def test_uploader(mocker):

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

    rv_tools_encryption_parameters = UploaderEncryptionParameters()
    rv_tools_validation_parameters = UploaderValidationParameters(
        filename_contains=['rv', 'tools'],
        filename_endswith=['.xlsx']
    )

    rv_tools_uploader = NewUploader(
        name="RVTools",
        description="XLSX export from RVTools after scanning your Vmware infrastructure.",
        uploader_id="rv_tools",
        accepted_file_types=[".xls", ".xlsx"],
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
