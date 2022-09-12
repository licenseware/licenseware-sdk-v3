import datetime
from dataclasses import dataclass
from typing import Dict, List

from licenseware.config.config import Config
from licenseware.constants.states import States
from licenseware.exceptions.custom_exceptions import ErrorAlreadyAttached
from licenseware.utils.alter_string import get_altered_strings

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
    return [comp.get_metadata() for _, comp in report_components.items()]


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
        assert self.config.FRONTEND_URL is not None
        assert self.config.PUBLIC_TOKEN_REPORT_URL is not None
        assert self.config.APP_SECRET is not None
        assert self.config.get_machine_token is not None

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
        self._parrent_app = None

    def _get_component_by_id(self, component_id: str):
        assert self.components is not None

        for comp in self.components:
            if comp.component_id == component_id:
                return comp

        raise Exception(
            f"Component '{component_id}' not found on given report components"
        )  # pragma no cover

    def attach(self, component_id: str):

        if component_id in self.report_components.keys():
            raise ErrorAlreadyAttached(
                f"Report component '{component_id}' is already attached"
            )

        component = self._get_component_by_id(component_id)

        if component.order is None:
            component.order = len(self.report_components.keys()) + 1

        self.report_components[component.component_id] = component

    def get_metadata(self, tenant_id: str = None, parrent_app_metadata: dict = None):

        if not self.registrable:
            return

        # TODO - provide data related to given tenant_id

        if self._parrent_app is not None:
            parrent_app_metadata = self._parrent_app.get_metadata()

        metadata = {
            "app_id": self.app_id,
            "report_id": self.report_id,
            "name": self.name,
            "description": self.description,
            "url": self.url,
            "connected_apps": self.connected_apps,
            "flags": self.flags,
            "registrable": self.registrable,
            # TODO - updated_at will be used instead
            # "created_at": "2022-04-04T09:17:21.000000Z",
            "updated_at": datetime.datetime.utcnow().isoformat(),
            # TODO - not sure what this is it's on app, uploader also
            # "private_for_tenants": [],
            "report_components": _parse_report_components(self.report_components),
            # TODO - not needed, preview report is loaded dynamically in fe
            # "preview_image_url": "https:\/\/api-dev.licenseware.io\/ifmp\/reports\/infrastructure_mapping_report\/preview_image",
            "public_url": self.public_url,
            "snapshot_url": self.snapshot_url,
            # TODO - enable this if tenant_id has data for this report
            "status": States.DISABLED,
            # TODO - get status from uploaders
            "processing_status": States.IDLE,
            # TODO - change this each time a new processing has been done
            "last_update_date": None,
            "main_app": parrent_app_metadata,
            # TODO - get list of connected apps metadata
            "apps": [],
            "filters": self.filters,
        }

        # TODO - inform fe to use report_id instead of id
        # "id": 2,
        # TODO - not needed anymore, report is loaded dynamically in preview
        # "preview_image_dark_url": None,

        return metadata
