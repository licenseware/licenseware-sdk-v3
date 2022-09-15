import datetime
from dataclasses import dataclass
from typing import Dict, List

from licenseware.config.config import Config
from licenseware.constants.states import States
from licenseware.dependencies import requests
from licenseware.exceptions.custom_exceptions import ErrorAlreadyAttached
from licenseware.redis_cache.redis_cache import RedisCache
from licenseware.uploader.default_handlers.helpers import get_uploader_status_key
from licenseware.utils.alter_string import get_altered_strings
from licenseware.utils.logger import log

from .report_component import NewReportComponent
from .report_filter import ReportFilter


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

    def get_metadata(self):

        if not self.registrable:
            return

        stats = self._get_statuses_and_apps_metadata()

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
            "report_components": self._get_report_components_metadata(),
            "public_url": self.public_url,
            "snapshot_url": self.snapshot_url,
            "status": stats.report_statuses,
            "processing_status": stats.uploader_statuses,
            "last_update_date": stats.uploader_statuses,
            "parrent_app": stats.parrent_app_metadata,
            "apps": stats.apps,
            "filters": self.filters,
        }

        return metadata

    def _get_statuses_and_apps_metadata(self):
        class StatsAndMeta:
            parrent_app_metadata = None
            uploader_statuses = None
            report_statuses = None
            apps = None

        if self._parrent_app is not None:
            StatsAndMeta.parrent_app_metadata = self._parrent_app.get_metadata()
            StatsAndMeta.uploader_statuses = self._get_tenant_uploader_statuses(
                self._parrent_app.app_id
            )
            StatsAndMeta.report_statuses = self._get_tenant_report_statuses(
                StatsAndMeta.uploader_statuses
            )
            StatsAndMeta.apps = self._get_connected_apps_metadata(
                StatsAndMeta.parrent_app_metadata
            )

        return StatsAndMeta

    def _get_tenant_uploader_statuses(self, app_id: str):
        redisdb = RedisCache(self.config)
        results = redisdb.get(get_uploader_status_key(None, app_id, None))
        return results

    def _get_tenant_report_statuses(self, uploader_statuses):
        report_status = lambda r: {
            "status": States.DISABLED
            if r["status"] == States.RUNNING
            else States.ENABLED
        }
        report_statuses = [{**r, **report_status(r)} for r in uploader_statuses]
        return report_statuses

    def _get_connected_apps_metadata(self, parrent_app_metadata: dict):

        connected_apps_metadata = [parrent_app_metadata]

        if self.connected_apps is None:
            return connected_apps_metadata

        for urlorpath in self.connected_apps:
            if not urlorpath.startswith("http"):
                urlorpath = self.config.BASE_URL + "/" + urlorpath

            response = requests.get(urlorpath, headers=self.config.machine_auth_headers)
            if response.status_code != 200:
                log.error(response.content)
                raise Exception(
                    f"Can't get connected app metadata from url {urlorpath}"
                )
            connected_apps_metadata.append(response.json())

        return connected_apps_metadata

    def _attach_all(self):
        if not self.components:
            return
        for component in self.components:
            self.attach(component.component_id)

    def _get_report_components_metadata(self):
        if not self.report_components:
            self._attach_all()
        return [comp.get_metadata() for _, comp in self.report_components.items()]
