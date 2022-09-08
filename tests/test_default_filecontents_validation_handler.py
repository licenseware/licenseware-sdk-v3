import os

from licenseware import FileUploadHandler
from licenseware.uploader import UploaderValidationParameters
from licenseware.uploader.default_handlers import (
    default_filecontents_validation_handler,
    helpers,
)

# pytest -s -v tests/test_default_filecontents_validation_handler.py


# pytest -s -v tests/test_default_filecontents_validation_handler.py::test_sniff_delimiter
def test_sniff_delimiter():

    result_map = {"semicolon.csv": ";", "comma.csv": ",", "pipe.csv": "|"}

    snifffp = "./tests/test_files/sniff_delimiter_csv/"
    filepaths = [
        os.path.join(snifffp, f) for f in os.listdir(snifffp) if f.endswith(".csv")
    ]

    for fp in filepaths:
        f = FileUploadHandler(fp)
        delimiter = helpers.sniff_delimiter(f)
        assert delimiter == result_map[os.path.basename(fp)]

    fp = "./tests/test_files/lms_detail.csv"
    f = FileUploadHandler(fp)

    delimiter = helpers.sniff_delimiter(f)
    assert delimiter == ","


# pytest -s -v tests/test_default_filecontents_validation_handler.py::test_required_input_type_response
def test_required_input_type_response():

    fp = "./tests/test_files/lms_detail.csv"
    f = FileUploadHandler(fp)
    vparams = UploaderValidationParameters(required_input_type="csv")

    assert helpers.required_input_type_response(f, vparams) == True

    vparams = UploaderValidationParameters(required_input_type="excel")

    res = helpers.required_input_type_response(f, vparams)
    assert "File is not of required input type" in res

    fp = "./tests/test_files/RVTools.xlsx"
    f = FileUploadHandler(fp)

    vparams = UploaderValidationParameters(
        required_input_type="excel", required_sheets=["tabvInfo"]
    )

    assert helpers.required_input_type_response(f, vparams) == True


# pytest -s -v tests/test_default_filecontents_validation_handler.py::test_text_contains_all_response
def test_text_contains_all_response():

    fp = "./tests/test_files/lms_detail.csv"
    f = FileUploadHandler(fp)
    vparams = UploaderValidationParameters(
        text_contains_all=[
            "RL_SCRIPT_VERSION",
            "TIMESTAMP",
            "MACHINE_ID",
            "VMACHINE_ID",
        ]
    )

    assert helpers.text_contains_all_response(f, vparams) == True

    vparams = UploaderValidationParameters(text_contains_all=["NOT", "IN", "FILE"])

    res = helpers.text_contains_all_response(f, vparams)
    assert isinstance(res, str)
    assert "File must contain the all following keywords" in res


# pytest -s -v tests/test_default_filecontents_validation_handler.py::test_text_contains_any_response
def test_text_contains_any_response():

    fp = "./tests/test_files/lms_detail.csv"
    f = FileUploadHandler(fp)
    vparams = UploaderValidationParameters(
        text_contains_any=[
            "RL_SCRIPT_VERSION",
            "TIMESTAMP",
            "MACHINE_ID",
            "VMACHINE_ID",
        ]
    )

    assert helpers.text_contains_any_response(f, vparams) == True

    vparams = UploaderValidationParameters(text_contains_any=["NOT IN THIS FILE"])

    res = helpers.text_contains_any_response(f, vparams)

    assert isinstance(res, str)
    assert "File must contain at least one of the following keywords" in res


# pytest -s -v tests/test_default_filecontents_validation_handler.py::test_get_csv_df
def test_get_csv_df():

    fp = "./tests/test_files/lms_detail.csv"
    f = FileUploadHandler(fp)
    vparams = UploaderValidationParameters(min_rows_number=5, header_starts_at=0)

    df = helpers.get_csv_df(
        f,
        min_rows_number=vparams.min_rows_number,
        header_starts_at=vparams.header_starts_at,
    )

    for col in ["RL_SCRIPT_VERSION", "TIMESTAMP", "MACHINE_ID", "VMACHINE_ID"]:
        assert col in list(df.columns)


# pytest -s -v tests/test_default_filecontents_validation_handler.py::test_get_df_sheets
def test_get_df_sheets():

    fp = "./tests/test_files/RVTools.xlsx"
    f = FileUploadHandler(fp)

    sheets = helpers.get_df_sheets(f)

    assert "tabvInfo" in sheets


# pytest -s -v tests/test_default_filecontents_validation_handler.py::test_get_excel_dfs
def test_get_excel_dfs():

    fp = "./tests/test_files/RVTools.xlsx"
    f = FileUploadHandler(fp)

    dfs = helpers.get_excel_dfs(
        f, min_rows_number=1, header_starts_at=0, required_sheets=["tabvInfo"]
    )

    assert "tabvInfo" in dfs.keys()
    assert "DNS Name" in dfs["tabvInfo"].columns


