import pytest
from licenseware import FilterUI, AllowedFilters
from licenseware import get_mongo_query_from_filters


# pytest -s -v tests/test_get_mongo_query_from_filters.py


def test_get_mongo_query_from_filters():

    filter_payload = [
        FilterUI(
            filter_type=AllowedFilters.EQUALS,
            column="tenant_id",
            filter_value="uuid3-id",
        )
    ]

    mongo_filters = get_mongo_query_from_filters(filter_payload)

    assert mongo_filters == {"tenant_id": "uuid3-id"}
