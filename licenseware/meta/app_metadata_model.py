from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .uploader_metadata_model import UploaderMetadataModel
    from .report_metadata_model import (
        ReportComponentMetadataModel,
        ReportMetadataModel,
    )

from dataclasses import asdict, dataclass
from typing import List


@dataclass
class AppMetaPartnerModel:
    partner_app: bool
    partner_icon: str
    partner_url: str
    partner_name: str

    def dict(self):
        return asdict(self)


@dataclass
class AppMetaModel:
    partner_meta: AppMetaPartnerModel

    def dict(self):
        return asdict(self)


@dataclass
class AppMetadataModel:
    app_id: str
    status: str
    name: str
    description: str
    icon: str
    history_report_url: str
    updated_at: str
    editable_tables_url: str
    datatables_url: str
    flags: List[str] = None
    app_meta: AppMetaModel = None
    features: List[dict] = None
    integration_details: List[dict] = None

    def dict(self):
        return asdict(self)


@dataclass
class FullAppMetadataModel:
    app: AppMetadataModel
    uploaders: List[UploaderMetadataModel]
    reports: List[ReportMetadataModel]
    report_components: List[ReportComponentMetadataModel]

    def dict(self):
        return asdict(self)
