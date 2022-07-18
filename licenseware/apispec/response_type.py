from typing import Union
from dataclasses import dataclass


@dataclass
class ResponseType:
    method: str
    response: Union[type, str, int, list] 
    status_code: int