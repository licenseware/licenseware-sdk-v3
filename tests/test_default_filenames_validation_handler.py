import pytest
from licenseware.uploader.defaults import default_filenames_validation_handler
from licenseware.uploader import UploaderValidationParameters
from licenseware import FileTypes

# pytest -s -v tests/test_default_filenames_validation_handler.py

def test_default_filenames_validation_handler():
    
    filenames = ["cpuq.xlsx"]

    rv_tools_validation_parameters = UploaderValidationParameters(
        filename_contains=['rv', 'tools'],
        filename_endswith=FileTypes.GENERIC_EXCEL #['.xlsx']
    )

    res = default_filenames_validation_handler(filenames, rv_tools_validation_parameters)

    for r in res.validation:
        if r.filename == "cpuq.xlsx":
            assert r.message == 'File must contain at least one of the following keywords: rv, tools'  
