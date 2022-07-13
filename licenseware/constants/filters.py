from .base_types import BaseTypes


class Filters(BaseTypes):
    EQUALS = "equals"
    CONTAINS = "contains"
    IN_LIST = "in_list"
    GREATER_THAN = "greater_than"
    GREATER_THAN_OR_EQUAL_TO = "greater_or_equal_to"
    LESS_THAN = "less_than"
    LESS_THAN_OR_EQUAL_TO = "less_or_equal_to"
    