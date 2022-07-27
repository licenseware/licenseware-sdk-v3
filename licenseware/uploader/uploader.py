import requests
from typing import Callable, Tuple, List, Any, Union
from dataclasses import dataclass
from licenseware.utils.logger import log
from licenseware.uploader.encryption_parameters import UploaderEncryptionParameters
from licenseware.uploader.validation_parameters import UploaderValidationParameters
from licenseware.utils.alter_string import get_altered_strings
from licenseware.constants.states import States
from licenseware.constants.uploader_types import (
    FileValidationResponse, 
    UploaderQuotaResponse, 
    UploaderStatusResponse,
    UploaderId
)
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
    filenames_validation_handler: Callable[[List[str], UploaderValidationParameters], FileValidationResponse] = default_filenames_validation_handler
    filecontents_validation_handler: Callable[[Union[List[str], List[bytes]], UploaderValidationParameters], FileValidationResponse] = default_filecontents_validation_handler
    check_quota_handler: Callable[[Union[List[str], List[bytes]]], UploaderQuotaResponse] = default_check_quota_handler
    check_status_handler: Callable[[UploaderId], UploaderStatusResponse] = default_check_status_handler
    config: Any = None

    def __post_init__(self):
        
        assert self.config is not None
        assert hasattr(self.config, "APP_ID")
        assert hasattr(self.config, "REGISTER_UPLOADER_URL")
        assert hasattr(self.config, "get_machine_token")
        
        self.app_id = self.config.APP_ID

        appid = get_altered_strings(self.app_id).dash
        reportid = get_altered_strings(self.uploader_id).dash

        self.status = States.IDLE
        self.upload_validation_url = f"/{appid}/uploads/{reportid}/validation"
        self.upload_url = f"/{appid}/uploads/{reportid}/files"
        self.quota_validation_url = f"/{appid}/uploads/{reportid}/quota"
        self.status_check_url = f"/{appid}/uploads/{reportid}/status" 


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
                "validation_parameters": self.validation_parameters.dict(),
                "encryption_parameters": self.encryption_parameters.dict(),
                "upload_url": self.upload_url,
                "upload_validation_url": self.upload_validation_url,
                "quota_validation_url": self.quota_validation_url,
                "status_check_url": self.status_check_url,
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

    