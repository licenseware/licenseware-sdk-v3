from licenseware.apispec import ApiSpec
from licenseware.constants.apispec_types import ResponseType
from licenseware.datatable import DataTable
from licenseware.tenant import TenantRegistrationResponse
from .route_handlers import NewAppRouteHandlers



default_responses = [
    ResponseType(
        method="GET", 
        response="Missing Tenant or Authorization information", 
        status_code=403
    )
]


class AppApiSpecs:
    
    def __init__(self, routes: NewAppRouteHandlers):
       self.r = routes
   
    def __call__(self):
        return (

            ApiSpec(responses=default_responses)

            .route(method="GET", route=self.r.app_activation.url, handler=self.r.app_activation.handler.__name__)
            .response(response='App installed successfully', status_code=200)
            .response(response='App failed to install', status_code=500)

            .route(method="GET", route=self.r.editable_tables.url, handler=self.r.editable_tables.handler.__name__)
            .response(response=DataTable, status_code=200)

            .route(method="GET", route=self.r.terms_and_conditions.url, handler=self.r.terms_and_conditions.handler.__name__)
            .response(response=str, status_code=200)
            
            # Service 
            .route(method="GET", route=self.r.refresh_registration.url, handler=self.r.refresh_registration.handler.__name__)
            .response(response='Registering process was successful', status_code=200)
            .response(response='Registering process was unsuccessful', status_code=500)
            
            # User
            .route(method="GET", route=self.r.app_register.url, handler=self.r.app_register.handler.__name__)
            .response(response='Registering process was successful', status_code=200)
            .response(response='Registering process was unsuccessful', status_code=500)


            .route(method="GET", route=self.r.history_report.url, handler=self.r.history_report.handler.__name__)
            # TODO

            .route(method="GET", route=self.r.tenant_registration.url, handler=self.r.tenant_registration.handler.__name__)
            .response(response=TenantRegistrationResponse, status_code=200)
            .response(response="Query parameter tenant_id not provided", status_code=400)


            .route(self.r.features.url, handler=self.r.features.handler.__name__)
            # TODO
            
        )

    

    
    




