import uuid
from typing import Tuple, List
from dataclasses import dataclass, asdict

from licenseware import states
from licenseware.utils.file_validators import validate_filename
from licenseware.uiresponses.filenames_response import FileNameResponse, NameValidationResponse


@dataclass
class FileValidator:
    filename_contains: Tuple[str] = None
    filename_endswith: Tuple[str] = None
    ignore_filenames: Tuple[str] = None
    required_input_type: str = None
    required_sheets: Tuple[str] = None
    required_columns: Tuple[str] = None
    text_contains_all: Tuple[str] = None
    text_contains_any: Tuple[str] = None
    min_rows_number: int = 0
    header_starts_at: int = 0
    buffer: int = 9000
    filename_invalid_message: str = None
    filename_valid_message: str = "File is valid"
    filename_ignored_message: str = "File is ignored"
    regex_escape: bool = True
    ignored_by_uup: bool = False


    def validate_filenames(self, filenames:List[str]) -> FileNameResponse:
        """
            Given a list of filenames and validate them based on 
            `filename_contains` and `filename_endswith` input parameters
            return a list of dicts with validation status, filename and message
            
            it's recomented to leave `filename_invalid_message` paramters as is 
            because if None will provide the reason why filename validation failed
        """

        validation_response = []
        for filename in filenames:
            
            if self.ignore_filenames is not None:
                if any(filename.endswith(f) for f in self.ignore_filenames):
                    
                    validation_response.append(
                        NameValidationResponse(
                            status=states.SKIPPED,
                            filename=filename, 
                            message=self.filename_ignored_message
                        )
                    )
                    
                    continue
                
            try:
                validate_filename(
                    filename, 
                    contains=self.filename_contains or [], 
                    endswith=self.filename_endswith or [],
                    regex_escape=self.regex_escape
                )
                validation_response.append(
                    NameValidationResponse(
                            status=states.SUCCESS,
                            filename=filename, 
                            message=self.filename_valid_message
                        )
                    )
            except Exception as err:
                validation_response.append(
                    NameValidationResponse(
                            status=states.FAILED,
                            filename=filename, 
                            message=self.filename_invalid_message or str(err)
                        )
                    )

        filename_response = FileNameResponse(
            event_id=str(uuid.uuid4()),
            status=states.SUCCESS,
            message="File names were analysed",
            validation=tuple(validation_response)
        )

        return filename_response


    def dict(self):
        return asdict(self)