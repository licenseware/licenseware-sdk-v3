import pytest

from licenseware import insert_mongo_limit_skip_filters

# pytest -s -v tests/test_insert_mongo_limit_skip_filters.py


def test_insert_mongo_limit_skip_filters():

    pipeline = [
        {"$match": {"tenant_id": "tenant_id"}},
        {
            "$project": {
                "_id": 0,
                "device_name": "$name",
                "operating_system_caption": 1,
            }
        },
    ]

    pipeline_limit_skip = insert_mongo_limit_skip_filters(
        skip=0, limit=20, pipeline=pipeline
    )

    assert len(pipeline_limit_skip) == 4
    assert pipeline_limit_skip[-1] == {"$limit": 20}
    assert pipeline_limit_skip[-2] == {"$skip": 0}

    pipeline_no_limit_skip_None = insert_mongo_limit_skip_filters(
        skip=None, limit=None, pipeline=pipeline
    )

    assert len(pipeline_no_limit_skip_None) == 2

    pipeline_no_limit_skip_0 = insert_mongo_limit_skip_filters(
        skip=0, limit=0, pipeline=pipeline
    )

    assert len(pipeline_no_limit_skip_0) == 2

    pipeline_no_limit_skip_float = insert_mongo_limit_skip_filters(
        skip=0, limit=1.56, pipeline=pipeline
    )

    assert len(pipeline_no_limit_skip_float) == 2
