import requests
from dataclasses import dataclass
from typing import Callable, Tuple, List, Any, Union
from licenseware.constants.states import States
from licenseware.uploader.validation_parameters import UploaderValidationParameters
from licenseware.uploader.encryption_parameters import UploaderEncryptionParameters
from .uploader_types import (
    FileValidationResponse, 
    UploaderQuotaResponse, 
    UploaderStatusResponse,
    UploaderId
)

from licenseware.utils.logger import log
from .uploader_apispecs import UploaderApiSpecs
from licenseware.uploader.defaults import (
    default_filenames_validation_handler, 
    default_filecontents_validation_handler,
    default_check_quota_handler,
    default_check_status_handler,
)



@dataclass
class NewUploader:
    name: str 
    description: str
    uploader_id: str
    accepted_file_types: tuple
    validation_parameters: UploaderValidationParameters = None
    encryption_parameters: UploaderEncryptionParameters = None
    flags: Tuple[str] = None
    icon: str = None
    filenames_validation_handler: Callable[[List[str], UploaderValidationParameters], FileValidationResponse] = None
    filecontents_validation_handler: Callable[[Union[List[str], List[bytes]], UploaderValidationParameters], FileValidationResponse] = None
    check_quota_handler: Callable[[Union[List[str], List[bytes]]], UploaderQuotaResponse] = None
    check_status_handler: Callable[[UploaderId], UploaderStatusResponse] = None
    config: Any = None

    def __post_init__(self):
        
        assert self.config is not None
        assert hasattr(self.config, "APP_ID")
        assert hasattr(self.config, "REGISTER_UPLOADER_URL")
        assert hasattr(self.config, "get_machine_token")
        
        self.app_id= self.config.APP_ID
        self.status = States.IDLE
        self.upload_validation_url = f"/uploads/{self.uploader_id}/validation"
        self.upload_url = f"/uploads/{self.uploader_id}/files"
        self.quota_validation_url = f"/uploads/{self.uploader_id}/quota"
        self.status_check_url = f"/uploads/{self.uploader_id}/status" 
        self.apispecs = UploaderApiSpecs


    def validate_filenames(self, filenames: List[str]) -> FileValidationResponse:
        if self.filenames_validation_handler is None:
            return default_filenames_validation_handler(filenames, self.validation_parameters)
        return self.filenames_validation_handler(filenames, self.validation_parameters) 


    def validate_filecontents(self, files: list) -> FileValidationResponse:
        if self.filecontents_validation_handler is None: 
            return default_filecontents_validation_handler(files, self.validation_parameters)
        return self.filecontents_validation_handler(files, self.validation_parameters) 


    # TODO
    def check_quota(self, validation_response: FileValidationResponse):
        if self.check_quota_handler is None: 
            return default_check_quota_handler(validation_response)
        return self.check_quota_handler(validation_response) 
        

    def check_status(self, uploader_id:str):
        if self.check_status_handler is None: 
            return default_check_status_handler(uploader_id)
        return self.check_status_handler(uploader_id) 


    @property
    def metadata(self):
        
        metadata_payload = { # pragma: no cover
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

        return metadata_payload # pragma: no cover


    def register(self):

        response = requests.post( # pragma: no cover
            url=self.config.REGISTER_UPLOADER_URL, 
            json=self.metadata, 
            headers={"Authorization": self.config.get_machine_token()}
        )

        if response.status_code == 200: # pragma: no cover
            return {
                    "status": States.SUCCESS,
                    "message": f"Uploader '{self.uploader_id}' register successfully",
                    "content": self.metadata
                }, 200

        nokmsg = f"Could not register uploader '{self.uploader_id}'" # pragma: no cover
        log.error(nokmsg) # pragma: no cover
        return {"status": States.FAILED, "message": nokmsg, "content": self.metadata}, 400 # pragma: no cover

    