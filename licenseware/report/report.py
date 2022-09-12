import datetime
from dataclasses import dataclass
from typing import Dict, List

from licenseware.config.config import Config
from licenseware.constants.states import States
from licenseware.dependencies import requests
from licenseware.exceptions.custom_exceptions import ErrorAlreadyAttached
from licenseware.repository.mongo_repository.mongo_repository import MongoRepository
from licenseware.utils.alter_string import get_altered_strings
from licenseware.utils.logger import log

from .default_handlers import get_report_processing_status
from .report_component import NewReportComponent
from .report_filter import ReportFilter


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
        assert self.config.machine_auth_headers is not None

        self.app_id = self.config.APP_ID
        ns = get_altered_strings(self.app_id).dash
        reportid = get_altered_strings(self.report_id).dash

        if isinstance(self.filters, ReportFilter):
            self.filters = self.filters.metadata

        self.report_components: Dict[str, NewReportComponent] = dict()
        self.url = f"/{ns}/reports/{reportid}"
        self.public_url = f"/{ns}/public-reports/{reportid}"
        self.snapshot_url = f"/{ns}/snapshot-reports/{reportid}"
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

        if self._parrent_app is not None:
            parrent_app_metadata = self._parrent_app.get_metadata(tenant_id)

        processing_state = self._get_report_processing_state(tenant_id)
        report_status = (
            States.DISABLED
            if processing_state["status"] == States.RUNNING
            else States.ENABLED
        )

        report_components = _parse_report_components(self.report_components)
        apps = self._get_connected_apps_metadata(
            tenant_id, parrent_app_metadata, self.connected_apps
        )

        metadata = {
            "app_id": self.app_id,
            "report_id": self.report_id,
            "name": self.name,
            "description": self.description,
            "url": self.url,
            "connected_apps": self.connected_apps,
            "flags": self.flags,
            "registrable": self.registrable,
            "updated_at": datetime.datetime.utcnow().isoformat(),
            "report_components": report_components,
            "public_url": self.public_url,
            "snapshot_url": self.snapshot_url,
            "status": report_status,
            "processing_status": processing_state["status"],
            "last_update_date": processing_state["updated_at"],
            "parrent_app": parrent_app_metadata,
            "apps": apps,
            "filters": self.filters,
        }

        # TODO - inform fe main_app is parrent_app
        # TODO - inform fe to use report_id instead of id
        # "id": 2,
        # TODO - not needed anymore, report is loaded dynamically in preview
        # "preview_image_dark_url": None,
        # TODO - updated_at will be used instead
        # "created_at": "2022-04-04T09:17:21.000000Z",
        # TODO - not sure what this is it's on app, uploader also
        # "private_for_tenants": [],
        # TODO - not needed, preview report is loaded dynamically in fe
        # "preview_image_url": "https:\/\/api-dev.licenseware.io\/ifmp\/reports\/infrastructure_mapping_report\/preview_image",
        # TODO - enable this if tenant_id has data for this report

        return metadata

    def _get_connected_apps_metadata(
        self, tenant_id: str, parrent_app_metadata: dict, connected_apps: List[str]
    ):

        connected_apps_metadata = [parrent_app_metadata]

        if connected_apps is None:
            return connected_apps_metadata

        for metadata_url in connected_apps:
            response = requests.get(
                metadata_url, headers=self.config.machine_auth_headers
            )
            if response.status_code != 200:
                log.error(response.content)
                raise Exception(
                    f"Can't get connected app metadata from url {metadata_url}"
                )
            connected_apps_metadata.append(response.json())

        return connected_apps_metadata

    def _get_report_processing_state(self, tenant_id: str):

        if tenant_id is None:
            return {
                "status": States.IDLE,
                "updated_at": None,
            }

        status_repo = MongoRepository(
            self.config.mongo_db_connection,
            collection=self.config.MONGO_COLLECTION.UPLOADER_STATUS,
        )
        report_status = get_report_processing_status(tenant_id, status_repo)
        return report_status
