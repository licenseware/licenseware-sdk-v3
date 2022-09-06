from enum import Enum
from typing import Any, Dict, List

from licenseware.config.config import Config
from licenseware.constants.web_response import WebResponse
from licenseware.report.report import NewReport
from licenseware.report.report_public_token import ReportPublicToken
from licenseware.report.report_snapshot import ReportSnapshot
from licenseware.repository.mongo_repository.mongo_repository import MongoRepository
from licenseware.utils.alter_string import get_altered_strings
from licenseware.utils.create_xlsx_file import create_xlsx_file
from licenseware.utils.failsafe_decorator import failsafe


class RegisteredReports:  # pragma no cover
    """
    This class acts as a proxy between the web framework and the implementation
    """

    def __init__(self, reports: List[NewReport], config: Config) -> None:
        self.config = config
        self.reports = reports
        self.report_enum = Enum(
            "ReportEnum",
            {u.report_id: get_altered_strings(u.report_id).dash for u in self.reports},
        )
        self.report_dispacher: Dict[str, NewReport] = {u.report_id: u for u in reports}

    @failsafe
    def get_report_metadata(self, report_id: str):
        report = self._get_current_report(report_id)
        return report.metadata["data"][0]

    @failsafe
    def get_public_report_metadata(self, token: str, report_id: str):
        report = self._get_current_report(report_id)
        return report.metadata["data"][0]

    @failsafe
    def download_report(
        self, tenant_id: str, authorization: str, db_connection: Any, report_id: str
    ):
        repo = self._get_data_repo(db_connection)
        report = self._get_current_report(report_id)

        all_component_data = {}
        for comp in report.components:
            response = comp.get_component_data_handler(
                tenant_id, authorization, repo, None, None, None
            )
            all_component_data[comp.component_id] = response.content

        filepath, filename = create_xlsx_file(
            tenant_id, report.report_id, data=all_component_data, config=self.config
        )

        result = WebResponse(
            status_code=200, content={"filepath": filepath, "filename": filename}
        )
        return result

    @failsafe
    def create_public_report(
        self,
        tenant_id: str,
        authorization: str,
        db_connection: Any,
        report_id: str,
        expire,
    ):
        report = self._get_current_report(report_id)
        rpt = ReportPublicToken(tenant_id, authorization, report.report_id, self.config)
        token = rpt.get_token(expire)
        return WebResponse(status_code=200, content=token)

    @failsafe
    def delete_public_report(
        self,
        tenant_id: str,
        authorization: str,
        db_connection: Any,
        report_id: str,
        token: str,
    ):
        report = self._get_current_report(report_id)
        rpt = ReportPublicToken(tenant_id, authorization, report.report_id, self.config)
        token = rpt.delete_token(token)
        return WebResponse(status_code=200, content=token)

    @failsafe
    def create_snapshot_report(
        self,
        tenant_id: str,
        authorization: str,
        db_connection: Any,
        report_id: str,
    ):
        report = self._get_current_report(report_id)
        repo = self._get_snapshot_repo(db_connection)
        rpt = ReportSnapshot(
            tenant_id=tenant_id,
            authorization=authorization,
            repo=repo,
            config=self.config,
            report=report,
        )
        result = rpt.generate_snapshot()
        return WebResponse(status_code=200, content=result)

    @failsafe
    def get_snapshot_report_versions(
        self,
        tenant_id: str,
        authorization: str,
        db_connection: Any,
        report_id: str,
    ):
        report = self._get_current_report(report_id)
        repo = self._get_snapshot_repo(db_connection)
        rpt = ReportSnapshot(
            tenant_id=tenant_id,
            authorization=authorization,
            repo=repo,
            config=self.config,
            report=report,
        )
        result = rpt.get_available_versions()
        return WebResponse(status_code=200, content=result)

    @failsafe
    def get_snapshot_report_metadata(
        self,
        tenant_id: str,
        authorization: str,
        db_connection: Any,
        report_id: str,
        version: str,
    ):
        report = self._get_current_report(report_id)
        repo = self._get_snapshot_repo(db_connection)
        rpt = ReportSnapshot(
            tenant_id=tenant_id,
            authorization=authorization,
            repo=repo,
            config=self.config,
            version=version,
            report=report,
        )
        result = rpt.get_snapshot_metadata()
        return WebResponse(status_code=200, content=result)

    @failsafe
    def delete_snapshot_report(
        self,
        tenant_id: str,
        authorization: str,
        db_connection: Any,
        report_id: str,
        version: str,
    ):
        report = self._get_current_report(report_id)
        repo = self._get_snapshot_repo(db_connection)
        rpt = ReportSnapshot(
            tenant_id=tenant_id,
            authorization=authorization,
            repo=repo,
            config=self.config,
            version=version,
            report=report,
        )
        result = rpt.delete_snapshot()
        return WebResponse(status_code=200, content=result)

    # PRIVATE

    def _get_current_report(self, report_id: Enum):
        report_id = str(report_id).replace("ReportEnum.", "")
        return self.report_dispacher[report_id]

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
