from typing import Tuple, List
from dataclasses import dataclass, asdict


@dataclass
class ValidationResponse:
    status: str
    filename: str
    message: str

    def dict(self):
        return asdict(self) # pragma: no cover


@dataclass
class FileValidationResponse:
    status: str
    message: str
    validation: Tuple[ValidationResponse]
    event_id: str

    def dict(self):
        return asdict(self) # pragma: no cover



@dataclass
class FilenameValidationPayload:
    filenames: List[str] 
    
    def dict(self):
        return asdict(self) # pragma: no cover


@dataclass
class FilesUploadPayload:
    files: List[bytes] 
    
    def dict(self):
        return asdict(self) # pragma: no cover


@dataclass
class UploaderQuotaResponse:
    status:str
    message:str
    monthly_quota:int
    monthly_quota_consumed:int
    quota_reset_date:str

    def dict(self):
        return asdict(self) # pragma: no cover
