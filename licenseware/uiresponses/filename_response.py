from typing import Tuple
from dataclasses import dataclass, asdict


@dataclass
class NameValidationResponse:
    status: str
    filename: str
    message: str

    def dict(self):
        return asdict(self)


@dataclass
class FileNameResponse:
    status: str
    message: str
    validation: Tuple[NameValidationResponse]
    event_id: str

    def dict(self):
        return asdict(self)


# {
#   "status": "success",
#   "message": "Filenames are valid",
#   "validation": [
#     {
#       "status": "failed",
#       "filename": "cpuq",
#       "message": "Filename doesn't end with any of the specified values: .txt"
#     }
#   ],
#   "event_id": "26f5b1d6-0978-4a9c-a2c4-1d8365d39f1b"
# }