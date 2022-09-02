from licenseware.repository.mongo_repository.mongo_repository import MongoRepository


class CrudHandler:
    def get(
        self,
        tenant_id: str,
        authorization: str,
        id: str,
        foreign_key: str,
        distinct_key: str,
        limit: int,
        skip: int,
        repo: MongoRepository,
    ):

        if id is not None:
            return repo.find_one(filters={"_id": id, "tenant_id": tenant_id})

        if foreign_key is not None:
            raise Exception(
                "Please overwrite 'CrudHandler.get' method to handle 'foreign_key' query param"
            )

        if distinct_key is not None:
            return repo.distinct(distinct_key, filters={"tenant_id": tenant_id})

        return repo.find_many(filters={"tenant_id": tenant_id}, limit=limit, skip=skip)

    def put(
        self,
        tenant_id: str,
        authorization: str,
        id: str,
        new_data: dict,
        repo: MongoRepository,
    ):
        new_data.pop("_id", None)
        return repo.update_one(
            filters={"_id": id, "tenant_id": tenant_id}, data=new_data, upsert=False
        )

    def delete(
        self,
        tenant_id: str,
        authorization: str,
        id: str,
        repo: MongoRepository,
    ):
        return repo.delete_one(filters={"_id": id, "tenant_id": tenant_id})