# pytest -s -v tests/test_default_filecontents_validation_handler.py::test_required_columns_response
def test_required_columns_response():

    fp = "./tests/test_files/lms_detail.csv"
    f = FileUploadHandler(fp)
    vparams = UploaderValidationParameters(
        required_columns=["RL_SCRIPT_VERSION", "TIMESTAMP", "MACHINE_ID", "VMACHINE_ID"]
    )

    res = helpers.required_columns_response(f, vparams)
    assert res == True

    vparams = UploaderValidationParameters(required_columns=["NOT A COLUMN"])

    res = helpers.required_columns_response(f, vparams)

    assert isinstance(res, str)
    assert "File doesn't contain the following needed columns" in res

    fp = "./tests/test_files/RVTools.xlsx"
    f = FileUploadHandler(fp)

    vparams = UploaderValidationParameters(
        required_columns=["VM"], required_sheets=["tabvInfo"]
    )

    res = helpers.required_columns_response(f, vparams)
    assert res == True


# pytest -s -v tests/test_default_filecontents_validation_handler.py::test_required_sheets_response
def test_required_sheets_response():

    fp = "./tests/test_files/RVTools.xlsx"
    f = FileUploadHandler(fp)

    vparams = UploaderValidationParameters(required_sheets=[["vInfo"], ("tabvInfo",)])

    res = helpers.required_sheets_response(f, vparams)
    assert res == True

    vparams = UploaderValidationParameters(required_sheets=["Not a sheet"])

    res = helpers.required_sheets_response(f, vparams)

    assert isinstance(res, str)
    assert "File doesn't contain the following needed sheets" in res

    vparams = UploaderValidationParameters(required_sheets=["tabvInfo"])

    res = helpers.required_sheets_response(f, vparams)
    assert res == True


# pytest -s -v tests/test_default_filecontents_validation_handler.py::test_min_rows_number_response
def test_min_rows_number_response():

    fp = "./tests/test_files/RVTools.xlsx"
    f = FileUploadHandler(fp)

    vparams = UploaderValidationParameters(
        min_rows_number=10, required_sheets=["tabvInfo"]
    )

    res = helpers.min_rows_number_response(f, vparams)

    assert res == True

    vparams = UploaderValidationParameters(
        min_rows_number=10, required_sheets=["tabvCluster"]
    )

    res = helpers.min_rows_number_response(f, vparams)

    assert isinstance(res, str)
    assert "Sheet tabvCluster doesn't have the minimum number of rows" in res


# pytest -s -v tests/test_default_filecontents_validation_handler.py::test_get_filenames_response
def test_get_filenames_response():

    vparams = UploaderValidationParameters(
        filename_contains=["tools"],
        filename_endswith=[".xlsx"],
    )

    res = helpers.get_filenames_response(
        ["./tests/test_files/lms_detail.csv", "./tests/test_files/RVTools.xlsx"],
        vparams,
    )

    for r in res.validation:
        if r.filename == "lms_detail.csv":
            assert r.status == "failed"
        if r.filename == "RVTools.xlsx":
            assert r.status == "success"


# pytest -s -v tests/test_default_filecontents_validation_handler.py::test_get_failed_validations
def test_get_failed_validations():

    fp = "./tests/test_files/RVTools.xlsx"
    f = FileUploadHandler(fp)

    vparams = UploaderValidationParameters(
        filename_contains=["tools"],
        filename_endswith=[".xlsx"],
        required_sheets=["tabvInfo"],
    )

    res = helpers.get_failed_validations(f, vparams)

    assert isinstance(res, list)
    assert len(res) == 0


# pytest -s -v tests/test_default_filecontents_validation_handler.py::test_default_filecontents_validation_handler
def test_default_filecontents_validation_handler():

    # rvtoolsfp = "./tests/test_files/RVTools.xlsx"

    # with open(rvtoolsfp, 'rb') as f:
    #     file_binary = io.BytesIO(f.read())

    #     rvtoolsflask = FileStorage(
    #         stream=file_binary,
    #         filename=os.path.basename(rvtoolsfp),
    #         content_type="application/*",
    #     )

    #     rvtoolsfastapi = UploadFile(
    #         filename=os.path.basename(rvtoolsfp),
    #         file=file_binary,
    #         content_type="application/*",
    #     )

    # files = [rvtoolsflask, rvtoolsfastapi]

    fp = "./tests/test_files/RVTools.xlsx"
    files = [fp]

    rv_tools_validation_parameters = UploaderValidationParameters(
        filename_contains=["rv", "tools"],
        filename_endswith=[".xlsx"],
        required_input_type="excel",
        min_rows_number=1,
        header_starts_at=0,
        required_sheets=[
            ("tabvInfo", "tabvCPU", "tabvHost", "tabvCluster"),
            ("vInfo", "vCPU", "vHost", "vCluster"),
        ],
        required_columns=[
            "VM",
            "Host",
            "OS",
            "Sockets",
            "CPUs",
            "Model",
            "CPU Model",
            "Cluster",
            "# CPU",
            "# Cores",
            "ESX Version",
            "HT Active",
            "Name",
            "NumCpuThreads",
            "NumCpuCores",
        ],
    )

    response = default_filecontents_validation_handler(
        files, rv_tools_validation_parameters
    )

    for res in response.content.validation:
        # print(res.status, res.message)
        assert res.status == "success"
