from enum import Enum
from typing import Any, Dict, List

from licenseware.config.config import Config
from licenseware.constants.web_response import WebResponse
from licenseware.report.report_component import NewReportComponent
from licenseware.report.report_public_token import ReportPublicToken
from licenseware.report.report_snapshot import ReportSnapshot
from licenseware.repository.mongo_repository.mongo_repository import MongoRepository
from licenseware.utils.alter_string import get_altered_strings
from licenseware.utils.create_file import create_file
from licenseware.utils.failsafe_decorator import failsafe


class RegisteredComponents:  # pragma no cover
    """
    This class acts as a proxy between the web framework and the implementation
    """

    def __init__(self, components: List[NewReportComponent], config: Config) -> None:
        self.config = config
        self.components = components
        self.components_enum = Enum(
            "ReportComponentsEnum",
            {
                u.component_id: get_altered_strings(u.component_id).dash
                for u in self.components
            },
        )
        self.component_dispacher: Dict[str, NewReportComponent] = {
            u.component_id: u for u in components
        }

    def _get_current_component(self, component_id: Enum):
        component_id = str(component_id).replace("ReportComponentsEnum.", "")
        return self.component_dispacher[component_id]

    @failsafe
    def get_component_data(
        self,
        tenant_id: str,
        authorization: str,
        db_connection: Any,
        component_id: str,
        filters: dict,
        limit: int,
        skip: int,
    ):
        repo = self._get_data_repo(db_connection)
        component = self._get_current_component(component_id)

        return component.get_component_data_handler(
            tenant_id, authorization, repo, filters, limit, skip
        )

    @failsafe
    def get_public_component_data(
        self,
        token: str,
        db_connection: Any,
        component_id: str,
        filters: dict,
        limit: int,
        skip: int,
    ):
        repo = self._get_data_repo(db_connection)
        component = self._get_current_component(component_id)
        data = ReportPublicToken(config=self.config).get_token_data(token)
        return component.get_component_data_handler(
            data["tenant_id"],
            self.config.get_machine_token(),
            repo,
            filters,
            limit,
            skip,
        )

    @failsafe
    def get_snapshot_component_data(
        self,
        tenant_id: str,
        authorization: str,
        db_connection: Any,
        component_id: str,
        version: str,
        filters: dict,
        limit: int,
        skip: int,
    ):
        component = self._get_current_component(component_id)
        repo = self._get_snapshot_repo(db_connection)
        rpt = ReportSnapshot(
            tenant_id,
            authorization,
            repo,
            self.config,
            version,
            None,
            filters,
            None,
            limit,
            skip,
        )
        result = rpt.get_snapshot_component(component.component_id)
        return WebResponse(status_code=200, content=result)

    @failsafe
    def download_component(
        self,
        tenant_id: str,
        authorization: str,
        db_connection: Any,
        component_id: str,
        filetype: str,
    ):

        repo = self._get_data_repo(db_connection)
        component = self._get_current_component(component_id)

        result = component.get_component_data_handler(
            tenant_id, authorization, repo, None, 0, 0
        )
        if result.status_code != 200:
            return result

        filepath, filename = create_file(
            tenant_id,
            filename=component.component_id,
            filetype=filetype,
            data=result.content,
            config=self.config,
        )

        result = WebResponse(
            status_code=200, content={"filepath": filepath, "filename": filename}
        )

        return result

    @failsafe
    def download_snapshot_component(
        self,
        tenant_id: str,
        authorization: str,
        db_connection: Any,
        component_id: str,
        version: str,
        filetype: str,
    ):

        repo = self._get_snapshot_repo(db_connection)
        component = self._get_current_component(component_id)

        rpt = ReportSnapshot(tenant_id, authorization, repo, self.config, version)
        result = rpt.get_snapshot_component(component.component_id)

        filepath, filename = create_file(
            tenant_id,
            filename=component.component_id,
            filetype=filetype,
            data=result,
            config=self.config,
        )

        result = WebResponse(
            status_code=200, content={"filepath": filepath, "filename": filename}
        )

        return result

    # PRIVATE

    def _get_data_repo(self, db_connection: Any):
        return MongoRepository(
            db_connection,
            collection=self.config.MONGO_COLLECTION.DATA,
            data_validator="ignore",
        )

    def _get_snapshot_repo(self, db_connection: Any):
        return MongoRepository(
            db_connection,
            collection=self.config.MONGO_COLLECTION.REPORT_SNAPSHOTS,
            data_validator="ignore",
        )
