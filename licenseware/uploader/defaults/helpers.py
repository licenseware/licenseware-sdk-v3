import itertools
import pandas as pd
from typing import List, Union, IO
from functools import wraps
from licenseware import states
from licenseware import validators as v
from licenseware.utils.logger import log
from licenseware.uploader.file_upload_handler import FileUploadHandler
from licenseware.uploader.validation_parameters import UploaderValidationParameters
from .default_filenames_validation_handler import default_filenames_validation_handler


def reset_stream(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        stream = isinstance(args[0], FileUploadHandler)
        if stream: args[0].reset()
        response = f(*args, **kwargs)
        if stream: args[0].reset()
        return response
    return decorator

    

@reset_stream
def sniff_delimiter(f: FileUploadHandler, header_starts_at: int = 0):

    reader = pd.read_csv(
        f, 
        sep=None, 
        iterator=True, 
        engine='python',
        skiprows=header_starts_at,
        nrows=1
    )
    delimiter = reader._engine.data.dialect.delimiter
    reader.close()
    if delimiter in [",",";","\t"," ","|"]:
        return delimiter
    return ","


def required_input_type_response(f: FileUploadHandler, validation_parameters: UploaderValidationParameters):
    rit = True
    if validation_parameters.required_input_type is not None:
        rit = v.validate_required_input_type(f.filename, validation_parameters.required_input_type, raise_error=False)
    return rit


@reset_stream
def text_contains_all_response(f: FileUploadHandler, validation_parameters: UploaderValidationParameters):
    tcall = True
    if validation_parameters.text_contains_all is not None:
        tcall = v.validate_text_contains_all(
            str(f.read(validation_parameters.buffer)), 
            validation_parameters.text_contains_all,
            regex_escape=validation_parameters.regex_escape,
            raise_error=False
        )
    return tcall


@reset_stream
def text_contains_any_response(f: FileUploadHandler, validation_parameters: UploaderValidationParameters):
    tcany = True
    if validation_parameters.text_contains_any is not None:
        tcany = v.validate_text_contains_any(
            text=str(f.read(validation_parameters.buffer)),
            text_contains_any=validation_parameters.text_contains_any,
            regex_escape=validation_parameters.regex_escape,
            raise_error=False
        )
    return tcany
    

@reset_stream
def get_csv_df(
    f: FileUploadHandler, 
    min_rows_number: int = None,
    header_starts_at: int = None,
):

    df = pd.read_csv(
        f, 
        nrows=min_rows_number, 
        skiprows=header_starts_at,
        delimiter=sniff_delimiter(f, header_starts_at) 
    )

    return df


@reset_stream
def get_df_sheets(f: FileUploadHandler):
    sheets = pd.ExcelFile(f).sheet_names
    return sheets


@reset_stream
def get_excel_dfs(
    f: FileUploadHandler, 
    min_rows_number:int = None, 
    header_starts_at:int = 0,
    required_sheets: List[str] = None
):

    dfs = {}
    sheets = pd.ExcelFile(f).sheet_names

    if len(sheets) == 1:
        dfs[sheets[0]] = pd.read_excel(
            f, 
            nrows=min_rows_number, 
            skiprows=header_starts_at
        )
    else:

        if required_sheets is not None:
            if len(required_sheets) > 0:
                if isinstance(required_sheets[0], (list, tuple, set,)):
                    required_sheets = list(itertools.chain(*required_sheets))

        for sheet in sheets:  
            if required_sheets is not None:
                if sheet not in required_sheets: 
                    continue

            dfs[sheet] = pd.read_excel(
                f, 
                sheet_name=sheet, 
                nrows=min_rows_number, 
                skiprows=header_starts_at
            )

    return dfs


def _determine_if_csv_or_excel(filename:str, required_input_type: str):

    if required_input_type is None:
        if filename.endswith(".csv"):
            return "csv"
        elif filename.endswith((".xls", ".xlsx",)):
            return "excel"
        else:
            raise ValueError("Please specify `required_input_type`")

    return required_input_type


def required_columns_response(f: FileUploadHandler, validation_parameters: UploaderValidationParameters):

    required_input_type = _determine_if_csv_or_excel(f.filename, validation_parameters.required_input_type)
    
    reqcols = True
    if validation_parameters.required_columns is not None:
        
        if required_input_type in ['csv', '.csv']:
            df = get_csv_df(
                f, 
                validation_parameters.min_rows_number, 
                validation_parameters.header_starts_at,
            )                

            reqcols = v.validate_required_items(
                items=list(df.columns),
                item_type="columns",
                required_items=validation_parameters.required_columns,
                raise_error=False
            )

        elif required_input_type in ['excel', '.xls', '.xlsx', 'xls', 'xlsx']:
            
            dfs = get_excel_dfs(
                f, 
                validation_parameters.min_rows_number,
                validation_parameters.header_starts_at,
                validation_parameters.required_sheets
            )

            columns = []
            for _, df in dfs.items():
                columns.extend(list(df.columns))

            reqcols = v.validate_required_items(
                items=columns,
                item_type="columns",
                required_items=validation_parameters.required_columns,
                raise_error=False
            )

    return reqcols


def required_sheets_response(f: FileUploadHandler, validation_parameters: UploaderValidationParameters):

    required_input_type = _determine_if_csv_or_excel(f.filename, validation_parameters.required_input_type)

    reqsheets = True
    if validation_parameters.required_sheets is not None:

        if required_input_type in ['excel', '.xls', '.xlsx', 'xls', 'xlsx']:
            
            sheets = get_df_sheets(f)

            reqsheets = v.validate_required_items(
                items=sheets,
                item_type="sheets",
                required_items=validation_parameters.required_sheets,
                raise_error=False
            )

    return reqsheets



def min_rows_number_response(f: FileUploadHandler, validation_parameters: UploaderValidationParameters):

    required_input_type = _determine_if_csv_or_excel(f.filename, validation_parameters.required_input_type)

    minrows = True
    if required_input_type in ['csv', '.csv']:
        df = get_csv_df(
            f, 
            validation_parameters.min_rows_number, 
            validation_parameters.header_starts_at,
        )

        minrows = v.validate_min_rows_number(
            min_rows=validation_parameters.min_rows_number,
            current_rows=df.shape[0],
            raise_error=False
        )

    elif required_input_type in ['excel', '.xls', '.xlsx', 'xls', 'xlsx']:
        
        dfs = get_excel_dfs(
            f, 
            validation_parameters.min_rows_number,
            validation_parameters.header_starts_at,
            validation_parameters.required_sheets
        )
        
        for tab, df in dfs.items():
            minrows = v.validate_min_rows_number(
                item_type="Sheet " + tab,
                min_rows=validation_parameters.min_rows_number,
                current_rows=df.shape[0],
                raise_error=False
            )
            if isinstance(minrows, str):
                break

    return minrows




def get_filenames_response(files: Union[List[bytes], List[str]], validation_parameters: UploaderValidationParameters):

    filename_validation_response = default_filenames_validation_handler(
        [FileUploadHandler(f).filename for f in files],
        validation_parameters
    )

    for res in filename_validation_response.validation:
        if res.status == states.FAILED:
            return filename_validation_response

    return None


def get_error_message(failed_validations: List[str]):
    return ", ".join(failed_validations)


def get_failed_validations(f: FileUploadHandler, validation_parameters: UploaderValidationParameters):

    validations = dict(
        ritype    =  required_input_type_response(f, validation_parameters),
        tconall   =  text_contains_all_response(f, validation_parameters),
        tconany   =  text_contains_any_response(f, validation_parameters),
        reqcols   =  required_columns_response(f, validation_parameters),
        reqsheets =  required_sheets_response(f, validation_parameters),
        minrows   =  min_rows_number_response(f, validation_parameters)
    )

    failed_validations = [v for v in validations.values() if isinstance(v, str)]

    return failed_validations
