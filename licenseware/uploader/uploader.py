from dataclasses import dataclass
from typing import Any, Callable, List, Tuple, Union

import requests

from licenseware.constants.states import States
from licenseware.constants.uploader_types import (
    FileValidationResponse,
    UploaderId,
    UploaderQuotaResponse,
    UploaderStatusResponse,
)
from licenseware.uploader.defaults import (
    default_check_quota_handler,
    default_check_status_handler,
    default_filecontents_validation_handler,
    default_filenames_validation_handler,
)
from licenseware.uploader.encryption_parameters import UploaderEncryptionParameters
from licenseware.uploader.validation_parameters import UploaderValidationParameters
from licenseware.utils.alter_string import get_altered_strings
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
    icon: str = None
    filenames_validation_handler: Callable[
        [List[str], UploaderValidationParameters], FileValidationResponse
    ] = default_filenames_validation_handler
    filecontents_validation_handler: Callable[
        [Union[List[str], List[bytes]], UploaderValidationParameters],
        FileValidationResponse,
    ] = default_filecontents_validation_handler
    check_quota_handler: Callable[
        [Union[List[str], List[bytes]]], UploaderQuotaResponse
    ] = default_check_quota_handler
    check_status_handler: Callable[
        [UploaderId], UploaderStatusResponse
    ] = default_check_status_handler
    config: Any = None

    def __post_init__(self):

        assert self.config is not None
        assert hasattr(self.config, "APP_ID")
        assert hasattr(self.config, "REGISTER_UPLOADER_URL")
        assert hasattr(self.config, "get_machine_token")

        self.app_id = self.config.APP_ID

        self.validation_parameters = (
            self.validation_parameters.dict()
            if self.validation_parameters is not None
            else None
        )
        self.encryption_parameters = (
            self.encryption_parameters.dict()
            if self.encryption_parameters is not None
            else None
        )

        appid = get_altered_strings(self.app_id).dash
        uploaderid = get_altered_strings(self.uploader_id).dash

        self.status = States.IDLE
        self.upload_validation_url = f"/{appid}/uploads/{uploaderid}/validation"
        self.upload_url = f"/{appid}/uploads/{uploaderid}/files"
        self.quota_validation_url = f"/{appid}/uploads/{uploaderid}/quota"
        self.status_check_url = f"/{appid}/uploads/{uploaderid}/status"

    @property
    def metadata(self):

        metadata_payload = {
            "data": [
                {
                    "app_id": self.app_id,
                    "uploader_id": self.uploader_id,
                    "name": self.name,
                    "description": self.description,
                    "accepted_file_types": self.accepted_file_types,
                    "flags": self.flags,
                    "status": self.status,
                    "icon": self.icon,
                    "validation_parameters": self.validation_parameters,
                    "encryption_parameters": self.encryption_parameters,
                    "upload_url": self.upload_url,
                    "upload_validation_url": self.upload_validation_url,
                    "quota_validation_url": self.quota_validation_url,
                    "status_check_url": self.status_check_url,
                }
            ]
        }

        return metadata_payload

    def register(self):  # pragma no cover

        response = requests.post(
            url=self.config.REGISTER_UPLOADER_URL,
            json=self.metadata,
            headers={"Authorization": self.config.get_machine_token()},
        )

        if response.status_code == 200:
            return {
                "status": States.SUCCESS,
                "message": f"Uploader '{self.uploader_id}' register successfully",
                "content": self.metadata,
            }, 200

        nokmsg = f"Could not register uploader '{self.uploader_id}'"
        log.error(nokmsg)
        return {
            "status": States.FAILED,
            "message": nokmsg,
            "content": self.metadata,
        }, 400
