from typing import List

from licenseware.constants.filter_item_type import FilterUI

condition_switcher = {
    "equals": lambda column, filter_value: {column: filter_value},
    "contains": lambda column, filter_value: {column: {"$regex": filter_value}},
    "in_list": lambda column, filter_value: {
        "$expr": {"$in": [f"${column}", filter_value]}
    },
    "greater_than": lambda column, filter_value: {column: {"$gt": filter_value}},
    "greater_or_equal_to": lambda column, filter_value: {
        column: {"$gte": filter_value}
    },
    "less_than": lambda column, filter_value: {column: {"$lt": filter_value}},
    "less_or_equal_to": lambda column, filter_value: {column: {"$lte": filter_value}},
}


def get_mongo_query_from_filters(filter_payload: List[FilterUI]) -> dict:

    if filter_payload is None:
        return {}

    parsed_filter = {}
    for filter_section in filter_payload:
        parsed_filter.update(
            condition_switcher[filter_section.filter_type](
                filter_section.column, filter_section.filter_value
            )
        )

    return parsed_filter
