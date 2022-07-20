from typing import List, Union, NewType
from dataclasses import dataclass, field


RouteName = NewType("RouteName", str)


@dataclass
class ParamType:
    name:str
    type:str
    required: bool
    description: str


@dataclass
class ResponseType:
    method: str
    response: Union[type, str, int, list, dict] 
    status_code: int


@dataclass
class RouteType:
    route: str = None
    handler: str = None
    path_params: List[ParamType] = field(default_factory=list)
    query_params: List[ParamType] = field(default_factory=list)
    header_params: List[ParamType] = field(default_factory=list)
    cookie_params: List[ParamType] = field(default_factory=list)
    request_body: type = None
    request_form: type = None
    request_files: type = None
    responses: List[ResponseType] = field(default_factory=list)

