import random
import string
import uuid
from datetime import datetime
from typing import List

from licenseware.config.config import Config
from licenseware.repository.mongo_repository.mongo_repository import MongoRepository
from licenseware.utils.mongo_limit_skip_filters import insert_mongo_limit_skip_filters
from licenseware.utils.mongo_query_from_filters import get_mongo_query_from_filters

from .report import NewReport, NewReportComponent


def shortid(length=6):
    # Not colision prof
    # but enough when combined with tenant_id
    return "".join(random.choices(string.digits + string.ascii_uppercase, k=length))


class ReportSnapshot:
    def __init__(
        self,
        tenant_id: str,
        authorization: str,
        repo: MongoRepository,
        config: Config,
        version: str = None,
        report: NewReport = None,
        filters: List[dict] = None,
        limit: int = 0,
        skip: int = 0,
    ):
        self.report = report
        self.filters = filters
        self.authorization = authorization
        self.limit = limit
        self.skip = skip
        self.config = config
        self.tenant_id = tenant_id
        self.report_id = self.report.report_id if report is not None else None
        self.report_uuid = str(uuid.uuid4())
        self.version = version or shortid()
        self.snapshot_date = datetime.utcnow().isoformat()
        self.repo = repo
        self.data_repo = MongoRepository(
            repo.db_connection, collection=config.MONGO_COLLECTION.DATA
        )

    def generate_snapshot(self):

        if self.report.components is None:  # pragma no cover
            return {
                "version": "Can't generate snapshot no report components available",
            }

        report_metadata = self.insert_report_metadata()

        inserted_components = set()
        for comp in self.report.components:

            if comp.component_id in inserted_components:  # pragma no cover
                continue

            self.update_report_component_metadata(comp)
            self.insert_component_data(comp, report_metadata)

            if comp.component_id not in inserted_components:
                inserted_components.add(comp.component_id)

        return {"version": self.version}

    def get_available_versions(self):

        pipeline = [
            {"$match": {"tenant_id": self.tenant_id, "report_id": self.report_id}},
            {"$group": {"_id": 0, "version": {"$addToSet": "$version"}}},
            {"$project": {"_id": 0, "version": "$version"}},
        ]
        results = self.repo.execute_query(pipeline)
        return results[0] if len(results) == 1 else {"version": []}

    def get_snapshot_metadata(self):

        results = self.repo.find_one(
            filters={
                "tenant_id": self.tenant_id,
                "report_id": self.report_id,
                "version": self.version,
                "report_uuid": {"$exists": True},
            }
        )
        return results

    def get_snapshot_component(self, component_id: str, version: str = None):

        match_filters = get_mongo_query_from_filters(self.filters)

        pipeline = [
            {
                "$match": {
                    **match_filters,
                    **{
                        "tenant_id": self.tenant_id,
                        "component_id": component_id,
                        "version": version or self.version,
                        "for_report_uuid": {"$exists": True},
                    },
                }
            },
        ]

        pipeline = insert_mongo_limit_skip_filters(self.skip, self.limit, pipeline)
        results = self.repo.execute_query(pipeline)
        return results

    def update_component_snapshot(
        self, id: str, version: str, component_id: str, data: dict
    ):

        # non editable fields
        for field in [
            "_id",
            "tenant_id",
            "version",
            "for_report_uuid",
            "report_id",
            "component_uuid",
            "component_id",
            "report_snapshot_date",
        ]:
            data.pop(field, None)

        filters = {
            "_id": id,
            "tenant_id": self.tenant_id,
            "version": version,
            "component_id": component_id,
        }

        print(filters)

        updated_doc = self.repo.update_one(
            filters=filters,
            data=data,
            upsert=False,
        )

        if updated_doc:
            return updated_doc

        raise Exception(f"Provided fields {', '.join(data.keys())} not found")

    def _delete_by_version(self):

        deleted_docs = self.repo.delete_many(
            filters={
                "version": self.version,
                "tenant_id": self.tenant_id,
            }
        )

        return deleted_docs

    def delete_snapshot_version(self):
        self._delete_by_version()
        return {"message": f"Report snapshot version '{self.version}' was deleted"}

    def insert_report_metadata(self):

        report_metadata = self.report.get_metadata()
        report_metadata["report_components"] = []
        report_metadata["tenant_id"] = self.tenant_id
        report_metadata["version"] = self.version
        report_metadata["report_snapshot_date"] = self.snapshot_date
        report_metadata["report_uuid"] = self.report_uuid

        self.repo.insert_one(
            data=report_metadata,
        )

        return report_metadata

    def update_report_component_metadata(self, comp: NewReportComponent):

        comp_payload = comp.get_metadata()
        comp_payload["snapshot_url"] = comp.snapshot_url + f"/{self.version}"

        self.repo.update_one(
            filters={
                "tenant_id": self.tenant_id,
                "report_id": self.report_id,
                "report_uuid": self.report_uuid,
                "version": self.version,
                "report_snapshot_date": self.snapshot_date,
            },
            data={"report_components": [comp_payload]},
            append=True,
        )

    def insert_component_data(self, comp: NewReportComponent, report_metadata):

        component_data = comp.get_component_data_handler(
            self.tenant_id,
            self.authorization,
            self.data_repo,
            self.filters,
            self.limit,
            self.skip,
        ).content

        component_pinned = {
            "for_report_uuid": self.report_uuid,
            "component_uuid": str(uuid.uuid4()),
            "tenant_id": self.tenant_id,
            "report_id": self.report_id,
            "component_id": comp.component_id,
            "report_snapshot_date": report_metadata["report_snapshot_date"],
            "version": report_metadata["version"],
        }

        if isinstance(component_data, list) and len(component_data) > 0:
            component_data = [{**d, **component_pinned} for d in component_data]
            self.repo.insert_many(data=component_data)
        elif isinstance(component_data, dict) and len(component_data) > 0:
            component_data = {**component_data, **component_pinned}
            self.repo.insert_one(data=component_data)
