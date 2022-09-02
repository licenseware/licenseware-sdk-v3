from dataclasses import dataclass
from typing import Dict, List

import requests

from licenseware.config.config import Config
from licenseware.constants.states import States
from licenseware.utils.alter_string import get_altered_strings
from licenseware.utils.logger import log

from . import default_handlers
from .report_component import NewReportComponent
from .report_filter import ReportFilter


def _update_connected_apps(connected_apps, config):

    if connected_apps is None:
        connected_apps = [config.APP_ID]
    elif config.APP_ID not in connected_apps:
        connected_apps = list(connected_apps)
        connected_apps.append(config.APP_ID)

    return connected_apps


def _parse_report_components(report_components: Dict[str, NewReportComponent]):
    return [comp.metadata["data"][0] for _, comp in report_components.items()]


@dataclass
class NewReport:
    name: str
    description: str
    report_id: str
    config: Config
    connected_apps: List[str] = None
    flags: List[str] = None
    filters: ReportFilter = None
    components: List[NewReportComponent] = None
    registrable: bool = True

    def __post_init__(self):

        assert self.config.APP_ID is not None

        self.app_id = self.config.APP_ID
        ns = get_altered_strings(self.app_id).dash
        reportid = get_altered_strings(self.report_id).dash

        if isinstance(self.filters, ReportFilter):
            self.filters = self.filters.metadata

        self.report_components: Dict[str, NewReportComponent] = dict()
        self.url = f"/{ns}/reports/{reportid}"
        self.public_url = f"/{ns}/public-reports/{reportid}"
        self.snapshot_url = f"/{ns}/snapshot-reports/{reportid}"
        self.connected_apps = _update_connected_apps(self.connected_apps, self.config)

    def _get_component_by_id(self, component_id: str):
        assert self.components is not None

        for comp in self.components:
            if comp.component_id == component_id:
                return comp

        raise ValueError(
            f"Component '{component_id}' not found on given report components"
        )  # pragma no cover

    def attach(self, component_id: str):

        if component_id in self.report_components.keys():
            raise ValueError(f"Report component '{component_id}' is already attached")

        component = self._get_component_by_id(component_id)

        if component.order is None:
            component.order = len(self.report_components.keys()) + 1

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
                    "report_components": _parse_report_components(
                        self.report_components
                    ),
                    "connected_apps": self.connected_apps,
                    "filters": self.filters,
                    "registrable": self.registrable,
                    "public_for_tenants": default_handlers.get_tenants_with_public_reports(),
                }
            ]
        }

        return metadata_payload
