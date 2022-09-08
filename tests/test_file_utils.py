import os
import shutil

from licenseware import is_archive, recursive_unzip, unzip

# pytest -s -v tests/test_file_utils.py


# pytest -s -v tests/test_file_utils.py::test_file_utils_unzip
def test_file_utils_unzip():

    zippath = "./tests/test_files/zip.tar.xz"

    unzipedpath = unzip(zippath)

    assert os.path.exists(unzipedpath)

    assert os.listdir(unzipedpath) == [
        "sniff_delimiter_csv",
        "sniff_delimiter_csv.zip",
        "lms_detail_empty.csv",
        "RVTools.xlsx",
        "sniff_delimiter_csv.tar.xz",
        "lms_detail.csv",
    ]

    shutil.rmtree(unzipedpath)


# pytest -s -v tests/test_file_utils.py::test_file_utils_recursive_unzip
def test_file_utils_recursive_unzip():

    zippath = "./tests/test_files/zip.tar.xz"

    unzipedpath = recursive_unzip(zippath)

    assert os.path.exists(unzipedpath)

    for fname in os.listdir(unzipedpath):
        assert not is_archive(fname)

    shutil.rmtree(unzipedpath)
