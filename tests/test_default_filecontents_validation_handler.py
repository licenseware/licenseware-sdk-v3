import pytest
from licenseware.uploader.defaults import default_filecontents_validation_handler
import io
import os
from fastapi import UploadFile
from werkzeug.datastructures import FileStorage
from licenseware.uploader import UploaderValidationParameters


# pytest -s -v tests/test_default_filecontents_validation_handler.py


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

