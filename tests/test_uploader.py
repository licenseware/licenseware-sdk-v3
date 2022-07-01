import unittest
from licenseware import uploader

# python3 -m unittest tests/test_uploader.py



class TestUploader(unittest.TestCase):


    def test_filename_validator(self):

        rv_tools_validator = uploader.FileValidator(
            filename_contains=["rv_tools"],
            filename_endswith=[".xls"]
        )

        filenames = ["notok.csv", "rv_tools.xlsx"]
        response = rv_tools_validator.validate_filenames(filenames)

        # print(response)
        for resp in response.validation:
            if resp.filename == "notok.csv":
                assert resp.status == "failed"
            if resp.filename == "rv_tools":
                assert resp.status == "success"




    # def test_uploader(self):

    #     filepath = "./test_files/RVTools.xlsx"

    #     rv_tools_validator = uploader.FileValidator(
    #         filename_contains=["rv_tools"],
    #         filename_endswith=[".xls"]
    #     )

    #     rv_tools_uploader = uploader.New(
    #         app_id="ifmp-service",
    #         uploader_id="rv_tools",
    #         name="RV Tools",
    #         description="Upload rv tools files",
    #         accepted_file_types=(".xls", ".xlsx"),
    #         file_validator=rv_tools_validator
    #     )

    #     rv_tools_uploader