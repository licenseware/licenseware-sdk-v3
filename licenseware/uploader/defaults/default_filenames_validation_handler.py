import uuid
from typing import List
from licenseware import states
from licenseware.uiresponses.filename_response import FileNameResponse, NameValidationResponse
from licenseware.uploader.validation_parameters import UploaderValidationParameters
from licenseware.validators import validate_text_contains_any, validate_required_input_type



def default_filenames_validation_handler(filenames:List[str], validation_parameters: UploaderValidationParameters) -> FileNameResponse:
    
    validation_response = []

    filenames_ignored = [
        NameValidationResponse(
            status=states.SKIPPED,
            filename=filename, 
            message=validation_parameters.filename_ignored_message
        ) 
        for fn in filenames if fn in validation_parameters.ignore_filenames
    ]

    validation_response.extend(filenames_ignored)

    filenames_to_validate = [fn for fn in filenames if fn not in validation_parameters.ignore_filenames]
    for filename in filenames_to_validate:

        filename_contains_msg = validate_text_contains_any(
            filename, 
            validation_parameters.filename_contains, 
            regex_escape=validation_parameters.regex_escape, 
            raise_error=False
        )

        filename_endswith_msg = validate_required_input_type(
            filename,
            validation_parameters.filename_endswith,
            raise_error=False
        )

        if filename_contains_msg is True and filename_endswith_msg is True:

            validation_response.append(
                NameValidationResponse(
                    status=states.SUCCESS,
                    filename=filename, 
                    message=validation_parameters.filename_valid_message
                )
            )

        else:
            validation_response.append(
                NameValidationResponse(
                    status=states.FAILED,
                    filename=filename, 
                    message=validation_parameters.filename_invalid_message or filename_contains_msg + " " + filename_endswith_msg
                )
            )
            
    filename_response = FileNameResponse(
        event_id=str(uuid.uuid4()),
        status=states.SUCCESS,
        message="File names were analysed",
        validation=tuple(validation_response)
    )

    return filename_response