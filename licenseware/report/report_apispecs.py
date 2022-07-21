from typing import List
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


class ReportApiSpecs:
    
    def __init__(self, app_id: str):
       self.app_id = app_id
   
    def __call__(self):
        return (

        ApiSpec(
            title="Reports", 
            description="Aggregate data resulted from processed inputs",
            prefix=f"{self.app_id}/reports",
            responses=default_responses
        )
        
        # Report metadata
        .route(method="GET", route="/{report_id}", handler="TODO")
        .response(response=ReportType, status_code=200)

        
        # Report component
        .route(method="GET", route="/{report_id}/{component_id}", handler="TODO")
        .query_param("limit", description="Limit the number of results")
        .query_param("skip", description="Skip the first n results")
        .response(response=List[dict], status_code=200)
        

        # Report component with filter
        .route(method="POST", route="/{report_id}/{component_id}", handler="TODO")
        .query_param("limit", description="Limit the number of results")
        .query_param("skip", description="Skip the first n results")
        .request_body(FilterItemType)
        .response(response=List[dict], status_code=200)


    )



