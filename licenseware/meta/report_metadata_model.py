from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .app_metadata_model import AppMetadataModel

from typing import List
from dataclasses import dataclass, asdict


@dataclass
class ReportComponentMetadataModel:
    app_id: str
    component_id: str
    description: str
    url: str
    public_url: str
    snapshot_url: str
    order: int
    style_attributes: dict
    attributes: dict
    title: str
    type: str
    filters: List[dict]

    def dict(self):
        return asdict(self)


@dataclass
class ReportMetadataModel:
    app_id: str
    report_id: str
    name: str
    description: str
    url: str
    connected_apps: List[str]
    report_components: List[ReportComponentMetadataModel]
    flags: List[str]
    filters: List[dict]
    updated_at: str
    public_url: str
    snapshot_url: str
    parrent_app: AppMetadataModel
    apps: List[AppMetadataModel]
    status: List[dict]
    registrable: bool = True

    def dict(self):
        return asdict(self)
