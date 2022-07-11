import requests
from dataclasses import dataclass
from typing import Callable, Tuple, List, Any, Union
from licenseware.constants import states
from licenseware.uploader.validation_parameters import UploaderValidationParameters
from licenseware.uploader.encryption_parameters import UploaderEncryptionParameters
from licenseware.uploader.defaults import default_filenames_validation_handler, default_filecontents_validation_handler
from licenseware.uiresponses import FileValidationResponse
from licenseware.utils.logger import log


@dataclass
class NewUploader:
    name: str 
    description: str
    uploader_id: str
    accepted_file_types: tuple
    validation_parameters: UploaderValidationParameters = None
    encryption_parameters: UploaderEncryptionParameters = None
    flags: Tuple[str] = None
    status: str = None
    icon: str = None
    filenames_validation_handler: Callable[[List[str], UploaderValidationParameters], FileValidationResponse] = None
    filecontents_validation_handler: Callable[[Union[List[str], List[bytes]], UploaderValidationParameters], FileValidationResponse] = None
    config: Any = None

    def __post_init__(self):
        self.app_id= self.config.APP_ID
        self.upload_validation_url = f"/{self.uploader_id}/validation"
        self.upload_url = f"/{self.uploader_id}/files"
        self.quota_validation_url = f"/{self.uploader_id}/quota"
        self.status_check_url = f"/{self.uploader_id}/status" 

    def validate_filenames(self, filenames: List[str]) -> FileValidationResponse:

        if self.filenames_validation_handler is None:
            return default_filenames_validation_handler(filenames, self.validation_parameters)

        return self.filenames_validation_handler(filenames, self.validation_parameters)


    def validate_filecontents(self, files: list) -> FileValidationResponse:

        if self.filecontents_validation_handler is None:
            return default_filecontents_validation_handler(files, self.validation_parameters)

        return self.filenames_validation_handler(files, self.validation_parameters)

    @property
    def metadata(self):
        
        registry_payload = {
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

        return registry_payload


    def register(self):

        response = requests.post(
            url=self.config.REGISTER_UPLOADER_URL, 
            json=self.metadata, 
            headers={"Authorization": self.config.get_auth_token()}
        )

        if response.status_code == 200:
            return {
                    "status": states.SUCCESS,
                    "message": f"Uploader '{self.uploader_id}' register successfully",
                    "content": self.metadata
                }, 200

        nokmsg = f"Could not register uploader '{self.uploader_id}'"
        log.error(nokmsg)
        return {"status": states.FAILED, "message": nokmsg, "content": self.metadata}, 400

    