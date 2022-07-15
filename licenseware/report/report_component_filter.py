from typing import Tuple
from dataclasses import dataclass, asdict
from licenseware.utils.alter_string import get_altered_strings


@dataclass
class RCFilter:
    """
        Filter sample
        {
            "column": "result",
            "allowed_filters": ["equals", "contains", "in_list"],
            "visible_name": "Result",
            "column_type": "string",
            "allowed_values": ["Verify", "Used", "Licensable", "Restricted"],
        }
    """
    column: str 
    allowed_filters: Tuple[str]
    column_type: str = "string"  
    visible_name: str = None
    allowed_values: Tuple[str] = None

    def __post_init__(self):
        if self.visible_name is None:
            strver = get_altered_strings(self.column)
            self.visible_name = strver.title

    def dict(self):
        return asdict(self)
