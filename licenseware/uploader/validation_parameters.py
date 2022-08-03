from dataclasses import asdict, dataclass
from typing import Tuple


@dataclass
class UploaderValidationParameters:
    required_input_type: str = None
    filename_contains: Tuple[str] = None
    filename_endswith: Tuple[str] = None
    required_sheets: Tuple[str] = None
    required_columns: Tuple[str] = None
    min_rows_number: int = 0
    header_starts_at: int = 0
    text_contains_all: Tuple[str] = None
    text_contains_any: Tuple[str] = None
    ignore_filenames: Tuple[str] = None
    buffer: int = 15000
    filename_valid_message: str = "File is valid"
    filename_ignored_message: str = "File is ignored"
    regex_escape: bool = True
    ignored_by_uup: bool = False

    def dict(self):
        return asdict(self)  # pragma: no cover
