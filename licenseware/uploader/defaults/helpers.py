import pandas as pd
from typing import List, Union, IO
from licenseware import states
from licenseware import validators as v
from licenseware.utils.logger import log
from licenseware.uploader.file_upload_handler import FileUploadHandler
from licenseware.uploader.validation_parameters import UploaderValidationParameters
from .default_filenames_validation_handler import default_filenames_validation_handler



def sniff_delimiter(file: IO, filename: str):
    reader = pd.read_csv(file, sep=None, iterator=True, engine='python')
    delimiter = reader._engine.data.dialect.delimiter
    reader.close()
    if delimiter in [",",";"]:
        log.info(f"Sniffed delimiter '{delimiter}' for {filename}")
        return delimiter
    else:
        log.warning(f"Sniffed illegal delimiter {delimiter} for {filename}")
        return ","


def required_input_type_response(f: FileUploadHandler, validation_parameters: UploaderValidationParameters):
    rit = True
    if validation_parameters.required_input_type is not None:
        rit = v.validate_required_input_type(f.filename, validation_parameters.required_input_type, raise_error=False)
    return rit


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


def text_contains_any_response(f: FileUploadHandler, validation_parameters: UploaderValidationParameters):
    tcany = True
    if validation_parameters.text_contains_any is not None:
        tcany = v.validate_text_contains_any(
            str(f.read(validation_parameters.buffer)),
            validation_parameters.text_contains_any,
            regex_escape=validation_parameters.regex_escape,
            raise_error=False
        )
    return tcany
    
def get_csv_df(f: FileUploadHandler, validation_parameters: UploaderValidationParameters):

    df = pd.read_csv(
        f, 
        nrows=validation_parameters.min_rows_number, 
        skiprows=validation_parameters.header_starts_at,
        delimiter=sniff_delimiter(f, f.filename)
    )

    return df


def get_df_sheets(f: FileUploadHandler):
    sheets = pd.ExcelFile(f).sheet_names
    return sheets


def get_excel_dfs(f: FileUploadHandler, validation_parameters: UploaderValidationParameters):

    dfs = {}
    sheets = pd.ExcelFile(f).sheet_names

    if len(sheets) == 1:
        dfs[sheets[0]] = pd.read_excel(
            f, 
            nrows=validation_parameters.min_rows_number, 
            skiprows=validation_parameters.header_starts_at
        )
    else:
        for sheet in sheets:                        
            if sheet not in validation_parameters.required_sheets: 
                continue

            dfs[sheet] = pd.read_excel(
                f, 
                sheet_name=sheet, 
                nrows=validation_parameters.min_rows_number, 
                skiprows=validation_parameters.header_starts_at
            )

    return dfs


def required_columns_response(f: FileUploadHandler, validation_parameters: UploaderValidationParameters):

    reqcols = True
    if validation_parameters.required_columns is not None:
        
        if validation_parameters.required_input_type in ['csv', '.csv']:

            df = get_csv_df(f, validation_parameters)                

            reqcols = v.validate_required_items(
                items=list(df.columns),
                item_type="columns",
                required_items=validation_parameters.required_columns,
                raise_error=False
            )

        elif validation_parameters.required_input_type in ['excel', '.xls', '.xlsx', 'xls', 'xlsx']:
            
            dfs = get_excel_dfs(f, validation_parameters)

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

    reqsheets = True
    if validation_parameters.required_sheets is not None:

        if validation_parameters.required_input_type in ['excel', '.xls', '.xlsx', 'xls', 'xlsx']:
            
            sheets = get_df_sheets(f)

            reqsheets = v.validate_required_items(
                items=sheets,
                item_type="sheets",
                required_items=validation_parameters.required_sheets,
                raise_error=False
            )

    return reqsheets



def min_rows_number_response(f: FileUploadHandler, validation_parameters: UploaderValidationParameters):

    minrows = True
    if validation_parameters.required_input_type in ['csv', '.csv']:
        df = get_csv_df(f, validation_parameters)  

        minrows = v.validate_min_rows_number(
            min_rows=validation_parameters.min_rows_number,
            current_rows=df.shape[0]
        )

    elif validation_parameters.required_input_type in ['excel', '.xls', '.xlsx', 'xls', 'xlsx']:
        
        dfs = get_excel_dfs(f, validation_parameters)
        
        for _, df in dfs.items():
            minrows = v.validate_min_rows_number(
                min_rows=validation_parameters.min_rows_number,
                current_rows=df.shape[0]
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
