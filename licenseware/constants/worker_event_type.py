from dataclasses import dataclass
from typing import List


@dataclass
class WorkerEvent:
    tenant_id: str
    authorization: str
    uploader_id: str
    event_id: str
    app_id: str
    filepaths: List[str]
    clear_data: bool = False
