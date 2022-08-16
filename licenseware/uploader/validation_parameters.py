from dataclasses import asdict, dataclass
from typing import List


@dataclass
class UploaderValidationParameters:
    required_input_type: str = None
    filename_contains: List[str] = None
    filename_endswith: List[str] = None
    required_sheets: List[str] = None
    required_columns: List[str] = None
    min_rows_number: int = 0
    header_starts_at: int = 0
    text_contains_all: List[str] = None
    text_contains_any: List[str] = None
    ignore_filenames: List[str] = None
    buffer: int = 15000
    filename_valid_message: str = "File is valid"
    filename_ignored_message: str = "File is ignored"
    regex_escape: bool = True
    ignored_by_uup: bool = False

    def dict(self):
        return asdict(self)  # pragma: no cover
