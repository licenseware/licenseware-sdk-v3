from dataclasses import dataclass
from typing import Callable, Tuple, List
from licenseware.uploader.validation_parameters import UploaderValidationParameters
from licenseware.uploader.encryption_parameters import UploaderEncryptionParameters
from licenseware.uploader.defaults import default_filenames_validation_handler, default_filecontents_validation_handler
from licenseware.uiresponses import FileNameResponse, FileContentResponse



@dataclass
class NewUploader:
    app_id: str
    uploader_id: str
    name: str 
    description: str
    accepted_file_types: tuple
    validation_parameters: UploaderValidationParameters = None
    encryption_parameters: UploaderEncryptionParameters = None
    flags: Tuple[str] =None
    status: str = None
    icon: str = None
    upload_url: str = None
    upload_validation_url: str = None
    quota_validation_url: str = None
    status_check_url: str = None
    filenames_validation_handler: Callable[[List[str], UploaderValidationParameters], FileNameResponse] = None
    filecontents_validation_handler: Callable = None


    def validate_filenames(self, filenames: List[str]) -> FileNameResponse:

        if self.filenames_validation_handler is None:
            return default_filenames_validation_handler(filenames, self.validation_parameters)

        return self.filenames_validation_handler(filenames, self.validation_parameters)


    def validate_filecontents(self, files: list) -> FileContentResponse:

        if self.filecontents_validation_handler is None:
            return default_filecontents_validation_handler(files, self.validation_parameters)

        return self.filenames_validation_handler(files, self.validation_parameters)


    def get_registration_payload(self):
        
        payload = {
            'data': [{
                "app_id": self.app_id,
                "uploader_id": self.uploader_id,
                "name": self.name,
                "description": self.description,
                "accepted_file_types": self.accepted_file_types,
                "flags": self.flags,
                "status": self.status,
                "icon": self.icon,
                "upload_url": self.upload_url,
                "upload_validation_url": self.upload_validation_url,
                "quota_validation_url": self.quota_validation_url,
                "status_check_url": self.status_check_url,
                "validation_parameters": self.validation_parameters.dict(),
                "encryption_parameters": self.encryption_parameters.dict()
            }]
        }

        return payload

    