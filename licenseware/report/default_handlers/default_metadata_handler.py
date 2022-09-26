import time
from typing import List

from licenseware.config.config import Config
from licenseware.constants.alias_types import AppId
from licenseware.constants.states import States
from licenseware.utils.get_registry_metadata import get_registry_metadata
from licenseware.utils.logger import log


class DefaultMetadataHandler:
    def __init__(
        self,
        connected_apps: List[AppId],
        config: Config,
    ):
        self.config = config
        self.connected_apps = connected_apps

    def _get_connected_uploader_metadata(self, app_id: str):
        try:
            metadata = get_registry_metadata(
                url=self.config.REGISTRY_SERVICE_UPLOADERS_URL,
                headers=self.config.get_machine_headers(),
                app_id=app_id,
            )
            assert metadata is not None
            assert isinstance(metadata, list)
            assert len(metadata) > 0
            return metadata
        except Exception as err:
            log.error(err)
            return None

    def _get_connected_app_metadata(self, app_id: str):
        try:
            metadata = get_registry_metadata(
                url=self.config.REGISTRY_SERVICE_APPS_URL,
                headers=self.config.get_machine_headers(),
                app_id=app_id,
            )
            assert metadata is not None
            assert isinstance(metadata, list)
            assert len(metadata) > 0
            return metadata
        except Exception as err:
            log.error(err)
            return None

    def get_connected_apps_metadata(
        self, parrent_app_metadata: dict, _retry_in: int = 0
    ):
        if len(self.connected_apps) == 1 and parrent_app_metadata is not None:
            return [parrent_app_metadata]

        connected_apps_metadata = []
        for idx, app_id in enumerate(self.connected_apps):

            if idx == 0 and parrent_app_metadata is not None:
                continue

            metadata = self._get_connected_app_metadata(app_id)

            if metadata is None:
                if _retry_in > 120:
                    _retry_in = 0
                _retry_in = _retry_in + 5
                log.error(
                    f"Can't get connected app metadata for app id: {app_id}... Retrying in {_retry_in} seconds..."
                )
                time.sleep(_retry_in)
                self.get_connected_apps_metadata(parrent_app_metadata, _retry_in)
            else:
                connected_apps_metadata.extend(metadata)

        log.success(f"Succesfully got apps metadata for {self.connected_apps}")
        return connected_apps_metadata

    def get_connected_uploaders_metadata(
        self, uploaders_metadata: List[dict], _retry_in: int = 0
    ):

        connected_uploaders_metadata = []
        if len(self.connected_apps) == 1 and uploaders_metadata is not None:
            return uploaders_metadata

        if uploaders_metadata is not None:
            connected_uploaders_metadata.extend(uploaders_metadata)

        for idx, app_id in enumerate(self.connected_apps):

            if idx == 0 and uploaders_metadata is not None:
                continue

            metadata = self._get_connected_uploader_metadata(app_id)

            if metadata is None:
                if _retry_in > 120:
                    _retry_in = 0
                _retry_in = _retry_in + 5
                log.error(
                    f"Can't get connected uploaders metadata for app id: {app_id}... Retrying in {_retry_in} seconds..."
                )
                time.sleep(_retry_in)
                self.get_connected_apps_metadata(uploaders_metadata, _retry_in)
            else:
                connected_uploaders_metadata.extend(metadata)

        log.success(f"Succesfully got uploaders metadata for {self.connected_apps}")
        return connected_uploaders_metadata

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
