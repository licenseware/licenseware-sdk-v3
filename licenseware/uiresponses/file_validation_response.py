from typing import Tuple
from dataclasses import dataclass, asdict


@dataclass
class ValidationResponse:
    status: str
    filename: str
    message: str

    def dict(self):
        return asdict(self)


@dataclass
class FileValidationResponse:
    status: str
    message: str
    validation: Tuple[ValidationResponse]
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