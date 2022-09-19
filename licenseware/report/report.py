import datetime
import time
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

        apps_metadata = self._get_connected_apps_metadata(parrent_app_metadata)
        uploader_statuses = self._get_tenant_uploader_statuses(uploaders_metadata)
        report_statuses = self._get_tenant_report_statuses(uploader_statuses)

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
            "report_components": self.report_components_metadata,
            "public_url": self.public_url,
            "snapshot_url": self.snapshot_url,
            "status": report_statuses,
            "processing_status": uploader_statuses,
            "last_update_date": uploader_statuses,
            "parrent_app": parrent_app_metadata,
            "apps": apps_metadata,
            "filters": self.filters,
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

    def _get_app_metadata(self, app_id: str):
        try:
            auth_headers = {"auth_jwt": self.config.machine_token}
            response = requests.get(
                self.config.REGISTRY_SERVICE_APPS_URL,
                params={"app_id": app_id},
                headers=auth_headers,
            )
            if response.status_code != 200:
                log.warning(response.content)
                return None

            assert isinstance(response.json(), list)
            assert len(response.json()) == 1

            return response.json()
        except Exception as err:
            log.warning(err)
            return None

    def _get_connected_apps_metadata(self, parrent_app_metadata: dict):

        conn_apps_metadata = []
        if parrent_app_metadata:
            conn_apps_metadata = [parrent_app_metadata]

        if self.connected_apps is None:
            return conn_apps_metadata

        for app_id in self.connected_apps:
            if parrent_app_metadata:
                if parrent_app_metadata["app_id"] in app_id:
                    continue  # already got parrent app metadata

            app_metadata = self._get_app_metadata(app_id)
            if app_metadata is None:
                log.error(
                    f"Can't get connected app metadata for app id: {app_id}... Retrying..."
                )
                time.sleep(5)
                self._get_connected_apps_metadata(parrent_app_metadata)
            else:
                # Not sure why `app_metadata` sometimes keeps coming None here
                # Even if is checked for None...
                conn_apps_metadata.extend(app_metadata)

        log.success("Got conected apps metadata from registry service successfully")
        return conn_apps_metadata

    def _get_tenant_uploader_statuses(self, uploaders_metadata: List[dict]):

        if not uploaders_metadata:
            return self._get_tenant_uploader_statuses_from_cache()

        results = []
        for uploader in uploaders_metadata:
            results.extend(uploader["status"])

        return results

    def _get_tenant_uploader_statuses_from_cache(self):
        redisdb = RedisCache(self.config)
        results = redisdb.get(get_uploader_status_key(None, self.app_id, None))
        return results

    def _get_tenant_report_statuses(self, uploader_statuses):
        report_status = lambda r: {
            "status": States.DISABLED
            if r["status"] == States.RUNNING
            else States.ENABLED
        }
        report_statuses = [{**r, **report_status(r)} for r in uploader_statuses]
        return report_statuses
