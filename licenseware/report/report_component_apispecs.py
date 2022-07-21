from licenseware.apispec import ApiSpec
from licenseware.constants.apispec_types import ResponseType
from licenseware.constants.report_type import ReportType
from licenseware.constants.filter_item_type import FilterItemType


default_responses = [
    ResponseType(
        method="GET", 
        response="Missing Tenant or Authorization information", 
        status_code=403
    ),
    ResponseType(
        method="POST", 
        response="Missing Tenant or Authorization information", 
        status_code=403
    )
]


class ReportComponentApiSpecs:
    
    def __init__(self, app_id: str):
       self.app_id = app_id
   
    def __call__(self):
        return (

        ApiSpec(
            title="Report Components", 
            description="Individual report components",
            prefix=f"{self.app_id}/report-components",
            responses=default_responses
        )
        
        # Report component
        .route(method="GET", route="/{component_id}", handler="TODO")
        .query_param("limit", description="Limit the number of results")
        .query_param("skip", description="Skip the first n results")
        .response(response=ReportType, status_code=200)

        # Report component with filter
        .route(method="POST", route="/{component_id}", handler="TODO")
        .query_param("limit", description="Limit the number of results")
        .query_param("skip", description="Skip the first n results")
        .request_body(FilterItemType)
        .response(response=ReportType, status_code=200)

    )



