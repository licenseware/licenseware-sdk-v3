import uuid
from typing import List
from licenseware import states
from licenseware.utils.file_validators import validate_filename
from licenseware.uiresponses.filename_response import FileNameResponse, NameValidationResponse
from licenseware.uploader.validation_parameters import UploaderValidationParameters


def default_filenames_validation_handler(filenames:List[str], validation_parameters: UploaderValidationParameters) -> FileNameResponse:


    validation_response = []
    for filename in filenames:
        
        if validation_parameters.ignore_filenames is not None:
            if any(filename.endswith(f) for f in validation_parameters.ignore_filenames):
                
                validation_response.append(
                    NameValidationResponse(
                        status=states.SKIPPED,
                        filename=filename, 
                        message=validation_parameters.filename_ignored_message
                    )
                )
                
                continue
            
        try:
            validate_filename(
                filename, 
                contains=validation_parameters.filename_contains or [], 
                endswith=validation_parameters.filename_endswith or [], 
                regex_escape=validation_parameters.regex_escape
            )
            validation_response.append(
                NameValidationResponse(
                        status=states.SUCCESS,
                        filename=filename, 
                        message=validation_parameters.filename_valid_message
                    )
                )
        except Exception as err:
            validation_response.append(
                NameValidationResponse(
                        status=states.FAILED,
                        filename=filename, 
                        message=validation_parameters.filename_invalid_message or str(err)
                    )
                )

    filename_response = FileNameResponse(
        event_id=str(uuid.uuid4()),
        status=states.SUCCESS,
        message="File names were analysed",
        validation=tuple(validation_response)
    )

    return filename_response

