import datetime
from dataclasses import dataclass
from typing import Callable, List, Tuple, Union

from licenseware.config.config import Config
from licenseware.constants import alias_types as alias
from licenseware.constants.uploader_types import (
    FileValidationResponse,
    UploaderStatusResponse,
)
from licenseware.constants.web_response import WebResponse
from licenseware.constants.worker_event_type import WorkerEvent
from licenseware.redis_cache.redis_cache import RedisCache
from licenseware.uploader.default_handlers import (
    default_check_quota_handler,
    default_check_status_handler,
    default_filecontents_validation_handler,
    default_filenames_validation_handler,
    default_update_status_handler,
)
from licenseware.uploader.encryption_parameters import UploaderEncryptionParameters
from licenseware.uploader.validation_parameters import UploaderValidationParameters
from licenseware.utils.alter_string import get_altered_strings


@dataclass
class NewUploader:
    name: str
    description: str
    uploader_id: str
    accepted_file_types: tuple
    config: Config
    worker: Callable[[WorkerEvent], None]
    free_units: int = 1
    validation_parameters: UploaderValidationParameters = None
    encryption_parameters: UploaderEncryptionParameters = None
    flags: Tuple[str] = None
    icon: str = None
    filenames_validation_handler: Callable[
        [List[str], UploaderValidationParameters], WebResponse
    ] = default_filenames_validation_handler
    filecontents_validation_handler: Callable[
        [Union[List[str], List[bytes]], UploaderValidationParameters],
        WebResponse,
    ] = default_filecontents_validation_handler
    check_quota_handler: Callable[
        [
            alias.TenantId,
            alias.Authorization,
            alias.UploaderId,
            alias.FreeUnits,
            FileValidationResponse,
            alias.Repository,
            Config,
        ],
        WebResponse,
    ] = default_check_quota_handler
    check_status_handler: Callable[
        [alias.TenantId, alias.Authorization, alias.UploaderId, alias.RedisCache],
        WebResponse,
    ] = default_check_status_handler
    update_status_handler: Callable[
        [
            alias.TenantId,
            alias.Authorization,
            alias.UploaderId,
            alias.Status,
            alias.RedisCache,
            Config,
        ],
        UploaderStatusResponse,
    ] = default_update_status_handler
    registrable: bool = True

    def __post_init__(self):

        assert self.config.APP_ID is not None

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

        ns = get_altered_strings(self.app_id).dash
        uploaderid = get_altered_strings(self.uploader_id).dash

        self.upload_validation_url = f"/{ns}/uploads/{uploaderid}/validation"
        self.upload_url = f"/{ns}/uploads/{uploaderid}/files"
        self.quota_validation_url = f"/{ns}/uploads/{uploaderid}/quota"
        self.status_check_url = f"/{ns}/uploads/{uploaderid}/status"
        self._parrent_app = None

    def get_metadata(self):

        if not self.registrable:
            return

        metadata = {
            "app_id": self.app_id,
            "name": self.name,
            "uploader_id": self.uploader_id,
            "description": self.description,
            "upload_url": self.upload_url,
            "upload_validation_url": self.upload_validation_url,
            "quota_validation_url": self.quota_validation_url,
            "status_check_url": self.status_check_url,
            "accepted_file_types": self.accepted_file_types,
            "icon": self.icon,
            "flags": self.flags,
            "updated_at": datetime.datetime.utcnow().isoformat(),
            "validation_parameters": self.validation_parameters,
            "encryption_parameters": self.encryption_parameters,
            "status": self._get_tenant_uploader_id_statuses(),
            "parrent_app": self._parrent_app.get_metadata(),
        }

        return metadata

    def _get_tenant_uploader_id_statuses(self):
        redisdb = RedisCache(self.config)
        results = redisdb.get(f"*:{self.uploader_id}")
        return results
