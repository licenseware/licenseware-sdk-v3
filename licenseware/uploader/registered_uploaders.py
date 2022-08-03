from enum import Enum
from typing import Dict, List

from .uploader import NewUploader


class RegisteredUploaders:
    def __init__(self, uploaders: List[NewUploader]) -> None:
        self.uploaders = uploaders
        self.uploader_enum = Enum(
            "UploaderEnum", {u.uploader_id: u.uploader_id for u in self.uploaders}
        )
        self.uploader_dispacher: Dict[str, NewUploader] = {
            u.uploader_id: u for u in uploaders
        }

    def _get_current_uploader(self, uploader_id: Enum):
        uploader_id = str(uploader_id).replace("UploaderEnum.", "")
        return self.uploader_dispacher[uploader_id]

    def validate_filenames_flow(
        self, tenant_id: str, auth_jwt: str, uploader_id: Enum, filenames: list
    ):
        uploader = self._get_current_uploader(uploader_id)
        validation_response = uploader.filenames_validation_handler(
            filenames, uploader.validation_parameters
        )
        # quota_response = uploader.check_quota_handler(tenant_id, auth_jwt, validation_response=validation_response)
        # if quota_response is not None:
        #     return quota_response
        return validation_response

    def validate_filecontents_flow(
        self,
        tenant_id: str,
        auth_jwt: str,
        uploader_id: Enum,
        files: List[bytes],
        clear_data: bool,
        event_id: str,
    ):
        uploader = self._get_current_uploader(uploader_id)
        validation_response = uploader.filecontents_validation_handler(
            files, uploader.validation_parameters
        )
        # quota_response = uploader.check_quota_handler(tenant_id, auth_jwt, validation_response=validation_response)
        # if quota_response is not None:
        #     return quota_response
        return validation_response

    def check_quota(self, tenant_id: str, auth_jwt: str, uploader_id: Enum):
        self._get_current_uploader(uploader_id)
        # return uploader.check_quota_handler(tenant_id, auth_jwt)
        return "TODO"

    def check_status(self, tenant_id: str, auth_jwt: str, uploader_id: Enum):
        self._get_current_uploader(uploader_id)
        # return uploader.check_status_handler(tenant_id, auth_jwt)
        return "TODO"
