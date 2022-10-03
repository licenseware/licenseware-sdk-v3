import os
import shutil

from licenseware import (
    create_csv_file,
    create_file,
    create_json_file,
    create_xlsx_file,
)

from . import config


# pytest -s -v tests/test_create_files.py


# pytest -s -v tests/test_create_files.py::test_create_xlsx_file
def test_create_xlsx_file():

    filepath, filename = create_xlsx_file(
        tenant_id="some-tenant-id",
        filename="test.xlsx",
        data={"tabname": {"col1": "data"}},
        config=config,
    )
    assert os.path.exists(filepath)
    assert filename == "test.xlsx"

    shutil.rmtree(os.path.dirname(filepath))


# pytest -s -v tests/test_create_files.py::test_create_json_file
def test_create_json_file():

    filepath, filename = create_json_file(
        tenant_id="some-tenant-id",
        filename="test.json",
        data={"tabname": {"col1": "data"}},
        config=config,
    )
    assert os.path.exists(filepath)
    assert filename == "test.json"

    shutil.rmtree(os.path.dirname(filepath))


# pytest -s -v tests/test_create_files.py::test_create_csv_file
def test_create_csv_file():

    data = [
        {
            "device_type": "Virtual",
        },
        {
            "device_type": "Virtual",
        },
    ]

    filepath, filename = create_csv_file(
        tenant_id="some-tenant-id",
        filename="test.csv",
        data=data,
        config=config,
    )
    assert os.path.exists(filepath)
    assert filename == "test.csv"

    shutil.rmtree(os.path.dirname(filepath))


# pytest -s -v tests/test_create_files.py::test_create_file
def test_create_file():

    data = [
        {
            "device_type": "Virtual",
        },
        {
            "device_type": "Virtual",
        },
    ]

    filepath, filename = create_file(
        tenant_id="some-tenant-id",
        filename="test.csv",
        filetype="csv",
        data=data,
        config=config,
    )
    assert os.path.exists(filepath)
    assert filename == "test.csv"

    shutil.rmtree(os.path.dirname(filepath))
