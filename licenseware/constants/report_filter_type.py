from typing import List
from dataclasses import dataclass
from .allowed_filters import AllowedFilters
from .column_types import ColumnTypes
from .filter_item_type import FilterItemType


@dataclass
class ReportFilterType:
    TYPE: ColumnTypes
    FILTER: AllowedFilters
    metadata: List[FilterItemType]
    
