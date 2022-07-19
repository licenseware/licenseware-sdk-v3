from typing import Dict, Union, List
from licenseware.constants.http import HTTP_METHODS, HTTP_STATUS_CODES
from .apispec_types import (
    ApiSpecType, 
    RouteType,
    ParamType,
    ResponseType,
    RouteName
)



class ApiSpec:

    def __init__(self, title:str, description:str = None):
        self.title = title
        self.description = description
        self._current_route:str = None
        self._state: Dict[RouteName, RouteType] = dict()
        self._routes: Dict[RouteName, RouteType] = dict()


    def _update_routes(self):
        for route_name, route_data in self._state.items():
            self._routes[route_name] = route_data


    def route(self, route:str):
        
        if route in self._state:
            raise ValueError(f"Route '{route}' was previously defined")

        if route not in self._state: 
            self._state = dict()
            self._state[route] = RouteType()

        self._current_route = route
        self._state[route].route = route
        self._update_routes()
        return self


    def path_param(self, name:str, *, type:str = "string", required:bool = True, description:str = None):
        assert self._current_route is not None

        for item in self._state[self._current_route].path_params:
            if name == item.name:
                raise ValueError(f"Path parameter '{name}' already set")

        self._state[self._current_route].path_params.append(
            ParamType(name, type, required, description)
        )
        self._update_routes()

        return self


    def query_param(self, name:str, *, type:str = "string", required:bool = True, description:str = None):
        assert self._current_route is not None

        for item in self._state[self._current_route].query_params:
            if name == item.name:
                raise ValueError(f"Query parameter '{name}' already set")

        self._state[self._current_route].query_params.append(
            ParamType(name, type, required, description)
        )
        self._update_routes()

        return self

    def header_param(self, name:str, *, type:str = "string", required:bool = True, description:str = None):
        assert self._current_route is not None
        
        for item in self._state[self._current_route].header_params:
            if name == item.name:
                raise ValueError(f"Header parameter '{name}' already set")

        self._state[self._current_route].header_params.append(
            ParamType(name, type, required, description)
        )
        self._update_routes()

        return self

    def cookie_param(self, name:str, *, type:str = "string", required:bool = True, description:str = None):
        assert self._current_route is not None

        for item in self._state[self._current_route].cookie_params:
            if name == item.name:
                raise ValueError(f"Cookie parameter '{name}' already set")

        self._state[self._current_route].cookie_params.append(
            ParamType(name, type, required, description)
        )
        self._update_routes()

        return self

    def request_body(self, body: type):
        assert self._current_route is not None

        if self._state[self._current_route].request_body is not None:
            raise ValueError("Request body already set")

        self._state[self._current_route].request_body = body
        self._update_routes()

        return self


    def request_form(self, form: type):
        assert self._current_route is not None

        if self._state[self._current_route].request_form is not None:
            raise ValueError("Request form already set")

        self._state[self._current_route].request_form = form
        self._update_routes()

        return self


    def request_files(self, files: type):
        assert self._current_route is not None

        if self._state[self._current_route].request_files is not None:
            raise ValueError("Request files already set")

        self._state[self._current_route].request_files = files
        self._update_routes()

        return self


    def response(self, *, method: str, response: Union[type, str, int, list, dict], status_code: int):
        assert self._current_route is not None 
        assert method in HTTP_METHODS
        assert status_code in HTTP_STATUS_CODES

        for item in self._state[self._current_route].responses:
            if method == item.method:
                raise ValueError(f"Response for http '{method}' method already set")

        self._state[self._current_route].responses.append(
            ResponseType(method, response, status_code)
        )
        self._update_routes()

        return self 


    @property
    def metadata(self):

        return ApiSpecType(
            title=self.title,
            description=self.description,
            routes=list(self._routes.values())
        )




