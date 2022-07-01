from dataclasses import dataclass
from typing import Callable, List
from licenseware.uiresponses.filenames_response import FileNameResponse


@dataclass
class New:
    app_id: str
    uploader_id: str
    name: str 
    description: str
    accepted_file_types: tuple
    file_validator: Callable[[List[str]], FileNameResponse]
    