from typing import List
from dataclasses import dataclass


@dataclass
class WorkerEvent:
    tenant_id: str
    authorization: str
    uploader_id: str
    event_id: str
    app_id: str
    filepaths: List[str]
    clear_data: bool = False
