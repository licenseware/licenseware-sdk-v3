import sys
import time
from typing import List
from licenseware.constants.alias_types import AppId
from licenseware.utils.logger import log
from licenseware.config.config import Config
from licenseware.utils.get_registry_metadata import get_registry_metadata
from licenseware.constants.states import States


class DefaultMetadataHandler:
    def __init__(
        self,
        connected_apps: List[AppId],
        config: Config,
    ):
        self.config = config
        self.connected_apps = connected_apps
        self.metadata_handler = {
            "uploader": self._get_connected_uploader_metadata,
            "app": self._get_connected_app_metadata,
        }

    def _get_connected_uploader_metadata(self, app_id: str):
        return get_registry_metadata(
            url=self.config.REGISTRY_SERVICE_UPLOADERS_URL,
            headers=self.config.get_machine_headers(),
            app_id=app_id,
        )

    def _get_connected_app_metadata(self, app_id: str):
        return get_registry_metadata(
            url=self.config.REGISTRY_SERVICE_APPS_URL,
            headers=self.config.get_machine_headers(),
            app_id=app_id,
        )

    def get_connected_apps_metadata(self, parrent_app_metadata: dict):
        return self._get_connected_metadata("app", parrent_app_metadata)

    def get_connected_uploaders_metadata(self, uploaders_metadata: dict = None):
        return self._get_connected_metadata("uploader", uploaders_metadata)

    def extract_uploader_statuses(self, uploaders_metadata: List[dict]):
        statuses = []
        for um in uploaders_metadata:
            statuses.extend(um["status"])
        return statuses

    def extract_report_statuses(
        self,
        uploader_statuses: List[dict],
        tenants_with_data: List[dict],
    ):
        report_statuses = []
        for ustatus in uploader_statuses:
            for twd in tenants_with_data:
                if ustatus["tenant_id"] != twd["tenant_id"]:
                    continue

                rstatus = {
                    **ustatus,
                    "status": States.ENABLED
                    if ustatus["status"] == States.IDLE
                    else States.DISABLED,
                }
                report_statuses.append(rstatus)

        return report_statuses

    def _get_connected_metadata(self, name: str, given_metadata: dict = None):

        conn_metadata = []
        if given_metadata:
            conn_metadata = [given_metadata]

        if len(self.connected_apps) == 1:
            return conn_metadata

        for app_id in self.connected_apps:
            if given_metadata:
                if given_metadata["app_id"] == app_id:
                    continue  # already got parrent app metadata

            metadata = self.metadata_handler[name](app_id)
            if metadata is None:
                try:
                    if _retry_in > 120:
                        _retry_in = 0
                    _retry_in = _retry_in + 5
                    log.error(
                        f"Can't get connected {name} metadata for app id: {app_id}... Retrying in {_retry_in} seconds..."
                    )
                    time.sleep(_retry_in)
                    self.get_connected_entities_metadata(given_metadata, _retry_in)
                except KeyboardInterrupt:
                    log.info(f"Stopping getting connected {name}s metadata")
                    sys.exit(0)
            else:
                # Not sure why `app_metadata` sometimes keeps coming None here
                # Even if is checked for None...
                conn_metadata.extend(metadata)

        log.success(f"Got conected {name}s metadata from registry service successfully")
        return conn_metadata
