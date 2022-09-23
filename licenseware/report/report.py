import datetime
from dataclasses import dataclass
from typing import Callable, Dict, List

from licenseware.config.config import Config
from licenseware.constants import alias_types as alias
from licenseware.exceptions.custom_exceptions import ErrorAlreadyAttached
from licenseware.utils.alter_string import get_altered_strings

from .default_handlers import (
    DefaultMetadataHandler,
    default_get_tenants_with_data_handler,
)
from .report_component import NewReportComponent
from .report_filter import ReportFilter


@dataclass
class NewReport:
    name: str
    description: str
    report_id: str
    config: Config
    connected_apps: List[alias.AppId] = None
    flags: List[str] = None
    filters: ReportFilter = None
    components: List[NewReportComponent] = None
    registrable: bool = True
    tenants_with_data_handler: Callable[
        [alias.Repository, alias.TenantId],
        List[Dict[alias.TenantId, alias.UpdatedAt]],
    ] = default_get_tenants_with_data_handler
    external_metadata_handler: DefaultMetadataHandler = DefaultMetadataHandler

    def __post_init__(self):

        assert self.config.APP_ID is not None
        assert self.config.FRONTEND_URL is not None
        assert self.config.PUBLIC_TOKEN_REPORT_URL is not None
        assert self.config.APP_SECRET is not None

        self.app_id = self.config.APP_ID
        ns = get_altered_strings(self.app_id).dash
        reportid = get_altered_strings(self.report_id).dash

        if isinstance(self.filters, ReportFilter):
            self.filters = self.filters.metadata

        if self.connected_apps is None:
            self.connected_apps = [self.app_id]

        if self.app_id not in self.connected_apps:
            self.connected_apps.append(self.app_id)

        self.report_components: Dict[str, NewReportComponent] = dict()
        self.report_components_metadata = None
        self.url = f"/{ns}/reports/{reportid}"
        self.public_url = f"/{ns}/public-reports/{reportid}"
        self.snapshot_url = f"/{ns}/snapshot-reports/{reportid}"

    def attach(self, component_id: str):

        if component_id in self.report_components.keys():
            raise ErrorAlreadyAttached(
                f"Report component '{component_id}' is already attached"
            )

        component = self._get_component_by_id(component_id)

        if component.order is None:
            component.order = len(self.report_components.keys()) + 1

        self.report_components[component.component_id] = component
        self.report_components_metadata = self._get_report_components_metadata()

    def get_metadata(
        self, parrent_app_metadata: dict = None, uploaders_metadata: dict = None
    ):

        if not self.registrable:
            return

        tenants_with_data = self.tenants_with_data_handler(
            self.config.mongo_db_connection
        )
        metadata: DefaultMetadataHandler = self.external_metadata_handler(
            self.connected_apps, self.config
        )
        apps_metadata = metadata.get_connected_apps_metadata(parrent_app_metadata)
        uploaders_metadata = metadata.get_connected_uploaders_metadata(
            uploaders_metadata
        )
        uploader_statuses = metadata.extract_uploader_statuses(uploaders_metadata)
        report_statuses = metadata.extract_report_statuses(
            uploader_statuses, tenants_with_data
        )

        metadata = {
            "app_id": self.app_id,
            "report_id": self.report_id,
            "name": self.name,
            "description": self.description,
            "url": self.url,
            "connected_apps": self.connected_apps,
            "report_components": self.report_components_metadata,
            "flags": self.flags,
            "filters": self.filters,
            "registrable": self.registrable,
            "updated_at": datetime.datetime.utcnow().isoformat(),
            "public_url": self.public_url,
            "snapshot_url": self.snapshot_url,
            "parrent_app": parrent_app_metadata,
            "apps": apps_metadata,
            "status": report_statuses,
            "processing_status": uploader_statuses,
            "last_update_date": uploader_statuses,
        }

        return metadata

    def _get_component_by_id(self, component_id: str):
        assert self.components is not None

        for comp in self.components:
            if comp.component_id == component_id:
                return comp

        raise Exception(
            f"Component '{component_id}' not found on given report components"
        )  # pragma no cover

    def _attach_all(self):
        if not self.components:
            return
        for component in self.components:
            self.attach(component.component_id)

    def _get_report_components_metadata(self):
        if not self.report_components:
            self._attach_all()
        return [comp.get_metadata() for _, comp in self.report_components.items()]
