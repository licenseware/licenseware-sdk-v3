import uuid
import string
import random
from datetime import datetime
from bson.objectid import ObjectId
from .report import NewReport, NewReportComponent
from licenseware.repository.mongo_repository.mongo_repository import MongoRepository
from typing import List
from licenseware.utils.mongo_query_from_filters import get_mongo_query_from_filters
from licenseware.utils.mongo_limit_skip_filters import (
    insert_mongo_limit_skip_filters,
)


def shortid(length=6):
    # Not colision prof
    # but enough when combined with tenant_id
    return "".join(random.choices(string.digits + string.ascii_uppercase, k=length))


class ReportSnapshot:
    def __init__(
        self,
        tenant_id: str,
        authorization: str,
        report: NewReport,
        version: str,
        filters: List[dict],
        payload: List[dict],
        limit: int,
        skip: int,
        repo: MongoRepository,
    ):
        self.report = report
        self.filters = filters
        self.authorization = authorization
        self.limit = limit
        self.skip = skip
        self.payload = payload
        self.tenant_id = tenant_id
        self.report_id = self.report.report_id
        self.report_uuid = str(uuid.uuid4())
        self.version = version or shortid()
        self.snapshot_date = datetime.utcnow().isoformat()
        self.repo = repo

    def get_snapshot_version(self):
        snapshot = self.generate_snapshot()
        return f"Created snapshot version `{snapshot['version']}`"

    def get_available_versions(self):

        pipeline = [
            {"$match": {"tenant_id": self.tenant_id, "report_id": self.report_id}},
            {"$group": {"_id": 0, "versions": {"$addToSet": "$version"}}},
            {"$project": {"_id": 0, "versions": "$versions"}},
        ]
        results = self.repo.execute_query(pipeline)
        return results[0] if len(results) == 1 else results

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

    def get_snapshot_component(self):

        match_filters = get_mongo_query_from_filters(self.filters)

        pipeline = [
            {
                "$match": {
                    **match_filters,
                    **{
                        "tenant_id": self.tenant_id,
                        "report_id": self.report_id,
                        "component_id": self.request.args.get("component_id"),
                        "version": self.version,
                        "for_report_uuid": {"$exists": True},
                    },
                }
            },
        ]

        pipeline = insert_mongo_limit_skip_filters(self.skip, self.limit, pipeline)
        results = self.repo.execute_query(pipeline)
        return results

    def update_snapshot(self):

        updated_doc = self.repo.update_one(
            filters={
                "_id": self.payload["_id"],
                "tenant_id": self.tenant_id,
            },
            data=self.payload["new_data"],
        )

        if updated_doc:
            return self.payload["new_data"]

        raise Exception("Didn't found any match on field `_id` on this `tenant_id`")

    def _id_belongs_to_report(self, _id: str):

        results = self.repo.count(
            filters={
                "_id": _id,
                "tenant_id": self.tenant_id,
                "report_uuid": {"$exists": True},
            }
        )

        return bool(results)

    def _delete_by_ids(self):

        ids_to_delete = []
        for d in self.payload:
            if not d.get("_id"):
                continue
            # we can't delete report metadata and leave it's components hanging
            if self._id_belongs_to_report(d["_id"]):
                continue
            ids_to_delete.append(ObjectId(d["_id"]))

        deleted_docs = self.repo.delete_one(
            filters={
                "_id": {"$in": ids_to_delete},
                "tenant_id": self.tenant_id,
            }
        )

        return deleted_docs

    def _delete_by_versions(self):

        versions_to_delete = []
        for d in self.payload:
            if not d.get("version"):
                continue
            versions_to_delete.append(d["version"])

        deleted_docs = self.repo.delete_one(
            filters={
                "version": {"$in": versions_to_delete},
                "tenant_id": self.tenant_id,
            }
        )

        return deleted_docs

    def _delete_by_component_uuids(self):

        component_uuids_to_delete = []
        for d in self.payload:
            if not d.get("component_uuid"):
                continue
            component_uuids_to_delete.append(d["component_uuid"])

        deleted_docs = self.repo.delete_one(
            filters={
                "component_uuid": {"$in": component_uuids_to_delete},
                "tenant_id": self.tenant_id,
            }
        )

        return deleted_docs

    def _delete_by_report_uuids(self):

        report_uuids_to_delete = []
        for d in self.payload:
            if not d.get("report_uuid"):
                continue
            report_uuids_to_delete.append(d["report_uuid"])

        d1 = self.repo.delete_one(
            filters={
                "report_uuid": {"$in": report_uuids_to_delete},
                "tenant_id": self.tenant_id,
            }
        )

        d2 = self.repo.delete_one(
            filters={
                "for_report_uuid": {"$in": report_uuids_to_delete},
                "tenant_id": self.tenant_id,
            }
        )

        deleted_docs = d1 + d2

        return deleted_docs

    def delete_snapshot(self):

        self._delete_by_ids()
        self._delete_by_versions()
        self._delete_by_component_uuids()
        self._delete_by_report_uuids()

        return "Requested items were deleted"

    def insert_report_metadata(self):

        report_metadata, _ = self.report.metadata["data"]
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

        comp_payload = comp.metadata["data"]
        query_params = f"?version={self.version}&component_id={comp.component_id}"
        comp_payload["snapshot_url"] = self.report.snapshot_url + query_params

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
            self.repo,
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

    def generate_snapshot(self):

        report_metadata = self.insert_report_metadata()

        inserted_components = set()
        for comp in self.report.components:

            if comp.component_id in inserted_components:
                continue

            self.update_report_component_metadata(comp)
            self.insert_component_data(comp, report_metadata)

            if comp.component_id not in inserted_components:
                inserted_components.add(comp.component_id)

        return {"version": self.version}
