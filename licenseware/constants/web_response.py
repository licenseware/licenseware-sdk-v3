from typing import Any
from dataclasses import dataclass


@dataclass
class WebResponse:
    content: Any
    status_code: int
