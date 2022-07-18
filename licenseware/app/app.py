import requests
from typing import Any, Callable, Tuple
from dataclasses import dataclass
from licenseware.constants.states import States
from licenseware.utils.logger import log



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

        self.refresh_registration_url = "/refresh_registration"
        self.app_activation_url = "/activate_app"
        self.editable_tables_url = "/editable_tables"
        self.history_report_url = "/reports/history_report"
        self.tenant_registration_url = "/register_tenant"
        self.terms_and_conditions_url = "/terms_and_conditions"
        self.features_url = "/features"


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
                    "features_url": self.features_url,
                    "features": self.get_tenant_features_handler(),
                    "refresh_registration_url": self.refresh_registration_url,
                    "app_activation_url": self.app_activation_url,
                    "editable_tables_url": self.editable_tables_url,
                    "history_report_url": self.history_report_url,
                    "tenant_registration_url": self.tenant_registration_url,
                    "terms_and_conditions_url": self.terms_and_conditions_url,
                    "app_meta": self.app_meta,
                    "integration_details": self.integration_details
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

    