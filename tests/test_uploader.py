import unittest
from licenseware.uploader import (
    NewUploader, 
    UploaderValidationParameters,
    UploaderEncryptionParameters, 
)



# What goes to registry service 
# payload = {
#     'data': [{
#         "app_id": kwargs['app_id'],
#         "uploader_id": kwargs['uploader_id'],
#         "name": kwargs['name'],
#         "description": kwargs['description'],
#         "accepted_file_types": kwargs['accepted_file_types'],
#         "flags": kwargs['flags'] if len(kwargs['flags']) > 0 else None,
#         "status": kwargs['status'],
#         "icon": kwargs['icon'],
#         "upload_url": kwargs['upload_url'],
#         "upload_validation_url": kwargs['upload_validation_url'],
#         "quota_validation_url": kwargs['quota_validation_url'],
#         "status_check_url": kwargs['status_check_url'],
#         "validation_parameters": kwargs['validation_parameters'],
#         "encryption_parameters": kwargs['encryption_parameters']
#     }]
# }


# python3 -m unittest tests/test_uploader.py

class TestUploader(unittest.TestCase):


    def test_uploader(self):

        # def validate_filenames(filenames, validation_parameters: UploaderValidationParameters):
        #     print(validation_parameters.ignore_filenames)
        #     return filenames


        # def validate_filecontents(file):
        #     if file: return True
        #     return False


        filenames = ["notok.csv", "rv_tools.xlsx"]

        rv_tools_encryption_parameters = UploaderEncryptionParameters()
        rv_tools_validation_parameters = UploaderValidationParameters(
            filename_contains=['rv', 'tools'],
            filename_endswith=['.xlsx']
        )

        rv_tools_uploader = NewUploader(
            app_id="ifmp-service",
            uploader_id="rv_tools",
            name="RVTools",
            description="XLSX export from RVTools after scanning your Vmware infrastructure.",
            accepted_file_types=[".xls", ".xlsx"],
            validation_parameters=rv_tools_validation_parameters,
            encryption_parameters=rv_tools_encryption_parameters,
            filenames_validation_handler=None,
            filecontents_validation_handler=None,
            flags=None,
            status=None,
            icon=None,
            upload_url=None,
            upload_validation_url=None,
            quota_validation_url=None,
            status_check_url=None,
        )

        response = rv_tools_uploader.validate_filenames(filenames)
        # print(response)
        for resp in response.validation:
            if resp.filename == "notok.csv":
                assert resp.status == "failed"
            if resp.filename == "rv_tools":
                assert resp.status == "success"


        registration_payload = rv_tools_uploader.get_registration_payload()
        # print(registration_payload)
        assert "data" in registration_payload
