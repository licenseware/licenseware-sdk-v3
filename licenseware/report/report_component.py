import requests
from typing import Callable, Union, Any, Tuple
from dataclasses import dataclass
from licenseware.constants.states import States
from licenseware.utils.logger import log


@dataclass
class NewReportComponent:
    title: str
    component_id: str 
    component_type: str
    attributes: dict
    style_attributes: dict
    get_component_data_handler: Callable[[Any], Union[list, dict]]
    order: int = 0
    filters: Tuple[str] = None
    config: Any = None


    def __post_init__(self):

        assert self.config is not None
        assert hasattr(self.config, "APP_ID")
        assert hasattr(self.config, "REGISTER_REPORT_COMPONENT_URL")
        assert hasattr(self.config, "get_machine_token")

        self.app_id= self.config.APP_ID
        self.url = f'/report-components/{self.component_id}'
        self.public_url = f'/report-components/{self.component_id}/public'
        self.snapshot_url = f'/report-components/{self.component_id}/snapshot'


    def get_component_data(self, *args, **kwargs):
        return self.get_component_data_handler(*args, **kwargs)


    @property
    def metadata(self):

        metadata_payload = {
            'data': [{
                "app_id": self.app_id,
                "component_id": self.component_id,
                "url": self.url,
                "public_url": self.public_url,
                "snapshot_url": self.snapshot_url,
                "order": self.order,
                "style_attributes": self.style_attributes,
                "attributes": self.attributes,
                "title": self.title,
                "component_type": self.component_type,
                "filters": self.filters
            }]
        }

        return metadata_payload


    def register(self):

        response = requests.post( # pragma: no cover
            url=self.config.REGISTER_REPORT_COMPONENT_URL, 
            json=self.metadata, 
            headers={"Authorization": self.config.get_machine_token()}
        )

        if response.status_code == 200: # pragma: no cover
            return {
                    "status": States.SUCCESS,
                    "message": f"Report component '{self.component_id}' register successfully",
                    "content": self.metadata
                }, 200

        nokmsg = f"Could not register component '{self.component_id}'" # pragma: no cover
        log.error(nokmsg) # pragma: no cover
        return {"status": States.FAILED, "message": nokmsg, "content": self.metadata}, 400 # pragma: no cover

    


