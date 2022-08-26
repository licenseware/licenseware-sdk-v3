import pytest
import os, shutil
from licenseware import create_xlsx_file, Config

# pytest -s -v tests/test_create_xlsx_file.py


def test_create_xlsx_file():

    config = Config(FILE_UPLOAD_PATH="./test_files")

    dirpath, filename = create_xlsx_file(
        tenant_id="some-tenant-id",
        filename="test.xlsx",
        sheets={"tabname": {"col1": "data"}},
        config=config,
    )
    filepath = os.path.join(dirpath, filename)
    assert os.path.exists(filepath)
    assert filename == "test.xlsx"

    shutil.rmtree(dirpath)
