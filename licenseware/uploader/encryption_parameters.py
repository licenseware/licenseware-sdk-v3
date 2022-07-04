from typing import Tuple
from dataclasses import dataclass, asdict



@dataclass
class UploaderEncryptionParameters:
    filepaths: Tuple[str] = None
    filecontent: Tuple[str] = None
    columns: Tuple[str] = None


    def dict(self):
        return asdict(self)