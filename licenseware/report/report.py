import requests
from typing import List, Any, Tuple
from dataclasses import dataclass
from licenseware.utils.logger import log
from licenseware.constants.states import States
from .report_component import NewReportComponent
from .report_component_filter import RCFilter


def _update_connected_apps(connected_apps, config):

    if connected_apps is None:
        connected_apps = [config.APP_ID]
    elif config.APP_ID not in connected_apps:
        connected_apps = list(connected_apps)
        connected_apps.append(config.APP_ID)

    return connected_apps


def _update_filters(filters):

    if filters is not None:
        parsed_filters = []
        for filter in filters:
            if isinstance(filter, dict):
                parsed_filters.append(filter)
            elif isinstance(filter, RCFilter):
                parsed_filters.append(filter.dict())
            else:
                raise ValueError("Only `dict` and `RCFilter` types are allowed")
        filters = parsed_filters

    return filters



@dataclass
class NewReport:
    name: str
    description: str
    report_id: str
    preview_image: str = None
    preview_image_dark: str = None
    connected_apps: Tuple[str] = None
    flags: Tuple[str] = None
    filters: List[str] = None
    config: Any = None

    def __post_init__(self):

        assert self.config is not None
        assert hasattr(self.config, "APP_ID")
        assert hasattr(self.config, "REGISTER_REPORT_URL")
        assert hasattr(self.config, "get_machine_token")

        self.app_id= self.config.APP_ID
        self.report_components = {}
        self.url = f'/reports/{self.report_id}' 
        self.public_url = f'/reports/{self.report_id}/public' 
        self.snapshot_url = f'/reports/{self.report_id}/snapshot' 
        self.preview_image_url = f'/reports/{self.report_id}/preview_image' 
        self.preview_image_dark_url = f'/reports/{self.report_id}/preview_image_dark' 
        self.connected_apps = _update_connected_apps(self.connected_apps, self.config)
        self.filters = _update_filters(self.filters)
        

    def register_component(self, component: NewReportComponent):
        if component.component_id in self.report_components.keys():
            raise ValueError(f"Report component '{component.component_id}' is already registered")
        self.report_components[component.component_id] = component
    

    @property
    def metadata(self):

        metadata_payload = {
            "data": [
                {
                    "app_id": self.app_id,
                    "report_id": self.report_id,
                    "name": self.name,
                    "description": self.description,
                    "flags": self.flags,
                    "url": self.url,
                    "public_url": self.public_url,
                    "snapshot_url": self.snapshot_url,
                    "preview_image_url": self.preview_image_url,
                    "preview_image_dark_url": self.preview_image_dark_url,
                    "report_components": self.report_components,
                    "connected_apps": self.connected_apps,
                    "filters": self.filters
                }
            ]
        }
        
        return metadata_payload

    def register(self):

        response = requests.post( # pragma: no cover
            url=self.config.REGISTER_REPORT_URL, 
            json=self.metadata, 
            headers={"Authorization": self.config.get_machine_token()}
        )

        if response.status_code == 200: # pragma: no cover
            return {
                    "status": States.SUCCESS,
                    "message": f"Report '{self.report_id}' register successfully",
                    "content": self.metadata
                }, 200

        nokmsg = f"Could not register report '{self.report_id}'" # pragma: no cover
        log.error(nokmsg) # pragma: no cover
        return {"status": States.FAILED, "message": nokmsg, "content": self.metadata}, 400 # pragma: no cover

    