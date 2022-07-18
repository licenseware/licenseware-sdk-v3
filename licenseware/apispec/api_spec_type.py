from dataclasses import dataclass
from typing import List
from .param_type import ParamType
from .response_type import ResponseType


@dataclass
class ApiSpecType:
    route: str
    path_params: List[ParamType]
    query_params: List[ParamType]
    header_params: List[ParamType]
    cookie_params: List[ParamType]
    request_body: type
    request_form: type
    request_files: type
    responses: List[ResponseType]
