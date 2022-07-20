import requests
from typing import Any, Callable, Tuple, Dict
from dataclasses import dataclass
from licenseware.constants.states import States
from licenseware.utils.logger import log
from licenseware.uploader.uploader import NewUploader
from licenseware.report.report import NewReport, NewReportComponent
from .route_handlers import NewAppRouteHandlers
from .app_apispecs import AppApiSpecs


@dataclass
class NewApp:
    name:str
    description:str
    get_tenants_with_app_activated_handler: Callable
    get_tenants_with_data_available_handler: Callable
    get_tenants_with_public_reports_handler: Callable
    get_tenant_features_handler: Callable
    app_id:str = None
    flags: Tuple[str] = None
    icon:str = None
    app_meta: dict = None
    integration_details: Tuple[dict] = None
    config: Any = None


    def __post_init__(self):

        assert self.config is not None
        if hasattr(self.config, "APP_ID") and self.app_id is None:
            self.app_id = self.config.APP_ID
        assert hasattr(self.config, "REGISTER_APP_URL")
        assert hasattr(self.config, "get_machine_token")

        self.uploaders: Dict[str, NewUploader] = dict() 
        self.reports: Dict[str, NewReport] = dict()
        self.report_components: Dict[str, NewReportComponent] = dict()
        self.routes = NewAppRouteHandlers(self.app_id)
        self.apispecs = AppApiSpecs(self.routes)
        
    
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
            raise ValueError(f"Report component '{report_component.component_id}' is already attached")

        if report_component.order is None:
            report_component.order = len(self.report_components.keys()) + 1

        self.report_components[report_component.component_id] = report_component


    @property
    def metadata(self):

        metadata_payload = {
            "data": [
                {
                    "app_id": self.app_id,
                    "name": self.name,
                    "description": self.description,
                    "tenants_with_app_activated": self.get_tenants_with_app_activated_handler(),
                    "tenants_with_data_available": self.get_tenants_with_data_available_handler(),
                    "tenants_with_public_reports": self.get_tenants_with_public_reports_handler(),
                    "flags": self.flags,
                    "icon": self.icon,
                    "features": self.get_tenant_features_handler(),
                    "app_meta": self.app_meta,
                    "integration_details": self.integration_details,
                    **self.routes.urls
                }
            ]
        }
        
        return metadata_payload


    def register(self):

        response = requests.post( # pragma: no cover
            url=self.config.REGISTER_APP_URL, 
            json=self.metadata, 
            headers={"Authorization": self.config.get_machine_token()}
        )

        if response.status_code == 200: # pragma: no cover
            return {
                    "status": States.SUCCESS,
                    "message": f"App '{self.app_id}' register successfully",
                    "content": self.metadata
                }, 200

        nokmsg = f"Could not register app '{self.app_id}'" # pragma: no cover
        log.error(nokmsg) # pragma: no cover
        return {"status": States.FAILED, "message": nokmsg, "content": self.metadata}, 400 # pragma: no cover

    