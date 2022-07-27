import pytest
import io
import os
import shutil
import pandas as pd
from werkzeug.datastructures import FileStorage
from fastapi import UploadFile

from licenseware import FileUploadHandler

# pytest -s -v tests/test_file_upload_handler.py


# pytest -s -v tests/test_file_upload_handler.py::test_file_handler_objects
def test_file_handler_objects():

    csvfp = "./test_files/lms_detail.csv"
    f = FileUploadHandler(csvfp)

    assert "read" in dir(f)
    assert "seek" in dir(f)
    assert "tell" in dir(f)

    assert isinstance(f.readlines(1), list)
    assert isinstance(f.readline(1), bytes)



# pytest -s -v tests/test_file_upload_handler.py::test_file_handler_string_input
def test_file_handler_string_input():

    csvfp = "./test_files/lms_detail.csv"
    f = FileUploadHandler(csvfp)

    assert f.filename == "lms_detail.csv"

    assert "RL_SCRIPT_VERSION,TIMESTAMP,MACHINE_ID" in str(f.read(1000))
    f.reset()
    assert "RL_SCRIPT_VERSION,TIMESTAMP,MACHINE_ID" in str(f.read(100))
    f.reset()

    dfcsv = pd.read_csv(f.buffer)
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


    # flaskfilestorage.filename
    f = FileUploadHandler(flaskfilestorage)

    assert f.filename == "lms_detail.csv"

    # Same test as for file path as input
    assert "RL_SCRIPT_VERSION,TIMESTAMP,MACHINE_ID" in str(f.read(1000))
    f.reset()
    assert "RL_SCRIPT_VERSION,TIMESTAMP,MACHINE_ID" in str(f.read(100))
    f.reset()

    # print(f.data, type(f.data))
    dfcsv = pd.read_csv(f.buffer)
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

    # fastapiuploadfile.filename
    f = FileUploadHandler(fastapiuploadfile)

    assert f.filename == "lms_detail.csv"

    # Same test as for file path as input
    assert "RL_SCRIPT_VERSION,TIMESTAMP,MACHINE_ID" in str(f.read(1000))
    f.reset()
    assert "RL_SCRIPT_VERSION,TIMESTAMP,MACHINE_ID" in str(f.read(100))
    f.reset()

    dfcsv = pd.read_csv(f.buffer)
    # print(dfcsv.columns)
    assert "RL_SCRIPT_VERSION,TIMESTAMP,MACHINE_ID" in ",".join(list(dfcsv.columns))

    save_path = "./test_files/testdir/testfile.csv"
    f.save(save_path)
    assert os.path.exists(save_path)
    shutil.rmtree(os.path.dirname(save_path))



# pytest -s -v tests/test_file_upload_handler.py::test_file_handler_flask_filestorage_input_seek_2_params
def test_file_handler_flask_filestorage_input_seek_2_params():

    csvfp = "./test_files/RVTools.xlsx"

    with open(csvfp, 'rb') as f:
        file_binary = io.BytesIO(f.read())

        flaskfilestorage = FileStorage(
            stream=file_binary,
            filename=os.path.basename(csvfp),
            content_type="application/*",
        )

    f = FileUploadHandler(flaskfilestorage)

    assert f.filename == "RVTools.xlsx"

    sheets = pd.ExcelFile(f).sheet_names

    assert 'tabvInfo' in sheets



# pytest -s -v tests/test_file_upload_handler.py::test_file_handler_fastapi_uploadfile_input_seek_2_params
def test_file_handler_fastapi_uploadfile_input_seek_2_params():

    csvfp = "./test_files/RVTools.xlsx"

    with open(csvfp, 'rb') as f:
        file_binary = io.BytesIO(f.read())

        fastapiuploadfile = UploadFile(
            filename=os.path.basename(csvfp),
            file=file_binary,
            content_type="application/*",
        )


    f = FileUploadHandler(fastapiuploadfile)
    
    assert f.filename == "RVTools.xlsx"

    sheets = pd.ExcelFile(f).sheet_names

    assert 'tabvInfo' in sheets


    