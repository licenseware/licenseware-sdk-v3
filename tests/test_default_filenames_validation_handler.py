import pytest

from licenseware import FileTypes
from licenseware.uploader import UploaderValidationParameters
from licenseware.uploader.default_handlers import default_filenames_validation_handler

# pytest -s -v tests/test_default_filenames_validation_handler.py


def test_default_filenames_validation_handler():

    filenames = ["cpuq.xlsx", "rv_tools.xlsx"]

    rv_tools_validation_parameters = UploaderValidationParameters(
        filename_contains=["rv", "tools"],
        filename_endswith=FileTypes.GENERIC_EXCEL,  # ['.xlsx']
    )

    res = default_filenames_validation_handler(
        filenames, rv_tools_validation_parameters
    )

    for r in res.content.validation:

        if r.filename == "cpuq.xlsx":
            assert (
                r.message
                == "File must contain at least one of the following keywords: rv, tools"
            )

        if r.filename == "rv_tools.xlsx":
            assert r.message == "File is valid"
