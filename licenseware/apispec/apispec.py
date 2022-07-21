from typing import Dict, Union, List
from licenseware.constants.http import HTTP_METHODS, HTTP_STATUS_CODES
from licenseware.constants.apispec_types import (
    RouteType,
    ParamType,
    ResponseType,
    RouteName
)



class ApiSpec:
   
    def __init__(
        self, title:str = None, 
        description:str = None, 
        prefix:str = None, 
        responses: List[ResponseType] = None
    ):
        self.title = title
        self.description = description
        self.prefix = prefix
        self.responses = responses or []
        self.routes: List[RouteType] = None
        self._current_route:str = None
        self._current_method:str = None
        self._state: Dict[RouteName, RouteType] = dict()
        self._routes: Dict[RouteName, RouteType] = dict()

    def _update_routes(self):

        for route_name, route_data in self._state.items():
            self._routes[route_name] = route_data
        
        self.routes = list(self._routes.values())


    def route(self, *, method:str, route:str, handler:str):
        """
            method - http method GET, POST, PUT, DELETE
            route - route/path/enpoint
            handler - function which will handle this route
        """

        if method == self._current_method and route == self._current_route:
            raise ValueError(f"Route {route} with http method {method} already set")

        assert method in HTTP_METHODS
        assert route.startswith("/")

        if self.prefix is not None: 
            route = self.prefix + route
        
        if route not in self._state: 
            self._state = dict()
            self._state[route] = RouteType()

        self._current_route = route
        self._current_method = method
        self._state[route].route = route
        self._state[route].method = method
        self._state[route].handler = handler
        self._state[route].responses.extend(self.responses)
        self._update_routes()
        return self


    def path_param(self, name:str, *, description:str = None, type:str = "string", required:bool = True):
        assert self._current_route is not None
        assert self._current_method is not None


        for item in self._state[self._current_route].path_params:
            if name == item.name:
                raise ValueError(f"Path parameter '{name}' already set")

        self._state[self._current_route].path_params.append(
            ParamType(name, type, required, description)
        )
        self._update_routes()

        return self


    def query_param(self, name:str, *, description:str = None, type:str = "string", required:bool = True):
        assert self._current_route is not None
        assert self._current_method is not None


        for item in self._state[self._current_route].query_params:
            if name == item.name:
                raise ValueError(f"Query parameter '{name}' already set")

        self._state[self._current_route].query_params.append(
            ParamType(name, type, required, description)
        )
        self._update_routes()

        return self

    def header_param(self, name:str, *, description:str = None, type:str = "string", required:bool = True):
        assert self._current_route is not None
        assert self._current_method is not None

        
        for item in self._state[self._current_route].header_params:
            if name == item.name:
                raise ValueError(f"Header parameter '{name}' already set")

        self._state[self._current_route].header_params.append(
            ParamType(name, type, required, description)
        )
        self._update_routes()

        return self

    def cookie_param(self, name:str, *, description:str = None, type:str = "string", required:bool = True):
        assert self._current_route is not None
        assert self._current_method is not None


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
        assert self._current_method is not None


        if self._state[self._current_route].request_body is not None:
            raise ValueError("Request body already set")

        self._state[self._current_route].request_body = body
        self._update_routes()

        return self


    def request_form(self, form: type):
        assert self._current_route is not None
        assert self._current_method is not None


        if self._state[self._current_route].request_form is not None:
            raise ValueError("Request form already set")

        self._state[self._current_route].request_form = form
        self._update_routes()

        return self


    def request_files(self, files: type):
        assert self._current_route is not None
        assert self._current_method is not None


        if self._state[self._current_route].request_files is not None:
            raise ValueError("Request files already set")

        self._state[self._current_route].request_files = files
        self._update_routes()

        return self


    def response(self, response: Union[type, str, int, list, dict], status_code: int):
        assert self._current_route is not None 
        assert self._current_method is not None
        assert status_code in HTTP_STATUS_CODES

        for item in self._state[self._current_route].responses:
            if self._current_method == item.method and status_code == item.status_code:
                raise ValueError(f"Response for http '{self._current_method}' method with status code '{status_code}' already set")

        self._state[self._current_route].responses.append(
            ResponseType(self._current_method, response, status_code)
        )
        self._update_routes()

        return self 




