import uuid
import pandas as pd
from typing import List, Union, IO
from licenseware import states
from licenseware import validators as v
from licenseware.utils.logger import log
from licenseware.uploader.validation_parameters import UploaderValidationParameters
from licenseware.uploader.file_upload_handler import FileUploadHandler
from licenseware.uiresponses import FileValidationResponse, ValidationResponse
from .default_filenames_validation_handler import default_filenames_validation_handler


def _sniff_delimiter(file: IO, filename: str):
    reader = pd.read_csv(file, sep=None, iterator=True, engine='python')
    delimiter = reader._engine.data.dialect.delimiter
    reader.close()
    if delimiter in [",",";"]:
        log.info(f"Sniffed delimiter '{delimiter}' for {filename}")
        return delimiter
    else:
        log.warning(f"Sniffed illegal delimiter {delimiter} for {filename}")
        return ","


def _required_input_type_response(f: FileUploadHandler, validation_parameters: UploaderValidationParameters):
    rit = True
    if validation_parameters.required_input_type is not None:
        rit = v.validate_required_input_type(f.filename, validation_parameters.required_input_type, raise_error=False)
    return rit


def _text_contains_all_response(f: FileUploadHandler, validation_parameters: UploaderValidationParameters):
    tcall = True
    if validation_parameters.text_contains_all is not None:
        tcall = v.validate_text_contains_all(
            str(f.read(validation_parameters.buffer)), 
            validation_parameters.text_contains_all,
            regex_escape=validation_parameters.regex_escape,
            raise_error=False
        )
    return tcall


def _text_contains_any_response(f: FileUploadHandler, validation_parameters: UploaderValidationParameters):
    tcany = True
    if validation_parameters.text_contains_any is not None:
        tcany = v.validate_text_contains_any(
            str(f.read(validation_parameters.buffer)),
            validation_parameters.text_contains_any,
            regex_escape=validation_parameters.regex_escape,
            raise_error=False
        )
    return tcany
    
def _get_csv_df(f: FileUploadHandler, validation_parameters: UploaderValidationParameters):

    df = pd.read_csv(
        f, 
        nrows=validation_parameters.min_rows_number, 
        skiprows=validation_parameters.header_starts_at,
        delimiter=_sniff_delimiter(f, f.filename)
    )

    return df


def _get_df_sheets(f: FileUploadHandler):
    sheets = pd.ExcelFile(f).sheet_names
    return sheets


def _get_excel_dfs(f: FileUploadHandler, validation_parameters: UploaderValidationParameters):

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


def _required_columns_response(f: FileUploadHandler, validation_parameters: UploaderValidationParameters):

    reqcols = True
    if validation_parameters.required_columns is not None:
        
        if validation_parameters.required_input_type in ['csv', '.csv']:

            df = _get_csv_df(f, validation_parameters)                

            reqcols = v.validate_required_items(
                items=list(df.columns),
                item_type="columns",
                required_items=validation_parameters.required_columns,
                raise_error=False
            )

        elif validation_parameters.required_input_type in ['excel', '.xls', '.xlsx', 'xls', 'xlsx']:
            
            dfs = _get_excel_dfs(f, validation_parameters)

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


def _required_sheets_response(f: FileUploadHandler, validation_parameters: UploaderValidationParameters):

    reqsheets = True
    if validation_parameters.required_sheets is not None:

        if validation_parameters.required_input_type in ['excel', '.xls', '.xlsx', 'xls', 'xlsx']:
            
            sheets = _get_df_sheets(f)

            reqsheets = v.validate_required_items(
                items=sheets,
                item_type="sheets",
                required_items=validation_parameters.required_sheets,
                raise_error=False
            )

    return reqsheets



def _min_rows_number_response(f: FileUploadHandler, validation_parameters: UploaderValidationParameters):

    minrows = True
    if validation_parameters.required_input_type in ['csv', '.csv']:
        df = _get_csv_df(f, validation_parameters)  

        minrows = v.validate_min_rows_number(
            min_rows=validation_parameters.min_rows_number,
            current_rows=df.shape[0]
        )

    elif validation_parameters.required_input_type in ['excel', '.xls', '.xlsx', 'xls', 'xlsx']:
        
        dfs = _get_excel_dfs(f, validation_parameters)
        
        for _, df in dfs.items():
            minrows = v.validate_min_rows_number(
                min_rows=validation_parameters.min_rows_number,
                current_rows=df.shape[0]
            )
            if isinstance(minrows, str):
                break

    return minrows




def _get_filenames_response(files: Union[List[bytes], List[str]], validation_parameters: UploaderValidationParameters):

    filename_validation_response = default_filenames_validation_handler(
        [FileUploadHandler(f).filename for f in files],
        validation_parameters
    )

    for res in filename_validation_response.validation:
        if res.status == states.FAILED:
            return filename_validation_response

    return None


def _get_error_message(failed_validations: List[str]):
    return ", ".join(failed_validations)



def _get_failed_validations(f: FileUploadHandler, validation_parameters: UploaderValidationParameters):

    validations = dict(
        ritype    =  _required_input_type_response(f, validation_parameters),
        tconall   =  _text_contains_all_response(f, validation_parameters),
        tconany   =  _text_contains_any_response(f, validation_parameters),
        reqcols   =  _required_columns_response(f, validation_parameters),
        reqsheets =  _required_sheets_response(f, validation_parameters),
        minrows   =  _min_rows_number_response(f, validation_parameters)
    )

    failed_validations = [v for v in validations.values() if isinstance(v, str)]

    return failed_validations


def default_filecontents_validation_handler(
    files: Union[List[bytes], List[str]], 
    validation_parameters: UploaderValidationParameters
) -> FileValidationResponse:
    
    
    filename_validation_response = _get_filenames_response(files, validation_parameters)
    if filename_validation_response is not None:
        return filename_validation_response


    validation_response = []
    for file in files:
        
        f = FileUploadHandler(file)
        
        if validation_parameters.ignore_filenames is not None:
            if f.filename in validation_parameters.ignore_filenames:
                continue
        
        failed_validations = _get_failed_validations(f, validation_parameters)

        if not failed_validations:
            validation_response.append(
                ValidationResponse(
                    status=states.SUCCESS,
                    filename=f.filename, 
                    message=validation_parameters.filename_valid_message
                )
            )
        else:
            validation_response.append(
                ValidationResponse(
                    status=states.FAILED,
                    filename=f.filename, 
                    message=_get_error_message(failed_validations)
                )
            )

    file_response = FileValidationResponse(
        event_id=str(uuid.uuid4()),
        status=states.SUCCESS,
        message="File names and contents were analysed",
        validation=tuple(validation_response)
    )

    return file_response


