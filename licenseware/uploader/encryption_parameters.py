from dataclasses import asdict, dataclass
from typing import Tuple


@dataclass
class UploaderEncryptionParameters:
    filepaths: Tuple[str] = None
    filecontent: Tuple[str] = None
    columns: Tuple[str] = None

    def dict(self):
        return asdict(self)  # pragma: no cover
