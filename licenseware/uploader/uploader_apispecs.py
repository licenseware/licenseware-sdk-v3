from licenseware.apispec import ApiSpec, ResponseType
from .uploader_types import (
    FilenameValidationPayload, 
    FileValidationResponse,
    FilesUploadPayload,
    UploaderQuotaResponse
)


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


class UploaderApiSpecs:
    
    def __init__(self, app_id: str):
       self.app_id = app_id
   
    def __call__(self):
        return (

        ApiSpec(
            title="File Upload", 
            description="Validate filenames, upload files and check quota or status",
            prefix=f"{self.app_id}/uploads",
            responses=default_responses
        )

        # File names validation
        .route("/{uploader_id}/validation", handler="validate_filenames")
        .path_param("uploader_id")
        .request_body(FilenameValidationPayload)
        .response(method="POST", response=FileValidationResponse, status_code=200)
        .response(method="POST", response=UploaderQuotaResponse, status_code=402)


        # File content validation and upload
        .route("/{uploader_id}/files", handler="validate_filecontents")
        .path_param("uploader_id")
        .request_form(FilesUploadPayload)
        .query_param("clear_data", description="Boolean parameter, warning, will clear existing data. Accepts `true`/`false` values.")
        .query_param("event_id", description="The uuid4 string received on filenames validation")
        .response(method="POST", response=FileValidationResponse, status_code=200)
        .response(method="POST", response=UploaderQuotaResponse, status_code=402)


        # Uploader quota
        .route("/{uploader_id}/quota", handler="check_quota")
        .path_param("uploader_id")
        .response(method="GET", response=UploaderQuotaResponse, status_code=200)
        .response(method="GET", response=UploaderQuotaResponse, status_code=402)


        # Uploader status
        .route("/{uploader_id}/status", handler="check_status")
        .path_param("uploader_id")
        .response(method="GET", response=UploaderQuotaResponse, status_code=200)
        .response(method="GET", response=UploaderQuotaResponse, status_code=402)

    )



