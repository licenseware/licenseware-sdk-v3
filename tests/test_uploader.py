import pytest
from licenseware.uploader import (
    NewUploader, 
    UploaderValidationParameters,
    UploaderEncryptionParameters, 
)


# pytest tests/test_uploader.py

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
        def get_auth_token():
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
        # There are some cases where you may need to replace these
        # validation handlers with some custom handlers (hover to see types)
        filenames_validation_handler=None,
        filecontents_validation_handler=None,
        flags=None,
        status=None,
        icon=None,
        # External config object 
        # From which we would get uploader-registry-url
        config=config
    )

    response = rv_tools_uploader.validate_filenames(filenames)
    # print(response)
    for resp in response.validation:
        if resp.filename == "notok.csv":
            assert resp.status == "failed"
        if resp.filename == "rv_tools":
            assert resp.status == "success"

        
    payload = rv_tools_uploader.get_registration_payload()
    assert "data" in payload

    response, status_code = rv_tools_uploader.register()
    assert status_code == 200
    assert "success" == response['status']
