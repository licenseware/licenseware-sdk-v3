import uuid
from typing import List
from licenseware import states
from licenseware.utils.file_validators import validate_filename
from licenseware.uiresponses.filename_response import FileNameResponse, NameValidationResponse
from licenseware.uploader.validation_parameters import UploaderValidationParameters


def default_filecontents_validation_handler(files:list, validation_parameters: UploaderValidationParameters):
    pass

