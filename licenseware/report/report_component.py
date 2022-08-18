from dataclasses import dataclass
from typing import Any, Callable, Union

import requests

from licenseware.constants.attributes_type import AttributesType
from licenseware.constants.states import States
from licenseware.utils.alter_string import get_altered_strings
from licenseware.utils.logger import log

from .report_filter import ReportFilter
from .style_attributes import StyleAttrs

from typing import NewType

TenantId = NewType("tenant_id", str)
Authorization = NewType("authorization", str)
Filters = NewType("filters", str)
Limit = NewType("limit", int)
Skip = NewType("skip", int)


@dataclass
class NewReportComponent:
    title: str
    component_id: str
    attributes: AttributesType
    style_attributes: StyleAttrs
    get_component_data_handler: Callable[
        [
            TenantId,
            Authorization,
            Filters,
            Limit,
            Skip,
        ],
        Union[list, dict],
    ]
    order: int = None
    filters: ReportFilter = None
    config: Any = None

    def __post_init__(self):

        assert self.config is not None
        assert hasattr(self.config, "APP_ID")
        assert hasattr(self.config, "REGISTER_REPORT_COMPONENT_URL")
        assert hasattr(self.config, "get_machine_token")

        if isinstance(self.filters, ReportFilter):
            self.filters = self.filters.metadata

        self.app_id = self.config.APP_ID

        appid = get_altered_strings(self.app_id).dash
        compid = get_altered_strings(self.component_id).dash

        self.component_type = self.attributes.component_type
        self.url = f"/{appid}/report-components/{compid}"
        self.public_url = f"/{appid}/report-components/{compid}/public"
        self.snapshot_url = f"/{appid}/report-components/{compid}/snapshot"

    @property
    def metadata(self):

        metadata_payload = {
            "data": [
                {
                    "app_id": self.app_id,
                    "component_id": self.component_id,
                    "url": self.url,
                    "public_url": self.public_url,
                    "snapshot_url": self.snapshot_url,
                    "order": self.order,
                    "style_attributes": self.style_attributes.metadata,
                    "attributes": self.attributes.metadata,
                    "title": self.title,
                    "type": self.component_type,
                    "filters": self.filters,
                }
            ]
        }

        return metadata_payload

    def register(self):  # pragma: no cover

        response = requests.post(
            url=self.config.REGISTER_REPORT_COMPONENT_URL,
            json=self.metadata,
            headers={"Authorization": self.config.get_machine_token()},
        )

        if response.status_code == 200:
            return {
                "status": States.SUCCESS,
                "message": f"Report component '{self.component_id}' register successfully",
                "content": self.metadata,
            }, 200

        nokmsg = f"Could not register component '{self.component_id}'"
        log.error(nokmsg)
        return {
            "status": States.FAILED,
            "message": nokmsg,
            "content": self.metadata,
        }, 400
