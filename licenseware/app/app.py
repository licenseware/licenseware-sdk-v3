import datetime
from dataclasses import dataclass
from typing import Dict, List

from licenseware.config.config import Config
from licenseware.constants import alias_types as alias
from licenseware.constants.states import States
from licenseware.exceptions.custom_exceptions import ErrorAlreadyAttached
from licenseware.report.report import NewReport, NewReportComponent
from licenseware.uploader.uploader import NewUploader
from licenseware.meta.app_metadata_model import (
    AppMetaModel,
    AppMetadataModel,
    FullAppMetadataModel,
)


@dataclass
class NewApp:
    name: str
    description: str
    config: Config
    flags: List[str] = None
    icon: str = None
    app_meta: AppMetaModel = None
    features: List[dict] = None
    integration_details: List[dict] = None
    registrable: bool = True

    def __post_init__(self):

        self.attached_uploaders: Dict[alias.UploaderId, NewUploader] = {}
        self.attached_reports: Dict[alias.ReportId, NewReport] = {}
        self.attached_components: Dict[alias.ReportComponentId, NewReportComponent] = {}

        self.datatables_url = f"/datatables"
        self.history_report_url = f"/reports/history-report"

    def attach_uploaders(self, uploaders: List[NewUploader]):

        for uploader in uploaders:
            if not uploader.registrable:
                continue
            if uploader.uploader_id in self.attached_uploaders.keys():
                raise ErrorAlreadyAttached(
                    f"Uploader '{uploader.uploader_id}' already attached to this app"
                )
            self.attached_uploaders[uploader.uploader_id] = uploader

        return self.attached_uploaders

    def attach_reports(self, reports: List[NewReport]):

        for report in reports:
            if not report.registrable:
                continue
            if report.report_id in self.attached_reports.keys():
                raise ErrorAlreadyAttached(
                    f"Report '{report.report_id}' already attached to this app"
                )
            self.attached_reports[report.report_id] = report

        return self.attached_reports

    def attach_components(self, components: List[NewReportComponent]):

        for component in components:
            if not component.registrable:
                continue
            if component.component_id in self.attached_components.keys():
                raise ErrorAlreadyAttached(
                    f"Report component '{component.component_id}' already attached to this app"
                )
            self.attached_components[component.component_id] = component

        return self.attached_components

    def get_metadata(self, as_dict: bool = True):

        metadata = AppMetadataModel(
            app_id=self.config.APP_ID,
            status=States.AVAILABLE,
            name=self.name,
            description=self.description,
            icon=self.icon,
            history_report_url=self.history_report_url,
            flags=self.flags,
            updated_at=datetime.datetime.utcnow().isoformat(),
            editable_tables_url=self.datatables_url,  # TODO - remove this field when fe updated
            datatables_url=self.datatables_url,
            features=self.features,
            app_meta=self.app_meta,
            integration_details=self.integration_details,
        )

        return metadata.dict() if as_dict else metadata

    def get_full_metadata(self, as_dict: bool = True):

        app_metadata = self.get_metadata()
        uploaders_metadata = self.get_uploaders_metadata(app_metadata)
        reports_metadata = self.get_reports_metadata(app_metadata, uploaders_metadata)
        report_components = self.get_components_metadata()

        metadata = FullAppMetadataModel(
            app=app_metadata,
            uploaders=uploaders_metadata,
            reports=reports_metadata,
            report_components=report_components,
        )

        return metadata.dict() if as_dict else metadata

    def get_uploaders_metadata(self, parrent_app_metadata: dict):
        uploaders_metadata = (
            [
                i.get_metadata(parrent_app_metadata)
                for i in self.attached_uploaders.values()
            ]
            if self.attached_uploaders
            else []
        )
        return uploaders_metadata

    def get_reports_metadata(
        self, parrent_app_metadata: dict, uploaders_metadata: List[dict]
    ):
        reports_metadata = (
            [
                i.get_metadata(parrent_app_metadata, uploaders_metadata)
                for i in self.attached_reports.values()
            ]
            if self.attached_reports
            else []
        )
        return reports_metadata

    def get_components_metadata(self):
        report_components_metadata = (
            [i.get_metadata() for i in self.attached_components.values()]
            if self.attached_components
            else []
        )
        return report_components_metadata
