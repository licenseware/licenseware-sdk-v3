from dataclasses import dataclass
from typing import Any, List

import requests

from licenseware import tenant as t
from licenseware.constants.states import States
from licenseware.report.report import NewReport, NewReportComponent
from licenseware.uploader.uploader import NewUploader
from licenseware.utils.alter_string import get_altered_strings
from licenseware.utils.logger import log


@dataclass
class NewApp:
    name: str
    description: str
    flags: List[str] = None
    icon: str = None
    app_meta: dict = None
    integration_details: List[dict] = None
    config: Any = None

    def __post_init__(self):

        assert self.config is not None
        assert hasattr(self.config, "APP_ID")
        assert hasattr(self.config, "REGISTER_APP_URL")
        assert hasattr(self.config, "REGISTER_ALL_URL")
        assert hasattr(self.config, "get_machine_token")

        self.app_id = self.config.APP_ID
        appid = get_altered_strings(self.app_id).dash

        self.attached_uploaders = {}
        self.attached_reports = {}
        self.attached_components = {}

        self.app_activation_url = f"/{appid}/activate-app"
        self.refresh_registration_url = f"/{appid}/refresh-registration"
        self.editable_tables_url = f"/{appid}/editable-tables"
        self.history_report_url = f"/{appid}/reports/history-report"
        self.tenant_registration_url = f"/{appid}/register-tenant"
        self.terms_and_conditions_url = f"/{appid}/terms-and-conditions"
        self.features_url = f"/{appid}/features"

    def attach_uploaders(self, uploaders: List[NewUploader]):

        for uploader in uploaders:
            if uploader.uploader_id in self.attached_uploaders.keys():
                raise ValueError(
                    f"Uploader '{uploader.uploader_id}' already attached to this app"
                )
            self.attached_uploaders[uploader.uploader_id] = uploader

        return self.attached_uploaders

    def attach_reports(self, reports: List[NewReport]):

        for report in reports:
            if report.report_id in self.attached_reports.keys():
                raise ValueError(
                    f"Report '{report.report_id}' already attached to this app"
                )
            self.attached_reports[report.report_id] = report

        return self.attached_reports

    def attach_components(self, components: List[NewReportComponent]):

        for component in components:
            if component.component_id in self.attached_components.keys():
                raise ValueError(
                    f"Report component '{component.component_id}' already attached to this app"
                )
            self.attached_components[component.component_id] = component

        return self.attached_components

    @property
    def metadata(self):

        metadata_payload = {
            "data": [
                {
                    "app_id": self.app_id,
                    "name": self.name,
                    "description": self.description,
                    "flags": self.flags,
                    "icon": self.icon,
                    "app_meta": self.app_meta,
                    "integration_details": self.integration_details,
                    "features": t.get_tenant_features(),
                    "tenants_with_app_activated": t.get_tenants_with_app_activated(),
                    "tenants_with_data_available": t.get_tenants_with_data_available(),
                    "refresh_registration_url": self.refresh_registration_url,
                    "app_activation_url": self.app_activation_url,
                    "editable_tables_url": self.editable_tables_url,
                    "history_report_url": self.history_report_url,
                    "tenant_registration_url": self.tenant_registration_url,
                    "terms_and_conditions_url": self.terms_and_conditions_url,
                    "features_url": self.features_url,
                }
            ]
        }

        return metadata_payload

    def register(self):  # pragma: no cover

        response = requests.post(
            url=self.config.REGISTER_APP_URL,
            json=self.metadata,
            headers={"Authorization": self.config.get_machine_token()},
        )

        if response.status_code == 200:
            return {
                "status": States.SUCCESS,
                "message": f"App '{self.app_id}' register successfully",
                "content": self.metadata,
            }, 200

        nokmsg = f"Could not register app '{self.app_id}'"
        log.error(nokmsg)
        return {
            "status": States.FAILED,
            "message": nokmsg,
            "content": self.metadata,
        }, 400

    @property
    def full_metadata(self):

        reports_metadata = (
            [i.metadata["data"] for i in self.attached_reports.values()][0]
            if self.attached_reports
            else []
        )
        uploaders_metadata = (
            [i.metadata["data"] for i in self.attached_uploaders.values()][0]
            if self.attached_uploaders
            else []
        )
        report_components_metadata = (
            [i.metadata["data"] for i in self.attached_components.values()][0]
            if self.attached_components
            else []
        )

        metadata = {
            "data": dict(
                apps=self.metadata["data"],
                reports=reports_metadata,
                uploaders=uploaders_metadata,
                report_components=report_components_metadata,
            )
        }

        return metadata

    def register_all(self):  # pragma: no cover

        response = requests.post(
            url=self.config.REGISTER_ALL_URL,
            json=self.full_metadata,
            headers={"Authorization": self.config.get_machine_token()},
        )

        if response.status_code == 200:
            return {
                "status": States.SUCCESS,
                "message": f"App full metadata '{self.app_id}' register successfully",
                "content": self.full_metadata,
            }, 200

        nokmsg = f"Could not register full metadata app '{self.app_id}'"
        log.error(nokmsg)
        return {
            "status": States.FAILED,
            "message": nokmsg,
            "content": self.full_metadata,
        }, 400
