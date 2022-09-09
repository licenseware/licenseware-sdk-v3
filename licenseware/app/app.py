import datetime
from dataclasses import dataclass
from typing import Dict, List

from licenseware.config.config import Config
from licenseware.constants import alias_types as alias
from licenseware.exceptions.custom_exceptions import ErrorAlreadyAttached
from licenseware.report.report import NewReport, NewReportComponent
from licenseware.uploader.uploader import NewUploader
from licenseware.utils.alter_string import get_altered_strings


@dataclass
class NewApp:
    name: str
    description: str
    config: Config
    flags: List[str] = None
    icon: str = None
    app_meta: List[dict] = None
    features: List[dict] = None
    integration_details: List[dict] = None

    def __post_init__(self):

        assert self.config.APP_ID is not None

        self.app_id = self.config.APP_ID
        appid = get_altered_strings(self.app_id).dash

        self.attached_uploaders: Dict[alias.UploaderId, NewUploader] = {}
        self.attached_reports: Dict[alias.ReportId, NewReport] = {}
        self.attached_components: Dict[alias.ReportComponentId, NewReportComponent] = {}

        self.datatables_url = f"/{appid}/datatables"
        self.history_report_url = f"/{appid}/reports/history-report"

    def attach_uploaders(self, uploaders: List[NewUploader]):

        for uploader in uploaders:
            if uploader.uploader_id in self.attached_uploaders.keys():
                raise ErrorAlreadyAttached(
                    f"Uploader '{uploader.uploader_id}' already attached to this app"
                )
            self.attached_uploaders[uploader.uploader_id] = uploader

        return self.attached_uploaders

    def attach_reports(self, reports: List[NewReport]):

        for report in reports:
            if report.report_id in self.attached_reports.keys():
                raise ErrorAlreadyAttached(
                    f"Report '{report.report_id}' already attached to this app"
                )
            self.attached_reports[report.report_id] = report

        return self.attached_reports

    def attach_components(self, components: List[NewReportComponent]):

        for component in components:
            if component.component_id in self.attached_components.keys():
                raise ErrorAlreadyAttached(
                    f"Report component '{component.component_id}' already attached to this app"
                )
            self.attached_components[component.component_id] = component

        return self.attached_components

    def get_metadata(self):

        metadata_payload = {
            # TODO - this id is not required, in fe needs to be updated with app_id
            # "id": 14,
            "app_id": self.app_id,
            # TODO - this will be always enabled - fe needs to remove handling for this field
            # "status": "enabled",
            "name": self.name,
            "description": self.description,
            "icon": self.icon,
            # TODO - app_activation_url is no longer needed
            # "app_activation_url": "https:\/\/api-dev.licenseware.io\/oem\/activate_app",
            # TODO - refresh_registration_url is no longer needed - notify will send all needed info
            # "refresh_registration_url": "https:\/\/api-dev.licenseware.io\/oem\/refresh_registration",
            # TODO - same as refresh_registration_url
            # "tenant_registration_url": "https:\/\/api-dev.licenseware.io\/oem\/register_tenant",
            "history_report_url": self.history_report_url,
            "flags": self.flags,
            # TODO - created at not needed, only updated_at will keep track of then this was updated
            # "created_at": "2022-08-22T13:38:02.000000Z",
            "updated_at": datetime.datetime.utcnow().isoformat(),
            # TODO - inform fe to update `editable_tables_url` field name to `datatables_url`
            "editable_tables_url": self.datatables_url,  # TODO - remove this field when fe updated
            "datatables_url": self.datatables_url,
            # TODO - not sure what this field returns, probably share reports only for some tenants?
            # "private_for_tenants": [],
            # TODO - now without app activation for each app there is only one terms and cond on first login
            # "terms_and_conditions_url": "https:\/\/api-dev.licenseware.io\/oem\/terms_and_conditions",
            "features": self.features,
            "app_meta": self.app_meta,
            "integration_details": self.integration_details,
        }

        return metadata_payload

    def get_full_metadata(self, tenant_id: str = None):

        app_metadata = self.get_metadata()

        uploaders_metadata = (
            [
                i.get_metadata(app_metadata, tenant_id)
                for i in self.attached_uploaders.values()
            ]
            if self.attached_uploaders
            else []
        )

        reports_metadata = (
            [i.get_metadata(tenant_id) for i in self.attached_reports.values()]
            if self.attached_reports
            else []
        )

        report_components_metadata = (
            [i.get_metadata(tenant_id) for i in self.attached_components.values()]
            if self.attached_components
            else []
        )

        metadata = {
            "app": app_metadata,
            "reports": reports_metadata,
            "uploaders": uploaders_metadata,
            "report_components": report_components_metadata,
        }

        return metadata
