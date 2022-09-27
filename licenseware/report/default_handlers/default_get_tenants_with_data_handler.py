from licenseware.config.config import Collections
from licenseware.repository.mongo_repository.mongo_repository import MongoRepository


def _get_repo(db_connection):

    repo = MongoRepository(
        db_connection,
        collection=Collections.DATA,
        data_validator="ignore",
    )

    return repo


def _get_pipeline(tenant_id: str):

    pipeline = [
        {
            "$group": {
                "_id": {"tenant_id": "$tenant_id"},
                "updated_at": {"$max": "$updated_at"},
            }
        },
        {
            "$project": {
                "_id": 0,
                "tenant_id": "$_id.tenant_id",
                "updated_at": "$updated_at",
            }
        },
    ]

    if tenant_id is not None:
        pipeline.insert(0, {"$match": {"tenant_id": tenant_id}})

    return pipeline


def default_get_tenants_with_data_handler(db_connection, tenant_id: str = None):

    repo = _get_repo(db_connection)
    pipeline = _get_pipeline(tenant_id)

    last_update_dates = repo.execute_query(pipeline)

    if last_update_dates == [{"tenant_id": None, "updated_at": None}]:
        last_update_dates = []

    return last_update_dates
