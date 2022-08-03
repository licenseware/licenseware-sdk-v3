from dataclasses import dataclass
from typing import Any, Dict, Tuple

import requests

from licenseware import tenant as t
from licenseware.constants.states import States
from licenseware.report.report import NewReport, NewReportComponent
from licenseware.uploader.uploader import NewUploader
from licenseware.utils.logger import log


@dataclass
class NewApp:
    name: str
    description: str
    flags: Tuple[str] = None
    icon: str = None
    app_meta: dict = None
    integration_details: Tuple[dict] = None
    config: Any = None

    def __post_init__(self):

        assert self.config is not None
        assert hasattr(self.config, "APP_ID")
        assert hasattr(self.config, "REGISTER_APP_URL")
        assert hasattr(self.config, "get_machine_token")

        self.app_id = self.config.APP_ID
        self.uploaders: Dict[str, NewUploader] = dict()
        self.reports: Dict[str, NewReport] = dict()
        self.report_components: Dict[str, NewReportComponent] = dict()

    def attach_uploader(self, uploader: NewUploader):

        if uploader.uploader_id in self.uploaders.keys():
            raise ValueError(f"Uploader '{uploader.uploader_id}' is already attached")

        self.uploaders[uploader.uploader_id] = uploader

    def attach_report(self, report: NewReport):

        if report.report_id in self.reports.keys():
            raise ValueError(f"Report '{report.report_id}' is already attached")

        self.reports[report.report_id] = report

    def attach_report_component(self, report_component: NewReportComponent):

        if report_component.component_id in self.report_components.keys():
            raise ValueError(
                f"Report component '{report_component.component_id}' is already attached"
            )

        if report_component.order is None:
            report_component.order = len(self.report_components.keys()) + 1

        self.report_components[report_component.component_id] = report_component

    @property
    def metadata(self):

        metadata_payload = {
            "data": [
                {
                    "name": self.name,
                    "icon": self.icon,
                    "flags": self.flags,
                    "app_id": self.app_id,
                    "app_meta": self.app_meta,
                    "description": self.description,
                    "integration_details": self.integration_details,
                    "tenants_with_app_activated": t.get_tenants_with_app_activated(),
                    "tenants_with_data_available": t.get_tenants_with_data_available(),
                    "tenants_with_public_reports": t.get_tenants_with_public_reports(),
                    "features": t.get_tenant_features(),
                }
            ]
        }

        return metadata_payload

    def register(self):

        response = requests.post(  # pragma: no cover
            url=self.config.REGISTER_APP_URL,
            json=self.metadata,
            headers={"Authorization": self.config.get_machine_token()},
        )

        if response.status_code == 200:  # pragma: no cover
            return {
                "status": States.SUCCESS,
                "message": f"App '{self.app_id}' register successfully",
                "content": self.metadata,
            }, 200

        nokmsg = f"Could not register app '{self.app_id}'"  # pragma: no cover
        log.error(nokmsg)  # pragma: no cover
        return {
            "status": States.FAILED,
            "message": nokmsg,
            "content": self.metadata,
        }, 400  # pragma: no cover
