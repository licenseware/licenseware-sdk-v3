from dataclasses import dataclass
from typing import Callable

from licenseware.config.config import Config
from licenseware.constants import alias_types as alias
from licenseware.constants.attributes_type import AttributesType
from licenseware.constants.states import States
from licenseware.constants.web_response import WebResponse
from licenseware.utils.alter_string import get_altered_strings
from licenseware.utils.logger import log

from .report_filter import ReportFilter
from .style_attributes import StyleAttrs


@dataclass
class NewReportComponent:
    title: str
    component_id: str
    attributes: AttributesType
    style_attributes: StyleAttrs
    get_component_data_handler: Callable[
        [
            alias.TenantId,
            alias.Authorization,
            alias.Repository,
            alias.Filters,
            alias.Limit,
            alias.Skip,
        ],
        WebResponse,
    ]
    component_type: str = None
    description: str = None
    order: int = None
    filters: ReportFilter = None
    config: Config = None

    def __post_init__(self):

        assert self.config is not None
        assert hasattr(self.config, "APP_ID")
        assert hasattr(self.config, "REGISTER_REPORT_COMPONENT_URL")
        assert hasattr(self.config, "get_machine_token")

        if isinstance(self.filters, ReportFilter):  # pragma no cover
            self.filters = self.filters.metadata

        self.app_id = self.config.APP_ID

        appid = get_altered_strings(self.app_id).dash
        compid = get_altered_strings(self.component_id).dash

        if self.component_type is None:
            self.component_type = self.attributes.component_type

        if hasattr(self.attributes, "metadata"):
            self.attributes = self.attributes.metadata

        if hasattr(self.style_attributes, "metadata"):
            self.style_attributes = self.style_attributes.metadata

        self.url = f"/{appid}/report-components/{compid}"
        self.public_url = f"/{appid}/public-report-components/{compid}"
        self.snapshot_url = f"/{appid}/snapshot-report-components/{compid}"

    @property
    def metadata(self):

        metadata_payload = {
            "data": [
                {
                    "app_id": self.app_id,
                    "component_id": self.component_id,
                    "description": self.description,
                    "url": self.url,
                    "public_url": self.public_url,
                    "snapshot_url": self.snapshot_url,
                    "order": self.order,
                    "style_attributes": self.style_attributes,
                    "attributes": self.attributes,
                    "title": self.title,
                    "type": self.component_type,
                    "filters": self.filters,
                }
            ]
        }

        return metadata_payload
