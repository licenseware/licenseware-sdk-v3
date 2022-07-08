import pytest
import io
import os
from fastapi import UploadFile
from werkzeug.datastructures import FileStorage
from licenseware.uploader import UploaderValidationParameters
from licenseware.uploader.file_upload_handler import FileUploadHandler
from licenseware.uploader.defaults import default_filecontents_validation_handler
from licenseware.uploader.defaults import helpers

# pytest -s -v tests/test_default_filecontents_validation_handler.py



# pytest -s -v tests/test_default_filecontents_validation_handler.py::test_sniff_delimiter
def test_sniff_delimiter():

    response = helpers.sniff_delimiter(f, "RVTools.xlsx")
    print(response)




def test_required_input_type_response():
    helpers.required_input_type_response

def test_text_contains_all_response():
    helpers.text_contains_all_response

def test_text_contains_any_response():
    helpers.text_contains_any_response

def test_get_csv_df():
    helpers.get_csv_df

def test_get_df_sheets():
    helpers.get_df_sheets

def test_get_excel_dfs():
    helpers.get_excel_dfs

def test_required_columns_response():
    helpers.required_columns_response

def test_required_sheets_response():
    helpers.required_sheets_response

def test_min_rows_number_response():
    helpers.min_rows_number_response

def test_get_filenames_response():
    helpers.get_filenames_response

def test_get_error_message():
    helpers.get_error_message

def test_get_failed_validations():
    helpers.get_failed_validations


def test_default_filecontents_validation_handler():

    lmsfp = "./test_files/lms_detail.csv"

    with open(lmsfp, 'rb') as f:
        file_binary = io.BytesIO(f.read())

        lmsflask = FileStorage(
            stream=file_binary,
            filename=os.path.basename(lmsfp),
            content_type="application/*",
        )

    lmsemptyfp = "./test_files/lms_detail_empty.csv"

    with open(lmsemptyfp, 'rb') as f:
        file_binary = io.BytesIO(f.read())

        lmsemptyfastapi = UploadFile(
            filename=os.path.basename(lmsemptyfp),
            file=file_binary,
            content_type="application/*",
        )


    rvtoolsfp = "./test_files/RVTools.xlsx"

    with open(rvtoolsfp, 'rb') as f:
        file_binary = io.BytesIO(f.read())

        rvtoolsflask = FileStorage(
            stream=file_binary,
            filename=os.path.basename(rvtoolsfp),
            content_type="application/*",
        )

        rvtoolsfastapi = UploadFile(
            filename=os.path.basename(rvtoolsfp),
            file=file_binary,
            content_type="application/*",
        )


    # files = [lmsflask, lmsemptyfastapi, rvtoolsflask, rvtoolsfastapi]
    files = [rvtoolsflask, rvtoolsfastapi]

    rv_tools_validation_parameters = UploaderValidationParameters(
        filename_contains=['rv', 'tools'],
        filename_endswith=['.xlsx'],
        required_input_type="excel",
        min_rows_number=1,
        header_starts_at=0,
        required_sheets=[
            ("tabvInfo", "tabvCPU", "tabvHost", "tabvCluster"),
            ("vInfo", "vCPU", "vHost", "vCluster"),
        ],
        required_columns = [
            'VM', 'Host', 'OS', 'Sockets', 'CPUs', 'Model', 'CPU Model',
            'Cluster', '# CPU', '# Cores', 'ESX Version', 'HT Active',
            'Name', 'NumCpuThreads', 'NumCpuCores'
        ]
    )


    response = default_filecontents_validation_handler(files, rv_tools_validation_parameters)

    print(response)

    for res in response.validation:
        if res.filename == "RVTools.xlsx":
            print(res.message)
            assert res.status == 'success'

