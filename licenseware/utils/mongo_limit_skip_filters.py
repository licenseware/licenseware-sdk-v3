from typing import List


def insert_mongo_limit_skip_filters(skip: int, limit: int, pipeline: List[dict]):

    if not isinstance(skip, int):
        return pipeline

    if not isinstance(limit, int):
        return pipeline

    if skip < 0:  # pragma no cover
        return pipeline

    if limit <= 0:
        return pipeline

    pipeline = pipeline + [{"$skip": skip}]
    pipeline = pipeline + [{"$limit": limit}]

    return pipeline
