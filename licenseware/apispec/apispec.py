from typing import Dict, Union
from .param_type import ParamType
from .response_type import ResponseType
from .api_spec_type import ApiSpecType
from licenseware.constants.http import HTTP_METHODS, HTTP_STATUS_CODES



class ApiSpec:

    def __init__(self):
        self._route = None
        self._path_params: Dict[str, ParamType] = dict()
        self._query_params: Dict[str, ParamType] = dict()
        self._header_params: Dict[str, ParamType] = dict()
        self._cookie_params: Dict[str, ParamType] = dict()
        self._request_body = None
        self._request_form = None
        self._request_files = None
        self._responses: Dict[str, ResponseType] = dict()


    def route(self, route:str):
        self._route = route
        return self

    def path_param(self, *, name:str, type:str = "string", required:bool = False, description:str = None):
        assert self._route is not None
        if name in self._path_params.keys():
            raise ValueError(f"Path parameter '{name}' already set")

        self._path_params[name] = ParamType(name, type, required, description)
    
        return self


    def query_param(self, *, name:str, type:str = "string", required:bool = False, description:str = None):
        assert self._route is not None
        if name in self._query_params.keys():
            raise ValueError(f"Query parameter '{name}' already set")

        self._query_params[name] = ParamType(name, type, required, description)

        return self

    def header_param(self, *, name:str, type:str = "string", required:bool = False, description:str = None):
        assert self._route is not None
        if name in self._header_params.keys():
            raise ValueError(f"Header parameter '{name}' already set")

        self._header_params[name] = ParamType(name, type, required, description)

        return self

    def cookie_param(self, *, name:str, type:str = "string", required:bool = False, description:str = None):
        assert self._route is not None
        if name in self._cookie_params.keys():
            raise ValueError(f"Cookie parameter '{name}' already set")

        self._cookie_params[name] = ParamType(name, type, required, description)

        return self


    def request_body(self, body: type):
        assert self._route is not None
        if self._request_body is not None:
            raise ValueError("Request body already set")
        
        self._request_body = body

        return self


    def request_form(self, form: type):
        assert self._route is not None
        if self._request_form is not None:
            raise ValueError("Request form already set")
        
        self._request_form = form

        return self


    def request_files(self, files: type):
        assert self._route is not None
        if self._request_files is not None:
            raise ValueError("Request files already set")
        
        self._request_files = files

        return self

    def response(self, *, method: str, response: Union[type, str, int, list], status_code: int):
        assert self._route is not None
        assert method in HTTP_METHODS
        assert status_code in HTTP_STATUS_CODES

        if method in self._responses.keys():
            raise ValueError(f"Response for http '{method}' method already set")

        self._responses[method] = ResponseType(method, response, status_code)

        return self


    @property
    def metadata(self):

        return ApiSpecType(
            route=self._route,
            path_params=list(self._path_params.values()),
            query_params=list(self._query_params.values()),
            header_params=list(self._header_params.values()),
            cookie_params=list(self._cookie_params.values()),
            request_body=self._request_body,
            request_form=self._request_form,
            request_files=self._request_files,
            responses=self._responses
        )




