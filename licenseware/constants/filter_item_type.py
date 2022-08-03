from dataclasses import dataclass
from typing import List

from licenseware.constants.allowed_filters import AllowedFilters
from licenseware.constants.column_types import ColumnTypes


@dataclass
class FilterItemType:
    column: str
    allowed_filters: List[AllowedFilters]
    column_type: ColumnTypes
    allowed_values: List[str]
    visible_name: str
