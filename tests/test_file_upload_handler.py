import pytest
import io
import os
import shutil
import pandas as pd
from werkzeug.datastructures import FileStorage
from fastapi import UploadFile

from licenseware.uploader import FileUploadHandler



# pytest -s -v tests/test_file_upload_handler.py


# pytest -s -v tests/test_file_upload_handler.py::test_file_handler_string_input
def test_file_handler_string_input():

    csvfp = "./test_files/lms_detail.csv"
    f = FileUploadHandler(csvfp)

    assert "RL_SCRIPT_VERSION,TIMESTAMP,MACHINE_ID" in str(f.read(1000))
    f.reset()
    assert "RL_SCRIPT_VERSION,TIMESTAMP,MACHINE_ID" in str(f.read(100))
    f.reset()

    dfcsv = pd.read_csv(f.data())
    assert "RL_SCRIPT_VERSION,TIMESTAMP,MACHINE_ID" in ",".join(list(dfcsv.columns))

    save_path = "./test_files/testdir/testfile.csv"
    f.save(save_path)
    assert os.path.exists(save_path)
    shutil.rmtree(os.path.dirname(save_path))


# pytest -s -v tests/test_file_upload_handler.py::test_file_handler_flask_file_storage_input
def test_file_handler_flask_file_storage_input():

    csvfp = "./test_files/lms_detail.csv"

    with open(csvfp, 'rb') as f:
        file_binary = io.BytesIO(f.read())

        flaskfilestorage = FileStorage(
            stream=file_binary,
            filename=os.path.basename(csvfp),
            content_type="application/*",
        )


    f = FileUploadHandler(flaskfilestorage)

    # Same test as for file path as input
    assert "RL_SCRIPT_VERSION,TIMESTAMP,MACHINE_ID" in str(f.read(1000))
    f.reset()
    assert "RL_SCRIPT_VERSION,TIMESTAMP,MACHINE_ID" in str(f.read(100))
    f.reset()

    # print(f.data, type(f.data))
    dfcsv = pd.read_csv(f.data())
    # print(dfcsv.columns)
    assert "RL_SCRIPT_VERSION,TIMESTAMP,MACHINE_ID" in ",".join(list(dfcsv.columns))

    save_path = "./test_files/testdir/testfile.csv"
    f.save(save_path)
    assert os.path.exists(save_path)
    shutil.rmtree(os.path.dirname(save_path))




# pytest -s -v tests/test_file_upload_handler.py::test_file_handler_fastapi_uploadfile_input
def test_file_handler_fastapi_uploadfile_input():

    csvfp = "./test_files/lms_detail.csv"

    with open(csvfp, 'rb') as f:
        file_binary = io.BytesIO(f.read())

        fastapiuploadfile = UploadFile(
            filename=os.path.basename(csvfp),
            file=file_binary,
            content_type="application/*",
        )

    f = FileUploadHandler(fastapiuploadfile)

    # Same test as for file path as input
    assert "RL_SCRIPT_VERSION,TIMESTAMP,MACHINE_ID" in str(f.read(1000))
    f.reset()
    assert "RL_SCRIPT_VERSION,TIMESTAMP,MACHINE_ID" in str(f.read(100))
    f.reset()

    dfcsv = pd.read_csv(f.data())
    # print(dfcsv.columns)
    assert "RL_SCRIPT_VERSION,TIMESTAMP,MACHINE_ID" in ",".join(list(dfcsv.columns))

    save_path = "./test_files/testdir/testfile.csv"
    f.save(save_path)
    assert os.path.exists(save_path)
    shutil.rmtree(os.path.dirname(save_path))

