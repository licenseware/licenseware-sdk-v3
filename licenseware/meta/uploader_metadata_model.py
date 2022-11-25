from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .app_metadata_model import AppMetadataModel

from dataclasses import asdict, dataclass
from typing import List

from licenseware.uploader.encryption_parameters import UploaderEncryptionParameters
from licenseware.uploader.validation_parameters import UploaderValidationParameters


@dataclass
class UploaderStatusMetadataModel:
    tenant_id: str
    uploader_id: str
    status: str
    updated_at: str

    def dict(self):
        return asdict(self)


@dataclass
class UploaderMetadataModel:
    app_id: str
    name: str
    uploader_id: str
    description: str
    upload_url: str
    upload_validation_url: str
    quota_validation_url: str
    status_check_url: str
    accepted_file_types: str
    icon: str
    flags: List[str]
    updated_at: str
    validation_parameters: UploaderValidationParameters
    encryption_parameters: UploaderEncryptionParameters
    status: List[UploaderStatusMetadataModel]
    parrent_app: AppMetadataModel

    def dict(self):
        return asdict(self)
