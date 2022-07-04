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
class FileContentResponse:
    status: str
    message: str
    validation: Tuple[NameValidationResponse]
    event_id: str

    def dict(self):
        return asdict(self)



# {
#   "tenant_id": "2b6d08d0-6e15-4011-b30b-162adf25ee6a",
#   "status": "failed",
#   "message": "Not all files are valid",
#   "validation": [
#     {
#       "status": "failed",
#       "filename": "No valid filenames",
#       "filepath": "File not saved",
#       "message": null
#     }
#   ],
#   "event_id": "baa7cff1-d374-482e-8c02-86660476a46e"
# }


# {
#   "status": "failed",
#   "message": "Monthly quota exceeded",
#   "monthly_quota": 1,
#   "monthly_quota_consumed": 1,
#   "quota_reset_date": "2022-08-03T07:23:52.492894",
#   "event_id": "684df86d-c507-46db-81b0-cfcf5986b6d2"
# }