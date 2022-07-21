from typing import Tuple, List, NewType
from dataclasses import dataclass, asdict


UploaderId = NewType("UploaderId", str)


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



@dataclass
class UploaderStatusResponse:
    status: str  
    
    def dict(self):
        return asdict(self) # pragma: no cover
