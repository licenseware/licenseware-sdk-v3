import requests
from typing import Callable, Union, Any
from dataclasses import dataclass
from licenseware.constants.states import States
from licenseware.constants.attributes_type import AttributesType
from licenseware.utils.logger import log
from licenseware.utils.alter_string import get_altered_strings
from .style_attributes import StyleAttrs
from .report_filter import ReportFilter



@dataclass
class NewReportComponent:
    title: str
    component_id: str 
    attributes: AttributesType
    style_attributes: StyleAttrs
    get_component_data_handler: Callable[[Any], Union[list, dict]]
    order: int = None
    filters: ReportFilter = None
    config: Any = None


    def __post_init__(self):

        assert self.config is not None
        assert hasattr(self.config, "APP_ID")
        assert hasattr(self.config, "REGISTER_REPORT_COMPONENT_URL")
        assert hasattr(self.config, "get_machine_token")

        self.app_id = self.config.APP_ID

        appid = get_altered_strings(self.app_id).dash
        compid = get_altered_strings(self.component_id).dash

        self.component_type = self.attributes.component_type
        self.url = f'/{appid}/report-components/{compid}'
        self.public_url = f'/{appid}/report-components/{compid}/public'
        self.snapshot_url = f'/{appid}/report-components/{compid}/snapshot'


    def get_component_data(self, *args, **kwargs):
        return self.get_component_data_handler(*args, **kwargs)


    @property
    def metadata(self):

        metadata_payload = { # pragma no cover
            'data': [{
                "app_id": self.app_id,
                "component_id": self.component_id,
                "url": self.url,
                "public_url": self.public_url,
                "snapshot_url": self.snapshot_url,
                "order": self.order,
                "style_attributes": self.style_attributes.metadata,
                "attributes": self.attributes.metadata,
                "title": self.title,
                "component_type": self.component_type,
                "filters": self.filters.metadata if self.filters is not None else None
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

    


